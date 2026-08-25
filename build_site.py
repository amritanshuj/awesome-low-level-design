#!/usr/bin/env python3
"""Generate GitHub Pages HTML for every problem, pattern, and OOP topic in the repo."""
from __future__ import annotations

import html
import re
from pathlib import Path

import markdown
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.lexers import get_lexer_by_name, guess_lexer_for_filename
from pygments.util import ClassNotFound

ROOT = Path(__file__).resolve().parent
PAGES = ROOT / "pages"
ASSETS = ROOT / "assets"
SKIP_DIRS = {"bin", "obj", ".idea", "node_modules", "__pycache__"}
CODE_EXT = {
    ".java": "java",
    ".py": "python",
    ".cpp": "cpp",
    ".cc": "cpp",
    ".cxx": "cpp",
    ".hpp": "cpp",
    ".h": "cpp",
    ".hh": "cpp",
    ".cs": "csharp",
    ".go": "go",
    ".ts": "typescript",
    ".js": "javascript",
    ".rs": "rust",
}
FMT = HtmlFormatter(style="monokai", noclasses=False, cssclass="highlight")
MD = markdown.Markdown(extensions=["fenced_code", "tables", "sane_lists", "nl2br"])


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


PROBLEMS = [
    ("easy", "Interview Favorite", "Design Parking Lot", "parking-lot.md", "parkinglot-class-diagram.png",
     {"java": "parkinglot", "python": "parkinglot", "cpp": "parkinglot", "csharp": "parkinglot", "go": "parkinglot", "ts": "ParkingLot"}),
    ("easy", "Interview Favorite", "Design Stack Overflow", "stack-overflow.md", "stackoverflow-class-diagram.png",
     {"java": "stackoverflow", "python": "stackoverflow", "cpp": "stackoverflow", "csharp": "stackoverflow", "go": "stackOverFlow", "ts": "StackOverflow"}),
    ("easy", "State Machine", "Design a Vending Machine", "vending-machine.md", "vendingmachine-class-diagram.png",
     {"java": "vendingmachine", "python": "vendingmachine", "cpp": "vendingmachine", "csharp": "vendingmachine", "go": "vendingmachine", "ts": "VendingMachine"}),
    ("easy", "Observability", "Design Logging Framework", "logging-framework.md", "loggingframework-class-diagram.png",
     {"java": "loggingframework", "python": "loggingframework", "cpp": "loggingframework", "csharp": "loggingframework", "go": "loggingframework", "ts": "LoggingFramework"}),
    ("easy", "Concurrency", "Design Traffic Signal Control System", "traffic-signal.md", "trafficcontrolsystem-class-diagram.png",
     {"java": "trafficsignalcontrolsystem", "python": "trafficsignalsystem", "cpp": "trafficsignalsystem", "csharp": "trafficsignalsystem", "go": "trafficsignalsystem", "ts": "TrafficSignalSystem"}),
    ("easy", "State Machine", "Design Coffee Vending Machine", "coffee-vending-machine.md", "coffeevendingmachine-class-diagram.png",
     {"java": "coffeevendingmachine", "python": "coffeevendingmachine", "cpp": "coffeevendingmachine", "csharp": "coffeevendingmachine", "go": "coffeevendingmachine", "ts": "CoffeeVendingMachine"}),
    ("easy", "CRUD", "Design a Task Management System", "task-management-system.md", "taskmanagementsystem-class-diagram.png",
     {"java": "taskmanagementsystem", "python": "taskmanagementsystem", "cpp": "taskmanagementsystem", "csharp": "taskmanagementsystem", "go": "taskmanagementsystem", "ts": "TaskManagement"}),
    ("medium", "Interview Favorite", "Design ATM", "atm.md", "atm-class-diagram.png",
     {"java": "atm", "python": "atm", "cpp": "atm", "csharp": "atm", "go": "atm"}),
    ("medium", "Social Graph", "Design LinkedIn", "linkedin.md", "linkedin-class-diagram.png",
     {"java": "linkedin", "python": "linkedin", "cpp": "linkedin", "csharp": "linkedIn", "go": "linkedin"}),
    ("medium", "Interview Favorite", "Design LRU Cache", "lru-cache.md", "lrucache-class-diagram.png",
     {"java": "lrucache", "python": "lrucache", "cpp": "lrucache", "csharp": "lrucache", "go": "lrucache"}),
    ("medium", "Interview Favorite", "Design Tic Tac Toe Game", "tic-tac-toe.md", "tictactoe-class-diagram.png",
     {"java": "tictactoe", "python": "tictactoe", "cpp": "tictactoe", "csharp": "tictactoe", "go": "tictactoe"}),
    ("medium", "Messaging", "Design Pub Sub System", "pub-sub-system.md", "pubsubsystem-class-diagram.png",
     {"java": "pubsubsystem", "python": "pubsubsystem", "cpp": "pubsubsystem", "csharp": "pubsubsystem", "go": "pubsubsystem"}),
    ("medium", "Interview Favorite", "Design an Elevator System", "elevator-system.md", "elevatorsystem-class-diagram.png",
     {"java": "elevatorsystem", "python": "elevatorsystem", "cpp": "elevatorsystem", "csharp": "elevatorsystem", "go": "elevatorsystem"}),
    ("medium", "Booking", "Design Car Rental System", "car-rental-system.md", "carrentalsystem-class-diagram.png",
     {"java": "carrentalsystem", "python": "carrentalsystem", "cpp": "carrentalsystem", "csharp": "carrentalsystem", "go": "carrentalsystem"}),
    ("medium", "Marketplace", "Design an Online Auction System", "online-auction-system.md", "onlineauctionsystem-class-diagram.png",
     {"java": "onlineauctionsystem", "python": "onlineauctionsystem", "cpp": "onlineauctionsystem", "csharp": "onlineauctionsystem", "go": "onlineauctionsystem"}),
    ("medium", "Booking", "Design Hotel Management System", "hotel-management-system.md", "hotelmanagementsystem-class-diagram.png",
     {"java": "hotelmanagementsystem", "python": "hotelmanagementsystem", "cpp": "hotelmanagementsystem", "csharp": "hotelmanagementsystem", "go": "hotelmanagementsystem"}),
    ("medium", "Payments", "Design a Digital Wallet Service", "digital-wallet-service.md", "digitalwalletservice-class-diagram.png",
     {"java": "digitalwalletservice", "python": "digitalwalletservice", "cpp": "digitalwalletservice", "csharp": "digitalwalletservice", "go": "digitalwalletservice"}),
    ("medium", "Booking", "Design Airline Management System", "airline-management-system.md", "airlinemanagementsystem-class-diagram.png",
     {"java": "airlinemanagementsystem", "python": "airlinemanagementsystem", "cpp": "airlinemanagementsystem", "csharp": "airlinemanagementsystem", "go": "airlinemanagementsystem"}),
    ("medium", "CRUD", "Design a Library Management System", "library-management-system.md", "librarymanagementsystem-class-diagram.png",
     {"java": "librarymanagementsystem", "python": "librarymanagementsystem", "cpp": "librarymanagementsystem", "csharp": "librarymanagementsystem", "go": "librarymanagementsystem"}),
    ("medium", "Social Graph", "Design a Social Network like Facebook", "social-networking-service.md", "socialnetworkingservice-class-diagram.png",
     {"java": "socialnetworkingservice", "python": "socialnetworkingservice", "cpp": "socialnetworkingservice", "csharp": "socialnetworkingservice", "go": "socialnetworkingservice"}),
    ("medium", "Booking", "Design Restaurant Management System", "restaurant-management-system.md", "restaurantmanagementsystem-class-diagram.png",
     {"java": "restaurantmanagementsystem", "python": "restaurantmanagementsystem", "cpp": "restaurantmanagementsystem", "csharp": "restaurantmanagementsystem", "go": "restaurantmanagementsystem"}),
    ("medium", "Booking", "Design a Concert Ticket Booking System", "concert-ticket-booking-system.md", "concertticketbookingsystem-class-diagram.png",
     {"java": "concertticketbookingsystem", "python": "concertticketbookingsystem", "cpp": "concertticketbookingsystem", "csharp": "concertticketbookingsystem", "go": "concertticketbookingsystem"}),
    ("hard", "Sports", "Design CricInfo", "cricinfo.md", "cricinfo-class-diagram.png",
     {"java": "cricinfo", "python": "cricinfo", "cpp": "cricinfo", "csharp": "cricinfo", "go": "cricinfo"}),
    ("hard", "Payments", "Design Splitwise", "splitwise.md", "splitwise-class-diagram.png",
     {"java": "splitwise", "python": "splitwise", "cpp": "splitwise", "csharp": "splitwise", "go": "splitwise"}),
    ("hard", "Game", "Design Chess Game", "chess-game.md", "chessgame-class-diagram.png",
     {"java": "chessgame", "python": "chessgame", "cpp": "chessgame", "csharp": "chessgame", "go": "chessgame"}),
    ("hard", "Interview Favorite", "Design a Snake and Ladder game", "snake-and-ladder.md", "snakeandladdergame-class-diagram.png",
     {"java": "snakeandladdergame", "python": "snakeandladdergame", "cpp": "snakeandladdergame", "csharp": "snakeandladdergame", "go": "snakeandladdergame"}),
    ("hard", "Interview Favorite", "Design Ride-Sharing Service like Uber", "ride-sharing-service.md", "ridesharingservice-class-diagram.png",
     {"java": "ridesharingservice", "python": "ridesharingservice", "cpp": "ridesharingservice", "csharp": "ridesharingservice", "go": "ridesharingservice"}),
    ("hard", "Scheduling", "Design Course Registration System", "course-registration-system.md", "courseregistrationsystem-class-diagram.png",
     {"java": "courseregistrationsystem", "python": "courseregistrationsystem", "cpp": "courseregistrationsystem", "csharp": "courseregistrationsystem", "go": "courseregistrationsystem"}),
    ("hard", "Interview Favorite", "Design Movie Ticket Booking System", "movie-ticket-booking-system.md", "movieticketbookingsystem-class-diagram.png",
     {"java": "movieticketbookingsystem", "python": "movieticketbookingsystem", "cpp": "movieticketbookingsystem", "csharp": "movieticketbookingsystem", "go": "movieticketbookingsystem"}),
    ("hard", "E-commerce", "Design Online Shopping System like Amazon", "online-shopping-service.md", "onlineshoppingservice-class-diagram.png",
     {"java": "onlineshoppingservice", "python": "onlineshoppingservice", "cpp": "onlineshoppingservice", "csharp": "onlineshoppingservice", "go": "onlineshoppingservice"}),
    ("hard", "Finance", "Design Online Stock Brokerage System", "online-stock-brokerage-system.md", "onlinestockbrokeragesystem-class-diagram.png",
     {"java": "onlinestockbrokeragesystem", "python": "onlinestockbrokeragesystem", "cpp": "onlinestockbrokeragesystem", "csharp": "onlinestockbrokeragesystem", "go": "onlinestockbrokeragesystem"}),
    ("hard", "Streaming", "Design Music Streaming Service like Spotify", "music-streaming-service.md", "musicstreamingservice-class-diagram.png",
     {"java": "musicstreamingservice", "python": "musicstreamingservice", "cpp": "musicstreamingservice", "csharp": "musicstreamingservice", "go": "musicstreamingservice"}),
    ("hard", "Marketplace", "Design Online Food Delivery Service like Swiggy", "food-delivery-service.md", "fooddeliveryservice-class-diagram.png",
     {"java": "fooddeliveryservice", "python": "fooddeliveryservice", "cpp": "fooddeliveryservice", "csharp": "fooddeliveryservice", "go": "fooddeliveryservice"}),
    ("extra", "File System", "Design File / Directory System", None, "filedirectory-class-diagram.png",
     {"java": "filedirectory"}),
    ("extra", "Learning", "Design Online Learning Platform", None, "onlinelearningplatform-class-diagram.png",
     {"java": "onlinelearningplatform"}),
    ("extra", "Voting", "Design Voting System", None, "votingsystem-class-diagram.png",
     {"java": "votingsystem", "python": "votingsystem", "cpp": "votingsystem", "csharp": "votingsystem", "go": "votingsystem"}),
]

