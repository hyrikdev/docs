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
- The guide lives in the public GitHub repository hyrikdev/docs; pushes to `main` deploy through Mintlify.

## 4. Decisions for the site owner

- **Who edits the page layouts after launch.** The service, location and landing page layouts were set up by
  the developer from the content of the old website. If the developer sets those layouts up again later, edits
  made by the team in the theme editor in the meantime would be lost. Agree on one rule, for example: after
  launch, the theme editor is the master copy and the developer only changes what is asked.
- **Templates created in the theme editor** (new location pages) exist only in that theme. Decide how the
  developer is told, so they're kept when the theme is updated.
- **Theme copies.** The guide recommends duplicating the live theme before big changes. Agree who may publish a
  copy, so two people don't overwrite each other's work.

## 5. Pages added on 2026-10-20

The **Coming from WordPress**, **Shopify and Horizon** and **Page recipes** groups, ten block pages, and the
**Technical** tab. They describe the theme as of 2026-10-20; the theme is still changing, so re-check the page
recipes and block pages after each release.

### Screenshots wanted

The storefront screenshots of these pages (24 images, desktop 1440 and phone 375) were taken on 2026-10-20
from the theme preview, which runs the same code as the live theme. The ones left need the Shopify admin, the
theme editor or GitHub.

| Page | Screenshot |
|---|---|
| `horizon/theme-settings.mdx` | The editor with Theme settings open (group list), and the **Logo and favicon** group. |
| `horizon/sections-groups-blocks.mdx` | The sidebar for the reverse engineering service page with **Service hero** opened down to its buttons; the header's static blocks (no Remove option); a FAQ category or card list showing its "nothing to show" note. |
| `horizon/what-is-horizon.mdx` | **Online Store → Themes** with the current theme and the theme library. |
| `page-recipes/overview.mdx` | The **Theme template** field on a page in the admin, and the editor's template picker (**Pages** list). |
| `page-recipes/homepage.mdx` | The sidebar with the 9 homepage sections. |
| `page-recipes/product-page.mdx` | The product record (Title, Description, Media). |
| `page-recipes/contact-pages.mdx` | **Settings → Notifications** (sender email). |
| `blocks/product-blocks.mdx` | The editor sidebar for the HandySCAN template: **Product information → Product media / Details**. |
| `technical/branches-and-deploy.mdx` | A shopify[bot] commit on GitHub; the theme library showing the theme connected to `main`. |
| `technical/migration-and-redirects.mdx` | The URL redirects **Import** dialog. |

### Facts to confirm

- **Admin names of three page fields**: the page headline, hero subheading and hero image fields (short landing
  pages) are described without a bold label.
- **Live theme templates**: that no live page uses the shared **landing** or **landing-short** template.
- **Store settings** the repo can't show: spam protection (**Online Store → Preferences**), the cookie banner
  (**Settings → Customer privacy**), the sender email (**Settings → Notifications**), Google Analytics.
- **Contact form email**: send a test from the live form and check the "Source page" line arrives.
- **Case study breadcrumb**: should show the case studies blog's title, not "Blog".
- **Shopify behaviour** stated from Shopify's documentation, not seen on screen: blocks can't be dragged
  between sections; section and nesting limits; no revision history for pages and posts; **Product media**
  always shows a carousel on phones; one development theme per CLI login.
- **Editor wording**: "Theme settings icon" vs "gear icon" (`horizon/theme-settings.mdx`, `blocks/header.mdx`).
- **Branches**: that `dev` is not connected to any theme, and whether new work branches from `dev` from now on.
- **Updating Horizon**: whether the store offers Horizon updates for this theme, and the public Horizon
  repository's release tags.
- **Launch**: whether re-running `import_services.py` at the domain switch is still needed (dry run first).
- **Old redirects**: what handled redirects on the WordPress site (no plugin shows in the saved pages).

## 6. Settings pages rebuilt on 2026-10-20

Every block page and the theme settings now follow one layout (What it does, Where to find it, Settings, Data
and metafields, Limitations), with settings tables written by `scripts/settings_tables.py` (see `README.md`).
Run it after each theme release.

### Facts to confirm

- **Block cart and checkout** moved from a **Tangent** group into **Cart** in the theme's work branch. The guide
  already shows it under **Cart**; until that change is released, the live editor still shows the old group.
- **Header on tablets**: `blocks/header.mdx` says the phone becomes a square call button on phones and tablets;
  the code hides it in the 750–989px menu layout. Check on a tablet.
- **Corner wording**: `blocks/buttons.mdx` says "square buttons", `theme-settings/buttons.mdx` says "2-pixel
  corners". Pick one.
- **Palette names**: the tables call the extra palette colors **Color 1** and **Color 2**; check the editor's names.
- **Card list › Cards** (card entries) is empty on every list, but the theme's help text still says to connect it
  on service pages. The guide says not to use it.
- **Analytics pixel**: the quote form's **Form name** is sent to analytics only if the Customer events pixel is
  set up in the store.
- **Markets**: the country / language picker stays hidden only while the store has one country and one language.

### Screenshots wanted

| Page | Screenshot |
|---|---|
| `blocks/card-list.mdx` | The Stats, Numbered steps, Quotes, Drawing notes, Check list and Note strip layouts. |
| `horizon/theme-settings.mdx` | The Theme settings group list in the editor. |
| `theme-settings/*.mdx` | Each group's panel open in the editor (Logo and favicon first). |
