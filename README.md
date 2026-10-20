# Tangent Solutions site guide

This folder holds the admin guide for the Tangent Solutions website (usetangent.com).
It explains, in plain language, how to edit the site in Shopify.

The guide is built with [Mintlify](https://mintlify.com), a tool that turns these files into a small website
with a menu and a search box.

## What is in this folder

| File or folder | What it is |
|---|---|
| `docs.json` | The guide's settings: its name, colors, logo and the menu on the left. |
| `*.mdx` files | The pages of the guide. Each file is one page. You can open them in any text editor. |
| `images/` | The screenshots used in the pages. |
| `logo/` | The Tangent logo and the small browser-tab icon. |
| `scripts/` | The script that writes the settings tables from the theme's code, and the plain-words notes for them. |
| `REVIEW.md` | A to-do list for the people who look after this guide: missing screenshots, facts to confirm, placeholders. |

## Preview the guide on your computer

You need Node.js (version 20 or newer) on your computer. Get it from [nodejs.org](https://nodejs.org).

1. Open a terminal (on a Mac: the Terminal app).
2. Install the Mintlify tool once:

   ```bash
   npm i -g mint
   ```

3. Go to this folder, then start the preview:

   ```bash
   cd path/to/tangent-docs
   mint dev
   ```

4. Open http://localhost:3000 in your browser. The page updates each time you save a file.
5. To stop the preview, go back to the terminal and press Control + C.

## Publish the guide online

1. Put this folder in a GitHub repository (done: hyrikdev/docs).
2. Sign up at [mintlify.com](https://mintlify.com).
3. In the Mintlify dashboard, connect the GitHub repository.
4. Mintlify builds the guide and gives you a web address for it.

From then on, every change pushed to the repository updates the online guide on its own.

## Editing a page

- Each page is a `.mdx` file. It is plain text with a few extra tags, such as `<Steps>` for numbered steps
  or `<Note>` for a highlighted note.
- To add a page to the menu on the left, add its file name (without `.mdx`) to `docs.json`.
- Keep screenshots in `images/` and refer to them as `/images/name.png`.

## Settings tables

The settings tables on the block and theme settings pages are written by a script from the theme's own code,
so the labels, options and defaults match the theme editor. The **Tangent uses** column counts what the site's
pages actually use. Text between `settings:begin` and `settings:end` is replaced each time the script runs: don't
edit it by hand.

After a theme release, from this folder, with the theme repository next to it:

```bash
python3 scripts/settings_tables.py --theme ../tangent
```

- `--check` only lists the pages that are out of date (it exits with an error if any are).
- `--print block:faq-category` shows one table without writing anything.
- To explain a setting in plain words, add it to `scripts/notes/<kind>_<name>.json`, for example
  `scripts/notes/block_card-list.json`: `{"<setting id>": "Your note"}`. The note replaces the theme's own help text.
