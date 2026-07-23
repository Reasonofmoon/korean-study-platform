# Korean Study Platform Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an independent static Hexo Korean-language learning platform with elementary, middle-school, and 2028 high-school routes.

**Architecture:** Hexo renders Markdown lessons through a single custom EJS theme. Page front matter supplies learning level, subject, order, study time, and availability; layouts aggregate those posts into a reusable filterable lesson ledger. The site is static, requires no account, and receives a small Node contract test after generation.

**Tech Stack:** Node.js 24, Hexo 8, EJS, CSS, browser-native JavaScript, Node test runner.

## Global Constraints

- Keep this repository independent; do not add the English-platform repository as a remote or submodule.
- Use the design tokens and primitives in `DESIGN.md`.
- Use the 2028 common high-school areas: 화법과 언어, 독서와 작문, 문학.
- Do not reuse third-party brand names, logos, teaching material, or media.
- Do not add accounts, tracking, or a database.

---

### Task 1: Create the Hexo project and project harness

**Files:**
- Create: `package.json`, `_config.yml`, `.gitignore`, `CLAUDE.md`
- Create: `.claude/agents/content-curator.md`, `.claude/agents/curriculum-qa.md`, `.claude/skills/korean-lesson-publishing/SKILL.md`, `.claude/skills/korean-platform-orchestrator/SKILL.md`

- [ ] Define only Hexo build, server, and test scripts in `package.json`.
- [ ] Install the declared dependencies and verify `npx hexo version` reports Hexo 8.
- [ ] Add the harness pointer and the reusable roles without creating command files.
- [ ] Commit project foundation after the build script is runnable.

### Task 2: Prove the site contract before implementing pages

**Files:**
- Create: `test/site-contract.test.cjs`

- [ ] Write a Node test that expects generated `public/index.html`, `public/high-2028/index.html`, and the three high-school subject labels.
- [ ] Run `npm test` before layouts exist and observe failure because the generated pages are absent.
- [ ] Keep the test limited to navigation and curriculum facts that a static build can prove.

### Task 3: Implement the design system, shared shell, and showcase

**Files:**
- Create: `themes/gugomun/layout/layout.ejs`, `themes/gugomun/layout/_partial/header.ejs`, `themes/gugomun/layout/_partial/footer.ejs`
- Create: `themes/gugomun/layout/showcase.ejs`, `themes/gugomun/source/css/site.css`, `source/design-system/index.md`

- [ ] Render semantic header, navigation, main, and footer landmarks.
- [ ] Implement the token-only paper-and-ink design system and focus/reduced-motion rules.
- [ ] Render the documented card, chip, and ledger primitives in all supported static states.

### Task 4: Implement the learning routes and initial lessons

**Files:**
- Create: `themes/gugomun/layout/home.ejs`, `themes/gugomun/layout/level.ejs`, `themes/gugomun/layout/post.ejs`
- Create: `source/index.md`, `source/elementary/index.md`, `source/middle/index.md`, `source/high-2028/index.md`, `source/library/index.md`
- Create: `source/_posts/elementary-story-sequence.md`, `source/_posts/middle-poetry-speaker.md`, `source/_posts/high-2028-language-purpose.md`, `source/_posts/high-2028-reading-structure.md`, `source/_posts/high-2028-literature-viewpoint.md`
- Create: `themes/gugomun/source/js/filters.js`

- [ ] Use front matter as the source of truth for learning metadata.
- [ ] Render route-specific filter buttons as native buttons with `aria-pressed`.
- [ ] Filter lesson rows without removing their semantic document order.
- [ ] Make every learning page usable without JavaScript.

### Task 5: Generate, test, and inspect the production artifact

**Files:**
- Modify: `test/site-contract.test.cjs` only if a verified generated-path behavior requires coverage.

- [ ] Run `npm test` and observe the site contract passing.
- [ ] Run `npm run build` from a clean output directory.
- [ ] Serve the generated site and inspect home, high-2028, and a lesson at 375px, 768px, and 1280px.
- [ ] Verify the high-school filter states with keyboard focus and mouse activation.
- [ ] Commit verified source changes only after tests and build complete.
