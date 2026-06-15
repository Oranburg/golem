#!/usr/bin/env python3
# % voice-check: skip (build script; generated page text and catalog credits quote source language)
"""Build the static 'Law of the Golem' site from the project content. Static HTML, no toolchain, deployable to GitHub Pages."""
import json, os, subprocess, shutil, html, re

REPO = "/Users/sco/golem"
MH = "/Users/sco/Library/Mobile Documents/27N4MQEA55~pro~writer/Documents/JEW - Jewish Studies/MH"
ASSETS = os.path.join(MH, "assets")
RS = os.path.join(MH, "responsibility-study")
IMG_SRC = os.path.join(ASSETS, "images")
IMG_DST = os.path.join(REPO, "images")
DOCS = os.path.join(REPO, "docs")
CATALOG = os.path.join(ASSETS, "image-catalog.json")
BENCH = "/private/tmp/claude-501/-Users-sco/a1fc5453-dd70-4f87-bea7-2f4286075904/tasks/wmpknofiu.output"

os.makedirs(IMG_DST, exist_ok=True)

# ---- copy images ----
for fn in os.listdir(IMG_SRC):
    shutil.copyfile(os.path.join(IMG_SRC, fn), os.path.join(IMG_DST, fn))

with open(CATALOG) as f: catalog = json.load(f)["images"]
with open(BENCH) as f: bench_clusters = json.load(f)["result"]["clusters"]

# bench lookup by name token overlap
bench_entries = []
for c in bench_clusters:
    for e in c.get("entries", []):
        bench_entries.append(e)
def toks(s): return set(re.findall(r"[a-z0-9]+", (s or "").lower()))
def best_bench(subject):
    st = toks(subject)
    best, score = None, 0
    for e in bench_entries:
        ov = len(st & toks(e.get("name","")))
        if ov > score: best, score = e, ov
    return best if score >= 1 else None
CLUSTERS = {"C1":"Offensive strike","C2":"Defensive point-defense","C3":"Barriers, counter-systems & sensing","C4":"Dual-use & decision-support","C5":"Curative & life-saving"}
def cluster_of(e):
    t = " ".join(e.get("tags", []))
    for k in CLUSTERS:
        if k in t: return k
    return "C2"

NAV = [("index.html","Home"),("field-guide.html","Field Guide"),("civilian.html","Civilian Devices"),("registry.html","IP & Services"),("essay.html","The Essay"),("magazine.html","Magazine"),
       ("diagrams.html","Diagrams")]

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,600;0,700;1,400&family=Oswald:wght@500..700&family=Roboto:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Roboto+Mono:wght@400;500&display=swap" rel="stylesheet">')
CSSLINKS = ('<link rel="stylesheet" href="assets/css/lawj-palette.css">'
    '<link rel="stylesheet" href="assets/css/site.css">'
    '<link rel="stylesheet" href="assets/css/golem.css">')
THEME_INIT = ("<script>(function(){try{var t=localStorage.getItem('theme');"
    "if(t==='light'||t==='dark'){document.documentElement.setAttribute('data-theme',t);}"
    "else if(window.matchMedia&&window.matchMedia('(prefers-color-scheme: light)').matches){document.documentElement.setAttribute('data-theme','light');}"
    "else{document.documentElement.setAttribute('data-theme','dark');}}catch(e){document.documentElement.setAttribute('data-theme','dark');}})();</script>")
TOGGLE = ('<button class="theme-toggle" onclick="toggleTheme()" aria-label="Switch to light mode">'
    '<svg class="icon-sun" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>'
    '<svg class="icon-moon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg></button>')
NAVTOGGLE = """<button class="nav-toggle" onclick="var n=this.closest('.site-nav');n.classList.toggle('open');this.setAttribute('aria-expanded',n.classList.contains('open'))" aria-label="Toggle menu" aria-expanded="false"><span></span><span></span><span></span></button>"""
FOOTER = ('<footer class="site-footer"><div class="footer-inner"><div class="footer-links">'
    '<a href="https://oranburg.law/">Home</a>'
    '<a href="https://oranburg.law/insights/">Insights</a>'
    '<a href="https://oranburg.law/scholarship/">Scholarship</a>'
    '<a href="https://oranburg.law/K/" target="_blank" rel="noopener">Contracts Companion</a>'
    '<a href="https://oranburg.law/BA/" target="_blank" rel="noopener">Business Associations Companion</a>'
    '<a href="https://oranburg.law/cv/">CV</a>'
    '<a href="https://github.com/Oranburg/golem" target="_blank" rel="noopener">Source on GitHub</a>'
    '</div><p>&copy; 2026 Seth C. Oranburg. A working research project.</p></div></footer>')

def nav(active):
    items = "".join('<li><a href="%s"%s>%s</a></li>' % (h, ' aria-current="page"' if h==active else '', html.escape(l)) for h,l in NAV)
    return '<nav class="site-nav" aria-label="Project navigation">' + NAVTOGGLE + '<ul>' + items + '<li>' + TOGGLE + '</li></ul></nav>'

def breadcrumb(active):
    items = [("Seth C. Oranburg","https://oranburg.law/")]
    if active == "index.html":
        items.append(("Law of the Golem", None))
    else:
        items.append(("Law of the Golem","index.html"))
        items.append((dict(NAV).get(active, "Page"), None))
    lis = []
    for i,(label,href) in enumerate(items):
        sep = '<span class="breadcrumb-sep" aria-hidden="true">/</span>' if i>0 else ''
        inner = ('<a href="%s">%s</a>'%(href,html.escape(label))) if href else ('<span aria-current="page">%s</span>'%html.escape(label))
        lis.append('<li class="breadcrumb-item">%s%s</li>'%(sep,inner))
    return '<nav class="breadcrumb-bar" aria-label="Breadcrumb"><ol class="breadcrumb-list">%s</ol></nav>'%"".join(lis)

