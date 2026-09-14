# Documentation Website
# 文档网页

This directory contains the Docusaurus site shell for the repository docs.
这个目录包含为仓库的文档构建 Docusaurus 页面的命令

The Markdown content stays in the repository-level content directories:
仓库中的原Markdown文件没有变化：

- `../docs`
- `../quick-start`
- `../references`
- `../glossary`
- `../diagrams`

## Local development
## 本地部署

```bash
cd website
npm install
npm run start
```

## Build
## 构建

```bash
cd website
npm install
npm run build
```

The static site output is written to `website/build/`. The `html` branch is
intended to contain only that built static output for GitHub Pages.

静态页面的输出写入 `website/build/` 。
而 `html` 分支只存放构建好的静态页面用于 Github Pages 。

## 首页语言切换 / Homepage languages

导航右侧的语言菜单支持在「简体中文」和「English」之间切换，首页正文、导航和页脚随语言变化。左侧的 `English docs` 是文档入口。

- 中文首页：`/learn-claude-code/`
- 英文首页：`/learn-claude-code/en/`

The language menu switches the homepage, navigation, and footer between Chinese and English. Existing documentation URLs remain available. Run `npm run build` without `--locale` to build both languages before deploying the complete `build/` directory.

本地同时验证两种语言时，运行 `npm run build`，再运行 `npm run serve`。`npm run start` 默认只启动中文，可通过 `npm run start -- --locale en` 单独预览英文。
