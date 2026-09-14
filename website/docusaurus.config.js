// @ts-check

const lightCodeTheme = require('prism-react-renderer').themes.github;
const darkCodeTheme = require('prism-react-renderer').themes.dracula;

const organizationName = process.env.ORGANIZATION_NAME || 'original4422';
const projectName = process.env.PROJECT_NAME || 'learn-claude-code';
const isEnglish = process.env.DOCUSAURUS_CURRENT_LOCALE === 'en';
const deploymentBranch = process.env.DEPLOYMENT_BRANCH || 'html';
const siteUrl = process.env.SITE_URL || `https://${organizationName}.github.io`;
const baseUrl = process.env.BASE_URL || `/${projectName}/`;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: isEnglish ? 'Claude Code Internals' : 'Claude Code 源码研习',
  tagline: isEnglish
    ? 'Understand coding agents through guided chapters and runnable Python labs.'
    : '从一次提问到工具执行，通过双语导读与 Python 实验理解编程 Agent。',
  url: siteUrl,
  baseUrl,
  organizationName,
  projectName,
  deploymentBranch,
  trailingSlash: false,
  onBrokenLinks: 'warn',
  markdown: {
    mermaid: true,
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },
  i18n: {
    defaultLocale: 'zh-Hans',
    locales: ['zh-Hans', 'en'],
    localeConfigs: {
      'zh-Hans': {label: '简体中文', htmlLang: 'zh-Hans'},
      en: {label: 'English', htmlLang: 'en'},
    },
  },
  presets: [
    [
      'classic',
      {
        docs: {
          path: '../docs/en',
          routeBasePath: 'docs',
          sidebarPath: require.resolve('./sidebars.js'),
        },
        blog: false,
        theme: {
          customCss: require.resolve('./src/css/custom.css'),
        },
      },
    ],
  ],
  plugins: [
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'zh',
        path: '../docs/zh',
        routeBasePath: 'zh/docs',
        sidebarPath: require.resolve('./sidebars.zh.js'),
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'quick-start-en',
        path: '../quick-start/en',
        routeBasePath: 'quick-start',
        sidebarPath: require.resolve('./sidebars.quick-start.en.js'),
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'quick-start-zh',
        path: '../quick-start/zh',
        routeBasePath: 'zh/quick-start',
        sidebarPath: require.resolve('./sidebars.quick-start.zh.js'),
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'references-en',
        path: '../references/en',
        routeBasePath: 'references',
        sidebarPath: require.resolve('./sidebars.references.en.js'),
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'references-zh',
        path: '../references/zh',
        routeBasePath: 'zh/references',
        sidebarPath: require.resolve('./sidebars.references.zh.js'),
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'diagrams',
        path: '../diagrams',
        routeBasePath: 'diagrams',
        sidebarPath: require.resolve('./sidebars.diagrams.js'),
      },
    ],
    [
      '@docusaurus/plugin-content-docs',
      {
        id: 'glossary',
        path: '../glossary',
        routeBasePath: 'glossary',
        sidebarPath: require.resolve('./sidebars.glossary.js'),
      },
    ],
  ],
  themes: ['@docusaurus/theme-mermaid'],
  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      metadata: [
        {
          name: 'keywords',
          content: 'Claude Code, agent, LLM, Anthropic, source code, tutorial',
        },
      ],
      navbar: {
        title: 'Claude Code 源码研习',
        items: [
          {
            type: 'localeDropdown',
            position: 'right',
          },
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            docsPluginId: 'zh',
            position: 'left',
            label: '中文文档',
          },
          {
            to: '/docs/overview',
            position: 'left',
            label: 'English docs',
          },
          {
            type: 'dropdown',
            position: 'left',
            label: '快速开始',
            items: [
              {
                label: '中文',
                to: '/zh/quick-start/minimal-agent',
              },
              {
                label: 'English',
                to: '/quick-start/minimal-agent',
              },
            ],
          },
          {
            type: 'dropdown',
            position: 'left',
            label: '参考资料',
            items: [
              {
                label: '中文',
                to: '/zh/references/pattern-cheatsheet',
              },
              {
                label: 'English',
                to: '/references/pattern-cheatsheet',
              },
            ],
          },
          {
            to: '/diagrams/layered-architecture',
            position: 'left',
            label: '架构图',
          },
          {
            href: `https://github.com/${organizationName}/${projectName}`,
            label: 'GitHub',
            position: 'right',
          },
        ],
      },
      footer: {
        style: 'dark',
        links: [
          {
            title: '开始学习',
            items: [
              {label: '中文文档', to: '/zh/docs/overview'},
              {label: '快速开始', to: '/zh/quick-start/minimal-agent'},
              {label: '实验指南', to: '/zh/docs/experiments/实验指南'},
              {label: 'English docs', to: '/docs/overview'},
            ],
          },
          {
            title: '学习资料',
            items: [
              {label: '中文参考', to: '/zh/references/pattern-cheatsheet'},
              {label: '中文术语', to: '/glossary/zh'},
              {label: '架构图', to: '/diagrams/layered-architecture'},
            ],
          },
          {
            title: '项目源码',
            items: [
              {
                label: 'GitHub',
                href: `https://github.com/${organizationName}/${projectName}`,
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} ${isEnglish ? 'Claude Code Internals contributors.' : 'Claude Code 源码研习贡献者。'}`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ['bash', 'diff', 'json', 'python', 'typescript'],
      },
    }),
};

module.exports = config;