def page(active, title, body, lede="", mermaid=False):
    head_mermaid = ('<script type="module">import mermaid from '
        '"https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";'
        'mermaid.initialize({startOnLoad:true,theme:"dark",securityLevel:"loose",themeVariables:{fontFamily:"Roboto, sans-serif"}});</script>') if mermaid else ""
    ledehtml = '<p class="lede">%s</p>' % lede if lede else ""
    return ('<!doctype html><html lang="en" data-theme="dark"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        '<meta name="theme-color" content="#f5f3ee" media="(prefers-color-scheme: light)">'
        '<meta name="theme-color" content="#0A3255" media="(prefers-color-scheme: dark)">'
        '<title>%s | Law of the Golem</title>%s%s%s%s</head><body>'
        '<a href="#main-content" class="skip-link">Skip to content</a>'
        '<header class="site-header"><div class="header-inner">'
        '<a class="site-title" href="index.html">Law of the Golem</a>'
        '<p class="site-tagline">AI, agency, and responsibility for the things we set in motion</p></div></header>'
        '%s%s'
        '<main class="site-content" id="main-content"><h1>%s</h1>%s%s</main>'
        '%s<script src="assets/js/site.js"></script></body></html>') % (
            html.escape(title), FONTS, CSSLINKS, THEME_INIT, head_mermaid,
            breadcrumb(active), nav(active), html.escape(title), ledehtml, body, FOOTER)

def md_body(src):
    with open(src) as f: text = f.read()
    if text.lstrip().startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3: text = parts[2]
    text = re.sub(r"==\[\[.*?\]\]==", "", text, flags=re.S)   # strip author TK markup
    text = re.sub(r"\[VOID:.*?\]", "", text, flags=re.S)       # strip author void markers
    text = text.replace("../assets/images/","images/").replace("assets/images/","images/")
    p = subprocess.run(["pandoc","-f","markdown+tex_math_dollars","-t","html","--no-highlight"],
                       input=text, capture_output=True, text=True)
    return p.stdout

# ---- article / research pages ----
ARTICLES = [
 ("essay.html","The Principle the Prohibition Lacks",os.path.join(RS,"essay-missing-principle-ILLUSTRATED.md"),
   "The argument, illustrated. A CyberKnife and a loitering munition are both lethal and both irreversible, so the words meant to forbid one and permit the other forbid both."),
 ("magazine.html","AI, the Golem, and the Limits of a Ban",os.path.join(RS,"magazine-golem.md"),
   "The same argument for a wider readership: the machines we cannot forbid and cannot put down, and the old law of who answers."),
]
built = []
for href, title, src, lede in ARTICLES:
    if os.path.exists(src):
        with open(os.path.join(REPO,href),"w") as f: f.write(page(href,title,md_body(src),lede))
        built.append(href)

# ---- field guide ----
def classify(e, b):
    if e.get("flags"):
        f = e["flags"]
        return {k:int(bool(f.get(k,0))) for k in ("lethal","irrev","machine","gap")}
    name = (e.get("subject","")+" "+e.get("filename","")).lower()
    cl = cluster_of(e)
    locus = (b.get("humanDecisionLocus","") if b else "").lower()
    weapon = cl in ("C1","C2","C3")
    has = lambda *ks: any(k in name for k in ks)
    lethal = weapon or has("cyberknife","defibrillator","aed","icd","maven","gospel","lavender","waymo","collision")
    irrev = weapon or has("cyberknife","defibrillator","aed","icd","star","suturing","waymo","collision","maven","gospel","lavender")
    machine = any(tt in locus for tt in ["out of the loop","autonomous","fire and forget","automatic","on the loop","closed-loop","closed loop"]) or has("harpy","kargu","lancet","shahed","phalanx","aegis","iron dome","trophy","cram","c-ram","spider","mine","defibrillator","icd","aed","insulin","pancreas","star","waymo")
    gap = bool(machine) and has("harpy","kargu","shahed","lancet","spider","mine","icd","aed","waymo","dao") and not has("switchblade","reaper","cyberknife")
    return {"lethal":int(bool(lethal)),"irrev":int(bool(irrev)),"machine":int(bool(machine)),"gap":int(bool(gap))}

INTANGIBLE = ("maven","facial recognition","shotspotter","predictive polic","organ allocation","unos")
CIVILIAN_KEYS = ("cyberknife","defibrillator","cardioverter","automated external","insulin","artificial pancreas","smart tissue","autonomous surgical","suturing","waymo","self-driving","driverless","autonomous vehicle")
SAVING_KEYS = ("bear","battlefield extraction","s-met","smet","squad multipurpose","zipline","medical-delivery","medical delivery","medevac","casualty","ventilator","intellivent","auto-injector","autoinjector","atnaa","duodote","nerve-agent","nerve agent","tourniquet")
def domain_of(e):
    tags = " ".join(e.get("tags", [])).lower()
    s = (e.get("subject","")+" "+e.get("filename","")+" "+e.get("description","")).lower()+" "+tags
    if "civilian" in tags or any(k in s for k in CIVILIAN_KEYS): return ("civilian", None)
    if "saving" in tags or any(k in s for k in SAVING_KEYS): return ("battlefield", "save")
    return ("battlefield", "destroy")

def license_note(e):
    r = (e.get("rights","") or "").lower()
    if "public domain" in r: return "public domain"
    if "creative commons" in r or re.search(r"\bcc[ -]", r): return "Creative Commons"
    return "academic-use image"

def img_style(e):
    # default is object-fit:cover, centered (set in CSS); the catalog overrides only
    # where a center-crop would hide the device. fit:contain letterboxes the whole
    # silhouette on black; pos sets the focal point (e.g. "top", "30% 40%").
    s = []
    if e.get("fit") == "contain": s.append("object-fit:contain")
    if e.get("pos"): s.append("object-position:%s" % e["pos"])
    return (' style="%s"' % ";".join(s)) if s else ""

