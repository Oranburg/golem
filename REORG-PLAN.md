# Reorganization plan: split the systems by domain

**Goal.** The Field Guide becomes battlefield only, organized as life-saving battlefield tech against life-destroying battlefield tech, so it shows that a ban on "lethal or irreversible decisions" catches the autonomous medevac in the same net as the loitering munition. The non-battlefield civilian devices move to their own page. The IP and Services registry (intangible systems) stays as it is. Three pages of systems, three faces of one question: the words fail (battlefield), the thing cannot be renounced (civilian), and the answerable human is where the line may actually sit (registry).

**Resume.** Progress lives in three places: the checkboxes below, the harness task list, and `git log` (each phase commits). If restarted, read the checkboxes and the last commit to find where to continue.

## Phase 1: restructure with the devices already cataloged
- [x] 1. Classify each catalog entry: battlefield vs civilian; within battlefield, destroying vs saving. (build_site.py)
  - Civilian: CyberKnife, AED, ICD, insulin pump, STAR, Waymo.
  - Battlefield-destroying: the C1, C2, C3 weapons plus Iron Drone Raider.
  - Battlefield-saving: reserved for the Phase 2 devices.
- [x] 2. Rebuild field-guide.html as battlefield only, grouped Life-destroying and Life-saving, with a new lede.
- [x] 3. Create civilian.html: CyberKnife, AED, ICD, insulin pump, STAR, Waymo. Same grid and sorter, its own lede.
- [x] 4. Add civilian.html to the nav, update ledes, cross-link the three pages.
- [x] 5. Rebuild, smoke-test, commit, push, verify live.

## Phase 2: research and add the battlefield-lifesaving devices
- [x] 6. Research real images, credit, rights, specs: BEAR, S-MET, Zipline medical drone, a field or closed-loop ventilator, the nerve-agent auto-injector.
- [x] 7. Batch-ingest into image-catalog.json with the battlefield-saving classification.
- [x] 8. Append the new source URLs to source-urls-for-permacc.md.
- [x] 9. Rebuild so they appear in Life-saving, smoke-test, commit, push, verify live.

## Phase 3: document and finalize
- [x] 10. Update the wiki (Current Status, Software Documentation) for the three-page structure. Push the wiki.
- [x] 11. File an issue for the deferred armed-robots batch (Ghost SWORD, Spot and Digidog, Knightscope).
- [x] 12. Final verification and report.
