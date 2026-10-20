#!/usr/bin/env python3
"""Generate the settings tables of the guide from the theme's own schemas.

Every guide page that documents settings carries one or more markers:

    {/* settings:begin source=block:card-list level=3 */}
    ...generated, do not edit by hand...
    {/* settings:end */}

`source` is `block:<file>` (blocks/<file>.liquid), `section:<file>` (sections/<file>.liquid) or
`theme:<group>` (a group of config/settings_schema.json, by its English name in lower case with dashes, e.g.
`theme:color-palette`).
`level` is the heading level used for the schema's own sub-groups (its `header` settings).

Columns: Setting | Values | Default | Tangent uses | Notes.
- Labels, options and info texts are resolved through locales/en.default.schema.json, so they match the editor.
- "Tangent uses" is counted from every template and section group of the theme (blocks and sections), or read
  from config/settings_data.json for theme settings.
- Notes = "Shown when …" (from visible_if), then the schema's info text, or instead of it a plain-words note
  from scripts/notes/<kind>_<name>.json, e.g. scripts/notes/block_card-list.json = {"<setting id>": "note"}
  (theme settings: scripts/notes/theme_<group slug>.json, e.g. theme_buttons.json).

Usage (from the guide's root):
    python3 scripts/settings_tables.py --theme ../tangent           # rewrite every marked page
    python3 scripts/settings_tables.py --theme ../tangent --check   # exit 1 if a page is out of date
    python3 scripts/settings_tables.py --theme ../tangent --only blocks/faq.mdx
    python3 scripts/settings_tables.py --theme ../tangent --print block:faq-category
"""

import argparse
import collections
import glob
import json
import os
import re
import sys

MARK = re.compile(r"(\{/\* settings:begin (?P<args>[^*]*?) \*/\}\n)(?P<body>.*?)(\{/\* settings:end \*/\})", re.S)
GUIDE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_json(path):
    text = open(path, encoding="utf-8").read()
    text = re.sub(r"^\s*/\*.*?\*/", "", text, flags=re.S)
    text = re.sub(r"^\s*//.*$", "", text, flags=re.M)
    return json.loads(text)


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", str(text).lower()).strip("-")


def schema_of(path):
    text = open(path, encoding="utf-8").read()
    m = re.search(r"{%-?\s*schema\s*-?%}(.*?){%-?\s*endschema\s*-?%}", text, re.S)
    return json.loads(m.group(1)) if m else {}


class Theme:
    def __init__(self, root):
        self.root = root
        self.locale = load_json(os.path.join(root, "locales/en.default.schema.json"))
        self.settings_schema = load_json(os.path.join(root, "config/settings_schema.json"))
        self.settings_data = load_json(os.path.join(root, "config/settings_data.json")).get("current", {})
        self.instances = collections.defaultdict(list)  # (kind, type) -> [settings dict]
        self.templates = collections.defaultdict(set)  # (kind, type) -> {template file}
        self.turned_off = collections.defaultdict(list)  # copies inside a hidden section or block
        for path in sorted(glob.glob(os.path.join(root, "templates/*.json")) + glob.glob(os.path.join(root, "sections/*.json"))):
            data = load_json(path)
            name = os.path.relpath(path, root)
            for section in data.get("sections", {}).values():
                off = bool(section.get("disabled"))
                self._collect("section", section, name, off)
                self._walk_blocks(section.get("blocks", {}), name, off)

    def _collect(self, kind, node, name, off):
        key = (kind, node.get("type"))
        if off:
            self.turned_off[key].append(node.get("settings", {}) or {})
            return
        self.instances[key].append(node.get("settings", {}) or {})
        self.templates[key].add(name)

    def _walk_blocks(self, blocks, name, off):
        for block in blocks.values():
            hidden = off or bool(block.get("disabled"))
            self._collect("block", block, name, hidden)
            self._walk_blocks(block.get("blocks", {}), name, hidden)

    def t(self, value):
        if isinstance(value, str) and value.startswith("t:"):
            node = self.locale
            for key in value[2:].split("."):
                node = node.get(key, {}) if isinstance(node, dict) else {}
            return node if isinstance(node, str) else value
        return value

    def source(self, spec):
        kind, _, name = spec.partition(":")
        if kind == "theme":
            for group in self.settings_schema:
                if slug(self.t(group.get("name", ""))) == name:
                    return group.get("settings", []), None
            raise SystemExit(f"Unknown theme settings group: {name}")
        folder = {"block": "blocks", "section": "sections"}[kind]
        path = os.path.join(self.root, folder, name + ".liquid")
        if not os.path.exists(path):
            raise SystemExit(f"Missing schema file: {folder}/{name}.liquid")
        return schema_of(path).get("settings", []), self.instances.get((kind, name), [])

    def theme_setting(self, setting_id):
        for group in self.settings_schema:
            for setting in group.get("settings", []):
                if setting.get("id") == setting_id:
                    return setting
        return None


