"""Scènes 2D (kit plan) du bit « Flexbox : aligner des éléments sur une ligne » (flexbox).

Quatre étapes dans assets/flex.scene.json :
  conteneur  (section « Un conteneur flex et ses enfants ») : display: flex range les enfants directs, pas les petits-enfants.
  repartir   (section « Répartir et aligner ») : justify-content déplace les éléments le long de la ligne, align-items en travers.
  axes       (section « Le piège : flex-direction: column ») : l'axe principal tourne, justify-content le suit ;
             l'étape s'arrête sur l'axe secondaire devenu horizontal, sans le corriger : c'est l'exercice qui suit.
  wrap       (section « Passer à la ligne ») : six cartes de base 160px comprimées sur une ligne de 600px, puis
             flex-wrap: wrap (trois par ligne), puis une fenêtre de 400px (deux par ligne). Un autre exemple que
             l'exercice (galerie, 200px), pour ne pas en donner la solution.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px. Entités au premier niveau (coordonnées absolues),
calculées par des petites fonctions de mise en page : un conteneur peut changer de taille sans déplacer ses enfants.
Dessin : un conteneur = layer ; un élément = node. Les encarts disent le CSS appliqué à chaque instant.
Couleurs : v un bloc rangé par le flux normal, g un enfant rangé par un conteneur flex ; r l'axe principal, b l'axe secondaire.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import hud, scene, wait, write


def ent(id, kind, at, size=None, tone=None, **kw):
    d = {"id": id, "kind": kind, "at": [round(v, 3) for v in at]}
    if tone: d["tone"] = tone
    if size: d["size"] = [round(v, 3) for v in size] + ([] if kind == "zone" else [1])
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def box(id, x0, y0, w, h, zone=False, **kw):
    """Changement d'entité par son coin haut gauche (x0, y0) et sa taille."""
    d = {"id": id, "at": [round(x0 + w / 2, 3), round(y0 + h / 2, 3)], "size": [round(w, 3), round(h, 3)] + ([] if zone else [1])}
    d.update(kw)
    return d


def ent_box(id, kind, x0, y0, w, h, tone, **kw):
    return ent(id, kind, (x0 + w / 2, y0 + h / 2), (w, h), tone, **kw)


# ── Étape 1 : le conteneur et ses enfants directs ─────────────────────────────────────────────────────────────
X0, X1 = -8.0, 8.0           # intérieur de .entete
TOP = -4.1                   # haut de .entete
HEAD = 1.4                   # place du titre d'un conteneur
MHEAD = 1.5                  # titre + sous-titre de .menu
GAP = 0.6                    # gap: 16px
LI_H, LI_GAP = 1.0, 0.3
LIS = [("li-1", "li · Projets"), ("li-2", "li · À propos"), ("li-3", "li · Contact")]
LOGO_W, MENU_COL_W, LI_W = 3.6, 6.0, 3.2


def state_block():
    """Flux normal : deux blocs empilés sur toute la largeur, les liens empilés dans le menu."""
    y = TOP + HEAD
    out = [box("logo", X0, y, X1 - X0, 1.2)]
    y += 1.2 + 0.5
    mh = MHEAD + 3 * LI_H + 2 * LI_GAP + 0.4
    out.append(box("menu", X0, y, X1 - X0, mh))
    for i, (lid, _) in enumerate(LIS):
        out.append(box(lid, X0 + 0.5, y + MHEAD + i * (LI_H + LI_GAP), X1 - X0 - 1.0, LI_H))
    bottom = y + mh + 0.5
    out.append(box("entete", X0 - 0.5, TOP, X1 - X0 + 1.0, bottom - TOP))
    return out


def state_row():
    """.entete en flex : logo et menu côte à côte, à la largeur de leur contenu, étirés à la même hauteur."""
    y = TOP + HEAD
    mh = MHEAD + 3 * LI_H + 2 * LI_GAP + 0.4
    mx = X0 + LOGO_W + GAP
    out = [box("logo", X0, y, LOGO_W, mh), box("menu", mx, y, MENU_COL_W, mh)]
    for i, (lid, _) in enumerate(LIS):
        out.append(box(lid, mx + 0.5, y + MHEAD + i * (LI_H + LI_GAP), MENU_COL_W - 1.0, LI_H))
    out.append(box("entete", X0 - 0.5, TOP, X1 - X0 + 1.0, y + mh + 0.5 - TOP))
    return out


