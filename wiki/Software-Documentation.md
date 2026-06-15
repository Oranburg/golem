# Software Documentation

## What it is
A static website, generated from the project content. No build toolchain at serve time; the pages are plain HTML, so GitHub Pages serves them directly.

## Build
`python3 build_site.py` regenerates the whole site from:
- the Markdown articles in the project folder,
- the image catalog (`assets/image-catalog.json`),
- the systems bench data, and
- a hand-authored list of the intangible systems for the registry.

It converts Markdown to HTML with pandoc (footnotes and all), copies the images into `images/`, generates the system pages and the diagrams, and writes the landing page. It strips author markup of the form `==[[ ... ]]==` and `[VOID: ... ]` before any page is written, and it never publishes the working folder.

## How the systems are split
The build classifies each cataloged system by domain, then routes it to the right page:
- `domain_of()` marks each entry **civilian** or **battlefield**, and for battlefield, **life-destroying** or **life-saving**, from keywords and an optional `civilian` or `saving` tag.
- An `INTANGIBLE` filter routes the software-only entries (Maven, facial recognition, predictive policing, organ allocation) out of the photo grids; the intangible systems live in a separate hand-authored registry table.
- The **Field Guide** renders the battlefield entries in two valence sections (Life-destroying, subgrouped by offensive, defensive, and area-denial; Life-saving as one grid).
- The **Civilian Devices** page renders the off-battlefield entries.
- The **IP & Services** page renders the registry as a sortable, searchable table.

## Dependencies
- Python 3
- pandoc (Markdown to HTML)
- Mermaid, loaded from a CDN at view time for the diagrams.

## Page map
- `index.html` : landing, with the responsibility-path diagram and the nav cards.
- `field-guide.html` : the battlefield, life-saving set against life-destroying, photo grid and principle-sorter.
- `civilian.html` : the off-battlefield autonomous devices, photo grid and principle-sorter.
- `registry.html` : the intangible systems as a sortable table with the principle-sorter.
- `essay.html`, `magazine.html` : the same argument for two readerships.
- `diagrams.html` : the three Mermaid diagrams.
- `assets/css/` : the house design system (`lawj-palette.css` and `site.css` copied from the main site) plus `golem.css` for the project components. `assets/js/site.js` carries the theme toggle and nav.

## The principle-sorter
Each system carries four boolean attributes (lethal, irreversible, the machine makes the call, no answerable human). The checkboxes highlight the systems that match every checked criterion. The flags come from `classify()`: it honors an explicit per-entry `flags` object where one is set (used for the battlefield-medicine devices, so the closed-loop ventilator reads lethal, irreversible, and machine-deciding while the human-operated extraction robot does not), and otherwise derives them heuristically. The flags are a first-pass classification, deliberately open to revision; refining them is a tracked Issue and a research question, not only a bug.

## The image system
Images are ingested with `assets/ingest_image.py`, which downloads from a URL or copies a local file, renames it descriptively, and records its credit, rights, license, and usage note in `assets/image-catalog.json`. Public-domain and Creative Commons images are marked as such; manufacturer images are flagged as needing permission. Source pages are logged in `assets/source-urls-for-permacc.md` for archiving.

## Deploy
GitHub Pages, `main` branch root, with a `.nojekyll` file so the raw files are served as-is. Custom domain oranburg.law, so the project serves at oranburg.law/golem/. To deploy a change: rebuild, commit, push to `main`.
