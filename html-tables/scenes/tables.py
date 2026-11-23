"""Scènes 2D (kit plan) du bit « Les tableaux HTML » (html-tables).

Trois étapes dans assets/tables.scene.json :
  tableau    (section « Un tableau, c'est pour des données ») : le tableau se construit ligne par ligne, les colonnes
             naissent du même nombre de cellules, les th nomment colonnes et lignes, le lecteur d'écran s'en sert.
  structure  (section « Les parties d'un tableau ») : table > caption, thead, tbody en boîtes imbriquées ;
             exemple différent de l'exercice.
  miseenpage (section « Le piège : un tableau pour la mise en page ») : l'entête vu à l'écran, le tableau invisible
             derrière, puis ce qu'annonce un lecteur d'écran ; la solution de l'exercice (Flexbox) n'est pas montrée.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; entités au premier niveau.
Dessin : le tableau, une ligne (tr) = layer ; une cellule = node ; le lecteur d'écran = actor.
Couleurs : y donnée (td), v en-tête (th), r ce qu'entend le lecteur d'écran d'un faux tableau.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import L, hud, scene, send, wait, write


def r(v):
    return round(v, 3)


def ent(id, kind, x0, y0, w, h, tone=None, **kw):
    d = {"id": id, "kind": kind, "at": [r(x0 + w / 2), r(y0 + h / 2)], "size": [r(w), r(h), 1]}
    if tone: d["tone"] = tone
    if kind == "actor": del d["size"]
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


# ── Étape 1 : le tableau ──────────────────────────────────────────────────────────────────────────────────────
COLS = [(-8.0, 5.6), (-2.0, 3.6), (1.8, 3.6)]
ROWS = {"h": -3.0, "r1": -1.5, "r2": 0.0, "r3": 1.5}
CH = 1.1
HEAD = ["Sortie", "Distance", "Date"]
DATA = {"r1": ["Pic du Midi", "14 km", "12 avril"], "r2": ["Lac d'Oô", "9 km", "3 mai"], "r3": ["Gavarnie", "11 km", "7 juin"]}

ents = [ent("table", "layer", -8.6, -4.6, 14.8, 7.5, "n", title="table",
            detail="Un tableau HTML : des lignes `tr`, des cellules `td` (données) et `th` (en-têtes).")]
for rid, y in ROWS.items():
    ents.append(ent(f"tr-{rid}", "layer", -8.25, y - 0.2, 13.9, CH + 0.4, "n",
                    detail="Une ligne : `<tr>`, pour *table row*." if rid == "r1" else None))
for i, (x, w) in enumerate(COLS):
    ents.append(ent(f"th-{i}", "node", x, ROWS["h"], w, CH, "v", title=HEAD[i],
                    detail='Un **en-tête de colonne** : `<th scope="col">`, dans `<thead>`.' if i == 0 else None))
for rid, cells in DATA.items():
    for i, (x, w) in enumerate(COLS):
        ents.append(ent(f"{rid}-{i}", "node", x, ROWS[rid], w, CH, "y", title=cells[i],
                        detail="Une cellule de données : `<td>`, pour *table data*." if (rid, i) == ("r1", 1) else None))
ents.append(ent("reader", "actor", 8.4, -2.1, 1.4, 1.8, "r", label="lecteur d'écran",
                detail="Un **lecteur d'écran** lit la page à voix haute ; il annonce chaque cellule avec ses en-têtes."))

row_ids = lambda rid: [f"tr-{rid}"] + [f"{rid}-{i}" for i in range(3)]
tableau = {
    "id": "tableau", "label": "Ligne par ligne", "title": "Un tableau se construit ligne par ligne",
    "body": ["Le programme des sorties d'un club : des données qui ont un sens en lignes et en colonnes."],
    "show": ["table"],
    "script": [
        wait(900),
        scene(say="Un tableau se construit ligne par ligne : une tr, et ses cellules td.", show=row_ids("r1")),
        wait(1200),
        scene(say="Chaque ligne a trois cellules : les colonnes se forment toutes seules, sans balise pour elles.",
              show=row_ids("r2") + row_ids("r3")),
        wait(1500),
        scene(say="La ligne d'en-tête nomme les colonnes : des th, avec scope=\"col\".",
              show=["tr-h", "th-0", "th-1", "th-2"]),
        wait(1300),
        scene(say="Le nom de chaque sortie nomme sa ligne : il devient un th, avec scope=\"row\".",
              set=[{"id": f"{rid}-0", "tone": "v"} for rid in DATA]),
        wait(1300),
        # explain sur ce send : le moteur plante (le lecteur n'est pas dans le show de départ) ; la phrase va au say
        {"do": "pulse", "at": "r1-0"},
        {"do": "pulse", "at": "th-2"},
        scene(say="Un lecteur d'écran annonce chaque cellule avec ses deux en-têtes : « Pic du Midi, Date : 12 avril ».",
              show=["reader"], link=[L("r1-2", "reader")]),
        send(["r1-2", "reader"], label="Pic du Midi, Date"),
        wait(2400),
    ],
}

# ── Étape 3 : les parties d'un tableau (caption, thead, tbody) ───────────────────────────────────────────────
# Exemple différent de l'exercice : autre titre, colonne Date, deux sorties.
def sub_ent(id, kind, parent, at, size, tone=None, **kw):
    d = {"id": id, "kind": kind, "in": parent, "at": list(at)}
    if size: d["size"] = list(size) + ([] if kind == "zone" else [1])
    if tone: d["tone"] = tone
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


SX = [-4.8, 0.0, 4.8]
ents.append({"id": "s-table", "kind": "layer", "at": [0, 0], "size": [16.4, 13.2, 1], "tone": "n", "title": "table",
             "detail": "Le tableau entier : `<table>`, qui contient le titre, l'en-tête et le corps."})
ents.append(sub_ent("s-caption", "node", "s-table", (0, -4.6), (14.6, 1.3), "n", title="caption",
                    sub="Sorties du printemps",
                    detail="Le **titre** du tableau : `<caption>`, juste après `<table>`. Un lecteur d'écran l'annonce en premier."))
ents.append(sub_ent("s-thead", "layer", "s-table", (0, -1.85), (15.4, 3.4), "v", title="thead",
                    note="les lignes d'en-tête",
                    detail="`<thead>` regroupe la ou les lignes d'en-tête : des `<th scope=\"col\">`."))
for i, t in enumerate(["Sortie", "Distance", "Date"]):
    ents.append(sub_ent(f"s-th{i}", "node", "s-thead", (SX[i], 0.75), (4.3, 1.1), "v", title=t))
ents.append(sub_ent("s-tbody", "layer", "s-table", (0, 3.3), (15.4, 5.8), "y", title="tbody",
                    note="les lignes de données",
                    detail="`<tbody>` regroupe les lignes de données ; la première cellule de chaque ligne peut être un `<th scope=\"row\">`."))
for j, row in enumerate([["Pic du Midi", "14 km", "12 avril"], ["Lac d'Oô", "9 km", "3 mai"]]):
    for i, t in enumerate(row):
        ents.append(sub_ent(f"s-r{j}c{i}", "node", "s-tbody", (SX[i], -0.3 + j * 1.9), (4.3, 1.1), "v" if i == 0 else "y", title=t))

structure = {
    "id": "structure", "label": "caption, thead, tbody", "title": "Les trois parties d'un tableau",
    "body": ["Le même genre de tableau, rangé en parties : un titre, un en-tête, un corps."],
    "show": ["s-table"],
    "hud": [{"label": "partie", "value": "—"}],
    "script": [
        wait(900),
        scene(say="D'abord le titre du tableau : caption, juste après la balise table.",
              show=["s-caption"], hud=[hud("partie", "caption", "n")]),
        wait(1300),
        scene(say="Puis thead : la ligne d'en-tête, dont les th nomment chaque colonne.",
              show=["s-thead", "s-th0", "s-th1", "s-th2"], hud=[hud("partie", "thead", "v")]),
        wait(1300),
        scene(say="Enfin tbody : les lignes de données. Le nom de chaque sortie y est un th, il nomme sa ligne.",
              show=["s-tbody"] + [f"s-r{j}c{i}" for j in range(2) for i in range(3)], hud=[hud("partie", "tbody", "y")]),
        wait(2600),
    ],
}

# ── Étape 4 : le tableau de mise en page ──────────────────────────────────────────────────────────────────────
ents.append({"id": "m-head", "kind": "layer", "at": [-4, 0], "size": [15, 6, 1], "tone": "n", "title": "header, à l'écran"})
ents.append(sub_ent("m-td1", "zone", "m-head", (-4.6, 0.6), (4.2, 3.0), label="td"))
ents.append(sub_ent("m-td2", "zone", "m-head", (2.6, 0.6), (8.6, 3.0), label="td"))
ents.append(sub_ent("m-logo", "node", "m-head", (-4.6, 0.8), (2.8, 1.5), "y", title="CM"))
ents.append(sub_ent("m-nav", "node", "m-head", (2.6, 0.8), (7.0, 1.5), "y", title="nav", sub="Projets · Contact"))
ents.append({"id": "m-reader", "kind": "actor", "at": [8.6, 0.2], "tone": "r", "label": "lecteur d'écran"})

miseenpage = {
    "id": "miseenpage", "label": "Tableau de mise en page", "title": "Bien à l'écran, faux à l'oreille",
    "body": ["Un entête : le logo à gauche, le menu à droite."],
    "show": ["m-head", "m-logo", "m-nav"],
    "hud": [{"label": "à l'écran", "value": "rien à redire", "tone": "g"}],
    "script": [
        wait(1200),
        scene(say="Derrière, un tableau invisible : une ligne, deux cellules td, l'une pour le logo, l'autre pour le menu.",
              show=["m-td1", "m-td2"], set=[{"id": "m-head", "title": "header > table > tr > td"}]),
        wait(1400),
        scene(say="Un lecteur d'écran, lui, annonce « tableau, une ligne, deux colonnes », puis lit le menu comme une donnée.",
              show=["m-reader"], link=[L("m-nav", "m-reader")], hud=[hud("à l'oreille", "un tableau", "r")]),
        send(["m-nav", "m-reader"], label="tableau, 2 colonnes", tone="r"),
        wait(900),
        scene(say="Le test : ce contenu a-t-il un sens en lignes et en colonnes ? Non. Ce n'est donc pas un tableau.",
              hud=[hud("un tableau ?", "non", "r")]),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "html-tables",
    "title": "Les tableaux HTML", "lang": "fr", "kit": "plan",
    "legend": [{"tone": "y", "label": "donnée : td"}, {"tone": "v", "label": "en-tête : th"},
               {"tone": "r", "label": "faux tableau"}],
    "entities": ents, "steps": [tableau, structure, miseenpage],
}
write(lesson, *outputs(HERE, "tables.scene.json", "layout-html-tables"))