def state_row2():
    """.menu en flex aussi : ses liens passent en ligne ; le menu et le logo perdent de la hauteur."""
    y = TOP + HEAD
    mh = MHEAD + LI_H + 0.4
    mx = X0 + LOGO_W + GAP
    mw = 0.5 + 3 * LI_W + 2 * 0.4 + 0.5
    out = [box("logo", X0, y, LOGO_W, mh), box("menu", mx, y, mw, mh)]
    for i, (lid, _) in enumerate(LIS):
        out.append(box(lid, mx + 0.5 + i * (LI_W + 0.4), y + MHEAD, LI_W, LI_H))
    out.append(box("entete", X0 - 0.5, TOP, X1 - X0 + 1.0, y + mh + 0.5 - TOP))
    return out


def as_ents(states, spec):
    out = []
    for s in states:
        k, tone, kw = spec[s["id"]]
        e = ent(s["id"], k, s["at"], s["size"][:2], tone, **kw)
        out.append(e)
    return out


SPEC = {
    "entete": ("layer", "n", {"title": ".entete", "detail": "Le **conteneur** : c'est sur lui qu'on écrit `display: flex`."}),
    "logo": ("node", "v", {"title": ".logo", "sub": "CM"}),
    "menu": ("layer", "v", {"title": ".menu", "sub": "ul · 3 liens",
                            "detail": "Le menu est un enfant de `.entete` ; ses liens sont donc des **petits-enfants** de `.entete`."}),
    "li-1": ("node", "v", {"title": LIS[0][1]}),
    "li-2": ("node", "v", {"title": LIS[1][1]}),
    "li-3": ("node", "v", {"title": LIS[2][1]}),
}
start = state_block()
ents = as_ents([s for s in start if s["id"] == "entete"] + [s for s in start if s["id"] != "entete"], SPEC)
ents[1]["detail"] = "Le logo est un **enfant direct** de `.entete`."

conteneur = {
    "id": "conteneur", "label": "Conteneur et enfants", "title": "display: flex range les enfants directs",
    "body": ["Un entête, avec un logo et un menu de trois liens. Sans règle de disposition, ce sont des blocs, empilés."],
    "show": ["entete", "logo", "menu", "li-1", "li-2", "li-3"],
    "hud": [{"label": ".entete", "value": "display: block"}, {"label": ".menu", "value": "display: block"}],
    "script": [
        wait(1200),
        scene(say="display: flex sur le parent, .entete : ses deux enfants passent côte à côte, avec un gap entre eux.",
              hud=[hud(".entete", "display: flex", "g")],
              set=state_row() + [{"id": "logo", "tone": "g"}, {"id": "menu", "tone": "g"}], ms=1000),
        wait(1500),
        scene(say="Les liens du menu ne bougent pas : ce sont les petits-enfants de .entete, pas ses enfants.",
              set=[{"id": "menu", "sub": "liens toujours empilés"}]),
        wait(1600),
        scene(say="display: flex sur .menu : il devient à son tour un conteneur, et ses liens passent en ligne.",
              hud=[hud(".menu", "display: flex", "g")],
              set=state_row2() + [{"id": "menu", "sub": "ul · 3 liens"}] + [{"id": l, "tone": "g"} for l, _ in LIS], ms=1000),
        wait(2600),
    ],
}

# ── Étape 2 : justify-content et align-items ──────────────────────────────────────────────────────────────────
BX0, BX1 = -8.6, 8.6         # intérieur de .boite
BY0, BH = -2.0, 4.6          # haut de la zone des éléments, sa hauteur
ITEMS = [("it-a", 3.0, 1.4), ("it-b", 3.0, 2.6), ("it-c", 3.0, 1.9)]


def flex_items(justify, align):
    total = sum(w for _, w, _ in ITEMS)
    free = (BX1 - BX0) - total
    if justify == "flex-start":
        xs, between = BX0, 0
    elif justify == "center":
        xs, between = BX0 + free / 2, 0
    elif justify == "flex-end":
        xs, between = BX0 + free, 0
    else:  # space-between
        xs, between = BX0, free / (len(ITEMS) - 1)
    out, x = [], xs
    for iid, w, h in ITEMS:
        if align == "stretch":
            y0, hh = BY0, BH
        elif align == "center":
            y0, hh = BY0 + (BH - h) / 2, h
        else:
            y0, hh = BY0, h
        out.append(box(iid, x, y0, w, hh))
        x += w + between
    return out


ents += [ent("boite", "layer", (0, 0), (18.2, 6.8), "n", title=".boite",
             detail="Un conteneur flex ; ses trois enfants n'ont pas la même hauteur de contenu.")]
for s, (iid, _, _), name in zip(flex_items("flex-start", "stretch"), ITEMS, ["A", "B", "C"]):
    ents.append(ent(iid, "node", s["at"], s["size"][:2], "g", title=name))
ents[-3]["detail"] = "Trois enfants flex, de contenus de hauteurs différentes."

