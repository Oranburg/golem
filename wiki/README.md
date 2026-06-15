# Wiki pages (staged here until the wiki is initialized)

These Markdown files are the project wiki pages: Home, Roadmap, Current Status, Software Documentation, and the future project. They are kept in the repository so they are version-controlled and not lost.

GitHub does not create the wiki git repository until the first wiki page is created through the web interface, and there is no API or command-line way to create that first page. So publishing these is a one-time manual step:

1. Open https://github.com/Oranburg/golem/wiki and click "Create the first page". Save anything; this initializes the wiki repository.
2. Then publish these pages:

```
git clone https://github.com/Oranburg/golem.wiki.git
cp wiki/*.md golem.wiki/
cd golem.wiki && git add -A && git commit -m "Publish wiki pages" && git push
```

The one-time initialization is tracked as a repository Issue. Until the wiki is live, the files here are the source of truth for its content.
