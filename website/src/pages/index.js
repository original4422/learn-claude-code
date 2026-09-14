import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

const chineseTracks = [
  {
    title: '理解核心架构',
    description:
      '从启动流程到 Agent 主循环，跟随 17 章导读理解工具、权限、记忆与上下文管理。',
    href: '/zh/docs/overview',
    label: '阅读中文导读',
    altHref: '/docs/overview',
  },
  {
    title: '写出第一个 Agent',
    description:
      '从最小循环开始，逐步添加工具调用与流式聊天，用 3 篇教程把概念变成代码。',
    href: '/zh/quick-start/minimal-agent',
    label: '开始入门教程',
    altHref: '/quick-start/minimal-agent',
  },
  {
    title: '动手验证机制',
    description:
      '运行 15 个 Python 实验，把章节里的设计变成可观察的结果；先用 Mock 模式，无需 API Key。',
    href: '/zh/docs/experiments/实验指南',
    label: '查看实验指南',
    altHref: '/docs/experiments/experiment-guide',
  },
  {
    title: '随时查阅与回顾',
    description:
      '通过源码地图、设计模式速查卡、架构图与术语表，定位实现线索，串起知识脉络。',
    href: '/zh/references/pattern-cheatsheet',
    label: '打开中文参考',
    altHref: '/references/pattern-cheatsheet',
  },
];

const englishTracks = [
  {
    title: 'Understand the architecture',
    description:
      'Follow 17 guided chapters from startup to the agent loop, tools, permissions, memory, and context management.',
    href: '/docs/overview',
    label: 'Read the guide',
    altHref: '/zh/docs/overview',
  },
  {
    title: 'Build your first agent',
    description:
      'Start with a minimal loop, then add tools and streaming chat through three hands-on tutorials.',
    href: '/quick-start/minimal-agent',
    label: 'Start the tutorials',
    altHref: '/zh/quick-start/minimal-agent',
  },
  {
    title: 'Explore working experiments',
    description:
      'Run 15 Python labs to see the designs in action. Start in Mock mode with no API key.',
    href: '/docs/experiments/experiment-guide',
    label: 'Open the lab guide',
    altHref: '/zh/docs/experiments/实验指南',
  },
  {
    title: 'Look up and connect ideas',
    description:
      'Find implementation clues with source maps, pattern cheatsheets, architecture diagrams, and a glossary.',
    href: '/references/pattern-cheatsheet',
    label: 'Browse references',
    altHref: '/zh/references/pattern-cheatsheet',
  },
];

const copy = {
  'zh-Hans': {
    title: 'Claude Code 源码研习',
    description: '通过 17 章双语导读与 15 个 Python 实验，理解 Claude Code 的 Agent 循环、工具、权限、记忆与 MCP。首个实验无需 API Key。',
    eyebrow: '17 章双语导读 · 15 个 Python 实验',
    subtitle: '从一次提问到工具执行，拆解编程 Agent 的工作原理。结合源码导读与可运行的 Python 实验，逐步理解主循环、工具、权限、记忆与多 Agent 协作。',
    start: '动手写第一个 Agent',
    read: '阅读中文导读',
    startHref: '/zh/quick-start/minimal-agent',
    readHref: '/zh/docs/overview',
    note: 'Mock 模式无需 API Key · 独立教学项目，基于固定源码快照',
    alternate: 'English',
    alternateLang: 'en',
    tracks: chineseTracks,
  },
  en: {
    title: 'Claude Code Internals',
    description: 'Understand Claude Code through 17 bilingual chapters and 15 Python labs covering agent loops, tools, permissions, memory, and MCP. Start with no API key.',
    eyebrow: '17 bilingual chapters · 15 Python labs',
    subtitle: 'Follow a prompt all the way to tool execution. Combine source walkthroughs with runnable Python labs to understand the agent loop, tools, permissions, memory, and multi-agent collaboration.',
    start: 'Build your first agent',
    read: 'Read the guide',
    startHref: '/quick-start/minimal-agent',
    readHref: '/docs/overview',
    note: 'No API key needed in Mock mode · Independent learning project based on a fixed source snapshot',
    alternate: '中文',
    alternateLang: 'zh-Hans',
    tracks: englishTracks,
  },
};

export default function Home() {
  const {i18n: {currentLocale}} = useDocusaurusContext();
  const content = copy[currentLocale] ?? copy['zh-Hans'];
  return (
    <Layout
      title={content.title}
      description={content.description}>
      <main>
        <section className={styles.hero}>
          <div className={styles.heroInner}>
            <p className={styles.eyebrow}>{content.eyebrow}</p>
            <Heading as="h1" className={styles.title}>
              {content.title}
            </Heading>
            <p className={styles.subtitle}>
              {content.subtitle}
            </p>
            <div className={styles.actions}>
              <Link className="button button--primary button--lg" to={content.startHref}>
                {content.start}
              </Link>
              <Link className="button button--secondary button--lg" to={content.readHref}>
                {content.read}
              </Link>
            </div>
            <p className={styles.note}>
              {content.note}
            </p>
          </div>
        </section>
        <section className={styles.tracks}>
          {content.tracks.map((track) => (
            <article className={styles.track} key={track.title}>
              <Heading as="h2">{track.title}</Heading>
              <p>{track.description}</p>
              <div className={styles.trackLinks}>
                <Link to={track.href}>{track.label}</Link>
                <Link to={track.altHref} lang={content.alternateLang}>{content.alternate}</Link>
              </div>
            </article>
          ))}
        </section>
      </main>
    </Layout>
  );
}
