# 独立示例 / Standalone Examples

## 中文

本目录包含 5 个**自包含** Python 示例，不依赖 `experiments/shared/`。用于快速理解 Agent 循环、工具校验、流式拼接、简易记忆与多 Agent 协作。

| 文件 | 内容 |
|------|------|
| `01_mini_agent.py` | 最小 while 循环 + 计算器工具；无 API key 时使用 mock。 |
| `02_tool_use.py` | 用 `dataclasses` 做输入校验、注册表与调度。 |
| `03_streaming.py` | 模拟异步 SSE 事件流，拼接文本与 `tool_use` JSON。 |
| `04_memory.py` | 文件型记忆 + 简易 TF-IDF 召回。 |
| `05_multi_agent.py` | asyncio 队列：Leader 分派任务，两名 Worker 并行处理。 |

### 运行方式

```bash
cd learn_claude_code/examples
python3 01_mini_agent.py
python3 02_tool_use.py
python3 03_streaming.py
python3 04_memory.py
python3 05_multi_agent.py
```

可选：若已 `pip install anthropic` 并配置 `ANTHROPIC_API_KEY`，`01_mini_agent.py` 会调用真实 API（否则自动 mock）。

---

## English

Five **standalone** Python scripts with no imports from `experiments/shared/`. They demonstrate the agent loop, tool validation, streaming reassembly, file-backed memory with TF‑IDF recall, and a tiny leader/worker multi-agent demo.

| File | What it shows |
|------|----------------|
| `01_mini_agent.py` | Minimal loop + calculator tool; mock LLM without an API key. |
| `02_tool_use.py` | Dataclass validation, registry, and dispatch. |
| `03_streaming.py` | Mock async SSE stream; merge text and tool JSON fragments. |
| `04_memory.py` | Topic files plus a simple TF‑IDF index for recall. |
| `05_multi_agent.py` | `asyncio` queues: leader assigns work to two workers. |

### How to run

```bash
cd learn_claude_code/examples
python3 01_mini_agent.py
python3 02_tool_use.py
python3 03_streaming.py
python3 04_memory.py
python3 05_multi_agent.py
```

Optional: with `pip install anthropic` and `ANTHROPIC_API_KEY`, `01_mini_agent.py` calls the real API; otherwise it stays on the mock path.
