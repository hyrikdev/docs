# Review list

Things to finish or check before the guide is shared with the Tangent team.

## 1. Screenshots still needed

The site screenshots (35 images in `images/`, desktop 1440 and phone 375) were taken from the new design's
preview. The Shopify admin and the theme editor couldn't be captured. Add these, cropped to the relevant part,
and remove any store details (staff names, emails) before saving them:

| Page | Screenshot |
|---|---|
| `getting-started/theme-editor.mdx` | The theme editor: top bar (page picker, desktop/mobile switch, undo, Save), left sidebar, preview. |
| `getting-started/preview-and-publish.mdx` | **Online Store → Themes**: the current theme and the **Theme library**, with the **…** menu open (Duplicate, Preview, Publish). |
| `getting-started/sections-and-blocks.mdx` | The sidebar with a section expanded, showing nested groups, a **Card list** and its **Card** blocks. |
| `editing-pages/how-pages-work.mdx` | The page picker open on **Pages**, with the search box and a few templates (e.g. **location-chicago**). |
| `editing-pages/how-pages-work.mdx` | A setting connected to a page field (how a connected text looks in the editor). |
| `editing-pages/editing-content.mdx` | Drag handle, eye icon, **Add block** and the block menu with **Duplicate**. |
| `blocks/card-list.mdx` | The **Card list** settings panel (Layout, Card icon) and a **Card** settings panel (Title, Text, Label, Icon, Image). |
| `design-rules/icons.mdx` | The **Icon** drop-down list of a card, showing the "Tangent …" icon names. |
| `admin/pages-and-seo.mdx` | A page record: **Theme template**, **Search engine listing** (open), **Metafields**. |
| `admin/blog-posts.mdx` | The blog post editor: Title, Content, Excerpt, Image, Blog, Tags, Search engine listing. |
| `admin/faq-entries.mdx` | **Content → Metaobjects → FAQ** list and one FAQ entry (Question, Answer, Category). |
| `admin/menus.mdx` | **Online Store → Navigation** with the menus, and the menu editor. |
| `admin/files-and-images.mdx` | **Content → Files** with an image open and the **Alt text** field. |
| `admin/url-redirects.mdx` | The **Create URL redirect** form. |
| `how-to/add-location-page.mdx` | The **Create template** dialog (Name, Based on). |
| `how-to/change-phone-number.mdx` | **Settings → Store details** (phone field) and the header **Phone** block settings. |

## 2. Facts to confirm

- **Admin menu names.** The guide uses **Online Store → Pages / Blog posts / Navigation** and
  **Content → Metaobjects / Files**. Shopify has been moving items between **Online Store** and **Content**.
  Check the current names in the store's admin and adjust (each page also tells readers to use the admin search).
- **Theme editor wording** to check on screen: **Create template** and **Based on**; the block menu with
  **Duplicate** (the "…" button or right-click); **Remove block**; the eye icon to hide; **Change** / **Upload** /
  **Select** in the image picker.
- **Alt text.** The guide sends readers to **Content → Files** to add alt text. Check whether the theme editor's
  image picker also offers it, and mention it if so.
- **Restoring an older layout.** The guide says Shopify keeps older versions of each theme file and a developer
  can restore one. Confirm this matches how the theme is maintained (code editor history or the theme's code
  repository).
- **"Create a URL redirect"** tick box when a page's URL handle changes: check the exact label.
- **Section links** (anchors) such as `/editing-pages/how-pages-work#text-that-comes-from-the-pages-own-fields`
  and `/blocks/card-list#text-then-its-image-on-phones`: check they jump to the right heading in `mint dev`.
- **The new design's theme name** and when it will be published. The guide says "a theme that isn't published
  yet" (`help/troubleshooting.mdx`, `getting-started/preview-and-publish.mdx`). Update those pages after launch.
- **Phone number spread.** Counted in the theme: about 80 page layouts with their own call buttons (93 buttons)
  and contact details blocks (60), plus the header, the mobile call bar, the footer text and the footer menu. The
  guide asks readers to have a developer change the number site-wide. Confirm that's the intended process.
- **Old `/services/...` addresses** (14) can't be redirected inside Shopify. The guide says so and points to the
  developer. Update if a fix at the domain host is put in place.
- **Logo and favicon.** `logo/tangent-logo.svg` is copied from the theme's `assets/tangent-logo.svg`;
  `logo/favicon.svg` is the theme's pixel mark (`assets/ts-pixel-mark.svg`). Check the favicon reads well at
  small sizes.
- **Fonts.** `docs.json` loads Geist (headings) and Inter (body) from Google Fonts. Check they render in
  `mint dev`.
- **Light mode only.** `docs.json` turns off dark mode, because the logo has dark lettering. Add a light version
  of the logo if dark mode is wanted.

## 3. Placeholders

- **Support contact** in `help/contact.mdx`: name, email and response time of whoever looks after the theme.
- No GitHub repository or Mintlify account has been set up yet (see `README.md` for the steps).

## 4. Decisions for the site owner

- **Who edits the page layouts after launch.** The service, location and landing page layouts were set up by
  the developer from the content of the old website. If the developer sets those layouts up again later, edits
  made by the team in the theme editor in the meantime would be lost. Agree on one rule, for example: after
  launch, the theme editor is the master copy and the developer only changes what is asked.
- **Templates created in the theme editor** (new location pages) exist only in that theme. Decide how the
  developer is told, so they're kept when the theme is updated.
- **Theme copies.** The guide recommends duplicating the live theme before big changes. Agree who may publish a
  copy, so two people don't overwrite each other's work.
