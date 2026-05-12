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
npm run build
```

The static site output is written to `website/build/`. The `html` branch is
intended to contain only that built static output for GitHub Pages.

静态页面的输出写入 `website/build/` 。
而 `html` 分支只存放构建好的静态页面用于 Github Pages 。