# ---------- formatting ----------

def md(text):
    """One table cell: no pipes or line breaks, HTML tags and link targets removed."""
    text = re.sub(r"<[^>]+>", "", str(text))
    text = re.sub(r"\s*\[learn more\]\([^)]*\)", "", text, flags=re.I)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = text.replace("|", "/").replace("\n", " ").strip()
    return re.sub(r"\s+", " ", text)


def linked(value):
    """Words for a value that is a dynamic source or a link to another setting."""
    palette = re.search(r"color_palette\.(\w+)", value)
    if palette:
        return "Palette " + re.sub(r"^color(\d+)$", r"Color \1", palette.group(1)).lower().replace("color ", "Color ")
    if "settings." in value:
        return "Linked to another theme setting"
    if "product" in value:
        return "From the product"
    if "article" in value or "blog" in value:
        return "From the post"
    return "From a page field"


def option_label(theme, setting, value):
    for option in setting.get("options", []):
        if option.get("value") == value:
            return theme.t(option.get("label"))
    return value


def unit(setting):
    return setting.get("unit", "")


def short_text(value, limit=48):
    """A long text cut on a word boundary; lines are joined with a middle dot."""
    value = md(" · ".join(line.strip() for line in str(value).splitlines() if line.strip()))
    if len(value) <= limit:
        return f"“{value}”"
    return "“" + value[:limit].rsplit(" ", 1)[0].rstrip(",.;:") + " …”"


def join(labels):
    """List option labels; a label with a comma of its own switches the separator."""
    return (" · " if any("," in label for label in labels) else ", ").join(labels)


def show_value(theme, setting, value):
    kind = setting["type"]
    value = theme.t(value)
    if kind in ("select", "radio") and any(o.get("value") == value for o in setting.get("options", [])):
        return option_label(theme, setting, value)
    if kind == "checkbox" and value in (None, ""):
        return "Off"
    if value is None or value == "":
        return "Empty"
    if isinstance(value, str) and "{{" in value:
        return linked(value)
    if kind == "checkbox":
        return "On" if value else "Off"
    if kind in ("select", "radio"):
        return option_label(theme, setting, value)
    if kind == "range":
        return f"{value}{unit(setting)}"
    if kind == "text_alignment":
        return {"left": "Left", "center": "Center", "right": "Right"}.get(value, value)
    if kind == "color":
        if re.fullmatch(r"rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*0\s*\)", str(value)):
            return "Transparent"
        return str(value).upper() if str(value).startswith("#") else str(value)
    if kind == "image_picker":
        return str(value).rsplit("/", 1)[-1]
    if kind == "font_picker":
        m = re.fullmatch(r"(.+)_([ni])(\d)", str(value))
        if not m:
            return str(value)
        family = " ".join(w.upper() if w in ("ibm",) else w.capitalize() for w in m.group(1).split("_"))
        return f"{family} {int(m.group(3)) * 100}" + (" italic" if m.group(2) == "i" else "")
    if kind in ("text", "textarea", "richtext", "inline_richtext"):
        return short_text(value)
    return md(value)[:48]


def values_cell(theme, setting):
    kind = setting["type"]
    if kind in ("select", "radio"):
        labels = [theme.t(o.get("label")) for o in setting.get("options", [])]
        if len(labels) > 8:
            return f"{len(labels)} options: " + join(labels[:4] + ["…"])
        return join(labels)
    if kind == "range":
        return f"{setting['min']}–{setting['max']}{unit(setting)}"
    if kind == "checkbox":
        return "On, Off"
    return {
        "text": "Text", "textarea": "Text", "richtext": "Rich text", "inline_richtext": "Rich text",
        "color": "Color", "image_picker": "Image", "url": "Link", "video": "Video", "video_url": "Video link",
        "text_alignment": "Left, Center, Right", "product": "Product", "collection": "Collection",
        "collection_list": "Collections", "blog": "Blog", "page": "Page", "link_list": "Menu",
        "metaobject": "Entry", "metaobject_list": "Entries", "liquid": "Code", "font_picker": "Font",
        "color_scheme": "Color scheme", "html": "Code",
    }.get(kind, kind.replace("_", " ").capitalize())


