"""Scènes 2D (kit plan) du bit « Bloc, inline : le flux normal d'une page » (normal-flow).

Quatre étapes dans assets/flow.scene.json :
  flux     (section « Le flux normal ») : le navigateur pose les boîtes dans l'ordre du HTML ; les blocs prennent
           toute la largeur, les inline restent dans la ligne et passent à la suivante comme un mot.
  reponse  (section qui suit le quiz « Où tombe chaque élément ? ») : le code du header à gauche, son rendu à droite :
           trois blocs, donc trois lignes ; strong et a restent dans la phrase ; .logo prend toute la largeur.
  marge    (section « Le piège ») : la marge du haut d'un inline ne repousse rien. L'étape s'arrête sur le piège :
           la correction (inline-block) est l'exercice qui suit.
  display  (section « inline-block ») : block, inline et inline-block côte à côte, puis la même marge du haut sur
           les trois ; la scène porte le tableau de la section (où l'élément se place, ce qui s'applique).

Kit plan : x vers la droite, y vers le bas, en unités de 28 px. Entités au premier niveau (coordonnées absolues) :
une boîte inline est dessinée dans son paragraphe, sans `in`, pour que le paragraphe puisse grandir sans déplacer
ce qu'il contient.
Dessin : la page (body) et un paragraphe qui contient des inline = conteneurs (layer) ; un bloc sans enfant = node ;
un inline = file. Couleurs : v bloc, y inline, g inline-block, r la marge qui pose problème.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import hud, scene, wait, write


def ent(id, kind, at, size=None, tone=None, **kw):
    d = {"id": id, "kind": kind, "at": list(at)}
    if tone: d["tone"] = tone
    if size: d["size"] = list(size) + ([1] if kind != "zone" else [])
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


def line(n):
    return {"do": "line", "n": n}


# ── Étape 1 : le flux normal ─────────────────────────────────────────────────────────────────────────────────
W = 17          # largeur d'un bloc (toute la largeur du body)
L1, L2 = -0.85, 0.45   # milieu des deux lignes du paragraphe
ents = [
    ent("body", "layer", (0, -0.6), (19, 10.4), "n", title="body",
        detail="La page : le `body` est la boîte qui contient toutes les autres. Sa largeur est celle de la fenêtre."),
    ent("h1", "node", (0, -3.6), (W, 1.5), "v", title="h1 · Mes projets",
        detail="Un **bloc** commence sur une nouvelle ligne et prend **toute la largeur** de son parent."),
    ent("p", "layer", (0, -1.3), (W, 2.4), "v", title="p",
        detail="Le paragraphe est un **bloc** : il se pose sous le titre. Il contient du texte et des éléments **inline**."),
    ent("t1", "file", (-5.6, L1), (5.2, 1.0), "y", title="Un site pour un"),
    ent("strong", "file", (-0.8, L1), (3.8, 1.0), "y", title="strong · club",
        detail="`strong` est **inline** : il reste dans la phrase et ne prend que la largeur de son contenu."),
    ent("t2", "file", (3.6, L1), (4.6, 1.0), "y", title="de randonnée,"),
    ent("a", "file", (-6.0, L2), (4.4, 1.0), "y", title="a · voir le site",
        detail="Un lien `a` est **inline** : quand la ligne est pleine, il passe à la suivante, comme un mot."),
    ent("foot", "node", (0, 2.6), (W, 1.5), "v", title="p · © 2026"),
]
HTML = [
    "<h1>Mes projets</h1>",
    "<p>Un site pour un",
    "  <strong>club</strong> de randonnée,",
    '  <a href="#">voir le site</a>.</p>',
    "<p>© 2026</p>",
]
flux = {
    "id": "flux", "label": "Le flux normal", "title": "Les boîtes posées dans l'ordre du HTML",
    "body": ["Sans CSS de disposition, le navigateur lit le HTML dans l'ordre et pose chaque boîte selon son `display` par défaut."],
    "show": ["body"],
    "widgets": [{"kind": "editor", "title": "index.html", "lang": "text", "lines": HTML}],
    "script": [
        wait(900),
        line(1),
        scene(say="Le h1 est un bloc : il commence une ligne et prend toute la largeur, même pour deux mots.", show=["h1"]),
        wait(1300),
        line(2),
        scene(say="Le paragraphe est un bloc aussi : il se pose dessous, sur toute la largeur.", show=["p"]),
        wait(1100),
        line(3),
        scene(say="Dans le paragraphe, strong est inline : il reste dans la phrase, à la largeur de son mot.",
              show=["t1", "strong", "t2"]),
        wait(1500),
        line(4),
        scene(say="Le lien ne tient plus au bout de la ligne : il passe à la suivante, comme un mot, et le paragraphe grandit.",
              set=[{"id": "p", "at": [0, -0.65], "size": [W, 3.7, 1]}], show=["a"], ms=900),
        wait(1500),
        line(5),
        scene(say="Le dernier paragraphe ne contient presque rien, et prend quand même toute la largeur.",
              show=[{"id": "foot", "label": "toute la largeur"}]),
        wait(2600),
        line(0),
    ],
}

# ── Étape 2 : la marge verticale d'un inline ──────────────────────────────────────────────────────────────────
# Deux lignes de texte ; sur la seconde, un lien habillé en bouton. Sa marge du haut est une zone en pointillés.
Y1, Y2 = -0.7, 0.7
DY = 1.2        # la marge : 24 px
ents += [
    ent("p2", "layer", (0, -0.4), (14, 4.4), "n", title="p"),
    ent("m-l1", "file", (-0.9, Y1), (11.4, 1.0), "y", title="Envie d'en savoir plus sur le club ?"),
    ent("m-l2", "file", (-4.4, Y2), (4.4, 1.0), "y", title="Écrivez-nous :"),
    ent("btn", "node", (1.4, Y2), (6.0, 1.0), "v", title="a.bouton",
        detail="Un lien est **inline** : on l'habille en bouton avec un fond et du padding, mais il vit toujours dans la ligne de texte."),
    ent("marge", "zone", (1.4, Y2 - 0.5 - DY / 2), (6.0, DY), "r", label="margin-top"),
]
marge = {
    "id": "marge", "label": "La marge ignorée", "title": "Une marge du haut sur un inline",
    "body": ["Un lien habillé en bouton, au milieu d'un paragraphe. On lui donne une marge du haut."],
    "show": ["p2", "m-l1", "m-l2", "btn"],
    "hud": [{"label": "display", "value": "inline"}, {"label": "hauteur de ligne", "value": "normale"}],
    "script": [
        wait(1000),
        scene(say="On donne au lien une marge du haut de 24 px.", show=["marge"],
              set=[{"id": "btn", "label": "margin-top: 24px"}]),
        wait(1200),
        scene(say="Il est inline : sa ligne garde sa hauteur. La marge passe sous la ligne du dessus, et rien ne bouge.",
              hud=[{"label": "hauteur de ligne", "value": "inchangée", "tone": "r"}]),
        wait(2800),
    ],
}

# ── Étape « reponse » : le header du quiz, code et rendu ─────────────────────────────────────────────────────
# La page affichée à droite du code ; trois blocs empilés, la phrase avec ses deux inline.
RL = 1.95       # milieu de la ligne de texte du paragraphe
ents += [
    ent("r-head", "layer", (0, -0.65), (19, 7.9), "n", title="header",
        detail="Le `header` est un bloc : il contient les trois autres, empilés."),
    ent("r-logo", "node", (0, -2.7), (17, 1.4), "v", title="p.logo · CM",
        detail="Un paragraphe est un **bloc** : il prend toute la largeur, même pour deux lettres."),
    ent("r-h1", "node", (0, -0.9), (17, 1.6), "v", title="h1 · Camille Martin"),
    ent("r-p", "layer", (0, 1.5), (17, 2.4), "v", title="p"),
    ent("r-t1", "file", (-5.6, RL), (5.4, 1.0), "y", title="Développeuse web à"),
    ent("r-strong", "file", (-0.3, RL), (4.8, 1.0), "y", title="strong · Toulouse",
        detail="`strong` est **inline** : il reste dans la phrase."),
    ent("r-a", "file", (5.3, RL), (6.0, 1.0), "y", title="a · voir mes projets",
        detail="Le lien `a` est **inline** : il suit le mot d'avant, sur la même ligne."),
]
HEADER = [
    "<header>",
    '  <p class="logo">CM</p>',
    "  <h1>Camille Martin</h1>",
    "  <p>Développeuse web à",
    "    <strong>Toulouse</strong>,",
    '    <a href="#projets">voir mes projets</a>.</p>',
    "</header>",
]
reponse = {
    "id": "reponse", "label": "La réponse", "title": "Trois blocs, trois lignes",
    "body": ["Le header du quiz : le code, puis ce que le navigateur affiche, sans aucun CSS."],
    "show": ["r-head"],
    "hud": [{"label": "lignes", "value": "0"}],
    "widgets": [{"kind": "editor", "title": "index.html", "lang": "text", "lines": HEADER}],
    "script": [
        wait(900),
        line(2),
        scene(say="Le logo est un paragraphe, donc un bloc : une ligne à lui, sur toute la largeur, pour deux lettres.",
              show=[{"id": "r-logo", "label": "toute la largeur"}], hud=[hud("lignes", "1")]),
        wait(1500),
        line(3),
        scene(say="Le h1 est un bloc : il commence une nouvelle ligne, dessous.", show=["r-h1"], hud=[hud("lignes", "2")]),
        wait(1200),
        line(4),
        scene(say="Le second paragraphe, un bloc aussi : la troisième ligne.", show=["r-p", "r-t1"],
              hud=[hud("lignes", "3")]),
        wait(1200),
        line(5),
        scene(say="strong est inline : Toulouse reste dans la phrase.", show=["r-strong"]),
        wait(1100),
        line(6),
        scene(say="Le lien aussi : il suit le mot d'avant. Trois lignes en tout, pas cinq.", show=["r-a"],
              hud=[hud("lignes", "3 : trois blocs", "g")]),
        wait(2600),
        line(0),
    ],
}

# ── Étape « display » : block, inline, inline-block côte à côte ──────────────────────────────────────────────
# Trois colonnes ; dans chacune, une phrase et un lien rangé selon son display. Puis une marge du haut de 24 px.
CX = {"b": -11.0, "i": 0.0, "ib": 11.0}
CW = 10.0       # largeur d'une colonne
M = 1.0         # la marge du haut : 24 px
YA, YB = -1.4, 0.0      # deux lignes de texte
ents += [
    ent("d-col-b", "layer", (CX["b"], 0), (CW, 7), "v", title="display: block",
        detail="**block** : se place sur sa propre ligne, sur toute la largeur. `width`, `height` et les marges du haut et du bas s'appliquent."),
    ent("d-col-i", "layer", (CX["i"], 0), (CW, 7), "y", title="display: inline",
        detail="**inline** : se place dans la ligne, à la largeur de son contenu. `width`, `height` et les marges du haut et du bas sont ignorées."),
    ent("d-col-ib", "layer", (CX["ib"], 0), (CW, 7), "g", title="display: inline-block",
        detail="**inline-block** : se place dans la ligne, comme un inline. `width`, `height` et toutes les marges s'appliquent, comme pour un bloc."),
    # block : le lien seul sur sa ligne, la phrase reprend dessous
    ent("d-b-t1", "file", (CX["b"] - 2.3, YA), (4.4, 1.0), "y", title="Du texte,"),
    ent("d-b-a", "node", (CX["b"], YB), (9, 1.0), "v", title="le lien"),
    ent("d-b-t2", "file", (CX["b"] - 2.0, YB + 1.4), (5.0, 1.0), "y", title="et la suite."),
    ent("d-b-m", "zone", (CX["b"], YB), (9, M), "g", label="margin-top"),
    # inline : le lien dans la ligne
    ent("d-i-t1", "file", (CX["i"] - 2.4, YA), (4.4, 1.0), "y", title="Du texte,"),
    ent("d-i-a", "file", (CX["i"] + 2.0, YA), (3.6, 1.0), "y", title="le lien"),
    ent("d-i-t2", "file", (CX["i"] - 2.2, YB), (5.0, 1.0), "y", title="et la suite."),
    ent("d-i-m", "zone", (CX["i"] + 2.0, YA - 0.5 - M / 2), (3.6, M), "r", label="margin-top"),
    # inline-block : le lien dans la ligne, avec une vraie boîte
    ent("d-ib-t1", "file", (CX["ib"] - 2.4, YA), (4.4, 1.0), "y", title="Du texte,"),
    ent("d-ib-a", "node", (CX["ib"] + 2.0, YA), (3.6, 1.0), "g", title="le lien"),
    ent("d-ib-t2", "file", (CX["ib"] - 2.2, YB), (5.0, 1.0), "y", title="et la suite."),
    ent("d-ib-m", "zone", (CX["ib"] + 2.0, YA), (3.6, M), "g", label="margin-top"),
]
display = {
    "id": "display", "label": "Trois display", "title": "Trois valeurs de display, côte à côte",
    "body": ["La même phrase, avec un lien au milieu. Seule change la valeur de `display` du lien."],
    "show": ["d-col-b", "d-col-i", "d-col-ib"],
    "hud": [{"label": "margin-top", "value": "0"}],
    "script": [
        wait(900),
        scene(say="block : le lien prend sa propre ligne, sur toute la largeur ; la phrase reprend dessous.",
              show=["d-b-t1", "d-b-a", "d-b-t2"]),
        wait(1500),
        scene(say="inline : le lien reste dans la ligne, à la largeur de son texte.",
              show=["d-i-t1", "d-i-a", "d-i-t2"]),
        wait(1500),
        scene(say="inline-block : dans la ligne aussi, mais avec une vraie boîte, qui accepte width et height.",
              show=["d-ib-t1", "d-ib-a", "d-ib-t2"]),
        wait(1700),
        scene(say="Une marge du haut de 24 px sur le lien inline : elle n'écarte rien, la ligne garde sa hauteur.",
              show=["d-i-m"], hud=[hud("margin-top", "24px")]),
        wait(1700),
        scene(say="La même marge en block et en inline-block : elle compte : le lien et sa ligne descendent pour lui faire de la place.",
              show=["d-b-m", "d-ib-m"],
              set=[{"id": "d-b-a", "at": [CX["b"], YB + M]},
                   {"id": "d-b-t2", "at": [CX["b"] - 2.0, YB + 1.4 + M]},
                   {"id": "d-ib-t1", "at": [CX["ib"] - 2.4, YA + M]},
                   {"id": "d-ib-a", "at": [CX["ib"] + 2.0, YA + M]},
                   {"id": "d-ib-t2", "at": [CX["ib"] - 2.2, YB + M]}], ms=1000),
        wait(2800),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "normal-flow",
    "title": "Bloc, inline : le flux normal", "lang": "fr", "kit": "plan",
    "legend": [{"tone": "v", "label": "bloc"}, {"tone": "y", "label": "inline"}, {"tone": "g", "label": "inline-block"},
               {"tone": "r", "label": "marge"}],
    "entities": ents, "steps": [flux, reponse, marge, display],
}
write(lesson, *outputs(HERE, "flow.scene.json", "layout-normal-flow"))
