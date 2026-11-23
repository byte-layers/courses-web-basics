"""Scènes 2D (kit plan) du bit « Le HTML sémantique » (courses-web-basics/semantic-html).

Quatre étapes, une idée chacune, toutes sur le site d'un même club de randonnée :
- zones : remplacer les div par des balises sémantiques ne change rien à l'écran, mais donne au lecteur d'écran un
  plan de zones où sauter directement ;
- balises : la page d'un récit se range dans les sept balises qui nomment ses zones (header, nav, main, article,
  section, aside, footer), une à une ;
- article : le test de la publication (le récit copié seul garde son sens, une de ses parties non) ; le div qui
  ne sert qu'à la mise en page reste un div ;
- plan : les titres forment un plan ; choisis pour leur taille, ils donnent un plan faux.

Dessin : la page à gauche (un conteneur qui porte ses blocs), ce qu'en tire le navigateur ou ce qu'on en fait à
droite. Une zone qui en contient d'autres est un layer, une zone sans enfant dessiné est un node. Le lecteur
d'écran est un acteur, à droite.
Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Couleurs : n une boîte sans signification (div) ; g une balise qui dit ce qu'est son bloc, un titre à sa place ;
r un titre mal placé dans le plan, un bloc qui perd son sens ; v ce que le navigateur en tire, l'e-mail.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import L, scene, send, wait, write


def ent(id, kind, at, size=None, tone=None, parent=None, **kw):
    d = {"id": id, "kind": kind, "at": list(at)}
    if tone: d["tone"] = tone
    if size: d["size"] = list(size) + [1]
    if parent: d["in"] = parent
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


# ---------- 1. des zones
XP, XT = -7, 8
BOX = (11, 2.2)
ents = [
    ent("page", "layer", (XP, 0), (13, 17), "n", title="la page"),
    ent("z-head", "node", (0, -5.2), BOX, "n", parent="page", title="div", sub="Les Marcheurs du Dimanche"),
    ent("z-nav", "node", (0, -2.2), BOX, "n", parent="page", title="div", sub="Accueil · Sorties · Nous rejoindre"),
    ent("z-main", "node", (0, 1.6), (11, 4.2), "n", parent="page", title="div", sub="Nos derniers récits"),
    ent("z-foot", "node", (0, 5.6), BOX, "n", parent="page", title="div", sub="© 2026"),
    ent("tree", "layer", (XT, 0), (10, 17), "v", title="arbre d'accessibilité", sub="ce que lit un lecteur d'écran",
        detail="Le navigateur tire de la page un **arbre d'accessibilité** : les zones et les titres, que les lecteurs d'écran annoncent et où ils permettent de sauter."),
    ent("t-banner", "node", (0, -5.2), (8, 1.8), "v", parent="tree", title="bannière", sub="banner"),
    ent("t-nav", "node", (0, -2.2), (8, 1.8), "v", parent="tree", title="navigation"),
    ent("t-main", "node", (0, 1.6), (8, 1.8), "v", parent="tree", title="principal", sub="main"),
    ent("t-foot", "node", (0, 5.6), (8, 1.8), "v", parent="tree", title="pied de page", sub="contentinfo"),
    ent("reader", "actor", (17, 1.6), label="lecteur d'écran",
        detail="Un **lecteur d'écran** lit la page à voix haute. Il propose de sauter de zone en zone, ou de titre en titre."),
]
zones = {
    "id": "zones", "label": "Des zones", "title": "Le même écran, un plan en plus",
    "body": ["Une page en div s'affiche très bien, mais elle ne dit pas ce qu'est chaque bloc. Les balises sémantiques le disent, sans rien changer à l'écran."],
    "show": ["page", "z-head", "z-nav", "z-main", "z-foot", "tree", "reader"],
    "links": [],
    "script": [
        wait(1000),
        scene(set=[{"id": "tree", "label": "aucune zone"}],
              say="Une page faite de div s'affiche très bien, mais le navigateur n'y trouve aucune zone à annoncer."),
        wait(1500),
        scene(set=[{"id": "z-head", "title": "header", "tone": "g"}, {"id": "tree", "label": None}], show=["t-banner"],
              link=[L("z-head", "t-banner")],
              say="Le premier div devient un `<header>` : le navigateur annonce une bannière."),
        wait(1300),
        scene(set=[{"id": "z-nav", "title": "nav", "tone": "g"}, {"id": "z-main", "title": "main", "tone": "g"},
                   {"id": "z-foot", "title": "footer", "tone": "g"}],
              show=["t-nav", "t-main", "t-foot"],
              link=[L("z-nav", "t-nav"), L("z-main", "t-main"), L("z-foot", "t-foot")],
              say="Avec `<nav>`, `<main>` et `<footer>`, chaque bloc dit ce qu'il est : la page a un plan."),
        wait(1500),
        scene(set=[{"id": "page", "label": "rien n'a bougé à l'écran"}],
              say="À l'écran, pas un pixel n'a bougé : ces balises ajoutent du sens, pas d'apparence."),
        wait(1500),
        scene(link=[L("reader", "t-main")]),
        # pas d'explain ici : en kit plan, un explain sur un trajet dont les entités sont posées dans un parent (in)
        # fait planter le moteur (« Cannot read properties of undefined (reading 'size') »), voir le rapport.
        send(["reader", "t-main", "z-main"], label="aller au contenu"),
        scene(set=[{"id": "z-main", "label": "on y arrive directement"}],
              say="Le lecteur d'écran propose la liste des zones : un choix, et la personne arrive au contenu, sans tout écouter."),
        wait(2400),
    ],
}

# ---------- 2. les sept balises, sur la page d'un récit
P = (0, 0)
ents += [
    ent("b-page", "layer", P, (25, 22), "n", title="la page d'un récit"),
    ent("b-header", "layer", (0, -6.4), (23, 4.2), "g", parent="b-page", title="<header>", sub="en-tête"),
    ent("b-nav", "node", (0, 0.8), (19, 1.6), "g", parent="b-header", title="<nav>", sub="navigation : le menu"),
    ent("b-main", "layer", (-3.6, 1.8), (15.4, 10.4), "g", parent="b-page", title="<main>", sub="principal"),
    ent("b-article", "layer", (0, 0.9), (13.4, 7.2), "g", parent="b-main", title="<article>",
        sub="Boucle des trois lacs"),
    ent("b-sec1", "node", (0, -0.4), (11.4, 1.8), "g", parent="b-article", title="<section>", sub="Le parcours"),
    ent("b-sec2", "node", (0, 2), (11.4, 1.8), "g", parent="b-article", title="<section>", sub="Infos pratiques"),
    ent("b-aside", "node", (8.4, 1.8), (5.4, 4.4), "g", parent="b-page", title="<aside>", sub="à côté du sujet"),
    ent("b-footer", "node", (0, 8.4), (23, 1.8), "g", parent="b-page", title="<footer>", sub="pied de page"),
]
balises = {
    "id": "balises", "label": "Sept balises", "title": "Sept balises pour nommer les zones",
    "body": ["La page d'un récit du club, rangée zone par zone. Chaque balise dit ce qu'est son bloc."],
    "show": ["b-page"],
    "links": [],
    "script": [
        wait(900),
        scene(show=["b-header"], say="`<header>`, l'**en-tête** : le nom du site, en haut de la page."),
        wait(1100),
        scene(show=["b-nav"], say="`<nav>` : le **menu**, un groupe de liens pour naviguer dans le site."),
        wait(1100),
        scene(show=[{"id": "b-main", "label": "un seul par page"}],
              say="`<main>` : le **contenu principal**. Il n'y en a qu'un par page."),
        wait(1200),
        scene(show=["b-article"], set=[{"id": "b-main", "label": None}],
              say="`<article>` : un contenu **complet**, ici le récit d'une sortie."),
        wait(1100),
        scene(show=["b-sec1", "b-sec2"], say="`<section>` : une **partie** du récit, avec son titre."),
        wait(1100),
        scene(show=["b-aside"], say="`<aside>` : un encadré **à côté** du sujet, des liens vers d'autres récits."),
        wait(1100),
        scene(show=["b-footer"], say="`<footer>`, le **pied de page** : le contact, les mentions."),
        wait(2600),
    ],
}

# ---------- 3. article ou section, et le div de mise en page
ents += [
    ent("a-article", "layer", (-8, 0), (15, 13), "g", title="<article>", sub="Boucle des trois lacs"),
    ent("a-div", "layer", (0, 1.4), (13, 7.6), "n", parent="a-article", title="<div>"),
    ent("a-sec1", "node", (-3.1, 0.9), (5.6, 3.6), "g", parent="a-div", title="<section>", sub="Le parcours"),
    ent("a-sec2", "node", (3.1, 0.9), (5.6, 3.6), "g", parent="a-div", title="<section>", sub="Infos pratiques"),
    ent("a-mail", "layer", (10, 0), (11, 13), "v", title="copié seul dans un e-mail"),
    ent("a-copy1", "node", (0, -2.2), (9, 2.6), "g", parent="a-mail", title="Boucle des trois lacs",
        sub="le parcours, les infos"),
    ent("a-copy2", "node", (0, 2.4), (9, 2.6), "r", parent="a-mail", title="Infos pratiques",
        sub="… de quelle sortie ?"),
]
article = {
    "id": "article", "label": "Article ou section", "title": "Le test de la publication",
    "body": ["Copié seul ailleurs, un bloc garde-t-il son sens ? Oui : `<article>`. Non : `<section>`."],
    "show": ["a-article", "a-div", "a-sec1", "a-sec2", "a-mail"],
    "links": [],
    "labels": "left",
    "script": [
        wait(1000),
        scene(link=[L("a-article", "a-mail")]),
        send(["a-article", "a-mail"], tone="g", label="copier"),
        scene(show=[{"id": "a-copy1", "label": "garde son sens"}],
              say="Le récit, copié seul dans un e-mail, se comprend en entier : c'est un `<article>`."),
        wait(1600),
        scene(link=[L("a-sec2", "a-mail")], unlink=[L("a-article", "a-mail")]),
        send(["a-sec2", "a-mail"], tone="r", label="copier"),
        scene(show=[{"id": "a-copy2", "label": "perd son sens"}],
              say="« Infos pratiques », copiée seule, ne dit plus de quelle sortie elle parle : c'est une `<section>` du récit."),
        wait(1800),
        scene(set=[{"id": "a-div", "label": "côte à côte, pour la mise en page"}],
              say="Le `<div>` ne fait que poser les deux parties côte à côte. Rien à annoncer : il reste un `<div>`."),
        wait(2600),
    ],
}

# ---------- 4. les titres forment un plan
ents += [
    ent("recipe", "layer", (-9, 0), (13, 13), "n", title="la page"),
    ent("h-site", "node", (0, -3.4), (11, 1.9), "g", parent="recipe", title="h1", sub="Les Marcheurs du Dimanche"),
    ent("h-part", "node", (0, -0.4), (11, 1.9), "r", parent="recipe", title="h1", sub="Nos derniers récits"),
    ent("h-recit", "node", (0, 2.6), (11, 1.9), "r", parent="recipe", title="h4", sub="Boucle des trois lacs"),
    ent("outline", "layer", (8.5, 0), (17, 13), "v", title="le plan de la page"),
    ent("o-site", "node", (-3.6, -3.4), (8.6, 1.9), "g", parent="outline", title="Les Marcheurs du Dimanche"),
    ent("o-part", "node", (-3.6, -0.4), (8.6, 1.9), "r", parent="outline", title="Nos derniers récits"),
    ent("o-recit", "node", (3.6, 2.6), (8.6, 1.9), "r", parent="outline", title="Boucle des trois lacs"),
]
plan = {
    "id": "plan", "label": "Un plan", "title": "Les titres forment un plan",
    "body": ["Un seul h1, le sujet ; des h2 pour ses parties, des h3 pour leurs sous-parties, sans sauter de niveau. La taille, elle, se règle en CSS."],
    "show": ["recipe", "h-site", "h-part", "h-recit", "outline"],
    "links": [],
    "script": [
        wait(1000),
        scene(show=["o-site", "o-part", "o-recit"],
              say="Choisis à l'œil, ces titres donnent un plan faux : deux sujets, puis un saut jusqu'au niveau 4."),
        wait(1700),
        scene(set=[{"id": "h-part", "title": "h2", "tone": "g"}, {"id": "o-part", "at": [-1.8, -0.4], "tone": "g"}],
              say="« Nos derniers récits » est une partie de la page : un `<h2>`, un cran sous le `<h1>`.", ms=900),
        wait(1300),
        scene(set=[{"id": "h-recit", "title": "h3", "tone": "g"}, {"id": "o-recit", "at": [0, 2.6], "tone": "g"}],
              say="Un récit est une sous-partie des récits : un `<h3>`, un cran plus bas, sans sauter de niveau.", ms=900),
        wait(1300),
        scene(set=[{"id": "outline", "label": "sans saut de niveau"}],
              say="Le lecteur d'écran suit ce plan de titre en titre. La taille du texte se règle en CSS."),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "semantic-html-plan", "title": "Le sens avant la forme (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "n", "label": "sans sens"}, {"tone": "g", "label": "à sa place"},
               {"tone": "r", "label": "mal placé"}, {"tone": "v", "label": "lu ailleurs"}],
    "entities": ents, "steps": [zones, balises, article, plan],
}
write(lesson, *outputs(HERE, "semantic.scene.json", "web-semantic"))
