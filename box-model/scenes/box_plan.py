"""Scènes 2D (kit plan) du bit « Le modèle de boîte » (courses-web-basics/box-model).

Cinq étapes, une idée chacune :
- couches : une boîte se lit de l'intérieur vers l'extérieur ; le fond s'étend dans le padding, la marge écarte la
  voisine ; la largeur occupée grandit à chaque couche ;
- espaces : la règle CSS à gauche, ligne par ligne ; à droite deux cartes collées qui prennent une bordure (avec
  son style), puis du padding (le texte s'éloigne du bord, le fond s'étend) et une marge (les cartes s'écartent, le
  fond de la page apparaît). Valeurs différentes de celles de l'exercice ;
- largeur : par défaut, width ne règle que le contenu, padding et bordure s'ajoutent (300 → 350, la carte
  déborde de sa colonne) ;
- borderbox : avec box-sizing: border-box, width règle la boîte entière et le contenu se réduit (250) ;
- inline : le code à gauche, le rendu à droite ; un <div> (bloc) prend toute la largeur, un <span> (en ligne) se
  glisse dans le texte et ignore width ; display: inline-block la lui fait accepter. Exemple différent de
  l'exercice.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Échelle des étapes « largeur » et « borderbox » : 1 unité = 30 px de la page (300 px = 10 unités).
Une règle par sorte : une couche est une boîte posée dans la suivante (in), la marge est une zone en pointillés
(transparente : le fond du parent s'y voit) ; une ligne de code est un node ; ce que le navigateur affiche est
posé dans un layer « la page affichée ».
Couleurs : y le fond de l'élément (contenu et padding : le fond s'étend dans le padding), b la bordure, n le parent
(la page grise) et les lignes de code, v la voisine et le texte affiché ; r ce qui déborde ou est ignoré, g ce qui tient.
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


def line(n):
    return {"do": "line", "n": n}


# ---------- 1. les quatre couches
ents = [
    ent("parent", "layer", (0, 0), (21, 15.5), "n", title="le parent"),
    ent("margin", "zone", (0, -1.4), (17, 10.2), parent="parent", label="margin"),
    ent("border", "layer", (0, 0), (14, 7.8), "b", parent="margin", title="border"),
    ent("padding", "layer", (0, 0.85), (12.8, 5.2), "y", parent="border", title="padding"),
    ent("content", "node", (0, 0.6), (8, 2.0), "y", parent="padding", title="contenu", sub="width: 300px"),
    ent("voisine", "node", (0, 4.6), (12, 1.8), "v", parent="parent", title="la carte voisine"),
]
couches = {
    "id": "couches", "label": "Quatre couches", "title": "Une boîte en quatre couches",
    "body": ["Le contenu, le padding, la bordure, la marge : on lit la boîte de l'intérieur vers l'extérieur."],
    "hud": [{"label": "largeur occupée", "value": "300 px"}],
    "show": ["parent", {"id": "margin", "dim": True}, {"id": "border", "dim": True}, {"id": "padding", "dim": True},
             "content", "voisine"],
    "links": [],
    "script": [
        wait(1000),
        scene(set=[{"id": "content", "label": "le texte, l'image"}],
              say="Au centre, le contenu : `width` et `height` règlent sa taille, ici 300 px de large."),
        wait(1300),
        scene(set=[{"id": "padding", "dim": None, "label": "20px · le fond s'y étend"}],
              hud=[hud("largeur occupée", "340 px")],
              say="Le padding éloigne le contenu du bord ; le fond de l'élément s'étend dedans."),
        wait(1300),
        scene(set=[{"id": "border", "dim": None, "label": "5px solid"}], hud=[hud("largeur occupée", "350 px")],
              say="La bordure entoure le padding : une épaisseur, un style, une couleur."),
        wait(1300),
        scene(set=[{"id": "margin", "dim": None}, {"id": "voisine", "at": [0, 5.9]}], hud=[hud("largeur occupée", "350 px + marges")],
              say="La marge est dehors, transparente : elle écarte la voisine, et le fond du parent s'y voit.", ms=1000),
        wait(2600),
    ],
}

# ---------- 2. espaces : bordure, padding, marge sur deux cartes
H0, H1 = 4.0, 5.6          # hauteur d'une carte sans padding, avec padding
W0, W1 = 11.8, 13.4        # largeur d'une carte sans padding, avec padding
TW, TH = 11.4, 2.2         # le texte d'une carte (il ne change pas de taille)
ents += [
    ent("s-page", "layer", (0, 0.4), (16, 16), "n", title="la page affichée"),
    ent("s-c1", "layer", (0, -2.2), (W0, H0), "n", parent="s-page", title="carte 1"),
    ent("s-t1", "node", (0, 0.8), (TW, TH), "v", parent="s-c1", title="Emprunter", sub="le texte touche le bord"),
    ent("s-c2", "layer", (0, 1.8), (W0, H0), "n", parent="s-page", title="carte 2"),
    ent("s-t2", "node", (0, 0.8), (TW, TH), "v", parent="s-c2", title="Travailler sur place", sub="le texte touche le bord"),
    ent("s-gap", "zone", (0, 0.35), (W1, 1.3), parent="s-page", label="margin-bottom : 24px"),
]
CSS_S = [".carte {", "  background-color: rgb(255, 255, 255);", "  border: 2px solid rgb(11, 107, 203);",
         "  padding: 16px;", "  margin-bottom: 24px;", "}"]
espaces = {
    "id": "espaces", "label": "Dedans, dehors", "title": "Padding dedans, marge dehors",
    "body": ["La règle `.carte`, ligne par ligne, sur deux cartes collées. La question à se poser : le fond de la carte doit-il s'étendre dans cet espace ?"],
    "hud": [{"label": "bordure", "value": "invisible"}],
    "show": ["s-page", "s-c1", "s-t1", "s-c2", "s-t2"],
    "links": [],
    "widgets": [{"kind": "editor", "title": "style.css", "lang": "text", "lines": CSS_S}],
    "script": [
        line(1), wait(1000),
        scene(set=[{"id": "s-c1", "label": "rien ne les sépare"}],
              say="Deux cartes collées : leur texte touche le bord, et rien ne les sépare."),
        wait(1200), line(3),
        scene(set=[{"id": "s-c1", "tone": "b", "label": "2px solid"}, {"id": "s-c2", "tone": "b", "label": "2px solid"}],
              hud=[hud("bordure", "2px solid", "b")],
              say="La bordure : une épaisseur, le style `solid` et une couleur. Sans le style, elle reste invisible."),
        wait(1400), line(4),
        scene(set=[{"id": "s-c1", "at": [0, -3.2], "size": [W1, H1, 1], "label": "padding : le fond s'étend"},
                   {"id": "s-c2", "at": [0, 2.4], "size": [W1, H1, 1], "label": None},
                   {"id": "s-t1", "at": [0, 0.6], "sub": "loin du bord"},
                   {"id": "s-t2", "at": [0, 0.6], "sub": "loin du bord"}],
              hud=[hud("padding", "16px", "y")],
              say="Le **padding** éloigne le texte du bord. Le fond de la carte s'étend dans cet espace : c'est dedans.", ms=1000),
        wait(1500), line(5),
        scene(show=["s-gap"], set=[{"id": "s-c2", "at": [0, 3.9]}],
              hud=[hud("margin-bottom", "24px", "n")],
              say="La **marge** écarte la carte suivante. Le gris de la page apparaît entre les deux : c'est dehors.", ms=1000),
        wait(2600),
    ],
}

# ---------- 3. la vraie largeur (content-box) ; 4. border-box
U300 = 10.0           # 300 px
PAD, BOR = 20 / 30, 5 / 30
W_CB = U300 + 2 * (PAD + BOR)   # content-box : 350 px
ents += [
    ent("col", "zone", (0, 0), (U300, 9), label="la colonne : 300 px"),
    ent("card", "layer", ((W_CB - U300) / 2, 1.4), (W_CB, 4.6), "r", parent="col", title="la carte",
        sub="width: 300px; padding: 20px; border: 5px"),
    ent("card-c", "node", (0, 0.7), (U300, 1.8), "y", parent="card", title="contenu : 300 px"),
]
largeur = {
    "id": "largeur", "label": "La vraie largeur", "title": "width ne règle que le contenu",
    "body": ["Par défaut, `width` ne règle que le contenu : padding et bordure s'ajoutent autour."],
    "hud": [{"label": "width", "value": "300px"}, {"label": "occupée", "value": "?"},
            {"label": "box-sizing", "value": "content-box"}],
    "show": ["col", "card", "card-c"],
    "links": [],
    "script": [
        wait(1200),
        scene(set=[{"id": "card-c", "label": "width = le contenu"}],
              say="Par défaut, `width: 300px` règle le contenu seul : il remplit déjà les 300 px de la colonne."),
        wait(1400),
        scene(set=[{"id": "card", "label": "déborde de 50 px"}], hud=[hud("occupée", "350 px", "r")],
              say="Le padding et la bordure s'ajoutent des deux côtés : 300 + 20 + 20 + 5 + 5 = 350 px."),
        wait(2600),
    ],
}
borderbox = {
    "id": "borderbox", "label": "border-box", "title": "box-sizing: border-box",
    "body": ["Avec `box-sizing: border-box`, `width` désigne toute la boîte, padding et bordure compris."],
    "hud": [{"label": "width", "value": "300px"}, {"label": "occupée", "value": "350 px", "tone": "r"},
            {"label": "box-sizing", "value": "content-box"}],
    "show": ["col", {"id": "card", "label": "déborde de 50 px"}, "card-c"],
    "links": [],
    "script": [
        wait(1200),
        scene(set=[{"id": "card", "at": [0, 1.4], "size": [U300, 4.6, 1], "tone": "g", "label": None},
                   {"id": "card-c", "size": [U300 - 2 * (PAD + BOR), 1.8, 1], "title": "contenu : 250 px"}],
              hud=[hud("box-sizing", "border-box", "g"), hud("occupée", "300 px", "g")],
              say="Avec `box-sizing: border-box`, `width` désigne toute la boîte : le contenu se réduit à 250 px.", ms=1100),
        wait(1400),
        scene(set=[{"id": "card", "label": "tient dans les 300 px"}],
              say="La carte tient exactement dans sa colonne, padding et bordure compris."),
        wait(2600),
    ],
}

# ---------- 5. bloc ou en ligne
XC, XR = -9, 9
DY = 2.0
CODE_I = [
    ("i1", 0, "<div>Tarifs</div>"),
    ("i2", 0, "<p>Le pass :"),
    ("i3", 1, "<span class=\"prix\">5 €</span>"),
    ("i4", 1, "par mois.</p>"),
    ("i5", 0, ".prix { width: 100px; }"),
]
Y0 = -(len(CODE_I) - 1) * DY / 2
ents += [ent(id, "node", (XC + ind * 0.9, Y0 + i * DY), (13 - ind * 1.8, 1.6), "n", title=txt)
         for i, (id, ind, txt) in enumerate(CODE_I)]
ents += [
    ent("i-page", "layer", (XR, 0), (15, 11), "n", title="la page affichée"),
    ent("i-div", "node", (0, -2.6), (13.4, 1.8), "v", parent="i-page", title="Tarifs", sub="toute la largeur"),
    ent("i-p", "layer", (0, 2.0), (13.4, 4.2), "n", parent="i-page", title="<p>, une ligne de texte"),
    ent("i-w1", "node", (-4.4, 0.6), (3.8, 1.6), "v", parent="i-p", title="Le pass :"),
    ent("i-badge", "node", (-1.6, 0.6), (1.6, 1.6), "y", parent="i-p", title="5 €"),
    ent("i-w2", "node", (1.6, 0.6), (4.0, 1.6), "v", parent="i-p", title="par mois."),
]
inline = {
    "id": "inline", "label": "Bloc ou en ligne", "title": "Un bloc, et une boîte en ligne",
    "body": ["Le code à gauche, ce que le navigateur affiche à droite. Un `<span>` ne se comporte pas comme un `<div>`."],
    "hud": [{"label": "display du span", "value": "inline"}],
    "labels": "left",
    "show": ["i1", "i2", "i3", "i4", "i5", "i-page"],
    "links": [],
    "script": [
        wait(900),
        scene(show=["i-div"], link=[L("i1", "i-div")],
              say="Un élément **bloc**, comme `<div>`, prend toute la largeur et commence sur une nouvelle ligne."),
        wait(1400),
        scene(show=["i-p", "i-w1", "i-badge", "i-w2"], link=[L("i3", "i-badge")],
              say="Un élément **en ligne** (*inline*), comme `<span>`, se glisse dans le texte, à la suite des mots."),
        wait(1400),
        scene(set=[{"id": "i-badge", "tone": "r"}], link=[L("i5", "i-badge")], hud=[hud("width", "ignorée", "r")],
              say="La règle demande 100 px. Le `<span>` l'ignore : il garde la largeur de son texte."),
        wait(1600),
        scene(set=[{"id": "i-badge", "at": [-0.4, 0.6], "size": [4.0, 1.6, 1], "tone": "g", "label": "100 px"},
                   {"id": "i-w2", "at": [4.1, 0.6]}],
              hud=[hud("display du span", "inline-block", "g"), hud("width", "100px", "g")],
              say="Avec `display: inline-block`, il reste dans la ligne et accepte enfin sa largeur.", ms=1000),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "box-model-plan", "title": "Le modèle de boîte (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "y", "label": "fond de l'élément"}, {"tone": "b", "label": "bordure"},
               {"tone": "r", "label": "déborde, ignoré"}, {"tone": "g", "label": "tient"}],
    "entities": ents, "steps": [couches, espaces, largeur, borderbox, inline],
}
write(lesson, *outputs(HERE, "box.scene.json", "web-box"))