OOP = [
    ("classes-and-objects", "Classes and Objects", "classesandobjects", "classes_and_objects"),
    ("interfaces", "Interfaces", "interfaces", "interfaces"),
    ("encapsulation", "Encapsulation", "encapsulation", "encapsulation"),
    ("abstraction", "Abstraction", "abstraction", "abstraction"),
    ("inheritance", "Inheritance", "inheritance", "inheritance"),
    ("polymorphism", "Polymorphism", "polymorphism", "polymorphism"),
    ("association", "Association", "association", "association"),
    ("aggregation", "Aggregation", "aggregation", "aggregation"),
    ("composition", "Composition", "composition", "composition"),
    ("aggregation-vs-composition", "Aggregation vs Composition", "AggregationVsComposition", None),
]

PATTERNS = [
    ("singleton", "Singleton", "Creational", "singleton", "Creational Pattern/Singleton Design  Pattern"),
    ("factory-method", "Factory Method", "Creational", "factory", "Creational Pattern/Factory Design Pattern"),
    ("abstract-factory", "Abstract Factory", "Creational", "abstractfactory", "Creational Pattern/AbstractFactory Design Pattern"),
    ("builder", "Builder", "Creational", "builder", "Creational Pattern/Builder Design Pattern"),
    ("prototype", "Prototype", "Creational", "prototype", "Creational Pattern/Prototype Design Pattern"),
    ("adapter", "Adapter", "Structural", "adapter", "Structural Pattern/Adapter Design Pattern"),
    ("bridge", "Bridge", "Structural", "bridge", "Structural Pattern/Bridge Design Pattern"),
    ("composite", "Composite", "Structural", "composite", "Structural Pattern/Composite Design Pattern"),
    ("decorator", "Decorator", "Structural", "decorator", "Structural Pattern/Decorator Design Pattern"),
    ("facade", "Facade", "Structural", "facade", "Structural Pattern/Facade Design Pattern"),
    ("flyweight", "Flyweight", "Structural", "flyweight", "Structural Pattern/Flyweight Design Pattern"),
    ("proxy", "Proxy", "Structural", "proxy", "Structural Pattern/Proxy Design Pattern"),
    ("iterator", "Iterator", "Behavioral", "iterator", "Behavioral Pattern/Iterator Design Pattern"),
    ("observer", "Observer", "Behavioral", "observer", "Behavioral Pattern/Observer Design Pattern"),
    ("strategy", "Strategy", "Behavioral", "strategy", "Behavioral Pattern/Strategy Design Pattern"),
    ("command", "Command", "Behavioral", "command", "Behavioral Pattern/Command Design Pattern"),
    ("state", "State", "Behavioral", "state", "Behavioral Pattern/State Design Pattern"),
    ("template-method", "Template Method", "Behavioral", "templatemethod", "Behavioral Pattern/Template Design Pattern"),
    ("visitor", "Visitor", "Behavioral", "visitor", "Behavioral Pattern/Visitor Design Pattern"),
    ("mediator", "Mediator", "Behavioral", "mediator", "Behavioral Pattern/Mediator Design Pattern"),
    ("memento", "Memento", "Behavioral", "memento", "Behavioral Pattern/Memento Design Pattern"),
    ("chain-of-responsibility", "Chain of Responsibility", "Behavioral", "chainofresponsibility", "Behavioral Pattern/Chain of Responsibilites"),
]

