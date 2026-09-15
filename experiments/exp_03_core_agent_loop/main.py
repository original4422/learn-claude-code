"""
Experiment 03 — Core Agent Loop

Replicates the async-generator state-machine pattern from src/query.ts.

Key concepts demonstrated:
  1. Async generator (`agent_loop`) that yields streaming events
  2. Immutable state updates via dataclass replacement
  3. While-true loop with terminal conditions
  4. Tool dispatch within the loop
  5. Consumer-driven iteration (REPL pulls events from the generator)

Run:
    python -m exp_03_core_agent_loop.main --mock
    python -m exp_03_core_agent_loop.main --provider anthropic
"""

from __future__ import annotations

import asyncio
import json
import sys
import os
from dataclasses import dataclass, field, replace
from enum import Enum
from typing import Any, AsyncIterator

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from shared import UnifiedLLMClient, LLMResponse, ToolUseBlock, StreamEvent
from shared.utils import (
    setup_argparser, header, section, step, info, warn, colored, count_tokens,
)


# ---------------------------------------------------------------------------
# State machine types (mirrors src/query.ts State / Terminal / Continue)
# ---------------------------------------------------------------------------

class TerminalReason(str, Enum):
    COMPLETED = "completed"
    MAX_TURNS = "max_turns"
    ERROR = "error"
    ABORTED = "aborted"


class TransitionReason(str, Enum):
    NEXT_TURN = "next_turn"
    RECOVERY = "recovery"


@dataclass(frozen=True)
class AgentState:
    """Immutable state snapshot — replaced (not mutated) each iteration."""
    messages: tuple[dict[str, Any], ...]
    turn: int = 1
    max_turns: int = 10
    transition: TransitionReason | None = None


@dataclass
class AgentEvent:
    """Events yielded from the agent loop to consumers."""
    type: str  # text_delta, tool_use, tool_result, state_update, terminal
    data: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Built-in tools
# ---------------------------------------------------------------------------

TOOLS = {
    "calculator": {
        "name": "calculator",
        "description": "Evaluate a math expression",
        "input_schema": {
            "type": "object",
            "properties": {"expression": {"type": "string"}},
            "required": ["expression"],
        },
    },
    "read_file": {
        "name": "read_file",
        "description": "Read a file and return its content",
        "input_schema": {
            "type": "object",
            "properties": {"path": {"type": "string"}},
            "required": ["path"],
        },
    },
}


async def execute_tool(name: str, tool_input: dict[str, Any]) -> str:
    """Execute a tool and return the result string."""
    if name == "calculator":
        expr = tool_input.get("expression", "0")
        try:
            result = eval(expr, {"__builtins__": {}})  # noqa: S307
            return json.dumps({"result": result})
        except Exception as e:
            return json.dumps({"error": str(e)})
    elif name == "read_file":
        path = tool_input.get("path", "")
        return json.dumps({"content": f"[mock file content of {path}]", "size": 42})
    return json.dumps({"error": f"Unknown tool: {name}"})


# ---------------------------------------------------------------------------
# Core agent loop — the heart of the experiment
# ---------------------------------------------------------------------------

