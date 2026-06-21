import fs from "node:fs";
import path from "node:path";

const root = path.resolve(new URL("..", import.meta.url).pathname);

function walk(dir) {
  const out = [];
  for (const name of fs.readdirSync(dir)) {
    // Не обходим scripts (фикстуры с намеренно битыми ссылками), .obsidian, .git.
    // 08_Graph/09_Archive/07_Templates ОБХОДИМ — они валидные цели wikilink'ов
    // (иначе ссылки на них из index/Sources ложно считаются битыми). Dandelion-правила
    // всё равно применяются только к 03_Wiki.
    if (name === ".obsidian" || name === ".git" || name === "scripts"
        || name === ".pytest_cache" || name === "__pycache__") continue;
    const p = path.join(dir, name);
    const st = fs.statSync(p);
    if (st.isDirectory()) out.push(...walk(p));
    else if (name.endsWith(".md")) out.push(p);
  }
  return out;
}

function rel(file) {
  return path.relative(root, file).replace(/\\/g, "/");
}

function parseFrontmatter(text) {
  if (!text.startsWith("---\n")) return null;
  const end = text.indexOf("\n---", 4);
  if (end === -1) return null;
  const raw = text.slice(4, end).trim();
  const data = {};
  let currentKey = null;
  for (const line of raw.split(/\r?\n/)) {
    const match = line.match(/^([A-Za-z0-9_-]+):\s*(.*)$/);
    if (match) {
      currentKey = match[1];
      data[currentKey] = match[2].trim();
      continue;
    }
    const listMatch = line.match(/^\s+-\s+(.+)$/);
    if (listMatch && currentKey) {
      data[currentKey] = data[currentKey]
        ? `${data[currentKey]}, ${listMatch[1].trim()}`
        : listMatch[1].trim();
    }
  }
  return data;
}

const files = walk(root);
const wikiPages = new Set();
const baseNames = new Map();

for (const file of files) {
  const noExt = rel(file).replace(/\.md$/, "");
  wikiPages.add(noExt);
  const base = path.posix.basename(noExt);
  if (!baseNames.has(base)) baseNames.set(base, []);
  baseNames.get(base).push(noExt);
}

const EDGE_VOCAB = new Set(["part_of","measures","derived_from","causes","affects","depends_on","segments","evidence"]);

const findings = {
  files: files.length,
  brokenLinks: [],
  missingFrontmatter: [],
  missingOwner: [],
  missingStatus: [],
  missingSource: [],
  missingConfidence: [],
  noOutboundLinks: [],
  lowConfidence: [],
  draftPages: [],
  decisionsWithoutReviewDate: [],
  duplicateBasenames: [],
  noUpLink: [],
  unknownEdgeType: [],
  reportLinkFromWiki: [],
};

for (const [base, pages] of baseNames.entries()) {
  if (pages.length > 1) findings.duplicateBasenames.push({ base, pages });
}

for (const file of files) {
  const text = fs.readFileSync(file, "utf8");
  const relative = rel(file);
  const dir = path.posix.dirname(relative);
  const fm = parseFrontmatter(text);
  const isTemplate = relative.startsWith("07_Templates/");

  if (!fm) findings.missingFrontmatter.push(relative);
  else {
    if (!fm.owner) findings.missingOwner.push(relative);
    if (!fm.status) findings.missingStatus.push(relative);
    if (!fm.source) findings.missingSource.push(relative);
    if (!fm.confidence) findings.missingConfidence.push(relative);
    if (fm.confidence === "low") findings.lowConfidence.push(relative);
    if (fm.status === "draft") findings.draftPages.push(relative);
    if (!isTemplate && fm.type === "decision" && !fm.review_after) {
      findings.decisionsWithoutReviewDate.push(relative);
    }
  }

  if (relative.startsWith("03_Wiki/")) {
    const typed = [...text.matchAll(/^\s*([a-z_]+)::\s*\[\[([^\]]+)\]\]/gm)];
    if (!typed.some(m => m[1] === "part_of")) findings.noUpLink.push(relative);
    for (const m of typed) if (!EDGE_VOCAB.has(m[1])) findings.unknownEdgeType.push({ file: relative, type: m[1] });
    if (/\[\[[^\]]*Agent Reports\/[^\]]*\]\]/.test(text)) findings.reportLinkFromWiki.push(relative);
  }

  const links = [...text.matchAll(/\[\[([^\]]+)\]\]/g)]
    .map((m) => m[1].split("|")[0].split("#")[0].trim())
    .filter(Boolean);
  if (links.length === 0 && !relative.startsWith("07_Templates/")) findings.noOutboundLinks.push(relative);

  for (const raw of links) {
    const rawNorm = path.posix.normalize(raw).replace(/^\.\//, "");
    const relativeNorm = path.posix.normalize(path.posix.join(dir, raw)).replace(/^\.\//, "");
    const base = path.posix.basename(rawNorm);
    if (wikiPages.has(rawNorm) || wikiPages.has(relativeNorm) || baseNames.has(base)) continue;
    findings.brokenLinks.push({ file: relative, link: raw });
  }
}

const summary = {
  files: findings.files,
  brokenLinks: findings.brokenLinks.length,
  missingFrontmatter: findings.missingFrontmatter.length,
  missingOwner: findings.missingOwner.length,
  missingStatus: findings.missingStatus.length,
  missingSource: findings.missingSource.length,
  missingConfidence: findings.missingConfidence.length,
  noOutboundLinks: findings.noOutboundLinks.length,
  lowConfidence: findings.lowConfidence.length,
  draftPages: findings.draftPages.length,
  decisionsWithoutReviewDate: findings.decisionsWithoutReviewDate.length,
  duplicateBasenames: findings.duplicateBasenames.length,
  noUpLink: findings.noUpLink.length,
  unknownEdgeType: findings.unknownEdgeType.length,
  reportLinkFromWiki: findings.reportLinkFromWiki.length,
};

console.log(JSON.stringify({ summary, findings }, null, 2));

if (findings.brokenLinks.length > 0 || findings.missingFrontmatter.length > 0) {
  process.exitCode = 1;
}
