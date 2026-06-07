#!/usr/bin/env node
import fs from 'fs';
import path from 'path';
import { pathToFileURL } from 'url';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);

function usage() {
  console.error('Usage: node render-html-pdf.mjs input.html output.pdf [--screenshot preview.png] [--chrome /path/to/Chrome]');
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length < 2) usage();

const inputHtml = path.resolve(args[0]);
const outputPdf = path.resolve(args[1]);
let screenshot = '';
let chromePath = process.env.CHROME_PATH || '';

for (let i = 2; i < args.length; i += 1) {
  if (args[i] === '--screenshot') {
    screenshot = path.resolve(args[++i] || '');
  } else if (args[i] === '--chrome') {
    chromePath = args[++i] || '';
  } else {
    usage();
  }
}

if (!fs.existsSync(inputHtml)) {
  throw new Error(`HTML file not found: ${inputHtml}`);
}

function loadPuppeteer() {
  const candidates = [
    process.cwd(),
    '/Users/jude/同步空间/作品集/APP/bazi/fatepaw',
    '/Users/jude/同步空间/作品集/APP/bazi/backend-dev',
  ];
  for (const dir of candidates) {
    try {
      const localRequire = createRequire(path.join(dir, 'package.json'));
      return localRequire('puppeteer');
    } catch {}
  }
  return require('puppeteer');
}

function findChrome() {
  const candidates = [
    chromePath,
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  ].filter(Boolean);
  return candidates.find((p) => fs.existsSync(p));
}

const puppeteer = loadPuppeteer();

async function launchBrowser() {
  const args = ['--no-sandbox', '--disable-setuid-sandbox', '--allow-file-access-from-files'];
  try {
    return await puppeteer.launch({ headless: 'new', args });
  } catch (err) {
    const executablePath = findChrome();
    if (!executablePath) throw err;
    return await puppeteer.launch({ headless: 'new', executablePath, args });
  }
}

const browser = await launchBrowser();
try {
  const page = await browser.newPage();
  await page.setViewport({ width: 794, height: 1123, deviceScaleFactor: 1 });
  await page.goto(pathToFileURL(inputHtml).href, { waitUntil: 'networkidle0', timeout: 60000 });
  await page.evaluateHandle('document.fonts.ready');
  await page.emulateMediaType('print');
  await fs.promises.mkdir(path.dirname(outputPdf), { recursive: true });
  await page.pdf({
    path: outputPdf,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: '0px', right: '0px', bottom: '0px', left: '0px' },
  });
  if (screenshot) {
    await fs.promises.mkdir(path.dirname(screenshot), { recursive: true });
    await page.screenshot({ path: screenshot, fullPage: false });
  }
  console.log(outputPdf);
  if (screenshot) console.log(screenshot);
} finally {
  await browser.close();
}
