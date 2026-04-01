# 概念 ↔ 源码速查（中文）

路径相对于仓库根目录 `claude-code-snapshot/`。**文档章节**指向 `learn_claude_code/docs/zh/` 下对应总览（与顶层 `docs/zh/` 镜像内容一致时可互换）。

| 概念 | 主要源文件 | 辅助文件 | 文档章节 |
|------|------------|----------|----------|
| CLI 入口 | `src/entrypoints/cli.tsx` | `src/main.tsx` | `02-startup-flow.md` |
| 启动与初始化 | `src/main.tsx` | `src/utils/sessionStart.ts` | `02-startup-flow.md` |
| Agent 核心循环 | `src/query.ts` | `src/utils/messages.ts` | `03-core-loop.md` |
| 工具抽象与执行 | `src/Tool.ts` | `src/utils/toolResultStorage.ts` | `04-tool-system.md` |
| 权限与规则 | `src/utils/permissions/` | `src/utils/settings/permissionValidation.ts` | `05-permission-security.md` |
| 系统提示与上下文 | `src/utils/systemPrompt.ts` | `src/utils/messages/mappers.ts` | `06-context-prompt.md` |
| 会话与记忆 | `src/utils/sessionStorage.ts` | `src/services/compact/sessionMemoryCompact.ts` | `07-memory-system.md` |
| 终端 UI / REPL | `src/screens/REPL.tsx` | `src/interactiveHelpers.tsx` | `08-terminal-ui.md` |
| MCP 工具与集成 | `tools/MCPTool/MCPTool.ts` | `src/entrypoints/mcp.ts`, `src/utils/mcpValidation.ts` | `09-mcp-integration.md` |
| Swarm / 多 Agent | `src/utils/swarm/` | `src/utils/teammateMailbox.ts`, `src/utils/swarm/permissionSync.ts` | `10-multi-agent.md` |
| 插件与技能 | `src/utils/plugins/` | `src/utils/skills/` | `11-plugin-skill.md` |
| 流式与 API 客户端 | `src/utils/stream.ts` | `src/utils/model/model.ts` | `12-api-streaming.md` |
| 设置与配置 | `src/utils/settings/settings.ts` | `src/utils/settings/mdm/settings.ts` | `13-config-settings.md` |
| 压缩 / Autocompact | `src/services/compact/compact.ts` | `src/services/compact/microCompact.ts`, `src/services/compact/autoCompact.ts` | `14-compact-context-mgmt.md` |
| 斜杠命令 | `src/commands/` | `src/utils/slashCommandParsing.ts` | `15-command-system.md` |
| Token 预算 | `src/utils/tokenBudget.ts` | `src/utils/tokens.ts` | `14-compact-context-mgmt.md` |
| Vim 模式 | `src/vim/` | `src/screens/REPL.tsx` | `08-terminal-ui.md` |
| 工具注册与搜索 | `src/utils/toolSearch.ts` | `src/utils/toolSchemaCache.ts` | `04-tool-system.md` |

---

*若本地仅检出 `learn_claude_code/`，请使用仓库根目录的 `docs/zh/` 或 `learn_claude_code/docs/zh/` 中同名章节。*
