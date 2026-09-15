"""Core data types shared across experiments."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class ToolUseBlock:
    id: str
    name: str
    input: dict[str, Any]


@dataclass
class LLMResponse:
    text: str = ""
    tool_uses: list[ToolUseBlock] = field(default_factory=list)
    usage: dict[str, int] = field(default_factory=dict)
    stop_reason: str = "end_turn"

    @property
    def has_tool_use(self) -> bool:
        return len(self.tool_uses) > 0

    def to_message(self) -> dict[str, Any]:
        """Keep the complete assistant turn in provider-independent history.

        ``content`` holds text; optional ``tool_uses`` holds id/name/input dicts.
        Results remain separate role="tool_result" messages with tool_use_id.
        The client translates this history at each provider boundary.
        """
        message: dict[str, Any] = {"role": "assistant", "content": self.text}
        if self.tool_uses:
            message["tool_uses"] = [asdict(tool_use) for tool_use in self.tool_uses]
        return message


@dataclass
class StreamEvent:
    type: str  # content_delta, tool_use_start, tool_use_delta, tool_use_end, message_stop
    text: str = ""
    tool_use: ToolUseBlock | None = None
    partial_json: str = ""
    index: int = 0
