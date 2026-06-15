# Future Project: Download Your Insights

A scoped, non-essential, non-gating feature. It exists partly to demonstrate that the wiki and the Issues features both work and cross-reference each other, and partly because it would be genuinely useful.

## The idea
As a reader moves through the field guide and the articles, let them collect their own notes and selections (a flagged system, a highlighted sentence, a question of their own) and export the collection as a single Markdown file they can keep. A scholar reading the field guide could mark the cases that bear on their own work and walk away with a tidy Markdown brief, credits included.

## Why it is not essential
Nothing in the project depends on it. The articles, the field guide, the diagrams, and the argument all stand without it. It gates nothing in Phase 4.

## Sketch
- A small client-side store (localStorage) for the reader's selections.
- A control on each system card and each article section to add to the collection.
- An export button that assembles the selections, with their source credits from the catalog, into a downloadable `.md` file.
- No server; everything in the browser.

## Tracking
This page is mirrored by a GitHub Issue of the same name, labeled `enhancement` and `non-gating`, so the wiki and the Issues both show it.
