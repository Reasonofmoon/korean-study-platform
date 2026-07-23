const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

function readGenerated(relativePath) {
  return fs.readFileSync(path.join(process.cwd(), "public", relativePath), "utf8");
}

function readTheme(relativePath) {
  return fs.readFileSync(path.join(process.cwd(), "themes", "gugomun", relativePath), "utf8");
}

test("renders the three school paths and 2028 high-school subjects", () => {
  const home = readGenerated("index.html");
  const high = readGenerated(path.join("high-2028", "index.html"));

  assert.match(home, /초등/);
  assert.match(home, /중등/);
  assert.match(home, /고등 2028/);
  assert.match(high, /화법과 언어/);
  assert.match(high, /독서와 작문/);
  assert.match(high, /문학/);
});

test("renders the first three high-school lesson routes", () => {
  const high = readGenerated(path.join("high-2028", "index.html"));

  assert.match(high, /lessons\/high-2028-language-purpose/);
  assert.match(high, /lessons\/high-2028-reading-structure/);
  assert.match(high, /lessons\/high-2028-literature-viewpoint/);
});

test("uses the GitHub Pages project path for global styles", () => {
  const home = readGenerated("index.html");

  assert.match(home, /href="\/korean-study-platform\/css\/site\.css"/);
});

test("separates multiple curriculum links at every viewport", () => {
  const levelLayout = readTheme(path.join("layout", "level.ejs"));
  const css = readTheme(path.join("source", "css", "site.css"));

  assert.match(levelLayout, /class="curriculum-links"/);
  assert.match(css, /\.curriculum-links \{ display: flex; flex-wrap: wrap; gap: var\(--space-2\); \}/);
  assert.match(css, /\.curriculum-links \.button \{ margin-top: var\(--space-4\); flex: 0 0 auto; \}/);
});

test("wraps Korean reading content without horizontal clipping", () => {
  const css = readTheme(path.join("source", "css", "site.css"));

  assert.match(css, /\.article-entry p, \.article-entry li \{ overflow-wrap: anywhere; word-break: normal; \}/);
});

test("publishes a 13-note Common Korean I learning map", () => {
  const map = readGenerated(path.join("high-2028", "common-korean-1", "index.html"));
  const notes = [
    "visitor", "sura", "white-porcelain", "watchman", "goodwill",
    "media-communication", "voting", "media-world", "phonological-change",
    "grammar-vocabulary", "dialogue", "vegetarian-day", "community-writing"
  ];

  assert.match(map, /공통국어 1 학습 지도/);
  assert.equal((map.match(/lessons\/common-korean-1-/g) || []).length, 13);
  assert.match(map, /문학 해석과 감상/);
  assert.match(map, /매체와 사회적 읽기/);
  assert.match(map, /언어 지식과 상호작용/);
  assert.match(map, /논증과 공동체 글쓰기/);
  notes.forEach((slug) => assert.doesNotThrow(() => readGenerated(path.join("lessons", `common-korean-1-${slug}`, "index.html"))));
});

test("publishes a 34-work literature reading map without copied source text", () => {
  const guide = readGenerated(path.join("high-2028", "literature-2015", "index.html"));

  assert.match(guide, /문학 34편 읽기 지도/);
  assert.equal((guide.match(/class="literature-note"/g) || []).length, 34);
  assert.match(guide, /언어와 정서/);
  assert.match(guide, /이야기의 사건과 인물/);
  assert.match(guide, /사회와 관계/);
  assert.match(guide, /무대와 매체/);
  assert.match(guide, /기록과 성찰/);
  assert.doesNotMatch(guide, /자료 위치|문학의 본질과 구조|문학의 수용과 생산/);
});

test("publishes a separate 32-work literature reading map without source structure", () => {
  const guide = readGenerated(path.join("high-2028", "literature-reading-2", "index.html"));

  assert.match(guide, /문학 추가 읽기 지도/);
  assert.equal((guide.match(/class="literature-note"/g) || []).length, 32);
  assert.match(guide, /감각과 정서/);
  assert.match(guide, /인물과 사건/);
  assert.match(guide, /무대와 매체/);
  assert.match(guide, /비교와 확장/);
  assert.match(guide, /기록과 성찰/);
  assert.doesNotMatch(guide, /문학의 본질과|문학의 소통|한국 문학의|문학의 흐름/);
  assert.doesNotMatch(guide, /지학사/);
  assert.ok(guide.indexOf("어느 날 고궁을 나오면서") < guide.indexOf("두근두근 내 인생"));
});
