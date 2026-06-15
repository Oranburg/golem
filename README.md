# Law of the Golem

AI, agency, and responsibility for the things we set in motion. An artificial system is a golem in an old and exact sense: a thing a person animates that acts and cannot answer for what it does. This repository is the project's home and its website.

**Live site:** https://oranburg.law/golem/

## What is here
A static website, generated from the project's research and writing:
- The essay (the central argument) and a magazine version for a wider readership.
- A field guide of the battlefield (life-saving systems set against life-destroying ones), a civilian-devices page, and a sortable registry of intangible systems, each with credits and an interactive principle-sorter.
- The Jewish legal history of responsibility.
- Three Mermaid diagrams of the argument.

## Build and deploy
`python3 build_site.py` regenerates the whole site from the Markdown sources, the image catalog, and the systems bench. It needs Python 3 and pandoc. The output is plain static HTML; GitHub Pages serves it from the `main` branch root, with a `.nojekyll` file so the files are served as-is, at oranburg.law/golem/. To ship a change: rebuild, commit, push.

## Images
Images are tracked in `assets/image-catalog.json` with the credit, rights, and a usage note for each. Public-domain and Creative Commons images are marked; manufacturer images appear here for academic comment and criticism and are flagged for permission before any formal publication. New images are ingested with `assets/ingest_image.py`.

## Status
The articles are drafts with open verification flags. The current status and software documentation live in the wiki. Nothing here is final; the website serves the current drafts.