def default_cell(theme, setting):
    if setting.get("default") is None:
        return "Off" if setting["type"] == "checkbox" else "—"
    return show_value(theme, setting, setting["default"])


def tangent_cell(theme, setting, instances, shown=None):
    if instances is None:  # theme setting
        if "_value" in setting:
            return show_value(theme, setting, setting["_value"])
        value = theme.settings_data.get(setting["id"], setting.get("default"))
        return show_value(theme, setting, value)
    if not instances:
        return "Not used"
    if shown is not None:
        instances = [inst for inst in instances if shown(setting, inst) is not False]
        if not instances:
            return "Hidden on every copy"
    kind = setting["type"]
    values = [inst.get(setting["id"], setting.get("default")) for inst in instances]
    total = len(values)
    short = all(isinstance(v, str) and len(v) <= 40 and "{{" not in v for v in values if v)
    few_words = kind == "text" and short and len(set(values)) <= 4  # show them like options
    if not few_words and kind in ("text", "textarea", "richtext", "inline_richtext", "image_picker", "url", "video", "video_url",
                "liquid", "product", "collection", "blog", "page", "metaobject", "metaobject_list", "link_list",
                "collection_list"):
        dynamic = sum(1 for v in values if isinstance(v, str) and "{{" in v)
        filled = sum(1 for v in values if v not in (None, "", []))
        if filled == 0:
            return "Empty"
        parts = [f"Set on {filled:,} of {total:,}"] if filled < total else ["Set on all"]
        if dynamic:
            parts.append(f"{dynamic} from a page field")
        return ", ".join(parts)
    counts = collections.Counter(show_value(theme, setting, v) for v in values)
    if len(counts) == 1:
        return next(iter(counts))
    top = counts.most_common(2)
    parts = [f"{label} ({n:,})" for label, n in top]
    if len(counts) > 2:
        parts.append(f"{len(counts) - 2} more")
    return join(parts) if any("," in label for label, _ in top) else ", ".join(parts)


COND = re.compile(r"(?:(block|section)\.)?settings\.(\w+)\s*(==|!=|>=|<=|>|<)?\s*('[^']*'|\"[^\"]*\"|\w+)?")


def bold_name(name):
    """**Label**, keeping an explanation after a comma out of the bold."""
    label, sep, rest = md(name).partition(", the one")
    return f"**{label}**" + (f", the one{rest}" if sep else "")


def literal(raw):
    raw = raw.strip()
    if raw[:1] in "'\"":
        return raw[1:-1]
    if raw in ("true", "false"):
        return raw == "true"
    if raw in ("blank", "nil", "empty"):
        return None
    try:
        return float(raw)
    except ValueError:
        return raw


def is_shown(setting, inst, by_id, spec_is_section):
    """Whether the editor shows this setting for one saved copy: True, False, or None when unsure."""
    expr = setting.get("visible_if")
    if not expr:
        return True
    parts = re.split(r"\s+(and|or)\s+", expr.strip().strip("{}").strip())
    if parts == ["false"]:
        return False
    results, ops = [], []
    for part in parts:
        if part in ("and", "or"):
            ops.append(part)
            continue
        m = COND.fullmatch(part.strip())
        if not m or m.group(1) is None or (m.group(1) == "section") != spec_is_section or m.group(2) not in by_id:
            return None
        other = by_id[m.group(2)]
        value = inst.get(m.group(2), other.get("default"))
        if m.group(3) is None:
            results.append(bool(value))
            continue
        want = literal(m.group(4))
        if want is None:
            same = value in (None, "", [])
        elif isinstance(want, float):
            try:
                value = float(value)
            except (TypeError, ValueError):
                return None
            same = value == want
        else:
            same = value == want
        if m.group(3) in ("==", "!="):
            results.append(same if m.group(3) == "==" else not same)
        elif isinstance(want, float) and isinstance(value, float):
            results.append({">": value > want, "<": value < want, ">=": value >= want, "<=": value <= want}[m.group(3)])
        else:
            return None
    result = results[-1]  # Liquid reads and / or from right to left
    for op, left in zip(reversed(ops), reversed(results[:-1])):
        result = (left and result) if op == "and" else (left or result)
    return result


