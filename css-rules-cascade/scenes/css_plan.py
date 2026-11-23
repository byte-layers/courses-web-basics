"""Scènes 2D (kit plan) du bit « CSS : règles, sélecteurs et cascade » (courses-web-basics/css-rules-cascade).

Cinq étapes, une idée chacune (css.scene.json) :
- regle : le sélecteur trouve tous les éléments qu'il vise, et ses déclarations s'appliquent à chacun ;
- ranger : une feuille reliée par plusieurs pages ; on change une couleur à un endroit, toutes les pages suivent ;
- selecteurs : une balise vise tous ses éléments, une classe tous ceux qui la portent, un id un seul ;
- cascade : deux règles se disputent un élément ; la plus spécifique gagne, quel que soit l'ordre ; l'ordre ne
  départage que des égales. Exemple volontairement différent de l'exercice « Qui gagne ? » (pas de solution donnée) ;
- heritage : la couleur posée sur body descend dans ses enfants, la bordure non ; une règle qui vise l'enfant
  passe avant ce qu'il hérite.

Dessin : la feuille de style à gauche (un conteneur, une boîte par règle, dans l'ordre où elles sont écrites), la page
à droite (un conteneur qui porte ses éléments). Un lien = « cette règle vise cet élément » ; pointillé quand elle perd.
Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Couleurs : une couleur = la couleur que la règle donne. b texte bleu, r texte rose, v fond pervenche, n gris (et
apparence par défaut).
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


XS, XP = -8.5, 8.5
EL = (10, 1.9)

# ---------- 1. une règle
ents = [
    ent("sheet", "layer", (XS, 0), (12, 14), "n", title="style.css"),
    ent("r-h2", "node", (0, -1.2), (10, 4.4), "b", parent="sheet", title="h2 { … }", sub="color: rgb(11, 107, 203);"),
    ent("page", "layer", (XP, 0), (12, 14), "n", title="la page"),
    ent("p-h1", "node", (0, -4.2), EL, "n", parent="page", title="h1", sub="Médiathèque"),
    ent("p-h2a", "node", (0, -1.6), EL, "n", parent="page", title="h2", sub="Bienvenue"),
    ent("p-p", "node", (0, 1.0), EL, "n", parent="page", title="p", sub="Plus de 40 000 ouvrages…"),
    ent("p-h2b", "node", (0, 3.6), EL, "n", parent="page", title="h2", sub="Nos nouveautés"),
]
regle = {
    "id": "regle", "label": "Une règle", "title": "Un sélecteur, des déclarations",
    "body": ["Le sélecteur dit quels éléments la règle vise ; ses déclarations s'appliquent à chacun d'eux."],
    "show": ["sheet", "r-h2", "page", "p-h1", "p-h2a", "p-p", "p-h2b"],
    "links": [],
    "script": [
        wait(1000),
        scene(link=[L("r-h2", "p-h2a"), L("r-h2", "p-h2b")], set=[{"id": "r-h2", "label": "vise tous les h2"}],
              say="Le sélecteur `h2` cherche dans la page tous les éléments `<h2>` : il en trouve deux."),
        wait(1300),
        send(["r-h2", "p-h2a"], tone="b", label="color"),
        scene(set=[{"id": "p-h2a", "tone": "b"}, {"id": "p-h2b", "tone": "b"}],
              say="La déclaration `color` s'applique à chacun : les deux titres deviennent bleus."),
        wait(1300),
        scene(set=[{"id": "p-h1", "label": "pas visé"}, {"id": "p-p", "label": "pas visé"}],
              say="Le `<h1>` et le paragraphe ne sont pas visés : ils gardent leur apparence."),
        wait(1300),
        scene(set=[{"id": "r-h2", "sub": "color: … ; text-align: center;"},
                   {"id": "p-h2a", "label": "bleu, centré"}, {"id": "p-h2b", "label": "bleu, centré"}],
              say="Une deuxième déclaration dans le même bloc, et les deux titres sont aussi centrés."),
        wait(2600),
    ],
}

# ---------- 1 bis. ranger : une feuille pour toutes les pages
ents += [
    ent("g-sheet", "layer", (0, -5), (12, 5.6), "n", title="style.css", sub="une seule feuille"),
    ent("g-rule", "node", (0, 0.7), (10, 2.6), "b", parent="g-sheet", title="h2 { … }", sub="color: bleu;"),
    ent("g-p1", "layer", (-12.5, 4.5), (11, 5), "n", title="index.html", sub="<link href=\"style.css\">"),
    ent("g-h1", "node", (0, 0.7), (9, 1.9), "n", parent="g-p1", title="h2", sub="Bienvenue"),
    ent("g-p2", "layer", (0, 4.5), (11, 5), "n", title="contact.html", sub="<link href=\"style.css\">"),
    ent("g-h2", "node", (0, 0.7), (9, 1.9), "n", parent="g-p2", title="h2", sub="Nous écrire"),
    ent("g-p3", "layer", (12.5, 4.5), (11, 5), "n", title="tarifs.html", sub="<link href=\"style.css\">"),
    ent("g-h3", "node", (0, 0.7), (9, 1.9), "b", parent="g-p3", title="h2", sub="Nos tarifs"),
]
ranger = {
    "id": "ranger", "label": "Une feuille", "title": "Une feuille de style, toutes les pages",
    "body": ["Chaque page relie la même feuille par `<link>` : ses règles s'appliquent partout."],
    "hud": [{"label": "à modifier", "value": "—"}],
    "show": ["g-sheet", "g-rule", "g-p1", "g-h1", "g-p2", "g-h2"],
    "links": [],
    "script": [
        wait(1000),
        scene(link=[L("g-rule", "g-h1"), L("g-rule", "g-h2")],
              set=[{"id": "g-h1", "tone": "b"}, {"id": "g-h2", "tone": "b"}],
              say="Deux pages relient la même feuille par `<link>` : leurs titres `<h2>` sont bleus."),
        wait(1300),
        scene(show=["g-p3", "g-h3"], link=[L("g-rule", "g-h3")],
              say="Une troisième page la relie à son tour : elle est habillée pareil, sans rien réécrire."),
        wait(1400),
        scene(set=[{"id": "g-rule", "tone": "r", "sub": "color: rose;", "label": "modifiée ici"},
                   {"id": "g-h1", "tone": "r"}, {"id": "g-h2", "tone": "r"}, {"id": "g-h3", "tone": "r"}],
              hud=[hud("à modifier", "un seul : style.css", "r")],
              say="On change la couleur **une fois**, dans `style.css` : les trois pages changent."),
        wait(2800),
    ],
}

# ---------- 1 ter. selecteurs : balise, classe, id
ents += [
    ent("v-sheet", "layer", (-14.5, 0), (11.5, 12.5), "n", title="style.css"),
    ent("v-tag", "node", (0, -2.8), (10, 2.4), "b", parent="v-sheet", title="h2 { … }", sub="color: bleu;"),
    ent("v-cls", "node", (0, 0.6), (10, 2.4), "r", parent="v-sheet", title=".intro { … }", sub="color: rose;"),
    ent("v-id", "node", (0, 4.0), (10, 2.4), "v", parent="v-sheet", title="#presentation { … }", sub="background: pervenche;"),
    ent("v-page", "layer", (6.5, 0), (26, 12.5), "n", title="la page"),
    ent("v-s1", "layer", (-6.3, 0.9), (12, 9.6), "n", parent="v-page", title="section id=\"presentation\""),
    ent("v-h2a", "node", (0, -1.6), (10.5, 1.8), "n", parent="v-s1", title="h2", sub="Bienvenue"),
    ent("v-pa", "node", (0, 0.7), (10.5, 1.8), "n", parent="v-s1", title="p class=\"intro\""),
    ent("v-p", "node", (0, 3.0), (10.5, 1.8), "n", parent="v-s1", title="p"),
    ent("v-s2", "layer", (6.3, 0.9), (12, 9.6), "n", parent="v-page", title="section id=\"nouveautes\""),
    ent("v-h2b", "node", (0, -1.6), (10.5, 1.8), "n", parent="v-s2", title="h2", sub="Nos nouveautés"),
    ent("v-pb", "node", (0, 0.7), (10.5, 1.8), "n", parent="v-s2", title="p class=\"intro\""),
]
selecteurs = {
    "id": "selecteurs", "label": "Les sélecteurs", "title": "Une balise, une classe, un id",
    "body": ["Le sélecteur choisit les éléments visés : tous ceux d'une balise, tous ceux d'une classe, ou un seul, par son id."],
    "show": ["v-sheet", "v-tag", "v-cls", "v-id", "v-page", "v-s1", "v-h2a", "v-pa", "v-p", "v-s2", "v-h2b", "v-pb"],
    "links": [],
    "script": [
        wait(1000),
        scene(link=[L("v-tag", "v-h2a"), L("v-tag", "v-h2b")],
              set=[{"id": "v-h2a", "tone": "b"}, {"id": "v-h2b", "tone": "b"}],
              say="`h2`, une **balise** : la règle vise tous les `<h2>`, un dans chaque section."),
        wait(1400),
        scene(link=[L("v-cls", "v-pa"), L("v-cls", "v-pb")],
              set=[{"id": "v-pa", "tone": "r"}, {"id": "v-pb", "tone": "r"}],
              say="`.intro`, avec un point, une **classe** : tous les éléments qui portent `class=\"intro\"`, où qu'ils soient."),
        wait(1500),
        scene(link=[L("v-id", "v-s1")], set=[{"id": "v-s1", "tone": "v"}],
              say="`#presentation`, avec un dièse, un **id** : le seul élément qui porte `id=\"presentation\"`."),
        wait(1400),
        scene(set=[{"id": "v-p", "label": "pas visé"}, {"id": "v-s2", "label": "pas visée"}],
              say="Le paragraphe sans classe et l'autre section ne sont visés par aucune règle : ils gardent leur apparence."),
        wait(2800),
    ],
}

# ---------- 2. la cascade
ents += [
    ent("sheet2", "layer", (XS, 0), (12, 15), "n", title="style.css", sub="lue de haut en bas"),
    ent("c-prix", "node", (0, -3.6), (10, 2.4), "r", parent="sheet2", title=".prix", sub="color: rose;"),
    ent("c-art", "node", (0, -0.2), (10, 2.4), "n", parent="sheet2", title="article p", sub="color: gris;"),
    ent("c-id", "node", (0, 3.2), (10, 2.4), "b", parent="sheet2", title="#offre p", sub="color: bleu;"),
    ent("page2", "layer", (XP, 0), (12, 15), "n", title='article id="offre"'),
    ent("el-title", "node", (0, -2.2), EL, "n", parent="page2", title="h2", sub="Carte annuelle"),
    ent("el-prix", "node", (0, 1.2), EL, "n", parent="page2", title='p class="prix"', sub="12 €"),
]
cascade = {
    "id": "cascade", "label": "Qui gagne ?", "title": "La règle la plus spécifique gagne",
    "body": ["Quand deux règles donnent deux valeurs à la même propriété, le navigateur compare leur spécificité ; l'ordre ne départage que des égales."],
    "hud": [{"label": ".prix", "value": "0-1-0", "tone": "r"}, {"label": "article p", "value": "0-0-2"}],
    "show": ["sheet2", "c-prix", "c-art", "page2", "el-title", "el-prix"],
    "links": [],
    "script": [
        wait(1000),
        scene(link=[L("c-prix", "el-prix"), L("c-art", "el-prix")],
              say="Deux règles visent le prix, avec deux couleurs : laquelle gagne ?"),
        wait(1400),
        scene(set=[{"id": "c-art", "label": "écrite après"}],
              say="`article p` est écrite après. Mais l'ordre ne compte qu'entre deux règles de même spécificité."),
        wait(1500),
        scene(unlink=[L("c-art", "el-prix")], link=[L("c-art", "el-prix", dashed=True)],
              set=[{"id": "el-prix", "tone": "r", "label": "rose"}, {"id": "c-art", "label": "perd"}],
              hud=[hud(".prix", "0-1-0 : gagne", "r")],
              say="Une classe, 0-1-0, bat deux balises, 0-0-2 : le prix est rose."),
        wait(1500),
        scene(show=["c-id"], link=[L("c-id", "el-prix")], hud=[hud("#offre p", "1-0-1", "b")],
              say="Une troisième règle vise le prix avec un id : 1-0-1."),
        wait(1100),
        scene(unlink=[L("c-prix", "el-prix")], link=[L("c-prix", "el-prix", dashed=True)],
              set=[{"id": "el-prix", "tone": "b", "label": "bleu"}, {"id": "c-prix", "label": "perd"}],
              hud=[hud(".prix", "0-1-0"), hud("#offre p", "1-0-1 : gagne", "b")],
              say="On compare d'abord les id : le premier chiffre suffit, la règle bleue gagne."),
        wait(2600),
    ],
}

# ---------- 3. l'héritage
ents += [
    ent("h-sheet", "layer", (XS, 0), (12, 11), "n", title="style.css"),
    ent("h-body", "node", (0, -2), (10, 3), "b", parent="h-sheet", title="body { … }", sub="color: bleu; border: 2px solid;"),
    ent("h-note", "node", (0, 2.6), (10, 2.4), "r", parent="h-sheet", title=".note { … }", sub="color: rose;"),
    ent("h-page", "layer", (XP, 0), (12, 12), "n", title="<body>"),
    ent("h-h1", "node", (0, -3), EL, "n", parent="h-page", title="h1", sub="Le club de lecture"),
    ent("h-p", "node", (0, 0), EL, "n", parent="h-page", title="p", sub="Rendez-vous jeudi"),
    ent("h-pn", "node", (0, 3), EL, "n", parent="h-page", title="p class=\"note\"", sub="Entrée libre"),
]
heritage = {
    "id": "heritage", "label": "L'héritage", "title": "Du parent vers ses enfants",
    "body": ["Certaines propriétés, comme la couleur et la police du texte, descendent du parent vers ses enfants."],
    "show": ["h-sheet", "h-body", "h-page", "h-h1", "h-p", "h-pn"],
    "links": [],
    "script": [
        wait(1000),
        scene(link=[L("h-body", "h-page")], set=[{"id": "h-page", "tone": "b", "label": "bleu, avec une bordure"}],
              say="La règle vise `<body>`, et lui seul : son texte devient bleu, et il reçoit une bordure."),
        wait(1400),
        scene(set=[{"id": "h-h1", "tone": "b", "label": "hérité"}, {"id": "h-p", "tone": "b", "label": "hérité"},
                   {"id": "h-pn", "tone": "b", "label": "hérité"}],
              say="Ses enfants n'ont aucune règle, et pourtant leur texte est bleu : la couleur **s'hérite**."),
        wait(1500),
        scene(set=[{"id": "h-h1", "label": "bleu, sans bordure"}, {"id": "h-p", "label": "bleu, sans bordure"},
                   {"id": "h-pn", "label": "bleu, sans bordure"}],
              say="La bordure, elle, reste sur `<body>` : les bordures, les marges et les fonds **ne s'héritent pas**."),
        wait(1500),
        scene(show=["h-note"], link=[L("h-note", "h-pn")],
              set=[{"id": "h-pn", "tone": "r", "label": "sa propre règle gagne"}],
              say="Une règle qui vise l'élément lui-même passe **avant** ce qu'il hérite : la note est rose."),
        wait(2800),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "css-rules-cascade-plan", "title": "Règles, sélecteurs et cascade (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "b", "label": "texte bleu"}, {"tone": "r", "label": "texte rose"},
               {"tone": "v", "label": "fond pervenche"}, {"tone": "n", "label": "gris, par défaut"}],
    "entities": ents, "steps": [regle, ranger, selecteurs, cascade, heritage],
}
write(lesson, *outputs(HERE, "css.scene.json", "web-css"))
