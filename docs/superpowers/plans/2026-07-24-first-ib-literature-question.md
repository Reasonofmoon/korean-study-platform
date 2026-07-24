# First IB-Style Literature Question Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Publish one independently written MYP Year 5-style Korean literature analysis question for the existing `가는 길` exploration card.

**Architecture:** Keep the question with its work card in the existing static Hexo page so that the learning context, prompt, and scoring descriptor stay together. Extend the existing site contract test to protect the required metadata, original rubric, non-affiliation notice, and absence of source-text or publisher structure.

**Tech Stack:** Hexo 8, Markdown/HTML content, Node.js built-in test runner.

## Global Constraints

- Do not copy source prose, textbook questions, choices, answers, source order, or official IBO markscheme wording.
- Use only independently authored prompt and task-specific scoring descriptors.
- Label the exercise as IB-style practice and state that it is not affiliated with or endorsed by IBO.
- Keep the page in the high-2028 `문학` learning path.

---

### Task 1: Protect the first question contract

**Files:**
- Modify: `test/site-contract.test.cjs`
- Test: `test/site-contract.test.cjs`

**Interfaces:**
- Consumes: generated `public/high-2028/literature-exploration/index.html`.
- Produces: a contract that identifies the first item as `KOR-MYP5-LIT-001`, confirms the required metadata and disclaimer, and rejects copied source-structure labels.

- [ ] **Step 1: Write the failing test**

```js
test("publishes an original MYP-style question for 가는 길", () => {
  const guide = readGenerated(path.join("high-2028", "literature-exploration", "index.html"));

  assert.match(guide, /KOR-MYP5-LIT-001/);
  assert.match(guide, /MYP Year 5/);
  assert.match(guide, /분석/);
  assert.match(guide, /IBO와 제휴하거나 승인받은 문항이 아닙니다/);
  assert.doesNotMatch(guide, /출판사|1단원|2단원|정답/);
});
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `node --test test/site-contract.test.cjs`

Expected: the new test fails because `KOR-MYP5-LIT-001` is not yet published.

- [ ] **Step 3: Commit**

```bash
git add test/site-contract.test.cjs
git commit -m "test: define first IB-style literature question contract"
```

### Task 2: Publish one original question and task-specific descriptor

**Files:**
- Modify: `source/high-2028/literature-exploration/index.md`
- Modify: `test/site-contract.test.cjs`
- Test: `test/site-contract.test.cjs`

**Interfaces:**
- Consumes: the `가는 길` card and its independent reading cue.
- Produces: one 8-point MYP Year 5-style analysis exercise with independently written scoring descriptors.

- [ ] **Step 1: Add the minimal practice section**

```html
<section class="ib-practice" aria-labelledby="ib-question-ganeun-gil">
  <h4 id="ib-question-ganeun-gil">창작 분석 문항 · KOR-MYP5-LIT-001</h4>
  <p><strong>프로그램 단계:</strong> MYP Year 5 · <strong>측정:</strong> 분석 · <strong>명령어:</strong> 분석하고 근거를 들어 정당화하기 · <strong>8점 · 15분</strong></p>
  <p><strong>과제:</strong> 원문에서 이동의 리듬을 만드는 표현 방식 두 가지를 골라, 화자의 태도가 어떻게 드러나는지 분석하세요. 각 방식이 만드는 효과를 설명하고, 두 근거가 서로 보완되는지 판단하세요.</p>
  <p><strong>채점 관점:</strong> 1–2점은 한 특징을 지목한다. 3–4점은 특징과 효과를 연결한다. 5–6점은 두 근거를 분석해 태도와 연결한다. 7–8점은 근거의 관계까지 설명하며 가능한 다른 해석을 검토한다.</p>
  <p><small>이 연습 문항과 채점 관점은 독자 창작물이며, IBO와 제휴하거나 승인받은 문항이 아닙니다.</small></p>
</section>
```

- [ ] **Step 2: Run the focused test to verify it passes**

Run: `node --test test/site-contract.test.cjs`

Expected: all site-contract tests pass.

- [ ] **Step 3: Build and inspect the published route**

Run: `npm run build && npm test`

Expected: build exits 0 and every contract test passes.

- [ ] **Step 4: Commit**

```bash
git add source/high-2028/literature-exploration/index.md test/site-contract.test.cjs docs/superpowers/plans/2026-07-24-first-ib-literature-question.md
git commit -m "feat: add first IB-style literature practice"
```
