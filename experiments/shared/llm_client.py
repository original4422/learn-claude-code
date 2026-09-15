"""
Unified LLM client supporting Anthropic, OpenAI, and Mock providers.

Usage:
    client = UnifiedLLMClient(provider="mock")  # or "anthropic" or "openai"
    response = await client.chat(messages=[{"role": "user", "content": "Hello"}])
    async for event in client.stream_chat(messages=[...]):
        print(event)
"""

from __future__ import annotations

import asyncio
import json
import os
from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, AsyncIterator

from .types import LLMResponse, ToolUseBlock, StreamEvent
from .mock_data import get_mock_response, get_mock_stream_events


class UnifiedLLMClient:
    def __init__(
        self,
        provider: str = "mock",
        model: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        scenario: str = "default",
    ):
        self.provider = provider
        self.scenario = scenario
        self.model = model
        self._call_count = 0

        if provider == "anthropic":
            import anthropic
            self.model = model or "claude-sonnet-4-20250514"
            self._client = anthropic.AsyncAnthropic(
                api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"),
            )
        elif provider == "openai":
            import openai
            self.model = model or "gpt-4o"
            self._client = openai.AsyncOpenAI(
                api_key=api_key or os.environ.get("OPENAI_API_KEY"),
                base_url=base_url or os.environ.get("OPENAI_BASE_URL"),
            )
        elif provider == "mock":
            self._client = None
        else:
            raise ValueError(f"Unknown provider: {provider}")

    async def chat(
        self,
        messages: list[dict[str, Any]],
        system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        max_tokens: int = 4096,
    ) -> LLMResponse:
        self._call_count += 1

        if self.provider == "mock":
            return await self._mock_chat(messages, tools)
        elif self.provider == "anthropic":
            return await self._anthropic_chat(messages, system, tools, max_tokens)
        elif self.provider == "openai":
            return await self._openai_chat(messages, system, tools, max_tokens)
        raise ValueError(f"Unknown provider: {self.provider}")

    async def stream_chat(
        self,
        messages: list[dict[str, Any]],
        system: str | None = None,
        tools: list[dict[str, Any]] | None = None,
        max_tokens: int = 4096,
    ) -> AsyncIterator[StreamEvent]:
        self._call_count += 1

        if self.provider == "mock":
            async for event in self._mock_stream(messages, tools):
                yield event
        elif self.provider == "anthropic":
            async for event in self._anthropic_stream(messages, system, tools, max_tokens):
                yield event
        elif self.provider == "openai":
            async for event in self._openai_stream(messages, system, tools, max_tokens):
                yield event

    # --- Mock provider ---

    async def _mock_chat(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None,
    ) -> LLMResponse:
        await asyncio.sleep(0.1)
        return get_mock_response(self.scenario, self._call_count)

    async def _mock_stream(
        self,
        messages: list[dict[str, Any]],
        tools: list[dict[str, Any]] | None,
    ) -> AsyncIterator[StreamEvent]:
        for event in get_mock_stream_events(self.scenario, self._call_count):
            await asyncio.sleep(0.05)
            yield event

    # --- Anthropic provider ---

    async def _anthropic_chat(
        self,
        messages: list[dict[str, Any]],
        system: str | None,
        tools: list[dict[str, Any]] | None,
        max_tokens: int,
    ) -> LLMResponse:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": self._to_anthropic_messages(messages),
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = tools

        resp = await self._client.messages.create(**kwargs)
        return self._parse_anthropic_response(resp)

    async def _anthropic_stream(
        self,
        messages: list[dict[str, Any]],
        system: str | None,
        tools: list[dict[str, Any]] | None,
        max_tokens: int,
    ) -> AsyncIterator[StreamEvent]:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": self._to_anthropic_messages(messages),
            "stream": True,
        }
        if system:
            kwargs["system"] = system
        if tools:
            kwargs["tools"] = tools

        async with self._client.messages.stream(**kwargs) as stream:
            async for event in stream:
                parsed = self._parse_anthropic_stream_event(event)
                if parsed:
                    yield parsed

    def _to_anthropic_messages(self, messages: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Encode assistant calls and group consecutive results into one user turn."""
        anthropic: list[dict[str, Any]] = []
        previous_was_result = False
        for msg in deepcopy(messages):
            if msg["role"] == "tool_result":
                block = {
                    "type": "tool_result",
                    "tool_use_id": msg["tool_use_id"],
                    "content": msg.get("content", ""),
                }
                if "is_error" in msg:
                    block["is_error"] = msg["is_error"]
                if previous_was_result:
                    anthropic[-1]["content"].append(block)
                else:
                    anthropic.append({"role": "user", "content": [block]})
                previous_was_result = True
                continue

            previous_was_result = False
            if msg["role"] == "assistant" and "tool_uses" in msg:
                tool_uses = msg.pop("tool_uses")
                if tool_uses:
                    content = msg.get("content")
                    blocks = content if isinstance(content, list) else (
                        [{"type": "text", "text": content}] if content else []
                    )
                    msg["content"] = blocks + [{"type": "tool_use", **tool_use} for tool_use in tool_uses]
            anthropic.append(msg)
        return anthropic

    def _parse_anthropic_response(self, resp: Any) -> LLMResponse:
        text_parts: list[str] = []
        tool_uses: list[ToolUseBlock] = []

        for block in resp.content:
            if block.type == "text":
                text_parts.append(block.text)
            elif block.type == "tool_use":
                tool_uses.append(ToolUseBlock(
                    id=block.id,
                    name=block.name,
                    input=block.input,
                ))

        return LLMResponse(
            text="\n".join(text_parts),
            tool_uses=tool_uses,
            usage={"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens},
            stop_reason=resp.stop_reason,
        )

    def _parse_anthropic_stream_event(self, event: Any) -> StreamEvent | None:
        etype = getattr(event, "type", None)
        if etype == "content_block_start":
            block = event.content_block
            if block.type == "tool_use":
                return StreamEvent(
                    type="tool_use_start",
                    tool_use=ToolUseBlock(id=block.id, name=block.name, input={}),
                    index=event.index,
                )
        elif etype == "content_block_delta":
            delta = event.delta
            if delta.type == "text_delta":
                return StreamEvent(type="content_delta", text=delta.text, index=event.index)
            elif delta.type == "input_json_delta":
                return StreamEvent(type="tool_use_delta", partial_json=delta.partial_json, index=event.index)
        elif etype == "content_block_stop":
            return StreamEvent(type="tool_use_end", index=event.index)
        elif etype == "message_stop":
            return StreamEvent(type="message_stop")
        return None

    # --- OpenAI provider ---

    async def _openai_chat(
        self,
        messages: list[dict[str, Any]],
        system: str | None,
        tools: list[dict[str, Any]] | None,
        max_tokens: int,
    ) -> LLMResponse:
        oai_messages = self._to_openai_messages(messages, system)
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": oai_messages,
        }
        if tools:
            kwargs["tools"] = self._to_openai_tools(tools)

        resp = await self._client.chat.completions.create(**kwargs)
        return self._parse_openai_response(resp)

    async def _openai_stream(
        self,
        messages: list[dict[str, Any]],
        system: str | None,
        tools: list[dict[str, Any]] | None,
        max_tokens: int,
    ) -> AsyncIterator[StreamEvent]:
        oai_messages = self._to_openai_messages(messages, system)
        kwargs: dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens,
            "messages": oai_messages,
            "stream": True,
        }
        if tools:
            kwargs["tools"] = self._to_openai_tools(tools)

        stream = await self._client.chat.completions.create(**kwargs)
        tool_calls_acc: dict[int, dict[str, str]] = {}

        async for chunk in stream:
            delta = chunk.choices[0].delta if chunk.choices else None
            if not delta:
                continue
            if delta.content:
                yield StreamEvent(type="content_delta", text=delta.content)
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    idx = tc.index
                    if idx not in tool_calls_acc:
                        tool_calls_acc[idx] = {"id": tc.id or "", "name": "", "args": ""}
                        if tc.function and tc.function.name:
                            tool_calls_acc[idx]["name"] = tc.function.name
                            yield StreamEvent(
                                type="tool_use_start",
                                tool_use=ToolUseBlock(id=tc.id or "", name=tc.function.name, input={}),
                                index=idx,
                            )
                    if tc.function and tc.function.arguments:
                        tool_calls_acc[idx]["args"] += tc.function.arguments
                        yield StreamEvent(type="tool_use_delta", partial_json=tc.function.arguments, index=idx)
            if chunk.choices[0].finish_reason:
                yield StreamEvent(type="message_stop")

    def _to_openai_messages(
        self, messages: list[dict[str, Any]], system: str | None
    ) -> list[dict[str, Any]]:
        oai: list[dict[str, Any]] = []
        if system:
            oai.append({"role": "system", "content": system})
        for msg in deepcopy(messages):
            if msg["role"] == "tool_result":
                oai.append({
                    "role": "tool",
                    "tool_call_id": msg["tool_use_id"],
                    "content": msg.get("content", ""),
                })
            else:
                if msg["role"] == "assistant" and "tool_uses" in msg:
                    tool_uses = msg.pop("tool_uses")
                    if tool_uses:
                        msg["content"] = msg.get("content") or None
                        msg["tool_calls"] = [
                            {
                                "id": tool_use["id"],
                                "type": "function",
                                "function": {
                                    "name": tool_use["name"],
                                    "arguments": json.dumps(tool_use["input"]),
                                },
                            }
                            for tool_use in tool_uses
                        ]
                oai.append(msg)
        return oai

    def _to_openai_tools(self, tools: list[dict[str, Any]]) -> list[dict[str, Any]]:
        return [
            {
                "type": "function",
                "function": {
                    "name": t["name"],
                    "description": t.get("description", ""),
                    "parameters": t.get("input_schema", {}),
                },
            }
            for t in tools
        ]

    def _parse_openai_response(self, resp: Any) -> LLMResponse:
        choice = resp.choices[0]
        text = choice.message.content or ""
        tool_uses: list[ToolUseBlock] = []

        if choice.message.tool_calls:
            for tc in choice.message.tool_calls:
                tool_uses.append(ToolUseBlock(
                    id=tc.id,
                    name=tc.function.name,
                    input=json.loads(tc.function.arguments) if tc.function.arguments else {},
                ))

        return LLMResponse(
            text=text,
            tool_uses=tool_uses,
            usage={
                "input_tokens": resp.usage.prompt_tokens if resp.usage else 0,
                "output_tokens": resp.usage.completion_tokens if resp.usage else 0,
            },
            stop_reason=choice.finish_reason or "stop",
        )