LANG_META = [
    ("java", "Java"),
    ("python", "Python"),
    ("cpp", "C++"),
    ("csharp", "C#"),
    ("go", "Go"),
    ("ts", "TypeScript"),
    ("js", "JavaScript"),
    ("rust", "Rust"),
]


def collect_files(folder: Path) -> list[Path]:
    if not folder.exists():
        return []
    out = []
    for f in folder.rglob("*"):
        if not f.is_file():
            continue
        if any(p in SKIP_DIRS for p in f.parts):
            continue
        if f.suffix.lower() not in CODE_EXT:
            continue
        if f.stat().st_size > 250_000:
            continue
        out.append(f)
    def key(p: Path):
        n = p.name.lower()
        pri = 0 if ("demo" in n or n.startswith("main.")) else 1
        return (pri, str(p).lower())
    return sorted(out, key=key)


def find_readme(folder: Path) -> Path | None:
    if not folder.exists():
        return None
    for name in ("README.md", "readme.md", "README.MD"):
        p = folder / name
        if p.exists():
            return p
    return None


def highlight_code(path: Path, text: str) -> str:
    lang = CODE_EXT.get(path.suffix.lower(), "text")
    try:
        lexer = get_lexer_by_name(lang)
    except ClassNotFound:
        try:
            lexer = guess_lexer_for_filename(path.name, text)
        except ClassNotFound:
            lexer = get_lexer_by_name("text")
    return highlight(text, lexer, FMT)


