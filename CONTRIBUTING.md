# Contributing / 贡献指南

[English](#english) | [中文](#中文)

---

## English

Thank you for your interest in contributing to Claude Code Learn!

### Ways to Contribute

- **Improve documentation** -- Fix typos, clarify explanations, add missing details
- **Enhance experiments** -- Add new experiments, improve existing ones, fix bugs
- **Add translations** -- Improve Chinese or English translations
- **Add examples** -- Create new standalone examples demonstrating agent patterns
- **Report issues** -- Found a bug, broken link, or unclear explanation? Open an issue

### Development Setup

```bash
git clone <repo-url>
cd learn_claude_code
make setup          # creates venv, installs dependencies
make test-all       # verify everything works
make lint           # check code style
```

### Guidelines

1. **Keep experiments self-documenting** -- Each experiment should explain what it demonstrates via docstrings and output
2. **Bilingual** -- All documentation and user-facing text should have both Chinese and English versions
3. **Mock-first** -- Every experiment must work with `--mock` (no API key required)
4. **Self-contained examples** -- Files in `examples/` must not import from `experiments/shared/`
5. **Test before submitting** -- Run `make test-all` and `make lint` before opening a PR

### Pull Request Process

1. Fork the repository and create a feature branch
2. Make your changes following the guidelines above
3. Run `make test-all && make lint` to verify
4. Open a pull request with a clear description of the changes

---

## 中文

感谢你有兴趣参与 Claude Code Learn 项目！

### 参与方式

- **改进文档** -- 修复错别字、改善说明、补充遗漏内容
- **增强实验** -- 添加新实验、改进现有实验、修复 bug
- **改善翻译** -- 优化中文或英文版本的翻译质量
- **添加示例** -- 创建新的独立示例，展示 Agent 设计模式
- **报告问题** -- 发现 bug、断链或表述不清？请提 issue

### 开发环境搭建

```bash
git clone <repo-url>
cd learn_claude_code
make setup          # 创建虚拟环境，安装依赖
make test-all       # 验证所有实验可运行
make lint           # 检查代码风格
```

### 规范要求

1. **实验自文档化** -- 每个实验通过 docstring 和输出自行说明其演示内容
2. **双语** -- 所有文档和面向用户的文字都需提供中英双份
3. **Mock 优先** -- 每个实验必须支持 `--mock` 模式（无需 API key）
4. **示例独立** -- `examples/` 中的文件不得导入 `experiments/shared/`
5. **提交前测试** -- 提交 PR 前请运行 `make test-all && make lint`

### Pull Request 流程

1. Fork 仓库并创建功能分支
2. 按照上述规范进行修改
3. 运行 `make test-all && make lint` 确认通过
4. 提交 PR 并附上清晰的变更说明
