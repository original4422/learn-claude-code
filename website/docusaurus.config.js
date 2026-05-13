// @ts-check

const lightCodeTheme = require('prism-react-renderer').themes.github;
const darkCodeTheme = require('prism-react-renderer').themes.dracula;

const organizationName = process.env.ORGANIZATION_NAME || 'original4422';
const projectName = process.env.PROJECT_NAME || 'learn-claude-code';
const deploymentBranch = process.env.DEPLOYMENT_BRANCH || 'html';
const siteUrl = process.env.SITE_URL || `https://${organizationName}.github.io`;
const baseUrl = process.env.BASE_URL || `/${projectName}/`;

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: 'Claude Code Internals',
  tagline: 'A bilingual learning lab for understanding Claude Code internals.',
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
    defaultLocale: 'en',
    locales: ['en'],
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
        title: 'Claude Code Internals',
        items: [
          {
            type: 'docSidebar',
            sidebarId: 'tutorialSidebar',
            position: 'left',
            label: 'Docs',
          },
          {
            to: '/zh/docs/overview',
            position: 'left',
            label: '中文',
          },
          {
            type: 'dropdown',
            position: 'left',
            label: 'Quick Start',
            items: [
              {
                label: 'English',
                to: '/quick-start/minimal-agent',
              },
              {
                label: '中文',
                to: '/zh/quick-start/minimal-agent',
              },
            ],
          },
          {
            type: 'dropdown',
            position: 'left',
            label: 'References',
            items: [
              {
                label: 'English',
                to: '/references/pattern-cheatsheet',
              },
              {
                label: '中文',
                to: '/zh/references/pattern-cheatsheet',
              },
            ],
          },
          {
            to: '/diagrams/layered-architecture',
            position: 'left',
            label: 'Diagrams',
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
            title: 'Learn',
            items: [
              {
                label: 'English docs',
                to: '/docs/overview',
              },
              {
                label: '中文文档',
                to: '/zh/docs/overview',
              },
              {
                label: 'Quick start',
                to: '/quick-start/minimal-agent',
              },
              {
                label: '中文快速开始',
                to: '/zh/quick-start/minimal-agent',
              },
            ],
          },
          {
            title: 'Resources',
            items: [
              {
                label: 'References',
                to: '/references/pattern-cheatsheet',
              },
              {
                label: '中文参考',
                to: '/zh/references/pattern-cheatsheet',
              },
              {
                label: 'Glossary',
                to: '/glossary/en',
              },
              {
                label: '中文术语',
                to: '/glossary/zh',
              },
            ],
          },
          {
            title: 'Source',
            items: [
              {
                label: 'GitHub',
                href: `https://github.com/${organizationName}/${projectName}`,
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Claude Code Internals contributors.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ['bash', 'diff', 'json', 'python', 'typescript'],
      },
    }),
};

module.exports = config;