def render_md(text: str, rel_root: str) -> str:
    MD.reset()
    body = MD.convert(text)
    body = body.replace("../class-diagrams/", f"{rel_root}/class-diagrams/")
    body = body.replace("../../../../uml-diagrams/class-diagrams/", f"{rel_root}/class-diagrams/")
    body = re.sub(r"href=\"\.\./solutions/[^\"]+\"", "href=\"#java\"", body)
    return body


def drop_implementations(md: str) -> str:
    return re.sub(r"\n## Implementations[\s\S]*?(?=\n## |\Z)", "\n", md)


def lang_tabs(groups: list[tuple[str, str, str]]) -> str:
    if not groups:
        return "<p class='lede'>No source files found in the repository for this topic.</p>"
    buttons = []
    panels = []
    for lid, label, inner in groups:
        buttons.append(f'<button type="button" data-tab="{html.escape(lid)}">{html.escape(label)}</button>')
        panels.append(f'<section class="panel" id="{html.escape(lid)}" data-panel="{html.escape(lid)}">{inner}</section>')
    return f'<div class="tabs">{"".join(buttons)}</div>{"".join(panels)}'


def files_html(files: list[Path], readme: Path | None, rel_root: str, include_readme: bool = True) -> str:
    parts = []
    if include_readme and readme:
        parts.append(f'<div class="prose">{render_md(readme.read_text(encoding="utf-8", errors="replace"), rel_root)}</div>')
    for i, f in enumerate(files):
        rel = f.relative_to(ROOT)
        code = f.read_text(encoding="utf-8", errors="replace")
        open_attr = " open" if i == 0 and not (include_readme and readme) else ""
        parts.append(
            f'<details class="file"{open_attr}><summary>{html.escape(str(rel))}</summary>'
            f"{highlight_code(f, code)}</details>"
        )
    return "".join(parts) or "<p class='lede'>No files in this language.</p>"


