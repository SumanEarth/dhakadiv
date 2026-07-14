# মৌজা ম্যাপ আর্কাইভ সার্চ — Mouza Map Archive Search

A static, client-side search tool over your 40,598-row Excel index (`FolderPath`,
`FileName`). No backend, no database, no server costs — everything runs in the
visitor's browser.

## What's in this folder

| File | Purpose |
|---|---|
| `index.html` | The whole app — search box, results, styling, logic. Fetches `data.json`. |
| `data.json` | Your spreadsheet, converted. Folder paths are de-duplicated (913 unique folders vs. 40,598 rows), so the file is ~1.6 MB instead of ~6 MB — loads once, then everything is instant. |
| `convert.py` | Regenerates `data.json` whenever your source Excel changes. |

## How search works

- **Default (smart) mode**: type any words, in any order, in Bangla or English —
  e.g. `পল্লবী 11` or `Rajbari thana`. Every word must appear *somewhere* in the
  folder path or filename (AND search), case-insensitive. This is instant —
  plain substring matching over 40k rows takes single-digit milliseconds in the
  browser.
- **Typo-tolerant fallback**: if the AND search finds nothing, it automatically
  retries with fuzzy matching (via Fuse.js) so a misspelled or slightly-off
  query still surfaces close matches. You'll see a "কাছাকাছি মিল (fuzzy match)"
  label when this kicks in.
- **Regex mode**: tick the "Regex" checkbox to search with a raw JavaScript
  regular expression against the combined folder+filename text — e.g.
  `^13-RS-.*পাড়া$` or `Thana-(Faridpur|Rajbari)`.
- Results are capped at 300 rendered rows at a time (with a note if there are
  more) so the page stays smooth even on a broad query. Each row has a
  **Copy** button that copies `FolderPath / FileName` to the clipboard.

## Deploy it — GitHub + Cloudflare Pages (recommended)

This skips GitHub Pages entirely and lets Cloudflare build straight from your
repo — one hop, free, fast global CDN (good for Bangladesh-based visitors),
auto-redeploys on every push.

1. **Create a GitHub repo** (e.g. `mouza-map-search`) and push these three
   files to it (root of the repo, or a folder — you'll point Cloudflare at
   whichever directory holds `index.html`):
   ```bash
   git init
   git add index.html data.json convert.py README.md
   git commit -m "Mouza map archive search"
   git branch -M main
   git remote add origin https://github.com/<your-username>/mouza-map-search.git
   git push -u origin main
   ```

2. **Connect Cloudflare Pages**:
   - Go to the Cloudflare dashboard → **Workers & Pages** → **Create** → **Pages** → **Connect to Git**.
   - Authorize GitHub, select the repo.
   - Build settings: **Framework preset: None**, **Build command: (leave empty)**,
     **Build output directory: /** (or the subfolder if you put the files in one).
   - Click **Save and Deploy**. You'll get a live URL like
     `mouza-map-search.pages.dev` within a minute.

3. **Optional custom domain**: in the Pages project → **Custom domains**, add
   e.g. `maps.yourdomain.com`. If the domain's DNS is already on Cloudflare
   this is a one-click CNAME; otherwise it'll walk you through adding the
   record.

4. **Future updates**: any `git push` to `main` triggers an automatic
   rebuild/redeploy — nothing else to configure.

### If you'd rather use GitHub Pages instead
Repo → Settings → Pages → Source: deploy from `main` branch, root folder.
GitHub Pages works fine for this too; the only reason to prefer Cloudflare
Pages is faster edge caching and easier custom-domain/analytics handling.

## Updating the data later

When the source Excel changes (new divisions, corrected filenames, etc.):
```bash
pip install pandas openpyxl
python3 convert.py path/to/new-file.xlsx
git add data.json
git commit -m "Update map index"
git push
```
Cloudflare Pages (or GitHub Pages) picks it up automatically.

## Notes / limits

- This is a **search over the file *list***, not the PDFs themselves — the
  actual scanned maps aren't hosted here (per [[mouza-map-archive]], those
  live in your Google Drive archive). The Copy button is there so you can
  paste the exact path into Drive search.
- `data.json` is fetched in full on page load (~1.6 MB, gzip-compressed to a
  few hundred KB by Cloudflare/GitHub automatically). For 40k rows this is
  the simplest approach and keeps search instant with zero backend. If the
  dataset grows to several hundred thousand rows, the same file can be
  swapped for a small Cloudflare Worker + KV/D1 lookup — flag it if you get
  there and it's a straightforward next step.
