#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";

const [, , htmlPath, pdfPath, previewPath] = process.argv;

function fail(message) {
  console.error(`FAIL: ${message}`);
  process.exitCode = 1;
}

function pass(message) {
  console.log(`PASS: ${message}`);
}

function requireFile(filePath, label) {
  if (!filePath) {
    fail(`missing ${label} path`);
    return false;
  }
  if (!fs.existsSync(filePath)) {
    fail(`${label} does not exist: ${filePath}`);
    return false;
  }
  const size = fs.statSync(filePath).size;
  if (size <= 0) {
    fail(`${label} is empty: ${filePath}`);
    return false;
  }
  pass(`${label} exists (${size} bytes): ${filePath}`);
  return true;
}

if (!htmlPath || !pdfPath) {
  console.error("Usage: node scripts/validate-output.mjs output.html output.pdf [preview.png]");
  process.exit(2);
}

if (requireFile(htmlPath, "HTML")) {
  const html = fs.readFileSync(htmlPath, "utf8");
  const requiredPatterns = [
    ["A4 @page rule", /@page/i],
    ["210mm width contract", /210mm/i],
    ["297mm height contract", /297mm/i],
    ["page container", /class=(['\"][^'\"]*page|[^>]*\\bpage\\b)/i]
  ];

  for (const [label, pattern] of requiredPatterns) {
    if (pattern.test(html)) {
      pass(label);
    } else {
      fail(`HTML missing ${label}`);
    }
  }

  const forbidden = [
    ["placeholder lorem ipsum", /lorem ipsum/i],
    ["debug outline", /debug-outline|outline:\\s*1px\\s+solid\\s+red/i],
    ["unresolved TODO", /\\bTODO\\b|待写|待生成/]
  ];

  for (const [label, pattern] of forbidden) {
    if (pattern.test(html)) {
      fail(`HTML contains ${label}`);
    } else {
      pass(`no ${label}`);
    }
  }
}

requireFile(pdfPath, "PDF");
if (path.extname(pdfPath).toLowerCase() !== ".pdf") {
  fail(`PDF path does not end with .pdf: ${pdfPath}`);
}

if (previewPath) {
  requireFile(previewPath, "preview image");
}