def shown_when(theme, setting, by_id, names=None, spec_is_section=False, spec_is_theme=False):
    names = names or {}
    expr = setting.get("visible_if")
    if not expr:
        return ""
    inner = expr.strip().strip("{}").strip()
    if inner == "false":
        return None  # never shown in the editor
    clauses = re.split(r"\s+(and|or)\s+", inner)
    words = []
    for part in clauses:
        if part in ("and", "or"):
            words.append(part)
            continue
        m = COND.fullmatch(part.strip())
        if not m:
            return "Shown only with some other settings."
        scope, ref, op, raw = m.group(1), m.group(2), m.group(3), m.group(4)
        if scope is None and spec_is_theme and ref in by_id:  # a setting of the same group
            other = by_id[ref]
            name = bold_name(names.get(ref) or theme.t(other.get("label", ref)))
        elif scope is None:  # a theme setting
            other = theme.theme_setting(ref)
            if not other:
                return "Shown only with some other settings."
            name = f"Theme settings › **{md(theme.t(other.get('label', ref)))}**"
        elif ref in by_id and (scope == "section") == spec_is_section:
            other = by_id[ref]
            name = bold_name(names.get(ref) or theme.t(other.get("label", ref)))
        else:
            return "Shown only with some settings of the section around it."
        if op is None:
            words.append(f"{name} is on" if other.get("type") == "checkbox" else f"{name} is set")
            continue
        value = raw.strip("'\"")
        if value == "blank":
            words.append(f"{name} is {'empty' if op == '==' else 'set'}")
            continue
        if value in ("true", "false") and other.get("type") == "checkbox":
            on = (value == "true") == (op == "==")
            words.append(f"{name} is {'on' if on else 'off'}")
            continue
        shown = show_value(theme, other, int(value) if value.isdigit() else value)
        verb = {"==": "is", "!=": "is not", ">": "is more than", "<": "is less than", ">=": "is at least",
                "<=": "is at most"}[op]
        words.append(f"{name} {verb} {shown}")
    clauses, joined = [], []
    for word in words:  # drop a clause that repeats the one before it
        if word in ("and", "or") or word not in clauses:
            joined.append(word)
            if word not in ("and", "or"):
                clauses.append(word)
    while joined and joined[-1] in ("and", "or"):
        joined.pop()
    text = " ".join(joined)
    # "**X** is A or **X** is B or **X** is C" -> "**X** is A, B or C"
    def merge(m):
        name, first, rest = m.group(1), m.group(2), re.findall(r" or \*\*[^*]+\*\* is ([^*]+?)(?= or \*\*| and |$)", m.group(0))
        values = [first] + rest
        if any("," in v for v in values):
            return f"{name} is one of " + " · ".join(values)
        return f"{name} is " + ", ".join(values[:-1]) + " or " + values[-1]
    text = re.sub(r"(\*\*[^*]+\*\*) is ((?:(?! or | and ).)+?)(?: or \1 is (?:(?! or | and ).)+?)+(?= and |$)", merge, text)
    return "Shown when " + text + "."