def page_shell(title: str, rel_root: str, crumbs: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{html.escape(title)} · Low Level Design Guide</title>
  <link rel="icon" href="{rel_root}/assets/favicon.svg" type="image/svg+xml" />
  <link rel="icon" href="{rel_root}/assets/favicon-32.png" type="image/png" sizes="32x32" />
  <link rel="apple-touch-icon" href="{rel_root}/assets/apple-touch-icon.png" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="{rel_root}/assets/site.css" />
  <link rel="stylesheet" href="{rel_root}/assets/pygments.css" />
  <script src="{rel_root}/assets/page.js"></script>
</head>
<body>
  <header class="site-header">
    <div class="wrap">
      <a class="brand" href="{rel_root}/index.html"><span aria-hidden="true">💻</span> Low Level Design Guide</a>
      <nav class="nav-mini">
        <a href="{rel_root}/index.html#oop">OOP</a>
        <a href="{rel_root}/index.html#patterns">Patterns</a>
        <a href="{rel_root}/index.html#problems">Problems</a>
        <a href="{rel_root}/index.html#languages">Code</a>
        <a href="{rel_root}/pages/interview.html">Interview</a>
      </nav>
      <button class="icon-btn" id="themeBtn" type="button" aria-label="Toggle dark mode">
        <span class="icon-moon">☾</span><span class="icon-sun">☀</span>
      </button>
    </div>
  </header>
  <main class="page"><div class="wrap">
    <p class="crumbs">{crumbs}</p>
    {body}
  </div></main>
</body>
</html>
"""


def solution_dir(kind: str, folder: str) -> Path:
    if kind == "java":
        return ROOT / "solutions/java/src" / folder
    if kind == "python":
        return ROOT / "solutions/python" / folder
    if kind == "cpp":
        return ROOT / "solutions/cpp" / folder
    if kind == "csharp":
        return ROOT / "solutions/csharp" / folder
    if kind == "go":
        return ROOT / "solutions/golang" / folder
    if kind == "ts":
        return ROOT / "solutions/typescript/src" / folder
    return ROOT / "missing"


def write_problem_pages() -> list[tuple[str, str]]:
    out_dir = PAGES / "problems"
    out_dir.mkdir(parents=True, exist_ok=True)
    made = []
    slugs = []
    for item in PROBLEMS:
        difficulty, tag, title, md_name, diagram, langs = item
        slug = md_name[:-3] if md_name else slugify(title.replace("Design ", ""))
        slugs.append((slug, title))
    for i, item in enumerate(PROBLEMS):
        difficulty, tag, title, md_name, diagram, langs = item
        slug = slugs[i][0]
        rel_root = "../.."
        groups = []
        fallback_readme = None
        for key, label in LANG_META:
            folder = langs.get(key)
            if not folder:
                continue
            d = solution_dir(key, folder)
            files = collect_files(d)
            readme = find_readme(d)
            if not files and not readme:
                continue
            if fallback_readme is None and readme:
                fallback_readme = readme
            groups.append((key, label, files_html(files, readme, rel_root, include_readme=False)))
        spec = ""
        if md_name:
            md_path = ROOT / "problems" / md_name
            if md_path.exists():
                spec = render_md(drop_implementations(md_path.read_text(encoding="utf-8", errors="replace")), rel_root)
        elif fallback_readme:
            spec = render_md(
                drop_implementations(fallback_readme.read_text(encoding="utf-8", errors="replace")),
                rel_root,
            )
        diagram_html = ""
        dpath = ROOT / "class-diagrams" / diagram
        if dpath.exists():
            diagram_html = f'<figure class="diagram"><img src="{rel_root}/class-diagrams/{html.escape(diagram)}" alt="{html.escape(title)} class diagram" /></figure>'
        prev_link = next_link = ""
        if i:
            prev_link = f'<a href="{slugs[i-1][0]}.html"><span>Previous</span>{html.escape(slugs[i-1][1])}</a>'
        else:
            prev_link = f'<a href="{rel_root}/index.html#problems"><span>Index</span>All problems</a>'
        if i < len(slugs) - 1:
            next_link = f'<a href="{slugs[i+1][0]}.html"><span>Next</span>{html.escape(slugs[i+1][1])}</a>'
        else:
            next_link = f'<a href="{rel_root}/index.html#problems"><span>Index</span>All problems</a>'
        body = f"""
    <span class="badge">{html.escape(difficulty.title())} · {html.escape(tag)}</span>
    <h1>{html.escape(title)}</h1>
    <p class="lede">Requirements, class diagram, and complete implementations from this repository.</p>
    {diagram_html}
    <div class="prose">{spec}</div>
    <h2>Implementations</h2>
    {lang_tabs(groups)}
    <div class="pager">{prev_link}{next_link}</div>
"""
        crumbs = f'<a href="{rel_root}/index.html">Home</a> / <a href="{rel_root}/index.html#problems">Problems</a> / {html.escape(title)}'
        (out_dir / f"{slug}.html").write_text(page_shell(title, rel_root, crumbs, body), encoding="utf-8")
        made.append((slug, title))
        print("problem", slug)
    return made


def write_oop_pages() -> None:
    out_dir = PAGES / "oop"
    out_dir.mkdir(parents=True, exist_ok=True)
    lang_dirs = [
        ("java", "Java", "java"),
        ("cpp", "C++", "cpp"),
        ("python", "Python", "python"),
        ("csharp", "C#", "csharp"),
        ("go", "Go", "golang"),
        ("rust", "Rust", "rust"),
    ]
    for slug, title, folder, rust_folder in OOP:
        rel_root = "../.."
        groups = []
        for lid, label, dirname in lang_dirs:
            use = rust_folder if (lid == "rust" and rust_folder) else folder
            if lid == "rust" and not rust_folder:
                continue
            d = ROOT / "oop" / dirname / use
            files = collect_files(d)
            readme = find_readme(d)
            if not files and not readme:
                continue
            groups.append((lid, label, files_html(files, readme, rel_root)))
        body = f"""
    <span class="badge">OOP</span>
    <h1>{html.escape(title)}</h1>
    <p class="lede">Explanations and language samples from the repository <code>oop/</code> folder.</p>
    {lang_tabs(groups)}
    <p style="margin-top:28px"><a class="btn-primary" href="{rel_root}/index.html#oop">Back to index</a></p>
"""
        crumbs = f'<a href="{rel_root}/index.html">Home</a> / <a href="{rel_root}/index.html#oop">OOP</a> / {html.escape(title)}'
        (out_dir / f"{slug}.html").write_text(page_shell(title, rel_root, crumbs, body), encoding="utf-8")
        print("oop", slug)


def write_pattern_pages() -> None:
    out_dir = PAGES / "patterns"
    out_dir.mkdir(parents=True, exist_ok=True)
    only_java_py_js = {"abstractfactory", "command", "visitor"}
    for slug, title, kind, folder, js_path in PATTERNS:
        rel_root = "../.."
        groups = []
        mapping = [
            ("java", "Java", ROOT / "design-patterns/java" / folder),
            ("python", "Python", ROOT / "design-patterns/python" / folder),
        ]
        if folder not in only_java_py_js:
            mapping += [
                ("cpp", "C++", ROOT / "design-patterns/cpp" / folder),
                ("csharp", "C#", ROOT / "design-patterns/csharp" / folder),
                ("go", "Go", ROOT / "design-patterns/golang" / folder),
            ]
        mapping.append(("js", "JavaScript", ROOT / "design-patterns/Javascript" / js_path))
        for lid, label, d in mapping:
            files = collect_files(d)
            readme = find_readme(d)
            if not files and not readme:
                continue
            groups.append((lid, label, files_html(files, readme, rel_root)))
        body = f"""
    <span class="badge">{html.escape(kind)} Pattern</span>
    <h1>{html.escape(title)}</h1>
    <p class="lede">Implementations from <code>design-patterns/</code> in this repository.</p>
    {lang_tabs(groups)}
    <p style="margin-top:28px"><a class="btn-primary" href="{rel_root}/index.html#patterns">Back to index</a></p>
"""
        crumbs = f'<a href="{rel_root}/index.html">Home</a> / <a href="{rel_root}/index.html#patterns">Patterns</a> / {html.escape(title)}'
        (out_dir / f"{slug}.html").write_text(page_shell(title, rel_root, crumbs, body), encoding="utf-8")
        print("pattern", slug)


def write_language_pages(problems: list[tuple[str, str]]) -> None:
    out_dir = PAGES / "languages"
    out_dir.mkdir(parents=True, exist_ok=True)
    rel_root = "../.."
    hubs = {
        "java": ("Java", "java"),
        "python": ("Python", "python"),
        "cpp": ("C++", "cpp"),
        "csharp": ("C#", "csharp"),
        "go": ("Go", "go"),
        "ts": ("TypeScript", "ts"),
        "js": ("JavaScript", "js"),
        "rust": ("Rust", "rust"),
    }
    for slug, (label, tab) in hubs.items():
        prob_links = []
        for pslug, title in problems:
            # only include if that problem page exists; language tab may still be missing
            prob_links.append(f'<a href="../problems/{pslug}.html#{tab}">{html.escape(title)}</a>')
        pat_links = [f'<a href="../patterns/{s}.html#{tab}">{html.escape(t)}</a>' for s, t, *_ in PATTERNS]
        oop_links = [f'<a href="../oop/{s}.html#{slug if slug != "go" else "go"}">{html.escape(t)}</a>' for s, t, *_ in OOP]
        body = f"""
    <span class="badge">Language</span>
    <h1>{html.escape(label)} implementations</h1>
    <p class="lede">Every generated page that includes {html.escape(label)} samples from this repository.</p>
    <h2>LLD problems</h2>
    <div class="grid">{"".join(prob_links)}</div>
    <h2>Design patterns</h2>
    <div class="grid">{"".join(pat_links)}</div>
    <h2>OOP</h2>
    <div class="grid">{"".join(oop_links)}</div>
"""
        crumbs = f'<a href="{rel_root}/index.html">Home</a> / <a href="{rel_root}/index.html#languages">Languages</a> / {html.escape(label)}'
        (out_dir / f"{slug}.html").write_text(page_shell(f"{label} implementations", rel_root, crumbs, body), encoding="utf-8")
        print("lang", slug)


def write_interview_page(problems: list[tuple[str, str]]) -> None:
    rel_root = ".."
    links = "".join(f'<a href="problems/{s}.html">{html.escape(t)}</a>' for s, t in problems)
    body = f"""
    <span class="badge">Interview</span>
    <h1>Interview preparation</h1>
    <p class="lede">The repository interview template, cheat sheets, and every LLD problem you can practice locally on GitHub Pages.</p>
    <figure class="diagram">
      <img src="{rel_root}/images/interview-template.png" alt="How to answer an LLD interview problem" />
    </figure>
    <div class="prose">
      <h2>How to answer</h2>
      <ol>
        <li><strong>Clarify requirements</strong> — actors, constraints, and success cases.</li>
        <li><strong>Identify entities</strong> — classes, enums, and relationships.</li>
        <li><strong>Class design</strong> — fields, methods, and patterns.</li>
        <li><strong>Implementation</strong> — write the core flows.</li>
        <li><strong>Exception handling</strong> — concurrency, invalid input, edge cases.</li>
      </ol>
      <h2>SOLID at a glance</h2>
      <ul>
        <li><strong>SRP</strong> — one reason to change.</li>
        <li><strong>OCP</strong> — open for extension, closed for modification.</li>
        <li><strong>LSP</strong> — subtypes must be substitutable.</li>
        <li><strong>ISP</strong> — no fat interfaces.</li>
        <li><strong>DIP</strong> — depend on abstractions.</li>
      </ul>
      <p>DRY · YAGNI · KISS — don't repeat yourself, don't build unused features, keep the design simple.</p>
    </div>
    <h2>Practice problems in this repo</h2>
    <div class="grid">{links}</div>
"""
    crumbs = f'<a href="{rel_root}/index.html">Home</a> / Interview'
    (PAGES / "interview.html").write_text(page_shell("Interview preparation", rel_root, crumbs, body), encoding="utf-8")
    print("interview")


def main() -> None:
    PAGES.mkdir(parents=True, exist_ok=True)
    ASSETS.mkdir(parents=True, exist_ok=True)
    (ASSETS / "pygments.css").write_text(FMT.get_style_defs(".highlight"), encoding="utf-8")
    problems = write_problem_pages()
    write_oop_pages()
    write_pattern_pages()
    write_language_pages(problems)
    write_interview_page(problems)
    print("done", len(list(PAGES.rglob("*.html"))), "html pages")


if __name__ == "__main__":
    main()
