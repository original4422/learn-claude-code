# Concept ↔ Source Quick Map (English)

Paths are relative to the repo root `claude-code-snapshot/`. **Doc chapter** refers to `learn_claude_code/docs/en/` (or top-level `docs/en/` if mirrored).

| Concept | Primary sources | Supporting sources | Doc chapter |
|---------|-----------------|--------------------|-------------|
| CLI entry | `src/entrypoints/cli.tsx` | `src/main.tsx` | `02-startup-flow.md` |
| Startup / bootstrap | `src/main.tsx` | `src/utils/sessionStart.ts` | `02-startup-flow.md` |
| Agent core loop | `src/query.ts` | `src/utils/messages.ts` | `03-core-loop.md` |
| Tool model / execution | `src/Tool.ts` | `src/utils/toolResultStorage.ts` | `04-tool-system.md` |
| Permissions / rules | `src/utils/permissions/` | `src/utils/settings/permissionValidation.ts` | `05-permission-security.md` |
| System prompt / context | `src/utils/systemPrompt.ts` | `src/utils/messages/mappers.ts` | `06-context-prompt.md` |
| Session / memory | `src/utils/sessionStorage.ts` | `src/services/compact/sessionMemoryCompact.ts` | `07-memory-system.md` |
| Terminal UI / REPL | `src/screens/REPL.tsx` | `src/interactiveHelpers.tsx` | `08-terminal-ui.md` |
| MCP tools | `tools/MCPTool/MCPTool.ts` | `src/entrypoints/mcp.ts`, `src/utils/mcpValidation.ts` | `09-mcp-integration.md` |
| Swarm / multi-agent | `src/utils/swarm/` | `src/utils/teammateMailbox.ts`, `src/utils/swarm/permissionSync.ts` | `10-multi-agent.md` |
| Plugins / skills | `src/utils/plugins/` | `src/utils/skills/` | `11-plugin-skill.md` |
| Streaming / API | `src/utils/stream.ts` | `src/utils/model/model.ts` | `12-api-streaming.md` |
| Settings | `src/utils/settings/settings.ts` | `src/utils/settings/mdm/settings.ts` | `13-config-settings.md` |
| Compaction / autocompact | `src/services/compact/compact.ts` | `src/services/compact/microCompact.ts`, `src/services/compact/autoCompact.ts` | `14-compact-context-mgmt.md` |
| Slash commands | `src/commands/` | `src/utils/slashCommandParsing.ts` | `15-command-system.md` |
| Token budget | `src/utils/tokenBudget.ts` | `src/utils/tokens.ts` | `14-compact-context-mgmt.md` |
| Vim mode | `src/vim/` | `src/screens/REPL.tsx` | `08-terminal-ui.md` |
| Tool registry / search | `src/utils/toolSearch.ts` | `src/utils/toolSchemaCache.ts` | `04-tool-system.md` |

---

*If you only have the `learn_claude_code/` tree checked out, use `docs/en/` or `learn_claude_code/docs/en/` for the same chapter names.*
