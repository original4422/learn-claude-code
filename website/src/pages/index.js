import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import styles from './index.module.css';

const tracks = [
  {
    title: 'Architecture Walkthrough',
    description:
      'Read the guided chapters from startup flow to tool dispatch, permissions, memory, MCP, streaming, and commands.',
    href: '/docs/overview',
    altLabel: '中文文档',
    altHref: '/zh/docs/overview',
  },
  {
    title: 'Quick Start',
    description:
      'Build a minimal agent, add a tool, and wire a streaming chat loop through short tutorials.',
    href: '/quick-start/minimal-agent',
    altLabel: '中文快速开始',
    altHref: '/zh/quick-start/minimal-agent',
  },
  {
    title: 'Hands-on Labs',
    description:
      'Pair each chapter with a runnable Python experiment that recreates one production-shaped agent pattern.',
    href: '/docs/experiments/experiment-guide',
    altLabel: '中文实验指南',
    altHref: '/zh/docs/experiments/实验指南',
  },
  {
    title: 'References',
    description:
      'Keep the source-map notes, pattern cheatsheets, diagrams, and glossary close while reading.',
    href: '/references/pattern-cheatsheet',
    altLabel: '中文参考',
    altHref: '/zh/references/pattern-cheatsheet',
  },
];

export default function Home() {
  return (
    <Layout
      title="Claude Code Internals"
      description="A bilingual learning lab for understanding Claude Code internals">
      <main>
        <section className={styles.hero}>
          <div className={styles.heroInner}>
            <p className={styles.eyebrow}>Learning Lab</p>
            <Heading as="h1" className={styles.title}>
              Claude Code Internals
            </Heading>
            <p className={styles.subtitle}>
              A structured, bilingual tutorial for studying Claude Code as a real CLI agent:
              architecture, loop design, tools, permissions, memory, MCP, streaming, and
              hands-on Python labs.
            </p>
            <div className={styles.actions}>
              <Link className="button button--primary button--lg" to="/docs/overview">
                Start reading
              </Link>
              <Link className="button button--secondary button--lg" to="/zh/docs/overview">
                中文文档
              </Link>
            </div>
          </div>
        </section>
        <section className={styles.tracks}>
          {tracks.map((track) => (
            <article className={styles.track} key={track.title}>
              <Heading as="h2">{track.title}</Heading>
              <p>{track.description}</p>
              <div className={styles.trackLinks}>
                <Link to={track.href}>English</Link>
                <Link to={track.altHref}>{track.altLabel}</Link>
              </div>
            </article>
          ))}
        </section>
      </main>
    </Layout>
  );
}
