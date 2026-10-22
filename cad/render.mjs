// Regenerates docs/renders/*.png from the viewer.
// Run after cad/keyboard.py: node cad/render.mjs
// Needs playwright (npm i playwright) and network access for three.js.
import { chromium } from "playwright";
import { createServer } from "node:http";
import { readFile } from "node:fs/promises";
import { dirname, extname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const root = join(here, "viewer");
const outDir = join(here, "..", "docs", "renders");
const TYPES = { ".html": "text/html; charset=utf-8", ".txt": "text/plain" };

const SHOTS = [
  { file: "hero-graphite", view: "hero", cw: "graphite" },
  { file: "hero-chalk", view: "hero", cw: "chalk" },
  { file: "hero-signal", view: "hero", cw: "signal" },
  { file: "hero-graphite-exploded", view: "hero", cw: "graphite", explode: 1 },
  { file: "top-graphite", view: "top", cw: "graphite" },
  { file: "side-graphite", view: "side", cw: "graphite" },
  { file: "under-graphite", view: "under", cw: "graphite" },
  { file: "enclosed-hero-chalk", view: "hero", cw: "chalk", case: "enclosed" },
  { file: "enclosed-hero-graphite", view: "hero", cw: "graphite", case: "enclosed" },
  { file: "enclosed-hero-graphite-exploded", view: "hero", cw: "graphite", explode: 1, case: "enclosed" },
  { file: "enclosed-side-chalk", view: "side", cw: "chalk", case: "enclosed" },
];

const server = createServer(async (req, res) => {
  try {
    const url = new URL(req.url, "http://localhost");
    const path = join(root, url.pathname === "/" ? "index.html" : decodeURIComponent(url.pathname.slice(1)));
    res.writeHead(200, { "content-type": TYPES[extname(path)] ?? "application/octet-stream" });
    res.end(await readFile(path));
  } catch {
    res.writeHead(404).end();
  }
}).listen(0);

const browser = await chromium.launch();
try {
  const page = await browser.newPage({ viewport: { width: 1600, height: 1000 }, deviceScaleFactor: 1 });
  page.on("pageerror", (e) => console.error("page error:", e.message));
  const stage = page.locator(".stage");
  let loaded = null;
  for (const s of SHOTS) {
    const kase = s.case ?? "tray";
    if (kase !== loaded) {
      const query = kase === "tray" ? "" : `?case=${kase}`;
      await page.goto(`http://localhost:${server.address().port}/${query}`);
      await page.waitForFunction(() => window.keeb?.ready(), null, { timeout: 60000 });
      loaded = kase;
    }
    await page.evaluate(({ view, cw, explode }) => {
      window.keeb.setColorway(cw);
      window.keeb.setExplode(explode ?? 0);
      window.keeb.setView(view, true);
    }, s);
    await page.waitForTimeout(400);
    await stage.screenshot({ path: join(outDir, `${s.file}.png`) });
    console.log("wrote", `${s.file}.png`);
  }
} finally {
  await browser.close();
  server.close();
}
