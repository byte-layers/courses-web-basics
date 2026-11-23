"""Scènes 2D (kit plan) du bit « Le DOM : la page vue par JavaScript » (courses-web-basics/dom).

Un arbre se lit mieux à plat : boîtes avec leur nom dedans, liens parent → enfant. Le schéma Mermaid de la première
section est remplacé par la scène « arbre », qui montre en plus ce que la page affichée et le fichier deviennent.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Dessin, une règle par sorte :
- un fichier (index.html, script.js) = un nœud jaune (y) ;
- un objet du DOM = un bloc programme pervenche (v), le nom de sa balise dedans ; liens du parent vers ses enfants ;
- la page affichée = un conteneur bleu (b) qui porte ce qu'elle montre ;
- ce que JavaScript ajoute ou trouve passe en vert (g).
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
    if size: d["size"] = list(size) + [1]
    if parent: d["in"] = parent
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


N = (4.2, 1.4)   # un objet du DOM
ents = [
    # ── étape 1 : l'arbre ; script.js à droite, au-dessus de la liste, pour que son lien ne traverse pas l'arbre
    ent("file", "node", (-10, -7.6), (5.8, 1.8), "y", title="index.html", sub="le fichier",
        detail="Le **fichier HTML** que tu as écrit. Le navigateur le lit une fois ; ensuite, il ne change plus."),
    ent("doc", "program", (0, -7.6), N, "v", title="document",
        detail="La racine de l'arbre : l'objet **`document`**, par lequel JavaScript entre dans le DOM."),
    ent("html", "program", (0, -5.4), N, "v", title="html"),
    ent("head", "program", (-4, -3.2), N, "v", title="head"),
    ent("body", "program", (4, -3.2), N, "v", title="body",
        detail="Un **objet** par élément, rangé dans son parent : `body` contient le titre et la liste."),
    ent("h1", "program", (1, -1.0), N, "v", title="h1"),
    ent("ul", "program", (7.5, -1.0), N, "v", title="ul#projets"),
    ent("li1", "program", (3.5, 1.2), N, "v", title="li"),
    ent("li2", "program", (8, 1.2), N, "v", title="li"),
    ent("li3", "program", (12.5, 1.2), N, "g", title="li"),
    ent("js", "node", (13, -3.6), (5.6, 1.8), "y", title="script.js",
        detail="Le script crée un `<li>` et l'insère dans la liste avec `append`."),
    ent("page", "layer", (2, 5.0), (25, 3.4), "b", title="page affichée"),
    ent("p-h1", "node", (-7.5, 0.5), (6, 1.5), "b", parent="page", title="Ada Lovelace"),
    ent("p-li1", "file", (-0.5, 0.5), (4.6, 1.2), "b", parent="page", title="• Portfolio"),
    ent("p-li2", "file", (4.5, 0.5), (4.6, 1.2), "b", parent="page", title="• Météo"),
    ent("p-li3", "file", (9.5, 0.5), (4.6, 1.2), "g", parent="page", title="• HTML"),
]
TREE1 = [L("doc", "html"), L("html", "head"), L("html", "body")]
TREE2 = [L("body", "h1"), L("body", "ul"), L("ul", "li1"), L("ul", "li2")]
steps = []
steps.append({
    "id": "arbre", "label": "L'arbre", "title": "Le HTML devient un arbre d'objets, le DOM",
    "body": ["Le navigateur construit un objet par élément, rangé dans son parent. Il dessine cet arbre ; JavaScript le modifie."],
    "hud": [{"label": "index.html", "value": "lu"}],
    "show": ["file", "doc"],
    "links": [],
    "script": [
        wait(900),
        scene(link=[L("file", "doc")], ms=500),
        send(["file", "doc"], kind="read", tone="y", label="lecture"),
        scene(say="En lisant le HTML, le navigateur construit un **arbre** : un objet par élément, rangé dans son parent.",
              show=["html", "head", "body"], link=TREE1, unlink=[L("file", "doc")]),
        wait(1200),
        scene(say="`body` contient un titre et une liste, la liste deux `li` : l'arbre suit l'imbrication des balises.",
              show=["h1", "ul", "li1", "li2"], link=TREE2),
        wait(1400),
        scene(say="C'est cet arbre, le **DOM**, que le navigateur dessine à l'écran.",
              show=["page", "p-h1", "p-li1", "p-li2"]),
        wait(1500),
        scene(show=["js"], link=[L("js", "ul")], ms=500),
        send(["js", "ul"], tone="g", label="append(li)"),
        scene(say="JavaScript ajoute un `li` : il l'ajoute à l'**arbre**, dans la liste.", show=["li3"], link=[L("ul", "li3")]),
        wait(900),
        scene(say="La page affichée le montre aussitôt ; le fichier `index.html`, lui, n'a pas changé.",
              show=["p-li3"], hud=[hud("index.html", "inchangé", None), hud("DOM", "3 li", "g")]),
        wait(2600),
    ],
})

# ── étape 2 : querySelector ou querySelectorAll
A = (5.4, 1.5)
ents += [
    ent("js2", "node", (-15, -7), (8.2, 2.0), "y", title="script.js"),
    ent("body2", "program", (0, -7), N, "v", title="body"),
    ent("h1b", "program", (-10, -2), A, "v", title="h1"),
    ent("a1", "program", (-3.5, -2), A, "v", title="article.projet"),
    ent("a2", "program", (3, -2), A, "v", title="article.projet"),
    ent("a3", "program", (9.5, -2), A, "v", title="article.projet"),
    ent("nl", "layer", (3, 4.2), (21, 4.0), "g", title="NodeList", sub="length : 3",
        detail="Une **NodeList** : un `length`, des index, `for…of` la parcourt. C'est une liste, pas un élément : pas de `classList`."),
    ent("r0", "file", (-6.5, 0.6), (5.4, 1.3), "g", parent="nl", title="[0]"),
    ent("r1", "file", (0, 0.6), (5.4, 1.3), "g", parent="nl", title="[1]"),
    ent("r2", "file", (6.5, 0.6), (5.4, 1.3), "g", parent="nl", title="[2]"),
]
T2 = [L("js2", "body2"), L("body2", "h1b"), L("body2", "a1"), L("body2", "a2"), L("body2", "a3")]
ARTS = ["a1", "a2", "a3"]
steps.append({
    "id": "chercher", "label": "Chercher", "title": "querySelector rend le premier, querySelectorAll les rend tous",
    "body": ["Les deux méthodes cherchent avec un sélecteur CSS ; l'une s'arrête au premier élément trouvé, l'autre les prend tous."],
    "hud": [{"label": "rend", "value": "—"}],
    "show": ["js2", "body2", "h1b", "a1", "a2", "a3"],
    "links": T2,
    "script": [
        wait(800),
        scene(set=[{"id": "js2", "label": "querySelector(\".projet\")"}], ms=400),
        send(["js2", "body2", "a1"], tone="g", label=".projet"),
        scene(say="`querySelector(\".projet\")` parcourt l'arbre et s'arrête au **premier** élément qui correspond.",
              set=[{"id": "a1", "tone": "g"}], hud=[hud("rend", "1 élément", "g")]),
        wait(1200),
        scene(say="Il rend cet élément seul, pas une liste : un élément n'a pas de `length`.",
              set=[{"id": "a2", "dim": True}, {"id": "a3", "dim": True}]),
        wait(1600),
        scene(say="Même sélecteur, avec `querySelectorAll`.",
              set=[{"id": "js2", "label": "querySelectorAll(\".projet\")"}, {"id": "a1", "tone": "v"},
                   {"id": "a2", "dim": False}, {"id": "a3", "dim": False}], hud=[hud("rend", "—", None)]),
        send(["js2", "body2", "a1"], tone="g"),
        send(["body2", "a2"], tone="g"),
        send(["body2", "a3"], tone="g"),
        scene(say="Il parcourt tout l'arbre et rend **tous** les éléments trouvés, dans une `NodeList`.",
              set=[{"id": a, "tone": "g"} for a in ARTS], show=["nl", "r0", "r1", "r2"],
              link=[L("a1", "r0", dashed=True), L("a2", "r1", dashed=True), L("a3", "r2", dashed=True)],
              hud=[hud("rend", "une NodeList", "g")]),
        wait(1500),
        scene(say="Une `NodeList` a un `length` et des index, et `for…of` la parcourt ; mais c'est une liste, pas un élément : pas de `classList`.",
              hud=[hud("length", 3, "g")]),
        wait(2600),
    ],
})

# ── étape 3 : créer et insérer
ents += [
    ent("js3", "node", (-14, -6), (7, 2.0), "y", title="script.js"),
    ent("ul3", "program", (2, -6), N, "v", title="ul#competences"),
    ent("old", "program", (-1.5, -2), N, "v", title="li : HTML"),
    ent("neu", "program", (-14, -1.4), N, "g", title="li", label="hors de la page",
        detail="`document.createElement(\"li\")` fabrique un élément : il existe, mais il n'est dans aucun parent."),
    ent("page3", "layer", (4, 4.6), (24, 4.4), "b", title="page affichée"),
    ent("p-old", "file", (-6.5, 0.6), (6, 1.3), "b", parent="page3", title="• HTML"),
    ent("p-neu", "file", (0.5, 0.6), (6, 1.3), "g", parent="page3", title="• CSS"),
    ent("neu2", "program", (12.5, -2), N, "g", title="li : JavaScript"),
    ent("p-neu2", "file", (7.5, 0.6), (6, 1.3), "g", parent="page3", title="• JavaScript"),
]
steps.append({
    "id": "inserer", "label": "Créer, insérer", "title": "Fabriquer un élément, puis l'insérer",
    "body": ["`createElement` fabrique un élément hors de la page ; il n'apparaît qu'une fois inséré avec `append`."],
    "hud": [{"label": "dans la page", "value": "—"}],
    "show": ["js3", "ul3", "old", "page3", "p-old"],
    "links": [L("js3", "ul3", dashed=True), L("ul3", "old")],
    "script": [
        wait(800),
        scene(say="`createElement(\"li\")` fabrique un `li` : il existe, mais **hors de la page**.",
              show=["neu"], link=[L("js3", "neu")], hud=[hud("dans la page", "non", "r")]),
        wait(1300),
        send(["js3", "neu"], tone="g", label="textContent"),
        scene(say="`textContent` le remplit. Toujours rien à l'écran : il n'est dans aucun parent.",
              set=[{"id": "neu", "title": "li : CSS"}]),
        wait(1300),
        scene(say="`append` l'insère à la fin de la liste : il entre dans l'arbre, et la page affichée le montre.",
              set=[{"id": "neu", "at": [5.5, -2], "label": None}], unlink=[L("js3", "neu")], link=[L("ul3", "neu"), L("js3", "ul3")],
              show=["p-neu"], hud=[hud("dans la page", "oui", "g")], ms=1100),
        wait(1500),
        send(["js3", "ul3"], tone="g", label="append(li)"),
        scene(say="Dans une boucle, les trois gestes se répètent : un **nouvel** élément à chaque tour.",
              show=["neu2", "p-neu2"], link=[L("ul3", "neu2")]),
        wait(2600),
    ],
})

# ── étape 4 : changer un élément, le code à gauche, la page à droite
XC = -9
ents += [
    ent("k1", "node", (XC, -4.5), (14, 1.7), "y", title='titre.textContent = "Bonjour !"',
        detail="`textContent` **remplace** le texte de l'élément."),
    ent("k2", "node", (XC, -2.0), (14, 1.7), "y", title='carte.classList.add("en-avant")',
        detail="`classList.add` **pose** une classe ; la couleur, elle, est écrite dans le CSS."),
    ent("k3", "node", (XC, 0.5), (14, 1.7), "y", title='carte.classList.toggle("en-avant")',
        detail="`classList.toggle` pose la classe si elle manque, la **retire** si elle y est."),
    ent("css", "node", (XC, 5.0), (14, 2.2), "y", title=".en-avant : fond jaune clair", sub="style.css",
        detail="La règle CSS de la classe `en-avant` : la couleur reste ici, en un seul endroit."),
    ent("page4", "layer", (9, 0), (14, 13), "b", title="page affichée"),
    ent("q-h1", "node", (0, -3.6), (10.5, 2.2), "b", parent="page4", title="Mes projets", sub="h1"),
    ent("q-card", "node", (0, 1.4), (10.5, 3.0), "b", parent="page4", title="Portfolio", sub='class="projet"'),
]
steps.append({
    "id": "changer", "label": "Changer", "title": "textContent change le texte, classList la classe",
    "body": ["Le code à gauche, la page à droite : chaque ligne change un élément déjà trouvé."],
    "hud": [{"label": "carte", "value": "projet"}],
    "show": ["k1", "k2", "k3", "css", "page4", "q-h1", "q-card"],
    "links": [],
    "script": [
        wait(900),
        scene(link=[L("k1", "q-h1")], ms=400),
        send(["k1", "q-h1"], tone="g", label="textContent"),
        scene(say="`textContent` **remplace** le texte du titre : la page affiche aussitôt le nouveau.",
              set=[{"id": "q-h1", "title": "Bonjour !", "tone": "g"}]),
        wait(1400),
        scene(link=[L("k2", "q-card")], unlink=[L("k1", "q-h1")], ms=400),
        send(["k2", "q-card"], tone="g", label="add"),
        scene(say="`classList.add` **pose** la classe `en-avant` sur la carte. Le code n'écrit aucune couleur.",
              set=[{"id": "q-card", "sub": 'class="projet en-avant"'}], hud=[hud("carte", "projet en-avant", "g")]),
        wait(1100),
        scene(say="C'est la règle du CSS qui colore la carte, dès que la classe est là.",
              link=[L("css", "q-card", dashed=True)], set=[{"id": "q-card", "tone": "g"}]),
        wait(1500),
        scene(link=[L("k3", "q-card")], unlink=[L("k2", "q-card")], ms=400),
        send(["k3", "q-card"], tone="r", label="toggle"),
        scene(say="`classList.toggle` **retire** la classe, puisqu'elle y est : la carte retrouve son fond, sans couleur à effacer.",
              set=[{"id": "q-card", "sub": 'class="projet"', "tone": "b"}], unlink=[L("css", "q-card")],
              hud=[hud("carte", "projet", None)]),
        wait(1500),
        send(["k3", "q-card"], tone="g", label="toggle"),
        scene(say="Un second `toggle` la repose : un même geste allume et éteint.",
              set=[{"id": "q-card", "sub": 'class="projet en-avant"', "tone": "g"}], link=[L("css", "q-card", dashed=True)],
              hud=[hud("carte", "projet en-avant", "g")]),
        wait(2600),
    ],
})

lesson = {
    "format": "bl-scenes/0.3", "id": "dom-plan", "title": "Le DOM (2D)", "lang": "fr", "kit": "plan",
    "legend": [{"tone": "y", "label": "fichier"}, {"tone": "v", "label": "objet du DOM"}, {"tone": "b", "label": "page affichée"},
               {"tone": "g", "label": "ajouté, trouvé"}],
    "entities": ents,
    # ordre du bit : arbre, chercher, changer, inserer
    "steps": sorted(steps, key=lambda st: ["arbre", "chercher", "changer", "inserer"].index(st["id"])),
}
write(lesson, *outputs(HERE, "dom.scene.json", "js-dom"))
