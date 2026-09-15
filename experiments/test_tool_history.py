"""Offline regression tests for tool-call history; no SDK or API key required.

Run: python -m unittest discover -s experiments -p 'test_*.py' -v
"""

from __future__ import annotations

import json
import unittest
from copy import deepcopy
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

from exp_03_core_agent_loop.main import agent_loop
from shared import LLMResponse, ToolUseBlock, UnifiedLLMClient


def provider_response(provider, text, tool_uses=()):
    """Supply SDK-shaped responses so the real response parsers are exercised."""
    if provider == "anthropic":
        content = [SimpleNamespace(type="text", text=text)] if text else []
        content.extend(SimpleNamespace(type="tool_use", **vars(tool)) for tool in tool_uses)
        return SimpleNamespace(
            content=content,
            usage=SimpleNamespace(input_tokens=10, output_tokens=5),
            stop_reason="tool_use" if tool_uses else "end_turn",
        )
    return SimpleNamespace(
        choices=[SimpleNamespace(
            message=SimpleNamespace(
                content=text or None,
                tool_calls=[SimpleNamespace(
                    id=tool.id,
                    function=SimpleNamespace(name=tool.name, arguments=json.dumps(tool.input)),
                ) for tool in tool_uses],
            ),
            finish_reason="tool_calls" if tool_uses else "stop",
        )],
        usage=SimpleNamespace(prompt_tokens=10, completion_tokens=5),
    )


def fake_client(provider, responses):
    client = UnifiedLLMClient(provider="mock")
    client.provider = provider
    create = AsyncMock(side_effect=responses)
    client._client = SimpleNamespace(
        messages=SimpleNamespace(create=create),
        chat=SimpleNamespace(completions=SimpleNamespace(create=create)),
    )
    return client, create


