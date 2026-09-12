<div align="center">

# Claude Code 源码学习

**从一次提问到工具执行，拆解编程 Agent 的工作原理。**

17 章双语导读 · 15 个 Python 实验 · 5 个独立示例 · 首个实验无需 API Key

[![文档](https://img.shields.io/badge/文档-中英双语-blue)](./docs/zh/00-overview.md)
[![实验](https://img.shields.io/badge/实验-Python-3776AB?logo=python&logoColor=white)](./experiments/)
[![许可证](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)

[开始动手](#快速开始) · [选择学习路线](#学习路线) · [中文文档](./docs/zh/00-overview.md) · [English](./README_EN.md)

</div>

Claude Code 如何把一句需求变成多轮工具调用？什么时候需要确认权限？对话越来越长时，上下文又是怎样保留下来的？

本项目结合 **TypeScript 源码快照导读**与 **Python 迷你实现**，把这些问题拆成可以阅读、运行和修改的实验。你可以先跑通一个 Agent 循环，再逐步理解工具、权限、记忆、MCP 和多 Agent 协作。

> 这是独立的教学项目，围绕固定源码快照讲解架构模式；实验是简化实现，不代表 Claude Code 当前版本的完整行为。无需准备源码快照，也能阅读文档和运行实验。

## 你能学到什么

| 你关心的问题 | 对应内容 | 动手入口 |
| --- | --- | --- |
| Agent 如何反复调用工具，直到任务结束？ | [核心循环](./docs/zh/03-core-loop.md)、[工具系统](./docs/zh/04-tool-system.md) | [核心循环实验](./experiments/exp_03_core_agent_loop/) |
| 读写文件、执行命令前，如何判断权限？ | [权限与安全](./docs/zh/05-permission-security.md) | [权限引擎实验](./experiments/exp_05_permission_engine/) |
| 长对话如何管理提示词、记忆与上下文？ | [提示词组装](./docs/zh/06-context-prompt.md)、[记忆](./docs/zh/07-memory-system.md)、[上下文压缩](./docs/zh/14-compact-context-mgmt.md) | [上下文压缩实验](./experiments/exp_14_context_compaction/) |
| 如何接入外部工具，让多个 Agent 协作？ | [MCP](./docs/zh/09-mcp-integration.md)、[多 Agent](./docs/zh/10-multi-agent.md) | [MCP 实验](./experiments/exp_09_mcp_client/)、[多 Agent 实验](./experiments/exp_10_multi_agent/) |
| 流式响应如何变成终端里的交互体验？ | [终端 UI](./docs/zh/08-terminal-ui.md)、[流式 API](./docs/zh/12-api-streaming.md) | [流式 API 实验](./experiments/exp_12_streaming_api/) |

适合会一点 Python、了解基本 LLM 对话与工具调用、希望进一步理解 Agent 工程实现的开发者。刚接触 Agent，可以从[最小 Agent 教程](./quick-start/zh/01-minimal-agent.md)开始；熟悉 TypeScript 的读者可以结合[源码地图](./references/zh/source-map.md)深入阅读。

## 快速开始

准备 **Python 3.11+**。第一个核心循环实验的 Mock 模式只用标准库，无需安装依赖或配置 API Key。

```bash
git clone https://github.com/original4422/learn-claude-code.git
cd learn-claude-code/experiments
python3 -m exp_03_core_agent_loop.main --mock
```

第一条查询会展示以下过程（节选）：

```text
Turn 1: Calling LLM...
Tool Call: calculator({"expression": "2 + 3 * 4"})
Tool Result: {"result": 14}
Turn 2: Calling LLM...
Assistant: The result of 2 + 3 * 4 is 14.
Terminal: reason=completed, turns=2
```

你刚跑通了 **模型请求 → 工具调用 → 结果回传 → 下一轮响应**。Mock 使用预设响应，方便观察控制流；它不用于验证真实模型的推理能力。

接下来打开[第 03 章：核心循环](./docs/zh/03-core-loop.md)和[配套实验指南](./docs/zh/experiments/03-核心Agent循环实验.md)，对照输出阅读实现。

## 学习路线

不必从头读完所有章节。按你现在的目标选择入口：

| 路线 | 阅读与实验顺序 | 学完后能做什么 |
| --- | --- | --- |
| **先做一个小 Agent** | [最小 Agent](./quick-start/zh/01-minimal-agent.md) → [添加工具](./quick-start/zh/02-add-a-tool.md) → [流式聊天](./quick-start/zh/03-streaming-chat.md) | 理解最小循环，并给它添加工具与流式输出 |
| **看懂核心架构** | [总览](./docs/zh/00-overview.md) → [架构](./docs/zh/01-architecture.md) → [循环](./docs/zh/03-core-loop.md) → [工具](./docs/zh/04-tool-system.md) → [提示词](./docs/zh/06-context-prompt.md)，配合实验 03、04、12 | 说明一条请求如何经过模型、工具和事件流 |
| **系统研习** | [17 章文档](./docs/zh/00-overview.md) + [15 个实验](./experiments/README.md)，按章节编号推进 | 分析权限、记忆、扩展与上下文管理的设计取舍 |

```mermaid
flowchart LR
  A[跑通核心循环] --> B[理解工具与权限]
  B --> C[管理提示词与记忆]
  C --> D[接入 MCP 与多 Agent]
  D --> E[研究流式输出与上下文压缩]
```

<details>
<summary><strong>展开完整章节与实验索引（00–16）</strong></summary>

章节文件位于 `docs/zh/` 和 `docs/en/`，实验包位于 `experiments/`。编号一一对应，读完一章即可运行对应实验。

| 章节 | 文档文件 | Python 实验包 |
| --- | --- | --- |
| 00 | `00-overview.md` | — |
| 01 | `01-architecture.md` | — |
| 02 | `02-startup-flow.md` | `exp_02_startup_flow` |
| 03 | `03-core-loop.md` | `exp_03_core_agent_loop` |
| 04 | `04-tool-system.md` | `exp_04_tool_system` |
| 05 | `05-permission-security.md` | `exp_05_permission_engine` |
| 06 | `06-context-prompt.md` | `exp_06_prompt_assembly` |
| 07 | `07-memory-system.md` | `exp_07_memory_system` |
| 08 | `08-terminal-ui.md` | `exp_08_terminal_ui` |
| 09 | `09-mcp-integration.md` | `exp_09_mcp_client` |
| 10 | `10-multi-agent.md` | `exp_10_multi_agent` |
| 11 | `11-plugin-skill.md` | `exp_11_plugin_skill` |
| 12 | `12-api-streaming.md` | `exp_12_streaming_api` |
| 13 | `13-config-settings.md` | `exp_13_config_system` |
| 14 | `14-compact-context-mgmt.md` | `exp_14_context_compaction` |
| 15 | `15-command-system.md` | `exp_15_command_system` |
| 16 | `16-design-patterns.md` | `exp_16_design_patterns` |

</details>

## 继续运行实验

需要运行更多实验或连接真实模型时，在**仓库根目录**创建环境并安装依赖：

```bash
python3 -m venv experiments/.venv
source experiments/.venv/bin/activate  # Windows: experiments\.venv\Scripts\activate
python -m pip install -r experiments/requirements.txt
cd experiments
python -m exp_03_core_agent_loop.main --mock
```

| 模式 | 命令参数 | 配置 |
| --- | --- | --- |
| 离线 Mock | `--mock` | 无需密钥，使用预设响应 |
| Anthropic | `--provider anthropic` | 设置 `ANTHROPIC_API_KEY` |
| OpenAI 兼容接口 | `--provider openai` | 设置 `OPENAI_API_KEY`，可选 `OPENAI_BASE_URL` |

macOS / Linux 用户也可以在**仓库根目录**使用 Makefile：

```bash
make setup        # 创建环境并安装依赖
make test EXP=03  # 运行核心循环实验（Mock）
make test-all     # 运行全部 15 个实验（Mock）
make lint         # 检查代码风格
```

各实验参数以对应 `main.py` 和[实验指南](./docs/zh/experiments/00-实验指南.md)为准。

## 资料导航

| 目录 | 内容 |
| --- | --- |
| [docs/zh](./docs/zh/00-overview.md) / [docs/en](./docs/en/00-overview.md) | 17 章双语导读与配套实验指南 |
| [experiments](./experiments/) | 15 个 Python 实验及统一 LLM 客户端 |
| [examples](./examples/README.md) | 5 个独立示例：最小 Agent、工具、流式、记忆、多 Agent |
| [quick-start](./quick-start/zh/01-minimal-agent.md) | 3 篇循序渐进的入门教程 |
| [diagrams](./diagrams/) | 5 张 Mermaid 架构图 |
| [glossary](./glossary/zh.md) / [references](./references/zh/) | 术语表、设计模式速查与源码地图 |
| [website](./website/README.md) | Docusaurus 文档网站与本地预览说明 |

默认首页为本文件；[英文版](./README_EN.md)保留英文阅读入口，[README_ZH.md](./README_ZH.md)保留原有中文链接。

## 参与贡献

欢迎修正文档、补充实验，或提出你希望拆解的 Agent 机制。遇到实验问题，请在 Issue 中附上实验编号、Python 版本、执行命令与错误输出，方便复现。

提交代码前运行 `make test-all` 和 `make lint`，文档修改请同步中英文内容。详细说明见[贡献指南](./CONTRIBUTING.md)。

## 致谢与许可证

感谢 Anthropic 与社区在 Agent 工具链和 MCP 生态上的工作。本项目的文档、实验与示例为独立教学材料，依据 [MIT 许可证](./LICENSE)发布。分析所引用的源码快照遵循其原始许可与使用条款，本项目不代表 Anthropic 官方。