repartir = {
    "id": "repartir", "label": "Répartir, aligner", "title": "Le long de la ligne, puis en travers",
    "body": ["Trois éléments dans un conteneur flex, rangés au début de la ligne et étirés à la même hauteur : les deux réglages par défaut."],
    "show": ["boite", "it-a", "it-b", "it-c"],
    "hud": [{"label": "justify-content", "value": "flex-start"}, {"label": "align-items", "value": "stretch"}],
    "script": [
        wait(1200),
        scene(say="justify-content: center : l'espace libre se partage des deux côtés, les éléments se groupent au milieu.",
              hud=[hud("justify-content", "center", "g")], set=flex_items("center", "stretch"), ms=900),
        wait(1100),
        scene(say="flex-end : tout part au bout de la ligne.",
              hud=[hud("justify-content", "flex-end", "g")], set=flex_items("flex-end", "stretch"), ms=900),
        wait(1100),
        scene(say="space-between : le premier au début, le dernier à la fin, l'espace libre entre eux.",
              hud=[hud("justify-content", "space-between", "g")], set=flex_items("space-between", "stretch"), ms=900),
        wait(1500),
        scene(say="align-items agit en travers : center rend à chacun sa hauteur et les centre.",
              hud=[hud("align-items", "center", "g")], set=flex_items("space-between", "center"), ms=900),
        wait(1200),
        scene(say="flex-start les aligne en haut de la ligne.",
              hud=[hud("align-items", "flex-start", "g")], set=flex_items("space-between", "flex-start"), ms=900),
        wait(2400),
    ],
}

# ── Étape 3 : flex-direction: column, les axes tournent ───────────────────────────────────────────────────────
CTOP = -3.0
AX0, AX1 = -2.6, 6.6         # zone des éléments, en largeur
AXIS_X = -5.9                # l'axe vertical, à gauche
BTN_W, BTN_H, BTN_GAP = 3.4, 1.1, 0.4
IY0 = CTOP + 1.2             # haut de la zone des éléments
BTNS = [("btn-ok", "Réserver"), ("btn-no", "Annuler")]
MAIN_T, CROSS_T = "axe principal · justify-content", "axe secondaire · align-items"


def axes_state(direction, align):
    out = []
    cx = (AX0 + AX1) / 2
    if direction == "row":
        total = 2 * BTN_W + BTN_GAP
        x = cx - total / 2
        for bid, _ in BTNS:
            out.append(box(bid, x, IY0, BTN_W, BTN_H))
            x += BTN_W + BTN_GAP
        items_h = BTN_H
        out.append(box("ax-main", AX0, IY0 + items_h + 0.4, AX1 - AX0, 0.8, zone=True, label=MAIN_T))
        out.append(box("ax-cross", AXIS_X - 0.3, IY0, 0.6, items_h, zone=True, label="secondaire"))
    else:
        y = IY0
        for bid, _ in BTNS:
            if align == "stretch":
                out.append(box(bid, AX0, y, AX1 - AX0, BTN_H))
            else:
                out.append(box(bid, cx - BTN_W / 2, y, BTN_W, BTN_H))
            y += BTN_H + BTN_GAP
        items_h = 2 * BTN_H + BTN_GAP
        out.append(box("ax-main", AXIS_X - 0.3, IY0, 0.6, items_h, zone=True, label="principal"))
        out.append(box("ax-cross", AX0, IY0 + items_h + 0.4, AX1 - AX0, 0.8, zone=True, label=CROSS_T))
    bottom = IY0 + items_h + 0.4 + 0.8 + 0.5
    out.append(box("actions", -7.0, CTOP, 14.0, bottom - CTOP))
    return out


row = {s["id"]: s for s in axes_state("row", "stretch")}
ents += [
    ent("actions", "layer", row["actions"]["at"], row["actions"]["size"][:2], "n", title=".actions",
        detail="Le conteneur flex des deux boutons de la carte."),
    ent("ax-main", "zone", row["ax-main"]["at"], row["ax-main"]["size"][:2], "r", label=MAIN_T,
        detail="L'**axe principal** : la direction dans laquelle le conteneur range ses enfants. `justify-content` agit toujours sur lui."),
    ent("ax-cross", "zone", row["ax-cross"]["at"], row["ax-cross"]["size"][:2], "b", label="secondaire",
        detail="L'**axe secondaire**, perpendiculaire : `align-items` agit sur lui."),
] + [ent(bid, "node", row[bid]["at"], row[bid]["size"][:2], "g", title=name) for bid, name in BTNS]

