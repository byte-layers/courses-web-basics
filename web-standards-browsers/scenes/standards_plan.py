"""Scènes 2D (kit plan) du bit « Les standards du web et les moteurs des navigateurs »
(courses-web-basics/web-standards-browsers).

Trois leçons, une idée chacune :
- standards (standards.scene.json) : un organisme écrit un texte public par langage, tous les navigateurs le lisent.
- moteurs (moteurs.scene.json) : le moteur de rendu lit HTML et CSS et dessine, le moteur JavaScript exécute le
  script ; trois familles. Reprise de l'étape `moteurs` de web-page-languages/scenes/langages_plan.py.
- histoire (histoire.scene.json) : une frise ; fin des années 1990, chaque navigateur ajoute ses balises et une page
  s'affiche différemment ; la rétrocompatibilité garde les vieilles pages (doctype : mode standard ou mode quirks) ;
  2019, un seul standard HTML ; depuis 2022, Interop.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Dessin (moteurs) : un fichier = une boîte « file » à gauche ; le navigateur est un conteneur layer qui porte ses deux
moteurs et la page. Couleurs : y HTML, r CSS, g JavaScript, v le navigateur, n l'apparence par défaut.
Dessin (histoire) : une période = une colonne (zone) qui porte son nom ; un navigateur ou une règle = un node.
Couleurs : n un navigateur, r ce qui est propre à un navigateur ou imite les anciens, g ce qui suit le standard commun.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import L, scene, send, wait, write, hud


def ent(id, kind, at, size=None, tone=None, parent=None, **kw):
    d = {"id": id, "kind": kind, "at": list(at)}
    if tone: d["tone"] = tone
    if size: d["size"] = list(size) + ([] if kind == "zone" else [1])
    if parent: d["in"] = parent
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


# ---------- 0. standards : qui écrit quoi, qui le lit
X_ORG, X_DOC, X_NAV = -14, -3.5, 11
ROWS = [-5, 0, 5]
ORG = (7.6, 2.8)
DOC = (8.4, 2.6)
s_ents = [
    ent("o-html", "node", (X_ORG, ROWS[0]), ORG, "n", title="WHATWG", sub="éditeurs de navigateurs",
        detail="Le **WHATWG** est un groupe fondé en 2004 par des éditeurs de navigateurs. Depuis 2019, le W3C reconnaît son texte comme **le seul standard HTML**."),
    ent("o-css", "node", (X_ORG, ROWS[1]), ORG, "n", title="W3C", sub="groupe de travail CSS",
        detail="Le **W3C** (*World Wide Web Consortium*) réunit éditeurs de navigateurs, entreprises et universités."),
    ent("o-js", "node", (X_ORG, ROWS[2]), ORG, "n", title="Ecma International", sub="comité TC39",
        detail="Le comité **TC39** d'Ecma International publie une nouvelle édition d'ECMAScript chaque année depuis 2015."),
    ent("d-html", "file", (X_DOC, ROWS[0]), DOC, "y", title="HTML Living Standard",
        detail="Mis à jour **en continu** : pas de version 5 ou 6, un seul texte vivant."),
    ent("d-css", "file", (X_DOC, ROWS[1]), DOC, "r", title="les modules CSS",
        detail="Le CSS est découpé en **modules** (couleurs, boîtes, polices…), chacun avec sa version."),
    ent("d-js", "file", (X_DOC, ROWS[2]), DOC, "g", title="ECMAScript",
        detail="Le standard de JavaScript s'appelle **ECMAScript** ; son texte porte le numéro ECMA-262."),
    ent("navs", "layer", (X_NAV, 0), (9, 15), "v", title="les navigateurs"),
    ent("n-chrome", "node", (0, -4.2), (6.4, 2.2), "v", parent="navs", title="Chrome, Edge"),
    ent("n-firefox", "node", (0, 0), (6.4, 2.2), "v", parent="navs", title="Firefox"),
    ent("n-safari", "node", (0, 4.2), (6.4, 2.2), "v", parent="navs", title="Safari"),
]

standards = {
    "id": "standards", "label": "Les standards", "title": "Un texte public par langage",
    "body": ["Trois organismes écrivent les standards ; tous les navigateurs les appliquent."],
    "hud": [{"label": "une même page", "value": "—"}],
    "show": ["o-html", "navs", "n-chrome", "n-firefox", "n-safari"],
    "links": [],
    "script": [
        wait(800),
        scene(show=["d-html"], link=[L("o-html", "d-html", label="écrit")],
              say="Le **WHATWG** écrit le standard du HTML, mis à jour en continu."),
        wait(1300),
        scene(show=["o-css", "d-css"], link=[L("o-css", "d-css", label="écrit")],
              say="Le **W3C** écrit celui du CSS, découpé en modules."),
        wait(1300),
        scene(show=["o-js", "d-js"], link=[L("o-js", "d-js", label="écrit")],
              say="**Ecma International** écrit celui de JavaScript : ECMAScript, une édition par an."),
        wait(1300),
        scene(link=[L("d-html", "navs"), L("d-css", "navs"), L("d-js", "navs")],
              say="Ces textes sont **publics** : chaque navigateur les lit et les applique."),
        send(["d-html", "navs"], tone="y", label="lu"),
        send(["d-js", "navs"], tone="g", label="lu"),
        scene(hud=[hud("une même page", "même sens partout", "g")],
              say="Une balise, une propriété, une instruction veulent donc dire la même chose dans tous les navigateurs."),
        wait(2600),
    ],
}

write({
    "format": "bl-scenes/0.3", "id": "web-standards-browsers-standards", "title": "Qui écrit les standards du web (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "n", "label": "un organisme"}, {"tone": "y", "label": "HTML"}, {"tone": "r", "label": "CSS"},
               {"tone": "g", "label": "JavaScript"}, {"tone": "v", "label": "les navigateurs"}],
    "entities": s_ents, "steps": [standards],
}, *outputs(HERE, "standards.scene.json", "std-standards"))


# ---------- 1. moteurs
X_FILE = -11
FILE = (6.4, 2.4)
m_ents = [
    ent("html", "file", (X_FILE, -5), FILE, "y", title="index.html",
        detail="Le **HTML** dit ce que la page contient : un titre, un paragraphe, un bouton."),
    ent("css", "file", (X_FILE, 0), FILE, "r", title="style.css",
        detail="Le **CSS** dit à quoi ressemble chaque élément : couleurs, tailles, polices, disposition."),
    ent("js", "file", (X_FILE, 5), FILE, "g", title="script.js",
        detail="Le **JavaScript** dit ce qui se passe quand on agit : un clic, une saisie, un défilement."),
    ent("nav", "layer", (6.5, 0), (17, 15.5), "v", title="navigateur", sub="Chrome, Edge"),
    ent("render", "node", (-4.3, -4.2), (7, 2.8), "v", parent="nav", title="moteur de rendu", sub="Blink",
        detail="Le **moteur de rendu** lit le HTML et le CSS, calcule la place de chaque élément et dessine la page."),
    ent("jse", "node", (-4.3, 4.2), (7, 2.8), "v", parent="nav", title="moteur JavaScript", sub="V8",
        detail="Le **moteur JavaScript** exécute les scripts. V8, celui de Chrome, est aussi celui de Node.js."),
    ent("view", "layer", (4.3, 0.8), (7.2, 12.4), "n", parent="nav", title="la page"),
    ent("v-h1", "node", (0, -2.2), (5.8, 1.8), "y", parent="view", title="Bonjour !"),
    ent("v-btn", "node", (0, 2.2), (5.8, 1.8), "r", parent="view", title="Clique-moi"),
]

moteurs = {
    "id": "moteurs", "label": "Les moteurs", "title": "Deux moteurs dans chaque navigateur",
    "body": ["Le moteur de rendu dessine la page à partir du HTML et du CSS ; le moteur JavaScript exécute les scripts."],
    "show": ["html", "css", "js", "nav", "render", "jse", "view"],
    "links": [L("html", "render"), L("css", "render"), L("js", "jse")],
    "script": [
        wait(900),
        send(["html", "render"], label="contenu"),
        send(["css", "render"], tone="r", label="apparence"),
        scene(show=["v-h1", "v-btn"], link=[L("render", "view")],
              say="Le moteur de rendu lit le HTML et le CSS, puis dessine la page."),
        wait(1300),
        send(["js", "jse"], tone="g", label="script"),
        scene(link=[L("jse", "v-h1")], set=[{"id": "v-h1", "title": "Merci !", "tone": "g"}],
              say="Le moteur JavaScript exécute le script, qui change la page déjà dessinée."),
        wait(1600),
        scene(set=[{"id": "nav", "sub": "Firefox"}, {"id": "render", "sub": "Gecko"}, {"id": "jse", "sub": "SpiderMonkey"}],
              say="Chaque famille de navigateurs a ses deux moteurs : Gecko et SpiderMonkey pour Firefox…"),
        wait(1600),
        scene(set=[{"id": "nav", "sub": "Safari"}, {"id": "render", "sub": "WebKit"}, {"id": "jse", "sub": "JavaScriptCore"}],
              say="…WebKit et JavaScriptCore pour Safari. Tous appliquent les mêmes standards."),
        wait(2600),
    ],
}

write({
    "format": "bl-scenes/0.3", "id": "web-standards-browsers-engines", "title": "Les moteurs d'un navigateur (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "y", "label": "HTML, contenu"}, {"tone": "r", "label": "CSS, apparence"},
               {"tone": "g", "label": "JS, comportement"}, {"tone": "v", "label": "le navigateur"}],
    "entities": m_ents, "steps": [moteurs],
}, *outputs(HERE, "moteurs.scene.json", "std-engines"))


# ---------- 2. histoire : une frise
COLS = [-14.4, -4.8, 4.8, 14.4]    # une colonne par période
COL = (9, 15)                       # taille d'une colonne
ROW = [-4.2, 0, 4.4]                # rangées dans une colonne
BOX = (8, 2.8)

h_ents = [
    ent("p1", "zone", (COLS[0], 0), COL, "n", label="fin des années 1990"),
    ent("p2", "zone", (COLS[1], 0), COL, "n", label="pour ne rien casser"),
    ent("p3", "zone", (COLS[2], 0), COL, "n", label="2019"),
    ent("p4", "zone", (COLS[3], 0), COL, "n", label="depuis 2022"),
    ent("netscape", "node", (COLS[0], ROW[0]), BOX, "n", title="Netscape Navigator", sub="ajoute <blink>", label="le texte clignote",
        detail="`<blink>` faisait **clignoter** un texte, dans Netscape seulement."),
    ent("ie", "node", (COLS[0], ROW[1]), BOX, "n", title="Internet Explorer", sub="ajoute <marquee>", label="le texte défile",
        detail="`<marquee>` faisait **défiler** un texte, dans Internet Explorer d'abord. Il est obsolète, mais le standard HTML demande encore aux navigateurs de l'afficher."),
    ent("badge", "node", (COLS[0], ROW[2]), BOX, "r", title="« optimisé pour IE »", sub="sur beaucoup de sites"),
    ent("quirks", "node", (COLS[1], ROW[0]), BOX, "r", title="sans doctype", sub="mode quirks",
        detail="Le **mode quirks** (« bizarreries ») imite les anciens navigateurs, pour que les vieilles pages s'affichent comme avant."),
    ent("doctype", "node", (COLS[1], ROW[1]), BOX, "g", title="<!DOCTYPE html>", sub="mode standard",
        detail="Avec cette première ligne, le navigateur applique les **standards actuels**."),
    ent("living", "node", (COLS[2], ROW[1]), BOX, "g", title="HTML Living Standard", sub="du WHATWG",
        detail="Depuis 2019, le W3C reconnaît le standard du WHATWG comme **le seul standard HTML**."),
    ent("w3c", "node", (COLS[2], ROW[0]), BOX, "n", title="W3C", sub="le reconnaît"),
    ent("interop", "node", (COLS[3], ROW[0]), BOX, "g", title="Interop", sub="un projet commun, chaque année",
        detail="Les éditeurs des trois moteurs choisissent ensemble, chaque année, des fonctions sur lesquelles **réduire leurs écarts**."),
    ent("engines", "node", (COLS[3], ROW[1]), BOX, "n", title="Blink · Gecko · WebKit", sub="réduisent leurs écarts"),
]

histoire = {
    "id": "histoire", "label": "L'histoire", "title": "Des balises maison aux standards communs",
    "body": ["Les navigateurs ont longtemps divergé ; ils ont convergé vers les standards sans casser les vieilles pages."],
    "hud": [{"label": "une même page", "value": "—"}, {"label": "standard HTML", "value": "—"}],
    "show": ["p1"],
    "links": [],
    "script": [
        wait(800),
        scene(show=["netscape"],
              say="Fin des années 1990 : Netscape ajoute sa propre balise, `<blink>`, qui fait clignoter un texte."),
        wait(1300),
        scene(show=["ie"],
              say="Internet Explorer a la sienne, `<marquee>`, qui le fait défiler. Chacun veut attirer les créateurs de sites."),
        wait(1300),
        scene(show=["badge"], link=[L("ie", "badge")], hud=[hud("une même page", "s'affiche différemment", "r")],
              say="Une même page s'affiche différemment selon le navigateur ; beaucoup de sites affichent « optimisé pour Internet Explorer »."),
        wait(1600),
        scene(show=["p2", "quirks"], link=[L("ie", "quirks", dashed=True, label="imité")],
              say="Les navigateurs convergent, sans casser les vieilles pages : **sans doctype**, une page passe en mode quirks, qui imite les anciens navigateurs."),
        wait(1500),
        scene(show=["doctype"], hud=[hud("une même page", "standards actuels", "g")],
              say="Avec `<!DOCTYPE html>` en première ligne, le navigateur applique **les standards actuels**."),
        wait(1500),
        scene(show=["p3", "living", "w3c"], link=[L("w3c", "living")], hud=[hud("standard HTML", "un seul", "g")],
              say="2019 : le W3C reconnaît le HTML Living Standard du WHATWG comme **le seul standard HTML**."),
        wait(1500),
        scene(show=["p4", "interop", "engines"], link=[L("interop", "engines")],
              hud=[hud("une même page", "écarts sur le récent", "g")],
              say="Depuis 2022, les éditeurs des trois moteurs mènent chaque année le projet **Interop** pour réduire les écarts qui restent."),
        wait(2800),
    ],
}

write({
    "format": "bl-scenes/0.3", "id": "web-standards-browsers-history", "title": "Navigateurs et standards, une histoire (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "n", "label": "un navigateur"}, {"tone": "r", "label": "maison, ancien"},
               {"tone": "g", "label": "standard commun"}],
    "entities": h_ents, "steps": [histoire],
}, *outputs(HERE, "histoire.scene.json", "std-history"))
