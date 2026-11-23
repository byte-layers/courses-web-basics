"""Scènes 2D (kit plan) du bit « CSS Grid : des lignes et des colonnes » (css-grid).

Quatre étapes dans assets/grid.scene.json :
  pistes   (section « Une grille : les colonnes d'abord ») : les colonnes sont tracées d'abord, les enfants s'y rangent
           dans l'ordre, une ligne se crée toute seule ; 2fr 1fr 1fr élargit toute une colonne ; fr en note.
  span     (section « Un élément sur plusieurs colonnes ») : la deuxième carte prend grid-column: span 2, la suivante
           passe à la ligne et les autres la suivent (l'exercice, lui, étend la première carte).
  autofit  (section « auto-fit et minmax ») : le conteneur rétrécit, la grille retire une colonne quand 220 px ne
           tiennent plus, les cartes se rangent sur les colonnes restantes (l'exercice demande 250 px).
  combine  (section « Flex ou Grid ») : la page en Grid, l'entête en Flexbox (ligne), une carte en Flexbox (colonne).

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; entités au premier niveau, positions calculées.
Dessin : le conteneur = layer ; une colonne (piste) = zone en pointillés, avec sa taille ; une carte = node.
Couleurs : g un enfant de la grille ; v les colonnes (pistes) ; b un conteneur Flexbox ; y un enfant flex.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import hud, scene, wait, write


def r(v):
    return round(v, 3)


def box(id, x0, y0, w, h, zone=False, **kw):
    d = {"id": id, "at": [r(x0 + w / 2), r(y0 + h / 2)], "size": [r(w), r(h)] + ([] if zone else [1])}
    d.update(kw)
    return d


def ent(kind, b, tone=None, **kw):
    d = {"id": b["id"], "kind": kind, "at": b["at"], "size": b["size"]}
    if tone: d["tone"] = tone
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


# ── Étape 1 : les pistes d'abord ──────────────────────────────────────────────────────────────────────────────
GX0, GW = -9.0, 18.0         # intérieur de la grille
GAP = 0.8                    # gap: 24px
CTOP = -4.6                  # haut du conteneur
GTOP = CTOP + 2.8            # haut de la première ligne (place pour la note du conteneur)
ROW_H = 1.8
CARDS = [f"c{i}" for i in range(1, 7)]


def tracks(fr):
    free = GW - GAP * (len(fr) - 1)
    xs, x = [], GX0
    for f in fr:
        w = free * f / sum(fr)
        xs.append((x, w))
        x += w + GAP
    return xs


def grid_state(fr, rows, n_cards):
    cols = tracks(fr)
    out = []
    zh = rows * ROW_H + (rows - 1) * GAP + 0.6
    for i, (x, w) in enumerate(cols):
        out.append(box(f"col{i + 1}", x, GTOP - 0.6, w, zh, zone=True, label=f"{fr[i]}fr"))
    for k in range(n_cards):
        x, w = cols[k % len(cols)]
        out.append(box(CARDS[k], x, GTOP + (k // len(cols)) * (ROW_H + GAP), w, ROW_H))
    bottom = GTOP + zh - 0.6 + 0.6
    out.append(box("projets", GX0 - 0.6, CTOP, GW + 1.2, bottom - CTOP))
    return {b["id"]: b for b in out}


full = grid_state([1, 1, 1], 2, 6)
one = grid_state([1, 1, 1], 1, 3)
ents = [ent("layer", one["projets"], "n", title=".projets", detail="Le conteneur : `display: grid` et ses colonnes s'écrivent sur lui.")]
ents += [ent("zone", one[f"col{i}"], "v", label="1fr") for i in (1, 2, 3)]
ents += [ent("node", full[c], "g", title=c[1:]) for c in CARDS]
ents[1]["detail"] = "Une **colonne** de la grille : une piste, tracée avant qu'aucun élément ne s'y range."
ents[4]["detail"] = "Six cartes de projet, enfants directs de `.projets`, dans l'ordre du HTML."

pick = lambda st, ids: [st[i] for i in ids]
cols3 = ["col1", "col2", "col3"]
pistes = {
    "id": "pistes", "label": "Les colonnes d'abord", "title": "Les colonnes d'abord, puis les éléments",
    "body": ["Un conteneur `.projets` et six cartes. Avec Grid, on décrit les colonnes, pas les cartes."],
    "show": ["projets"],
    "hud": [{"label": "display", "value": "grid"}, {"label": "colonnes", "value": "aucune"}],
    "script": [
        wait(1000),
        scene(say="grid-template-columns: 1fr 1fr 1fr : la grille trace trois colonnes égales, avant d'y ranger quoi que ce soit.",
              hud=[hud("colonnes", "1fr 1fr 1fr", "g")], show=["col1", "col2", "col3"]),
        scene(set=[{"id": "projets", "note": "fr : une part de l'espace restant"}]),
        wait(1300),
        scene(say="Les enfants se rangent dans l'ordre du HTML, une case chacun.",
              show=pick(full, ["c1", "c2", "c3"])),
        wait(1200),
        scene(say="La première ligne est pleine : une deuxième se crée toute seule, sur les mêmes colonnes.",
              set=pick(full, cols3 + ["projets"]), show=pick(full, ["c4", "c5", "c6"]), ms=900),
        wait(1600),
        scene(say="Avec 2fr 1fr 1fr, l'espace se partage en quatre parts : deux pour la première colonne, et ses deux cartes s'élargissent ensemble.",
              hud=[hud("colonnes", "2fr 1fr 1fr", "g")],
              set=[b | ({"note": "2fr 1fr 1fr : 4 parts, 2 pour la 1re"} if b["id"] == "projets" else {})
                   for b in grid_state([2, 1, 1], 2, 6).values()],
              ms=1000),
        wait(2600),
    ],
}

# ── Étape 2 : auto-fit et minmax ──────────────────────────────────────────────────────────────────────────────
PX = 1 / 50                  # 1 px CSS = 1/50 d'unité : 1000 px = 20 unités
MIN, GAP_PX = 220, 24
A_TOP = -3.0
A_ROW = 1.6


def fit_state(width_px):
    n = max(1, (width_px + GAP_PX) // (MIN + GAP_PX))
    w = width_px * PX
    gap = GAP_PX * PX
    cw = (w - gap * (n - 1)) / n
    x0 = -w / 2
    out = []
    for k in range(6):
        out.append(box(f"a{k + 1}", x0 + (k % n) * (cw + gap), A_TOP + 1.6 + (k // n) * (A_ROW + gap), cw, A_ROW))
    rows = (6 + n - 1) // n
    h = 1.6 + rows * A_ROW + (rows - 1) * gap + 0.5
    out.append(box("galerie", x0 - 0.5, A_TOP, w + 1.0, h))
    return n, out


n0, s0 = fit_state(1000)
s0 = {b["id"]: b for b in s0}
ents += [ent("layer", s0["galerie"], "n", title=".projets",
             detail="`grid-template-columns: repeat(auto-fit, minmax(220px, 1fr))` : autant de colonnes que la largeur en permet, chacune d'au moins 220 px.")]
ents += [ent("node", s0[f"a{k}"], "g", title=str(k)) for k in range(1, 7)]


def step_to(width_px, say):
    n, st = fit_state(width_px)
    return scene(say=say, hud=[hud("largeur", f"{width_px} px"), hud("colonnes", str(n), "g")], set=st, ms=1100)


autofit = {
    "id": "autofit", "label": "auto-fit, minmax", "title": "Autant de colonnes que la largeur le permet",
    "body": ["La même grille de six cartes, avec `repeat(auto-fit, minmax(220px, 1fr))`. Le conteneur fait d'abord 1000 px de large."],
    "show": ["galerie", "a1", "a2", "a3", "a4", "a5", "a6"],
    "hud": [{"label": "largeur", "value": "1000 px"}, {"label": "colonnes", "value": str(n0)}],
    "script": [
        wait(1400),
        step_to(760, "La fenêtre rétrécit : à 760 px, quatre colonnes d'au moins 220 px ne tiennent plus. La grille passe à trois."),
        wait(1400),
        step_to(500, "À 500 px, deux colonnes : l'espace qui reste se partage entre elles, c'est le 1fr."),
        wait(1400),
        step_to(375, "Sur un téléphone, une seule colonne. Aucune règle par largeur d'écran n'a été écrite."),
        wait(2600),
    ],
}

# ── Étape 3 : un élément sur deux colonnes ────────────────────────────────────────────────────────────────────
# Exemple différent de l'exercice (là, c'est la première carte) : ici la deuxième carte, « Quiz », s'étend.
SPAN_T = ["Météo", "Quiz", "Courses", "Recettes", "Rando"]
S_IDS = [f"s{i}" for i in range(1, 6)]


def span_state(span_of=None):
    """Cases occupées par les cinq cartes, rangées dans l'ordre ; span_of : indice de la carte sur deux colonnes."""
    cols = tracks([1, 1, 1])
    out, cell = [], 0
    for k, sid in enumerate(S_IDS):
        n = 2 if k == span_of else 1
        if cell % 3 + n > 3:           # pas la place sur la ligne : on passe à la suivante
            cell += 3 - cell % 3
        x, _ = cols[cell % 3]
        w = sum(cols[(cell % 3) + j][1] for j in range(n)) + GAP * (n - 1)
        out.append(box(sid, x, GTOP + (cell // 3) * (ROW_H + GAP), w, ROW_H))
        cell += n
    return {b["id"]: b for b in out}


sp0 = span_state()
sz = grid_state([1, 1, 1], 2, 0)
ents += [ent("layer", sz["projets"], "n", title=".projets", detail="Une grille de trois colonnes : `repeat(3, 1fr)`.")
         | {"id": "span-grid"}]
ents += [ent("zone", sz[f"col{i}"], "v", label="1fr") | {"id": f"span-col{i}"} for i in (1, 2, 3)]
ents += [ent("node", sp0[sid], "g", title=SPAN_T[k]) for k, sid in enumerate(S_IDS)]

span = {
    "id": "span", "label": "span 2", "title": "Une carte sur deux colonnes",
    "body": ["La même grille de trois colonnes, avec cinq cartes rangées dans l'ordre."],
    "show": ["span-grid", "span-col1", "span-col2", "span-col3"],
    "hud": [{"label": "Quiz", "value": "une case"}],
    "script": [
        wait(1300),
        scene(say="Chaque carte occupe une case : trois sur la première ligne, deux sur la seconde.", show=S_IDS),
        wait(1100),
        scene(say="grid-column: span 2 sur la carte Quiz : elle s'étend sur deux colonnes. Plus de place pour Courses : elle passe à la ligne suivante, les autres la suivent.",
              hud=[hud("Quiz", "span 2", "g")],
              set=[span_state(1)["s2"] | {"label": "grid-column: span 2"}] + [span_state(1)[x] for x in ("s3", "s4", "s5")],
              ms=1100),
        wait(2600),
    ],
}

# ── Étape 4 : Grid pour la page, Flexbox dans l'entête et la carte ───────────────────────────────────────────
PW, PH = 20.0, 13.0
CW = (PW - 2 - 2 * GAP) / 3            # largeur d'une carte
ents += [
    {"id": "page", "kind": "layer", "at": [0, 0], "size": [PW, PH, 1], "tone": "n", "title": "la page : display: grid",
     "detail": "La page est une **grille** : l'entête sur toute la largeur, puis trois colonnes de cartes."},
    {"id": "p-head", "kind": "layer", "in": "page", "at": [0, -3.7], "size": [PW - 2, 3.2, 1], "tone": "g", "title": "header"},
    {"id": "p-logo", "kind": "node", "in": "p-head", "at": [-6.8, 0.55], "size": [2.4, 1.3, 1], "tone": "y", "title": "CM"},
    {"id": "p-nav", "kind": "node", "in": "p-head", "at": [5.6, 0.55], "size": [5.6, 1.3, 1], "tone": "y", "title": "nav"},
]
for i in range(3):
    ents.append({"id": f"p-card{i + 1}", "kind": "layer", "in": "page", "at": [r(-(CW + GAP) + i * (CW + GAP)), 2.3],
                 "size": [r(CW), 7.0, 1], "tone": "g", "title": f"carte {i + 1}"})
for j, (cid, title, h, y) in enumerate([("p-title", "titre", 1.1, -1.9), ("p-text", "texte", 1.8, -0.2), ("p-btn", "bouton", 1.1, 1.9)]):
    ents.append({"id": cid, "kind": "node", "in": "p-card1", "at": [0, y], "size": [r(CW - 1.2), h, 1], "tone": "y", "title": title})

combine = {
    "id": "combine", "label": "Grid et Flexbox", "title": "Un choix par conteneur",
    "body": ["Une page de portfolio : un entête, trois cartes de projet."],
    "show": ["page", "p-head", "p-card1", "p-card2", "p-card3"],
    "hud": [{"label": "la page", "value": "Grid"}],
    "script": [
        wait(1300),
        scene(say="La page aligne en deux directions : l'entête en haut, les cartes en colonnes. C'est une grille.",
              hud=[hud("la page", "Grid", "g")]),
        wait(1300),
        scene(say="Dans l'entête, une seule direction : le logo à gauche, le menu à droite. L'entête passe en Flexbox.",
              set=[{"id": "p-head", "tone": "b", "title": "header : display: flex"}],
              show=["p-logo", "p-nav"], hud=[hud("l'entête", "Flexbox", "b")]),
        wait(1500),
        scene(say="Dans une carte aussi : un titre, un texte, un bouton, l'un sous l'autre. Une colonne, donc Flexbox.",
              set=[{"id": "p-card1", "tone": "b", "title": "carte : flex, column"}],
              show=["p-title", "p-text", "p-btn"], hud=[hud("une carte", "Flexbox", "b")]),
        wait(1500),
        scene(say="Grid et Flexbox ne s'excluent pas : on choisit pour chaque conteneur, selon ses directions.",
              hud=[hud("le choix", "par conteneur", "g")]),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "css-grid",
    "title": "CSS Grid : des lignes et des colonnes", "lang": "fr", "kit": "plan",
    "legend": [{"tone": "v", "label": "colonne"}, {"tone": "g", "label": "enfant de la grille"},
               {"tone": "b", "label": "conteneur Flexbox"}, {"tone": "y", "label": "enfant flex"}],
    "entities": ents, "steps": [pistes, span, autofit, combine],
}
write(lesson, *outputs(HERE, "grid.scene.json", "layout-css-grid"))