class ToolHistoryTests(unittest.IsolatedAsyncioTestCase):
    def assert_tool_turn(self, provider, messages, text, tool_uses, results):
        assistant = messages[1]
        self.assertEqual(assistant["role"], "assistant")
        self.assertNotIn("tool_uses", assistant)
        if provider == "anthropic":
            expected_blocks = [{"type": "text", "text": text}] if text else []
            expected_blocks += [{"type": "tool_use", **vars(tool)} for tool in tool_uses]
            self.assertEqual(assistant["content"], expected_blocks)
            self.assertEqual(messages[2:], [{"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": tool.id, "content": result}
                for tool, result in zip(tool_uses, results, strict=True)
            ]}])
        else:
            self.assertEqual(assistant["content"], text or None)
            self.assertEqual(len(assistant["tool_calls"]), len(tool_uses))
            for call, tool in zip(assistant["tool_calls"], tool_uses, strict=True):
                self.assertEqual(call["id"], tool.id)
                self.assertEqual(call["type"], "function")
                self.assertEqual(call["function"]["name"], tool.name)
                self.assertEqual(json.loads(call["function"]["arguments"]), tool.input)
            self.assertEqual(messages[2:], [
                {"role": "tool", "tool_call_id": tool.id, "content": result}
                for tool, result in zip(tool_uses, results, strict=True)
            ])

    async def test_second_request_keeps_single_and_parallel_calls_with_or_without_text(self):
        all_tools = [
            ToolUseBlock("calc-1", "calculator", {"expression": "2 + 3 * 4"}),
            ToolUseBlock("calc-2", "calculator", {"expression": "100 / 5"}),
        ]
        for provider in ("anthropic", "openai"):
            for count in (1, 2):
                for text in ("Let me calculate.", ""):
                    with self.subTest(provider=provider, count=count, text=text):
                        calls = all_tools[:count]
                        client, create = fake_client(provider, [
                            provider_response(provider, text, calls),
                            provider_response(provider, "Done."),
                        ])
                        events = [event async for event in agent_loop("Calculate.", client)]
                        self.assertEqual(create.await_count, 2)
                        self.assertEqual(create.await_args_list[0].kwargs["messages"], [
                            {"role": "user", "content": "Calculate."},
                        ])
                        self.assert_tool_turn(
                            provider, create.await_args_list[1].kwargs["messages"], text,
                            calls, ['{"result": 14}', '{"result": 20.0}'][:count],
                        )
                        self.assertEqual(events[-1].data, {"reason": "completed", "turn": 2})

    async def test_tool_history_survives_multiple_rounds(self):
        first = ToolUseBlock("first", "calculator", {"expression": "1+1"})
        second = ToolUseBlock("second", "calculator", {"expression": "2+2"})
        for provider in ("anthropic", "openai"):
            with self.subTest(provider=provider):
                client, create = fake_client(provider, [
                    provider_response(provider, "", [first]),
                    provider_response(provider, "", [second]),
                    provider_response(provider, "4"),
                ])
                events = [event async for event in agent_loop("Calculate.", client)]
                requests = [call.kwargs["messages"] for call in create.await_args_list]
                self.assertEqual(requests[2][:len(requests[1])], requests[1])
                self.assert_tool_turn(provider, requests[2][2:], "", [second], ['{"result": 4}'])
                self.assertEqual(events[-1].data["turn"], 3)

    async def test_chat_and_stream_use_same_provider_conversion(self):
        async def empty_stream():
            if False:
                yield

        class StreamContext:
            async def __aenter__(self):
                return empty_stream()

            async def __aexit__(self, *args):
                return False

        history = [
            {"role": "user", "content": "Calculate."},
            LLMResponse(tool_uses=[
                ToolUseBlock("one", "calculator", {"expression": "1+1"}),
                ToolUseBlock("two", "calculator", {"expression": "2+2"}),
            ]).to_message(),
            {"role": "tool_result", "tool_use_id": "one", "content": "2"},
            {"role": "tool_result", "tool_use_id": "two", "content": "4"},
        ]
        original = deepcopy(history)
        for provider in ("anthropic", "openai"):
            with self.subTest(provider=provider):
                client, create = fake_client(provider, [provider_response(provider, "Done")])
                await client.chat(history, system="Use tools.")
                chat_messages = create.call_args.kwargs["messages"]
                if provider == "anthropic":
                    stream_call = Mock(return_value=StreamContext())
                    client._client.messages.stream = stream_call
                else:
                    create.side_effect = None
                    create.return_value = empty_stream()
                    stream_call = create
                self.assertEqual([event async for event in client.stream_chat(history, system="Use tools.")], [])
                self.assertEqual(stream_call.call_args.kwargs["messages"], chat_messages)
                self.assertEqual(history, original)

    def test_plain_text_and_native_messages_pass_through_without_mutation(self):
        client = UnifiedLLMClient()
        plain = [{"role": "user", "content": "Hello"}, {"role": "assistant", "content": "Hi"}]
        self.assertEqual(client._to_anthropic_messages(plain), plain)
        self.assertEqual(client._to_openai_messages(plain, "System"), [
            {"role": "system", "content": "System"}, *plain,
        ])
        native_anthropic = [
            {"role": "assistant", "content": [
                {"type": "tool_use", "id": "call", "name": "echo", "input": {"text": "中文"}},
            ]},
            {"role": "user", "content": [
                {"type": "tool_result", "tool_use_id": "call", "content": "中文"},
                {"type": "text", "text": "Continue."},
            ]},
        ]
        native_openai = [
            {"role": "assistant", "content": None, "tool_calls": [
                {"id": "call", "type": "function", "function": {"name": "echo", "arguments": "{}"}},
            ]},
            {"role": "tool", "tool_call_id": "call", "content": "中文"},
            {"role": "user", "content": [{"type": "text", "text": "Continue."}]},
        ]
        for convert, history in (
            (client._to_anthropic_messages, native_anthropic),
            (lambda messages: client._to_openai_messages(messages, None), native_openai),
        ):
            original = deepcopy(history)
            converted = convert(history)
            self.assertEqual(converted, original)
            converted[-1]["content"].append({"type": "text", "text": "New"})
            self.assertEqual(history, original)

    def test_response_message_is_an_independent_snapshot(self):
        response = LLMResponse(tool_uses=[ToolUseBlock("call", "echo", {"nested": [1]})])
        message = response.to_message()
        response.tool_uses[0].input["nested"].append(2)
        self.assertEqual(message["tool_uses"][0]["input"], {"nested": [1]})
        self.assertEqual(LLMResponse(text="Hello").to_message(), {"role": "assistant", "content": "Hello"})


if __name__ == "__main__":
    unittest.main()