def render(theme, spec, level, notes):
    settings, instances = theme.source(spec)
    by_id = {s["id"]: s for s in settings if s.get("id")}
    groups = [[None, []]]
    for s in settings:
        if s["type"] == "header":
            groups.append([theme.t(s.get("content")), []])
        elif s["type"] == "color_palette":
            current = theme.settings_data.get(s["id"], {}) or {}
            for role in dict(s.get("default", {}), **current):
                name = re.sub(r"^color(\d+)$", r"Color \1", role).capitalize()
                groups[-1][1].append({"type": "color", "id": f"{s['id']}.{role}", "label": name,
                                      "default": s.get("default", {}).get(role), "_value": current.get(role)})
        elif s["type"] == "paragraph" or not s.get("label"):
            continue
        else:
            groups[-1][1].append(s)
    spec_is_section = spec.startswith("section:")
    labels = collections.Counter(theme.t(s.get("label", "")) for _, rows in groups for s in rows)
    names = {}
    titles = collections.Counter((title, theme.t(s.get("label", ""))) for title, rows in groups for s in rows)
    for title, rows in groups:
        for s in rows:
            label = theme.t(s.get("label", ""))
            if labels[label] < 2:
                continue
            if title and titles[(title, label)] == 1:
                names[s["id"]] = f"{title} › {label}"
            elif s.get("visible_if"):  # same label in the same group: say which one by when it shows
                when = (shown_when(theme, s, by_id, {}, spec_is_section, spec.startswith("theme:")) or "")
                when = when.replace("Shown when ", "").rstrip(".").replace("**", "")
                names[s["id"]] = f"{label}, the one shown when {when}," if when else label
    out = []
    key = tuple(spec.split(":", 1))
    if instances is not None and not instances and theme.turned_off.get(key):
        instances = theme.turned_off[key]
        out.append(f"Turned off on the site: {len(instances)} saved {'copy' if len(instances) == 1 else 'copies'} "
                   "inside a hidden section or block. **Tangent uses** shows their saved values.\n")
    elif instances is not None:
        uses = len(instances)
        files = len(theme.templates.get(tuple(spec.split(":", 1)), ()))
        times = "once" if uses == 1 else f"{uses:,} times"
        where = "1 page layout or header/footer group" if files == 1 else f"{files} page layouts and header/footer groups"
        out.append(f"Used {times} across {where}. In **Tangent uses**, a "
                   "number in brackets is how many of those copies use that value.\n" if uses else
                   "Not used in any layout yet. **Tangent uses** shows “Not used”.\n")
    else:
        out.append("**Tangent uses** is the value saved in the live theme's settings.\n")
    for title, rows in groups:
        rows = [s for s in rows if shown_when(theme, s, by_id, names, spec_is_section, spec.startswith("theme:")) is not None]
        if not rows:
            continue
        if title:
            out.append(f"{'#' * level} {md(title)}\n")
        out.append("| Setting | Values | Default | Tangent uses | Notes |")
        out.append("|---|---|---|---|---|")
        for s in rows:
            info = notes.get(spec, {}).get(s["id"]) or (md(theme.t(s["info"])) if s.get("info") else "")
            note = " ".join(x for x in (shown_when(theme, s, by_id, names, spec_is_section, spec.startswith("theme:")), info) if x)
            out.append(" | ".join([
                f"| **{md(theme.t(s['label']))}**",
                md(values_cell(theme, s)),
                md(default_cell(theme, s)),
                md(tangent_cell(theme, s, instances, lambda st, inst: is_shown(st, inst, by_id, spec_is_section))),
                md(note) or "—",
            ]) + " |")
        out.append("")
    return "\n".join(out)


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--theme", required=True, help="path to the theme repository")
    parser.add_argument("--check", action="store_true", help="only report pages that are out of date")
    parser.add_argument("--only", nargs="+", metavar="PAGE", help="only these pages (paths from the guide's root)")
    parser.add_argument("--print", metavar="SOURCE", help="print the tables for one source, e.g. block:card-list")
    args = parser.parse_args()
    theme = Theme(os.path.abspath(args.theme))
    notes = {}
    for path in glob.glob(os.path.join(GUIDE, "scripts/notes/*.json")):
        kind, _, name = os.path.basename(path)[:-5].partition("_")
        notes[f"{kind}:{name}"] = json.load(open(path, encoding="utf-8"))
    if args.print:
        print(render(theme, args.print, 3, notes))
        return
    stale = []
    pages = [p for p in glob.glob(os.path.join(GUIDE, "**/*.mdx"), recursive=True) if "/node_modules/" not in p]
    if args.only:
        wanted = {os.path.abspath(os.path.join(GUIDE, p)) for p in args.only}
        pages = [p for p in pages if os.path.abspath(p) in wanted]
    for page in sorted(pages):
        text = open(page, encoding="utf-8").read()
        if "settings:begin" not in text:
            continue

        def replace(m):
            opts = dict(kv.split("=", 1) for kv in m.group("args").split())
            body = render(theme, opts["source"], int(opts.get("level", 3)), notes)
            return m.group(1) + "\n" + body + "\n" + m.group(4)

        new = MARK.sub(replace, text)
        if new != text:
            stale.append(os.path.relpath(page, GUIDE))
            if not args.check:
                open(page, "w", encoding="utf-8").write(new)
    verb = "out of date" if args.check else "updated"
    print(f"{len(stale)} page(s) {verb}" + (": " + ", ".join(stale) if stale else ""))
    sys.exit(1 if args.check and stale else 0)


if __name__ == "__main__":
    main()