axes = {
    "id": "axes", "label": "Les axes tournent", "title": "flex-direction: column fait tourner les axes",
    "body": ["Deux boutons dans un conteneur flex, centrés sur la ligne par `justify-content: center`."],
    "show": ["actions", "ax-main", "ax-cross", "btn-ok", "btn-no"],
    "hud": [{"label": "flex-direction", "value": "row"}, {"label": "justify-content", "value": "center"},
            {"label": "align-items", "value": "stretch"}],
    "script": [
        wait(1400),
        scene(say="flex-direction: column : les boutons s'empilent, l'axe principal devient vertical, et ils s'étirent sur toute la largeur.",
              hud=[hud("flex-direction", "column", "g")], set=axes_state("column", "stretch"), ms=1100),
        wait(1500),
        scene(say="justify-content suit l'axe principal : il agit maintenant en hauteur, et ne centre plus rien en largeur.",
              hud=[hud("justify-content", "center (en hauteur)", "r")]),
        wait(1600),
        scene(say="La largeur est devenue l'axe secondaire : c'est là qu'agit maintenant align-items, toujours sur stretch.",
              hud=[hud("align-items", "stretch (en largeur)", "b")]),
        wait(2600),
    ],
}

# ── Étape 4 : flex-wrap et la largeur de base ─────────────────────────────────────────────────────────────────
# Échelle de cette étape : 1 unité = 30 px. Cartes de base 160px, gap 12px.
PX = 30.0
BASE, WGAP = 160, 12
WX0, WTOP = -10.0, -4.0      # coin haut gauche de l'intérieur de .cartes
CARD_H, ROW_GAP = 1.6, 0.4
CARDS = [f"carte-{i}" for i in range(1, 7)]


def wrap_state(width_px, wrap):
    """Positions des six cartes dans un conteneur de width_px, avec ou sans passage à la ligne."""
    n = len(CARDS)
    if wrap:
        per = max(1, int((width_px + WGAP) // (BASE + WGAP)))
    else:
        per = n
    out, y = [], WTOP + HEAD
    for r in range(0, n, per):
        row = CARDS[r:r + per]
        w_px = (width_px - WGAP * (len(row) - 1)) / len(row)
        x = WX0
        for cid in row:
            out.append(box(cid, x, y, w_px / PX, CARD_H, title=f"{round(w_px)} px"))
            x += (w_px + WGAP) / PX
        y += CARD_H + ROW_GAP
    bottom = y - ROW_GAP + 0.5
    out.append(box("cartes", WX0 - 0.5, WTOP, width_px / PX + 1.0, bottom - WTOP))
    return out


w0 = {s["id"]: s for s in wrap_state(600, False)}
ents += [ent("cartes", "layer", w0["cartes"]["at"], w0["cartes"]["size"][:2], "n", title=".cartes",
             detail="Un conteneur flex de six cartes ; chaque carte a `flex: 1 1 160px`.")]
ents += [ent(c, "node", w0[c]["at"], w0[c]["size"][:2], "g", title=w0[c]["title"],
             detail="Une carte : sa **largeur de base** est 160 px ; elle peut grandir et rétrécir.") for c in CARDS]

wrap = {
    "id": "wrap", "label": "Passer à la ligne", "title": "Six cartes de 160 px dans 600 px",
    "body": ["Six cartes, chacune avec `flex: 1 1 160px`, dans un conteneur de 600 px. Le titre de chaque carte dit sa largeur affichée."],
    "show": ["cartes"] + CARDS,
    "hud": [{"label": "flex-wrap", "value": "nowrap"}, {"label": "conteneur", "value": "600 px"}],
    "script": [
        wait(1200),
        scene(say="Six fois 160 px ne tiennent pas dans 600 px. Sans flex-wrap, tout reste sur une ligne : chaque carte est comprimée à 90 px.",
              hud=[hud("flex-wrap", "nowrap", "r"), hud("une carte", "90 px", "r")]),
        wait(1800),
        scene(say="flex-wrap: wrap : trois cartes de 160 px tiennent par ligne, puis on passe à la ligne. Elles grandissent pour partager la place restante.",
              hud=[hud("flex-wrap", "wrap", "g"), hud("une carte", "192 px", "g")],
              set=wrap_state(600, True), ms=1000),
        wait(2000),
        scene(say="La fenêtre rétrécit, le conteneur passe à 400 px : deux cartes par ligne, sans aucune autre règle.",
              hud=[hud("conteneur", "400 px", "g"), hud("une carte", "194 px", "g")],
              set=wrap_state(400, True), ms=1000),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "flexbox",
    "title": "Flexbox : aligner des éléments", "lang": "fr", "kit": "plan",
    "legend": [{"tone": "v", "label": "bloc"}, {"tone": "g", "label": "enfant flex"},
               {"tone": "r", "label": "axe principal"}, {"tone": "b", "label": "axe secondaire"}],
    "entities": ents, "steps": [conteneur, repartir, axes, wrap],
}
write(lesson, *outputs(HERE, "flex.scene.json", "layout-flexbox"))
