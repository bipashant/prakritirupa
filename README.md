# प्रकृतिरूपा · She Who Is Nature

Website for *She Who Is Nature: Durga and Her Nine Forms*, an illustrated book by Bibek Sharma Chapagain.

A static site (plain HTML, CSS and JS, no build step) hosted on Vercel, with Vercel Web Analytics for visitor and download counts.

## Before going live: add the book

Put the PDF in the repo root, named exactly:

    she-who-is-nature.pdf

Until it's there, the download page shows "Almost ready" instead of an error.

## Deploy on Vercel

1. Go to [vercel.com/new](https://vercel.com/new) and import **bipashant/prakritirupa**.
2. Framework preset: **Other**. Leave build and output settings empty.
3. Click **Deploy**. The site goes live at **https://prakritirupa.vercel.app**.

Every push to `main` redeploys automatically.

If Vercel gives a different address, change `SITE_URL` at the top of `scripts/build.py`, run `python3 scripts/build.py`, and push. That keeps the share-preview image working.

## Analytics (free)

1. Vercel → **prakritirupa** project → **Analytics** tab → **Enable**.
2. Redeploy once (push any change, or use **Redeploy** in the Deployments tab). Analytics starts from the next deploy.

Reading the numbers in the **Pages** list:

| What you want | Where to look |
|---|---|
| People who visited | Row **/** → Visitors |
| People who downloaded | Row **/download** → Visitors |
| Total visits including repeats | Page Views column |

Every Download button goes through `/download`, so that page's visitor count is the download count.

The free Hobby plan includes 50,000 events a month and keeps one month of history.

## Editing

| What | Where |
|---|---|
| Page text, the nine forms, mantras | `scripts/build.py`, then run `python3 scripts/build.py` |
| Look and layout | `styles.css` |
| Story pop-up and hero embers | `main.js` |
| Images | `img/` (WebP, 1000 × 1506) |
| Download filename and caching | `vercel.json` |

Buy Me a Coffee: [buymeacoffee.com/bipashant](https://buymeacoffee.com/bipashant)