def card_html(e):
    fl = classify(e, best_bench(e.get("subject","")))
    desc = e.get("description","")
    posture = (e.get("posture","") or "").strip()
    searchblob = html.escape((e.get("subject","")+" "+desc+" "+posture).lower())
    cap = ['<b>%s</b>' % html.escape(e.get("subject","")),
           '<span class="desc">%s</span>' % html.escape(desc)]
    if posture:
        cap.append('<span class="posture">%s</span>' % html.escape(posture))
    cap.append('<span class="meta">Image: %s. %s.</span>' % (
        html.escape(e.get("credit","source on file")), html.escape(license_note(e))))
    return ('<figure class="card" data-s="%s" data-lethal="%d" data-irrev="%d" data-machine="%d" data-gap="%d">'
      '<img loading="lazy" src="images/%s" alt="%s"%s>'
      '<figcaption>%s</figcaption></figure>') % (
        searchblob, fl["lethal"], fl["irrev"], fl["machine"], fl["gap"],
        html.escape(e["filename"]), html.escape(e.get("subject","")), img_style(e),
        "".join(cap))

def ptest_block(note):
    return ('<div class="ptest"><div class="ptest-h">%s</div>'
      '<label><input type="checkbox" id="t-lethal" onchange="crit()"> lethal</label>'
      '<label><input type="checkbox" id="t-irrev" onchange="crit()"> irreversible</label>'
      '<label><input type="checkbox" id="t-machine" onchange="crit()"> the machine makes the call</label>'
      '<label><input type="checkbox" id="t-gap" onchange="crit()"> no answerable human</label>'
      '<span id="pcount" class="pcount"></span></div>') % html.escape(note)

def crosslink(active):
    pages = [("field-guide.html","the battlefield","the words fail"),
             ("civilian.html","civilian devices","it cannot be put down"),
             ("registry.html","the IP and services registry","who answers")]
    bits = []
    for h,label,gloss in pages:
        if h==active: bits.append('<b>%s</b> (%s)'%(html.escape(label),html.escape(gloss)))
        else: bits.append('<a href="%s">%s</a> (%s)'%(h,html.escape(label),html.escape(gloss)))
    return '<p class="crosslink">Three pages of real systems, three faces of one question: '+", ".join(bits)+'.</p>'

SORTER_JS = """<script>
function t(id){return document.getElementById('t-'+id).checked;}
function crit(){var L=t('lethal'),I=t('irrev'),M=t('machine'),G=t('gap');var any=L||I||M||G;
var cards=document.querySelectorAll('.card'),n=0;
cards.forEach(function(c){var m=(!L||c.dataset.lethal==='1')&&(!I||c.dataset.irrev==='1')&&(!M||c.dataset.machine==='1')&&(!G||c.dataset.gap==='1');
if(any&&m){c.classList.add('match');n++;}else{c.classList.remove('match');}});
var pc=document.getElementById('pcount');if(pc)pc.textContent=any?(n+' of '+cards.length+' systems match every checked principle'):'';}
function flt(){var q=document.getElementById('q').value.toLowerCase();
document.querySelectorAll('.card').forEach(function(c){c.style.display=(c.dataset.s.indexOf(q)>-1)?'':'none';});}
function pick(btn){document.querySelectorAll('.chip').forEach(function(c){c.classList.remove('on')});btn.classList.add('on');
var c=btn.dataset.c;document.querySelectorAll('.fg-sec').forEach(function(g){g.style.display=(c==='all'||g.dataset.c===c)?'':'none';});}
</script>"""

# split the cataloged systems by domain (battlefield vs civilian)
battlefield, civilian = [], []
for e in catalog:
    if any(k in e.get("subject","").lower() for k in INTANGIBLE): continue
    dom, val = domain_of(e)
    if dom == "civilian": civilian.append(e)
    else: battlefield.append((val, e))

# ---- field guide: the battlefield, life-saving against life-destroying ----
destroy = [e for v,e in battlefield if v=="destroy"]
save = [e for v,e in battlefield if v=="save"]
SUB = {k: CLUSTERS[k] for k in ("C1","C2","C3")}
def dcluster(e):
    c = cluster_of(e)
    return c if c in ("C1","C2","C3") else "C2"
dgroups = {}
for e in destroy:
    dgroups.setdefault(dcluster(e), []).append(e)

fg = [crosslink("field-guide.html"),
      '<div class="controls">' + ptest_block("Apply a principle and watch which systems it catches. No single one of these sorts the machines, and the same net catches the medevac and the missile.") +
      '<input id="q" type="search" placeholder="search systems..." oninput="flt()">'
      '<div class="chips"><button class="chip on" data-c="all" onclick="pick(this)">all</button>'
      '<button class="chip" data-c="destroy" onclick="pick(this)">life-destroying</button>'
      '<button class="chip" data-c="save" onclick="pick(this)">life-saving</button>'
      '</div></div>']
fg.append('<section class="fg-sec" data-c="destroy"><h2 class="valence">Life-destroying<small>weapons, defenses, counter-systems, and the sensors that cue them</small></h2>')
for k in ["C1","C2","C3"]:
    items = dgroups.get(k, [])
    if not items: continue
    fg.append('<h3 class="cluster" data-c="destroy"><span>%s</span>%s</h3><div class="grid" data-c="destroy">' % (k[1], html.escape(SUB[k])))
    for e in sorted(items, key=lambda x:x.get("subject","")):
        fg.append(card_html(e))
    fg.append('</div>')