async def agent_loop(
    user_message: str,
    client: UnifiedLLMClient,
    max_turns: int = 10,
) -> AsyncIterator[AgentEvent]:
    """
    Async generator implementing the agent loop.

    This mirrors `queryLoop()` in src/query.ts:
    - Maintains an immutable State that is replaced each iteration
    - Calls the LLM, checks for tool_use, executes tools, loops
    - Yields events so the consumer can render/stream them
    - Terminates when: no tool_use, max_turns reached, or error
    """
    state = AgentState(
        messages=({"role": "user", "content": user_message},),
        max_turns=max_turns,
    )

    yield AgentEvent(type="state_update", data={"turn": state.turn, "status": "started"})

    while True:
        # --- Check terminal condition: max turns ---
        if state.turn > state.max_turns:
            yield AgentEvent(
                type="terminal",
                data={"reason": TerminalReason.MAX_TURNS.value, "turn": state.turn},
            )
            return

        yield AgentEvent(type="state_update", data={"turn": state.turn, "status": "calling_llm"})

        # --- Call LLM ---
        try:
            response: LLMResponse = await client.chat(
                messages=list(state.messages),
                tools=list(TOOLS.values()),
            )
        except Exception as exc:
            yield AgentEvent(type="terminal", data={"reason": TerminalReason.ERROR.value, "error": str(exc)})
            return

        # --- Yield text content ---
        if response.text:
            yield AgentEvent(type="text_delta", data={"text": response.text})

        # --- No tool use → completed ---
        if not response.has_tool_use:
            yield AgentEvent(
                type="terminal",
                data={"reason": TerminalReason.COMPLETED.value, "turn": state.turn},
            )
            return

        # --- Execute tools ---
        assistant_msg = response.to_message()
        new_messages = list(state.messages) + [assistant_msg]

        for tool_use in response.tool_uses:
            yield AgentEvent(
                type="tool_use",
                data={"name": tool_use.name, "input": tool_use.input, "id": tool_use.id},
            )

            result = await execute_tool(tool_use.name, tool_use.input)

            yield AgentEvent(
                type="tool_result",
                data={"name": tool_use.name, "result": result, "id": tool_use.id},
            )

            new_messages.append({
                "role": "tool_result",
                "tool_use_id": tool_use.id,
                "content": result,
            })

        # --- Immutable state transition (replace, not mutate) ---
        state = replace(
            state,
            messages=tuple(new_messages),
            turn=state.turn + 1,
            transition=TransitionReason.NEXT_TURN,
        )


# ---------------------------------------------------------------------------
# Consumer: REPL that pulls events from the generator
# ---------------------------------------------------------------------------

async def run_repl(client: UnifiedLLMClient) -> None:
    header("Experiment 03: Core Agent Loop")
    info("This experiment demonstrates the async-generator agent loop pattern")
    info(f"Provider: {client.provider} | Model: {client.model or 'mock'}")

    queries = [
        "What is 2 + 3 * 4?",
        "Read the file data.txt and calculate 100 / 5",
    ]

    for i, query in enumerate(queries, 1):
        section(f"Query {i}: {query}")
        step(1, "Sending query to agent loop...")

        turn_count = 0
        async for event in agent_loop(query, client, max_turns=5):
            if event.type == "state_update":
                if event.data.get("status") == "calling_llm":
                    turn_count = event.data["turn"]
                    step(2, f"Turn {turn_count}: Calling LLM...")
            elif event.type == "text_delta":
                print(f"    {colored('Assistant:', 'cyan')} {event.data['text']}")
            elif event.type == "tool_use":
                print(f"    {colored('Tool Call:', 'magenta')} {event.data['name']}({json.dumps(event.data['input'])})")
            elif event.type == "tool_result":
                print(f"    {colored('Tool Result:', 'green')} {event.data['result']}")
            elif event.type == "terminal":
                reason = event.data["reason"]
                print(f"    {colored('Terminal:', 'yellow')} reason={reason}, turns={event.data.get('turn', '?')}")

    section("State Machine Summary")
    info("The loop follows: User msg -> LLM call -> Tool exec -> State replace -> Loop")
    info("Terminal conditions: completed (no tool_use), max_turns, error")
    info("Key pattern: async generator + immutable state + while(true)")


async def main() -> None:
    parser = setup_argparser("Experiment 03: Core Agent Loop")
    args = parser.parse_args()

    scenario = "agent_loop_calculator" if args.provider == "mock" else "default"
    client = UnifiedLLMClient(provider=args.provider, model=args.model, scenario=scenario)

    await run_repl(client)


if __name__ == "__main__":
    asyncio.run(main())
