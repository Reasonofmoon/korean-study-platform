const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");

function readGenerated(relativePath) {
  return fs.readFileSync(path.join(process.cwd(), "public", relativePath), "utf8");
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