fg.append('</section>')
fg.append('<section class="fg-sec" data-c="save"><h2 class="valence">Life-saving<small>battlefield medicine: built to keep a casualty alive</small></h2>')
fg.append('<div class="grid" data-c="save">')
for e in sorted(save, key=lambda x:x.get("subject","")):
    fg.append(card_html(e))
fg.append('</div></section>')
fg.append(SORTER_JS)
with open(os.path.join(REPO,"field-guide.html"),"w") as f:
    f.write(page("field-guide.html","Field Guide", "".join(fg),
        "The battlefield, with the life-saving set against the life-destroying. The same ground, the same autonomy, opposite ends: a rule that forbids AI in lethal or irreversible decisions would ground the autonomous medevac in the same breath as the loitering munition. Apply a principle to see what it catches. The flags are set from the sourced research and audited by hand, and they remain open to debate."))

# ---- civilian devices page (off the battlefield) ----
cv = [crosslink("civilian.html"),
      '<div class="controls">' + ptest_block("Apply a principle here too. Some of these decide life and death; some only run a household. Watch where the same principle catches and where it lets go.") +
      '<input id="q" type="search" placeholder="search devices..." oninput="flt()"></div>',
      '<div class="grid">']
for e in sorted(civilian, key=lambda x:x.get("subject","")):
    cv.append(card_html(e))
cv.append('</div>')
cv.append(SORTER_JS)
with open(os.path.join(REPO,"civilian.html"),"w") as f:
    f.write(page("civilian.html","Civilian Devices", "".join(cv),
        "Off the battlefield, the same question, across a wider range. A CyberKnife, an implanted defibrillator, an artificial pancreas, and an autonomous surgical robot already make irreversible calls in hospitals and inside the body. A self-driving car decides in milliseconds. And a vacuum, a mower, and a thermostat simply run themselves. The line between an autonomous machine that could end a life and one that only does a chore is exactly the line a clean rule has to draw, and the gradient here is the whole difficulty. This is why the thing cannot be put down; it is already here, and already deciding."))

