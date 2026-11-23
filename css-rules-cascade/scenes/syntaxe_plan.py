"""Scènes 2D (kit plan) du bit « CSS : règles, sélecteurs et cascade » (courses-web-basics/css-rules-cascade), syntaxe.

Trois étapes, une idée chacune (syntaxe.scene.json) :
- anatomie : une règle lue morceau par morceau (code annoté) : le sélecteur, le bloc, deux déclarations ;
- repli : la liste de polices est lue dans l'ordre ; la première que l'appareil possède est prise ; la famille
  générique, en dernier, existe partout ;
- silence : un chemin faux dans <link>, puis une propriété mal écrite : rien ne s'applique, et rien ne le signale.
  Exemple volontairement différent de l'exercice « Le CSS qui ne fait rien » (pas de solution donnée).

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Une règle par sorte : une ligne de code est un node ; un fichier ou un appareil est un layer qui porte ce qu'il
contient ; ce que le navigateur affiche est posé dans un layer « la page affichée ».
Couleurs : y le code CSS ; v le navigateur et ce qu'il affiche ; g appliqué ou trouvé ; r ignoré ou absent ;
n les notes, le HTML, l'appareil.
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


# ---------- 1. anatomie : une règle, morceau par morceau
XC, XN = -7, 9.5            # colonne du code, colonne des notes
DY = 2.6
CODE_A = [
    ("a1", 0, "h2 {"),
    ("a2", 1, "color: rgb(11, 107, 203);"),
    ("a3", 1, "text-align: center;"),
    ("a4", 0, "}"),
]
Y0 = -(len(CODE_A) - 1) * DY / 2


def ya(i):
    return Y0 + (i - 1) * DY


A = [ent(id, "node", (XC + ind * 1.0, ya(i + 1)), (12 - ind * 2, 1.7), "y", title=txt)
     for i, (id, ind, txt) in enumerate(CODE_A)]
A += [
    ent("z-bloc", "zone", (XC + 0.5, (ya(1) + ya(4)) / 2), (14.4, ya(4) - ya(1) + 3.2), "y", label="le bloc { … }"),
    ent("n-sel", "node", (XN, ya(1)), (12, 2), "n", title="le sélecteur", sub="les éléments visés : tous les h2"),
    ent("n-dec", "node", (XN, ya(2)), (12, 2), "n", title="une déclaration", sub="propriété : valeur ;",
        detail="`color` est la **propriété** : la couleur du texte. `rgb(11, 107, 203)` est la **valeur** : un bleu, "
               "en rouge, vert et bleu de 0 à 255. On écrit aussi `#0b6bcb` ou `blue`."),
    ent("n-dec2", "node", (XN, ya(3)), (12, 2), "n", title="une autre déclaration", sub="text-align : l'alignement"),
]
anatomie = {
    "id": "anatomie", "label": "La règle", "title": "Une règle, morceau par morceau",
    "body": ["Un sélecteur, puis un bloc de déclarations entre accolades."],
    "show": [c[0] for c in CODE_A],
    "links": [],
    "script": [
        wait(1000),
        scene(show=["n-sel"], link=[L("a1", "n-sel")],
              say="Le **sélecteur** dit quels éléments la règle vise : ici, tous les titres `<h2>` de la page."),
        wait(1300),
        scene(show=["z-bloc"],
              say="L'accolade `{` ouvre le **bloc de déclarations**, `}` le ferme. Tout ce qu'on applique est dedans."),
        wait(1300),
        scene(show=["n-dec"], link=[L("a2", "n-dec")],
              say="Une **déclaration** : la propriété `color`, deux-points, la valeur, puis un point-virgule."),
        wait(1500),
        scene(show=["n-dec2"], link=[L("a3", "n-dec2")],
              say="Une deuxième déclaration, dans le même bloc. Le `;` les sépare : un oubli, et la suivante ne marche plus."),
        wait(2600),
    ],
}

# ---------- 2. repli : la liste de polices
R = [
    ent("p-rule", "node", (-13, 0), (10, 3), "y", title="body { font-family: … }", sub="\"Segoe UI\", Verdana, sans-serif"),
    ent("p-list", "layer", (0, 0), (10, 11), "n", title="la liste, dans l'ordre"),
    ent("p-c1", "node", (0, -2.8), (8, 2), "y", parent="p-list", title="\"Segoe UI\""),
    ent("p-c2", "node", (0, 0), (8, 2), "y", parent="p-list", title="Verdana"),
    ent("p-c3", "node", (0, 2.8), (8, 2), "y", parent="p-list", title="sans-serif", sub="famille générique"),
    ent("p-dev", "layer", (13, 0), (11, 8), "n", title="l'appareil du visiteur"),
    ent("p-fonts", "node", (0, 0.8), (9, 3), "n", parent="p-dev", title="polices installées", sub="—"),
]
repli = {
    "id": "repli", "label": "La liste de repli", "title": "La première police présente gagne",
    "body": ["Le navigateur essaie les polices dans l'ordre, et prend la première que l'appareil possède."],
    "hud": [{"label": "police affichée", "value": "—"}],
    "show": ["p-rule", "p-list", "p-c1", "p-c2", "p-c3", "p-dev", "p-fonts"],
    "links": [L("p-rule", "p-list")],
    "script": [
        wait(1000),
        scene(set=[{"id": "p-dev", "title": "un PC Windows"},
                   {"id": "p-fonts", "sub": "Segoe UI, Verdana, Arial…"},
                   {"id": "p-c1", "tone": "g", "label": "trouvée"}],
              link=[L("p-c1", "p-dev")], hud=[hud("police affichée", "Segoe UI", "g")],
              say="Sur un **PC Windows**, Segoe UI est installée : elle est prise, la suite de la liste est ignorée."),
        wait(1600),
        scene(set=[{"id": "p-dev", "title": "un Mac"},
                   {"id": "p-fonts", "sub": "Helvetica, Verdana, Arial…"},
                   {"id": "p-c1", "tone": "r", "label": "absente"},
                   {"id": "p-c2", "tone": "g", "label": "trouvée"}],
              unlink=[L("p-c1", "p-dev")], link=[L("p-c2", "p-dev")], hud=[hud("police affichée", "Verdana", "g")],
              say="Sur un **Mac**, pas de Segoe UI : le navigateur passe à la suivante, Verdana."),
        wait(1600),
        scene(set=[{"id": "p-dev", "title": "un téléphone Android"},
                   {"id": "p-fonts", "sub": "Roboto, Noto Sans…"},
                   {"id": "p-c2", "tone": "r", "label": "absente"},
                   {"id": "p-c3", "tone": "g", "label": "existe partout"}],
              unlink=[L("p-c2", "p-dev")], link=[L("p-c3", "p-dev")],
              hud=[hud("police affichée", "Roboto, via sans-serif", "g")],
              say="Sur un **téléphone Android**, ni l'une ni l'autre. `sans-serif` existe partout : il prend la police sans empattements de l'appareil."),
        wait(2800),
    ],
}

# ---------- 3. silence : rien ne s'applique, rien ne le signale
S = [
    ent("s-link", "node", (-12, -5.5), (12, 2.2), "n", title="<link href=\"css/style.css\">", sub="dans index.html"),
    ent("s-missing", "node", (-12, -1.5), (9, 2.2), "r", title="css/style.css", sub="aucun fichier à ce chemin"),
    ent("s-sheet", "layer", (-12, 4), (13, 7.6), "y", title="style.css"),
    ent("s-h1r", "node", (0, -0.7), (11, 2), "y", parent="s-sheet", title="h1 { text-allign: center; }"),
    ent("s-pr", "node", (0, 2.0), (11, 2), "y", parent="s-sheet", title="p { font-size: 20px; }"),
    ent("s-page", "layer", (10, 0), (12, 10), "v", title="la page affichée"),
    ent("s-h1", "node", (0, -1.6), (10, 2.2), "v", parent="s-page", title="Le club de lecture", sub="h1"),
    ent("s-p", "node", (0, 1.6), (10, 2.2), "v", parent="s-page", title="Prochaine séance jeudi", sub="p"),
]
silence = {
    "id": "silence", "label": "Rien ne s'affiche", "title": "Ignoré, sans un message",
    "body": ["Un fichier introuvable, une propriété mal écrite : la règle ne fait rien, et rien ne le signale."],
    "hud": [{"label": "message d'erreur", "value": "aucun"}],
    "show": ["s-link", "s-sheet", "s-h1r", "s-pr", "s-page", "s-h1", "s-p"],
    "links": [],
    "script": [
        wait(1000),
        scene(show=["s-missing"], link=[L("s-link", "s-missing")]),
        send(["s-link", "s-missing"], tone="r", label="style.css ?"),
        scene(set=[{"id": "s-page", "label": "sans style"}],
              say="La page demande `css/style.css`. Le fichier est **à côté** de la page, pas dans un dossier `css` : rien n'est chargé."),
        wait(1600),
        scene(hide=["s-missing"],
              set=[{"id": "s-link", "title": "<link href=\"style.css\">", "tone": "g"}, {"id": "s-page", "label": None}],
              link=[L("s-link", "s-sheet")],
              say="Avec le bon chemin, `style.css` est chargée."),
        wait(1300),
        scene(set=[{"id": "s-pr", "tone": "g", "label": "appliquée"}, {"id": "s-p", "label": "20 px"}],
              link=[L("s-pr", "s-p")],
              say="La règle `p` s'applique : le paragraphe grandit."),
        wait(1400),
        scene(set=[{"id": "s-h1r", "tone": "r", "label": "propriété inconnue : ignorée"},
                   {"id": "s-h1", "label": "toujours à gauche"}],
              link=[L("s-h1r", "s-h1", dashed=True)],
              say="`text-allign`, avec deux l, n'existe pas : la déclaration est **ignorée**, le titre reste à gauche."),
        wait(1500),
        scene(hud=[hud("message d'erreur", "toujours aucun", "r"), hud("où le voir", "l'inspecteur")],
              say="Aucun message, ni dans la page ni dans l'éditeur. Seul l'**inspecteur** du navigateur montre la propriété barrée."),
        wait(2800),
    ],
}

write({
    "format": "bl-scenes/0.3", "id": "css-rules-cascade-syntaxe", "title": "Une règle CSS, sa police, ses silences (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "y", "label": "code CSS"}, {"tone": "v", "label": "le navigateur"},
               {"tone": "g", "label": "appliqué, trouvé"}, {"tone": "r", "label": "ignoré, absent"}],
    "entities": A + R + S, "steps": [anatomie, repli, silence],
}, *outputs(HERE, "syntaxe.scene.json", "web-css-syntaxe"))