# ---- IP & services registry (intangible systems, no product photo) ----
REGISTRY = [
 {"name":"Project Maven / Maven Smart System","cat":"military targeting","operator":"US Department of Defense; Palantir","what":"AI that fuses sensor feeds and nominates targets across a battlespace.","decision":"Human on the loop: the system recommends, a human approves.","answer":"Attenuated","rev":"No (the strike)","lethal":1,"irrev":1,"machine":1,"gap":1},
 {"name":"Gospel (Habsora)","cat":"military targeting","operator":"Israel Defense Forces","what":"AI that generates infrastructure and building targets at scale.","decision":"Reported thin human review of machine-generated targets.","answer":"Contested","rev":"No","lethal":1,"irrev":1,"machine":1,"gap":1},
 {"name":"Lavender","cat":"military targeting","operator":"Israel Defense Forces","what":"AI that marks individual people as targets.","decision":"Reported seconds of human review per name.","answer":"Contested","rev":"No","lethal":1,"irrev":1,"machine":1,"gap":1},
 {"name":"Predictive policing (ShotSpotter, Palantir Gotham)","cat":"policing","operator":"Police departments","what":"Software that flags gunshots, predicts crime locations, and fuses records to direct police.","decision":"A human acts on the prompt the software produces.","answer":"Diffuse","rev":"Partial","lethal":0,"irrev":0,"machine":1,"gap":0},
 {"name":"Facial recognition (Clearview AI, NEC)","cat":"identity","operator":"Law enforcement and agencies","what":"Matches a face against a database to identify and track a person.","decision":"A human acts on the match.","answer":"Diffuse","rev":"Partial","lethal":0,"irrev":0,"machine":1,"gap":0},
 {"name":"COMPAS recidivism scoring","cat":"liberty","operator":"Equivant; courts","what":"Scores a defendant's risk to inform bail and sentencing.","decision":"A judge decides, informed by the score.","answer":"Diffuse","rev":"No (time served)","lethal":0,"irrev":1,"machine":1,"gap":0},
 {"name":"Organ allocation algorithms (UNOS, OPTN)","cat":"allocation","operator":"UNOS / OPTN","what":"MELD, KDPI, and LAS scores that rank transplant candidates.","decision":"The algorithm ranks; clinicians and committees act within it.","answer":"Diffuse","rev":"No","lethal":1,"irrev":1,"machine":1,"gap":1},
 {"name":"Stuxnet","cat":"cyber weapon","operator":"Reported US and Israel","what":"A self-propagating worm that physically destroyed Iranian centrifuges and spread beyond its target.","decision":"None at the moment of harm; it acted on its own once released.","answer":"No","rev":"No","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"Mayhem (DARPA Cyber Grand Challenge)","cat":"autonomous cyber","operator":"ForAllSecure; DARPA","what":"An autonomous system that finds, exploits, and patches software flaws without a human.","decision":"The system reasons and acts on its own.","answer":"Operator, attenuated","rev":"Depends","lethal":0,"irrev":0,"machine":1,"gap":1},
 {"name":"Agentic AI assistants (Operator, Claude computer use, Devin)","cat":"AI agent","operator":"AI labs and their users","what":"LLM agents that browse, buy, send, execute, and write and deploy code.","decision":"The agent acts toward a goal a human set.","answer":"Contested","rev":"Mixed","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"Algorithmic trading (Knight Capital, 2010 Flash Crash)","cat":"markets","operator":"Trading firms","what":"Software that executes trades at machine speed; Knight lost about 440 million dollars in 45 minutes.","decision":"No human chose the trades; the code did.","answer":"The firm","rev":"No","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"Smart contracts and DAOs (The DAO, Ooki DAO)","cat":"on-chain","operator":"On-chain; token holders","what":"Code that executes irreversibly on its terms, and organizations run by that code with no central officer.","decision":"The code executes; there may be no human in the loop.","answer":"Contested","rev":"No (on-chain finality)","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"Automated content moderation","cat":"the public square","operator":"Platforms (Meta, YouTube, TikTok)","what":"AI that removes or demotes posts at a scale no human review could match.","decision":"Automated removal; appeals are thin.","answer":"The platform, weakly","rev":"Yes, but not at scale","lethal":0,"irrev":0,"machine":1,"gap":1},
 {"name":"Robodebt (Australia)","cat":"welfare","operator":"Services Australia","what":"An automated debt-recovery scheme (2016-2019) that cross-matched welfare income against averaged tax data and issued about 2 billion dollars in debt notices to 700,000 people.","decision":"The algorithm issued debt notices on its own; no caseworker reviewed an assessment before it went out.","answer":"The agency","rev":"Partial","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"MiDAS (Michigan unemployment fraud system)","cat":"welfare","operator":"Michigan UIA; Fast Enterprises","what":"An automated unemployment-fraud system (2013) that adjudicated fraud and triggered wage garnishments without human review, at a 93 percent error rate.","decision":"The system made final fraud determinations on its own; no human reviewed before penalties hit.","answer":"Contested","rev":"Partial","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"Dutch childcare-benefits algorithm (toeslagenaffaire)","cat":"welfare","operator":"Dutch Tax and Customs Administration","what":"A self-learning fraud model that flagged dual-nationality and low-income families and drove automated repayment demands averaging tens of thousands of euros.","decision":"The algorithm produced risk scores that drove repayment demands; human review existed in theory and was bypassed.","answer":"The agency","rev":"No","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"Ofqual A-level grading algorithm (UK, 2020)","cat":"education","operator":"Ofqual (UK)","what":"A model that replaced cancelled exams with grades anchored to each school's history, downgrading about 40 percent of teacher-assessed grades.","decision":"The algorithm set final grades automatically; a student's own circumstances were not considered.","answer":"The agency","rev":"Yes, not at scale","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"NSA SKYNET","cat":"intelligence","operator":"National Security Agency","what":"A machine-learning program that scored 55 million people's phone metadata in Pakistan to flag suspected couriers, feeding targeting.","decision":"The model flagged individuals; humans made the final call, but the flag was often the only evidence.","answer":"Contested","rev":"No (final)","lethal":1,"irrev":1,"machine":1,"gap":1},
 {"name":"NotPetya","cat":"cyber weapon","operator":"Sandworm (Russian GRU)","what":"A destructive wiper disguised as ransomware (2017) that spread on its own from a Ukrainian software update and destroyed data worldwide.","decision":"Fully autonomous after release; no operator controlled its spread or its targets.","answer":"No","rev":"No (final)","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"Amazon automated recruiting tool","cat":"hiring","operator":"Amazon","what":"A resume-scoring model trained on a male-dominated hiring history that learned to penalize resumes mentioning women.","decision":"The model ranked candidates on its own; recruiters rarely reviewed those it rejected.","answer":"The firm","rev":"Partial","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"HireVue AI video interviews","cat":"hiring","operator":"HireVue","what":"An AI that scores recorded interviews on word choice and tone to rank job candidates, used as a screening gate by large employers.","decision":"The score gates candidates; review of those it rejects is rare.","answer":"Contested","rev":"Partial","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"Arnold PSA (pretrial risk score)","cat":"pretrial","operator":"Courts; Arnold Ventures","what":"A pretrial tool that scores a defendant on nine criminal-history factors to predict failure to appear and new-crime risk.","decision":"A judge decides release; in practice many courts treat the score as dispositive.","answer":"The judge","rev":"Partial","lethal":0,"irrev":1,"machine":0,"gap":0},
 {"name":"SafeRent tenant screening","cat":"housing","operator":"SafeRent Solutions","what":"A tenant-screening service that scores applicants for landlords; it scored Black and Hispanic voucher-holders lower.","decision":"Landlords get the score; many use a threshold as an automatic gate.","answer":"Diffuse","rev":"Partial","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"US terrorist watchlist / No-Fly List","cat":"security","operator":"Terrorist Screening Center (FBI)","what":"A consolidated watchlist of over a million names, built by algorithmic nomination and matching, that blocks or flags people with no disclosed criteria.","decision":"The system matches a traveler to the list and a screener acts; no one human decides each nomination.","answer":"The agency","rev":"Partial","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"FICO credit score","cat":"finance","operator":"Fair Isaac; the credit bureaus","what":"A proprietary 300-850 credit score used in most US lending to set eligibility and rates, with undisclosed model weights.","decision":"The score is generated automatically; lenders use thresholds as hard gates with no review below the cutoff.","answer":"Diffuse","rev":"Partial","lethal":0,"irrev":1,"machine":1,"gap":1},
 {"name":"Allegheny Family Screening Tool","cat":"child welfare","operator":"Allegheny County, Pennsylvania","what":"A predictive model that scores families 1-20 on the risk of a future foster-care placement when a maltreatment call comes in.","decision":"A human screener decides whether to investigate, but must consult a supervisor when the call conflicts with a high score.","answer":"The agency","rev":"Partial","lethal":0,"irrev":1,"machine":0,"gap":0},
 {"name":"TikTok For You recommendation algorithm","cat":"the feed","operator":"ByteDance / TikTok","what":"A deep-learning recommender that selects each user's feed in real time, drawing most content from accounts the user does not follow.","decision":"The algorithm makes every selection in real time; no human reviews what any user is served.","answer":"The firm","rev":"Yes, not at scale","lethal":0,"irrev":0,"machine":1,"gap":1},
]
reg_rows = []
for r in REGISTRY:
    reg_rows.append(
      '<tr data-lethal="%d" data-irrev="%d" data-machine="%d" data-gap="%d" data-s="%s">'
      '<td class="r-name">%s<span class="r-cat">%s</span></td>'
      '<td>%s</td><td>%s</td><td>%s</td><td class="r-ans">%s</td><td>%s</td></tr>' % (
        r["lethal"],r["irrev"],r["machine"],r["gap"],
        html.escape((r["name"]+" "+r["what"]+" "+r["cat"]+" "+r["operator"]).lower()),
        html.escape(r["name"]), html.escape(r["cat"]),
        html.escape(r["what"]), html.escape(r["operator"]), html.escape(r["decision"]),
        html.escape(r["answer"]), html.escape(r["rev"])))
reg_ptest = ('<div class="ptest"><div class="ptest-h">Apply a principle and watch which systems it catches. '
  'In this section the no-answerable-human column fills almost entirely.</div>'
  '<label><input type="checkbox" id="t-lethal" onchange="crit()"> lethal</label>'
  '<label><input type="checkbox" id="t-irrev" onchange="crit()"> irreversible</label>'
  '<label><input type="checkbox" id="t-machine" onchange="crit()"> the machine makes the call</label>'
  '<label><input type="checkbox" id="t-gap" onchange="crit()"> no answerable human</label>'
  '<span id="pcount" class="pcount"></span></div>')
reg_body = (crosslink("registry.html") + reg_ptest +
  '<input id="q" type="search" placeholder="search systems..." oninput="rflt()">'
  '<div class="reg-wrap"><table class="registry"><thead><tr>'
  '<th onclick="rsort(0)">System</th><th onclick="rsort(1)">What it is</th><th onclick="rsort(2)">Operator</th>'
  '<th onclick="rsort(3)">Where the decision sits</th><th onclick="rsort(4)">Answerable?</th><th onclick="rsort(5)">Reversible?</th>'
  '</tr></thead><tbody id="reg-body">' + "".join(reg_rows) + '</tbody></table></div>' +
  """<script>
function t(id){return document.getElementById('t-'+id).checked;}
function crit(){var L=t('lethal'),I=t('irrev'),M=t('machine'),G=t('gap');var any=L||I||M||G;
var rows=document.querySelectorAll('#reg-body tr'),n=0;
rows.forEach(function(c){var m=(!L||c.dataset.lethal==='1')&&(!I||c.dataset.irrev==='1')&&(!M||c.dataset.machine==='1')&&(!G||c.dataset.gap==='1');
if(any&&m){c.classList.add('match');n++;}else{c.classList.remove('match');}});
document.getElementById('pcount').textContent=any?(n+' of '+rows.length+' systems match every checked principle'):'';}
function rflt(){var q=document.getElementById('q').value.toLowerCase();
document.querySelectorAll('#reg-body tr').forEach(function(c){c.style.display=(c.dataset.s.indexOf(q)>-1)?'':'none';});}
var rdir={};
function rsort(i){var b=document.getElementById('reg-body');var rows=[].slice.call(b.querySelectorAll('tr'));
rdir[i]=!rdir[i];rows.sort(function(a,c){var x=a.children[i].innerText.toLowerCase(),y=c.children[i].innerText.toLowerCase();return (x<y?-1:x>y?1:0)*(rdir[i]?1:-1);});
rows.forEach(function(r){b.appendChild(r);});}
</script>""")
with open(os.path.join(REPO,"registry.html"),"w") as f:
    f.write(page("registry.html","IP & Services", reg_body,
        "The intangible golems: the software, algorithms, and services that act without a body to photograph. This is where agency detaches from any object, and where the question of who answers is hardest. Sort by any column, or apply a principle and watch the no-answerable-human column fill. The flags are set from the sourced research and audited by hand, and they remain open to debate."))

# ---- diagrams ----
D1 = """flowchart TD
  A["An automated system causes a lethal or irreversible harm"] --> B{"Did a human make the discriminating call,<br/>or only set the machine in motion?"}
  B -->|"a human made the call<br/>(CyberKnife, supervised drone)"| C["Liability runs to the human.<br/>The fire is his arrow."]
  B -->|"the machine made the call"| D{"Is there a responsible human<br/>the law can still reach?"}
  D -->|"yes: operator, commander, founder"| E["Run it back to him.<br/>Veil-piercing reaches the human behind the golem."]
  D -->|"no: full autonomy, AI-run firm, DAO"| F["The accountability gap.<br/>No defendant; the residue the court cannot reach."]"""
D2 = """flowchart LR
  S["Sovereign / State"] --> P["Private military corporation<br/>(a corporate golem)"]
  P --> AI["AI targeting system<br/>(a weapon golem)"]
  AI --> K["The act: a strike"]
  S -. "delegates authority" .-> P
  P -. "delegates the decision" .-> AI
  K -. "who answers?" .-> Q{"At each layer, is there<br/>an answerable human?"}"""
D3 = """flowchart TD
  G["A thing acts and cannot answer<br/>(Sanhedrin 65b: the golem returns to dust)"] --> H{"Is the intermediary a competent person<br/>who could refuse?"}
  H -->|"yes (a piqqeach)"| I["No agency for a wrong.<br/>The doer bears it; the sender steps back."]
  H -->|"no (a golem, an AI: lav bar chiyuva)"| J["The whole act reverts to the sender.<br/>The fire is his arrow; the keeper is forewarned."]
  J --> R{"Is the act the taking of a life?"}
  R -->|"yes"| K["Directness is required; and a residue remains:<br/>exempt in the human court, liable before Heaven."]
  R -->|"no"| L["Liability runs to the sender in full."]"""
def dia(t,src,note):
    return '<section class="diagram"><h3>%s</h3><pre class="mermaid">%s</pre><p class="note">%s</p></section>'%(html.escape(t),src,html.escape(note))
diabody = (dia("The argument in one path", D1, "The trigger words do not sort the cases; the question that does is whether an answerable human survives.")
  + dia("The nested golem: the corporate decision to kill", D2, "A state animates a corporation that animates a machine. The decision to kill sits three non-answering layers deep.")
  + dia("The Jewish-law chain", D3, "Agency, the fire that is the sender's arrow, the directness the taking of a life demands, and the residue the court cannot reach."))
with open(os.path.join(REPO,"diagrams.html"),"w") as f:
    f.write(page("diagrams.html","Diagrams", diabody, "The argument, the nested golem, and the Jewish-law structure, drawn.", mermaid=True))

# ---- landing ----
cards = ""
for h,l,desc in [
  ("essay.html","The Essay","The central argument: the prohibition names a real worry but lacks the principle that would tell the forbidden from the permitted."),
  ("field-guide.html","The Field Guide","The battlefield, with life-saving tech set against life-destroying tech, so a ban on lethal or irreversible decisions grounds the medevac with the missile."),
  ("civilian.html","Civilian Devices","The machines that already make irreversible life-and-death calls off the battlefield: in hospitals, in cars, and inside the body."),
  ("registry.html","IP & Services","The intangible golems: software, algorithms, and agents that act with no body to photograph, in a sortable registry."),
  ("diagrams.html","Diagrams","The argument and the traditions, visualized."),
]:
    cards += '<a class="navcard" href="%s"><h3>%s</h3><p>%s</p></a>'%(h,html.escape(l),html.escape(desc))
landing = ('<section class="diagram"><pre class="mermaid">%s</pre></section>'
           '<div class="navcards">%s</div>') % (D1, cards)
with open(os.path.join(REPO,"index.html"),"w") as f:
    f.write(page("index.html","Law of the Golem", landing,
        "AI, agency, and responsibility for the things we set in motion. A CyberKnife and a loitering munition are both lethal and both irreversible, yet one belongs in a hospital and one is the worry. The question that sorts them is older: when a thing that cannot answer causes harm, is there still a person the law can reach?",
        mermaid=True))

# The raw-source archive page was removed deliberately. The build must never
# publish the working folder, which contains drafts, notes, and private material.

GOLEM_CSS = """/* Golem project components, on the Oranburg design system (site.css + lawj-palette.css). */
.skip-link{position:absolute;left:-999px;top:auto;width:1px;height:1px;overflow:hidden}
.skip-link:focus{position:fixed;top:0;left:0;width:auto;height:auto;padding:1rem;background:var(--accent-red);color:#fff;z-index:999;text-decoration:none}

/* breadcrumb back to the main site (matches the K subsite) */
.breadcrumb-bar{background:var(--bg-secondary);border-bottom:1px solid var(--border);padding:var(--space-sm) var(--space-lg)}
.breadcrumb-list{max-width:var(--max-width);margin:0 auto;display:flex;flex-wrap:wrap;list-style:none;padding:0;gap:0;font-size:.82rem;font-family:var(--font-body);color:var(--muted)}
.breadcrumb-item{display:flex;align-items:center}
.breadcrumb-sep{margin:0 var(--space-sm);color:var(--muted)}
.breadcrumb-item a{color:var(--accent);text-decoration:none}
.breadcrumb-item a:hover{color:var(--accent-2)}
.breadcrumb-item [aria-current="page"]{color:var(--text)}

/* content + long-form prose in the accent serif */
.site-content{max-width:var(--max-width);margin:0 auto;padding:var(--space-xl) var(--space-lg) var(--space-2xl)}
.site-content h1{font-family:var(--font-headline);font-weight:600;line-height:1.12;margin:.2rem 0 .6rem}
.lede{font-family:var(--font-accent);font-size:1.2rem;color:var(--text);max-width:64ch;margin:0 0 1.4rem}
.site-content h2{font-family:var(--font-headline);font-weight:600;font-size:1.5rem;margin:2rem 0 .6rem}
.site-content h3{font-family:var(--font-headline);font-weight:500;margin:1.4rem 0 .4rem}
.site-content > p,.site-content > ul,.site-content > ol,.site-content blockquote,.site-content > section p{font-family:var(--font-accent);font-size:1.05rem;line-height:1.66}
.site-content p{max-width:66ch}
.site-content img{max-width:100%;height:auto;border-radius:var(--radius-md);border:1px solid var(--border);margin:1rem 0 .3rem}
.site-content blockquote{border-left:3px solid var(--accent);margin:1rem 0;padding:.1rem 0 .1rem 1rem;color:var(--text)}
.footnotes{margin-top:2.5rem;border-top:1px solid var(--border);padding-top:1rem;font-size:.9rem;color:var(--muted);font-family:var(--font-body)}
.footnotes p{font-family:var(--font-body)}

/* landing nav cards */
.navcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:1rem;margin:.5rem 0 2rem}
.navcard{display:block;background:var(--bg-secondary);border:1px solid var(--border);border-radius:var(--radius-md);padding:1rem 1.1rem;text-decoration:none;color:var(--text)}
.navcard:hover{border-color:var(--accent)}
.navcard h3{margin:0 0 .35rem;font-family:var(--font-headline);font-weight:600;font-size:1.15rem}
.navcard p{margin:0;font-size:.88rem;color:var(--muted);font-family:var(--font-body)}

/* diagrams */
.diagram{background:var(--bg-secondary);border:1px solid var(--border);border-radius:var(--radius-md);padding:1rem;margin:1.5rem 0}
.diagram h3{margin:0 0 .5rem;font-family:var(--font-body);font-weight:600;font-size:.8rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.diagram .note{margin:.5rem .2rem 0;font-size:.88rem;color:var(--muted);font-family:var(--font-body)}
.diagram .mermaid{overflow-x:auto}

/* field guide controls + sorter */
.controls{position:sticky;top:0;background:var(--bg);padding:.8rem 0;z-index:5}
.ptest{background:var(--bg-secondary);border:1px solid var(--border);border-radius:var(--radius-md);padding:.8rem .9rem;margin:0 0 .8rem;font-size:.9rem;font-family:var(--font-body)}
.ptest-h{color:var(--muted);font-weight:600;font-size:.82rem;margin-bottom:.5rem}
.ptest label{display:inline-flex;align-items:center;gap:.4rem;margin:0 1rem .4rem 0;cursor:pointer}
.pcount{display:block;margin-top:.4rem;color:var(--accent);font-style:italic}
#q{width:100%;padding:.7rem .9rem;background:var(--bg-secondary);border:1px solid var(--border);border-radius:var(--radius-sm);color:var(--text);font-family:var(--font-body);font-size:1rem}
.chips{display:flex;flex-wrap:wrap;gap:.5rem;margin-top:.6rem}
.chip{font-family:var(--font-body);font-weight:600;font-size:.8rem;color:var(--muted);background:var(--bg-secondary);border:1px solid var(--border);border-radius:var(--radius-pill);padding:.5rem .8rem;cursor:pointer}
.chip.on{color:#fff;background:var(--accent);border-color:var(--accent)}
.valence{font-family:var(--font-headline);font-weight:700;font-size:1.7rem;color:var(--text);margin:2.4rem 0 .2rem;display:flex;flex-direction:column;gap:.15rem}
.valence small{font-family:var(--font-body);font-weight:400;font-size:.85rem;color:var(--muted);letter-spacing:0;text-transform:none}
.fg-sec{margin-bottom:1.4rem}
.crosslink{font-family:var(--font-body);font-size:.85rem;color:var(--muted);background:var(--bg-secondary);border:1px solid var(--border);border-radius:var(--radius-md);padding:.6rem .8rem;margin:0 0 1rem}
.crosslink a{color:var(--accent)}
.note.pending{font-family:var(--font-body);font-size:.9rem;color:var(--muted);font-style:italic;padding:.4rem 0}
.cluster{display:flex;align-items:center;gap:.7rem;margin:1.5rem 0 .9rem;font-family:var(--font-headline);font-weight:600;font-size:1.15rem;border-bottom:1px solid var(--border);padding-bottom:.4rem}
.cluster span{font-family:var(--font-body);font-weight:700;font-size:.78rem;color:#fff;background:var(--red-deep);border-radius:var(--radius-pill);width:26px;height:26px;display:inline-grid;place-items:center;flex:none}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(210px,1fr));gap:1.1rem}
.card{margin:0;background:var(--bg-secondary);border:1px solid var(--border);border-radius:var(--radius-md);overflow:hidden;display:flex;flex-direction:column}
.card img{width:100%;height:160px;object-fit:cover;background:#000;border:0;border-bottom:1px solid var(--border);border-radius:0;margin:0}
.card figcaption{padding:.8rem;display:flex;flex-direction:column;gap:.4rem;font-size:.88rem;font-family:var(--font-body)}
.card figcaption b{font-weight:700;font-size:.9rem;color:var(--text)}
.card .desc{font-size:.82rem;line-height:1.45;color:var(--text)}
.card .posture{font-size:.78rem;line-height:1.4;color:var(--muted)}
.card .posture b{color:var(--text);font-weight:600}
.card .meta{color:var(--muted);font-size:.72rem;line-height:1.35}
.card.match{outline:2px solid var(--accent);outline-offset:-1px}

/* archive */
ul.archive{columns:2;font-size:.88rem;font-family:var(--font-body)}
ul.archive a{color:var(--muted)}
/* IP & services registry table */
.reg-wrap{overflow-x:auto;border:1px solid var(--border);border-radius:var(--radius-md);margin-top:.8rem}
.registry{width:100%;border-collapse:collapse;font-family:var(--font-body);font-size:.86rem;min-width:780px}
.registry th{text-align:left;background:var(--bg-secondary);color:var(--text);font-weight:600;padding:.6rem .7rem;border-bottom:1px solid var(--border);cursor:pointer;white-space:nowrap;position:sticky;top:0}
.registry th:hover{color:var(--accent)}
.registry td{padding:.6rem .7rem;border-bottom:1px solid var(--border);vertical-align:top;color:var(--text)}
.registry tbody tr:hover td{background:var(--bg-soft)}
.registry .r-name{font-weight:700;min-width:150px}
.registry .r-cat{display:block;font-weight:400;font-size:.7rem;color:var(--muted);text-transform:uppercase;letter-spacing:.04em;margin-top:2px}
.registry .r-ans{font-weight:600}
.registry tbody tr.match td{background:rgba(109,172,222,.16)}
@media(max-width:640px){ul.archive{columns:1}}
"""
SITE_REPO = "/Users/sco/oranburg.github.io"
for rel in ["assets/css/lawj-palette.css","assets/css/site.css","assets/js/site.js"]:
    s = os.path.join(SITE_REPO, rel)
    if os.path.exists(s):
        os.makedirs(os.path.dirname(os.path.join(REPO, rel)), exist_ok=True)
        shutil.copyfile(s, os.path.join(REPO, rel))
os.makedirs(os.path.join(REPO, "assets", "css"), exist_ok=True)
with open(os.path.join(REPO, "assets", "css", "golem.css"), "w") as f:
    f.write(GOLEM_CSS)
if os.path.exists(os.path.join(REPO, "styles.css")):
    os.remove(os.path.join(REPO, "styles.css"))

# ---- .nojekyll + README ----
open(os.path.join(REPO,".nojekyll"),"w").close()
README = '''# Law of the Golem

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
'''
with open(os.path.join(REPO,"README.md"),"w") as f:
    f.write(README)

print("BUILT. pages:", ["index.html","field-guide.html","diagrams.html"] + built)
print("images:", len(os.listdir(IMG_DST)))
