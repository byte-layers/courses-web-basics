"""Scènes du bit « Où vit le JavaScript dans une page » (courses-web-basics/js-in-page), kit Feuilleté + widget editor.

Dessin, une règle par sorte (le même pour tout le stack JavaScript) :
- ce qui tourne dans le navigateur : la page affichée (plateau bleu, b), le moteur JavaScript (bloc pervenche, v, JS) et
  la console (bloc encre, i, >_). Le plateau « navigateur » du bit sur la console n'est pas dessiné ici : les cartes des
  éléments de la page le chevauchaient toutes ;
- un élément de la page = un petit bloc posé sur la page, bleu comme elle ; il porte le nom de sa balise ;
- un fichier JavaScript = un bloc fichier jaune (y), hors du navigateur, relié au moteur qui le lit ;
- le fichier HTML est dans l'éditeur à côté de la scène : la ligne surlignée est celle que le navigateur lit.
Couleurs : rose (r) pour ce qui casse (null, TypeError), vert (g) pour ce qui est trouvé.
Grille d'écran G(sx, sy) : page (-3,2 ; 1,6), moteur (2,8 ; -2,2), console (4,2 ; 4), script.js (8 ; -8).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import G, L, scene, send, wait, write, hud

H = 0.55


def rel(sx, sy, z=H):
    x, y = G(sx, sy)
    return [x, y, z]


def line(n):
    return {"do": "line", "n": n}


ents = [
    {"id": "page", "kind": "layer", "at": G(-3.2, 1.6), "size": [3.4, 3.4, 0.35], "tone": "b", "title": "page affichée",
     "detail": "La **page affichée** se remplit au fur et à mesure de la lecture du HTML, de haut en bas."},
    {"id": "h1", "kind": "file", "in": "page", "at": rel(0, -1.3, 0.35), "size": [1.4, 1.4, 0.35], "tone": "b", "title": "<h1>"},
    {"id": "p", "kind": "file", "in": "page", "at": rel(0, 1.3, 0.35), "size": [1.4, 1.4, 0.35], "tone": "b", "title": "<p>"},
    {"id": "moteur", "kind": "node", "at": G(2.8, -2.2), "tone": "v", "title": "moteur JavaScript", "icon": "JS",
     "detail": "Le **moteur JavaScript** exécute le script au moment où le navigateur le lui confie."},
    {"id": "console", "kind": "node", "at": G(4.2, 4.0), "size": [1.8, 1.8, 0.9], "tone": "i", "title": "console", "icon": ">_",
     "detail": "La **console** des outils de développement : `console.log` et les erreurs y écrivent."},
    {"id": "js", "kind": "file", "at": G(8, -8), "tone": "y", "title": "script.js",
     "detail": "Le fichier JavaScript, à côté de la page. La balise `<script src=\"script.js\">` le désigne."},
]
BASE = ["page", "moteur", "console"]
LINKS = [L("js", "moteur"), L("moteur", "console")]

LECTURE = ["<!DOCTYPE html>", "<html lang=\"fr\">", "<head>", "  <title>Mon portfolio</title>", "</head>", "<body>",
           "  <h1>Ada Lovelace</h1>", "  <p>Développeuse web</p>", "  <script src=\"script.js\"></script>", "</body>", "</html>"]


def page_lines(defer):
    return ["<head>", "  <script src=\"script.js\"%s></script>" % (" defer" if defer else ""), "</head>", "<body>",
            "  <h1>Médiathèque</h1>", "  <p id=\"compteur\">En attente…</p>", "</body>"]


steps = []

# ---------- 1. le navigateur lit de haut en bas
steps.append({
    "id": "lecture", "label": "De haut en bas", "title": "Le navigateur lit la page de haut en bas",
    "body": ["La ligne surlignée est celle que le navigateur lit. Une balise `<script>` l'arrête le temps d'exécuter le fichier."],
    "hud": [{"label": "lecture du HTML", "value": "en cours"}],
    "show": BASE + [{"id": "js", "dim": True}],
    "links": LINKS,
    "widgets": [{"kind": "editor", "title": "index.html", "lang": "text", "lines": LECTURE}],
    "script": [
        wait(700), line(6), wait(500), line(7),
        scene(say="Le navigateur lit le HTML de haut en bas : le titre entre dans la page.", show=["h1"]),
        wait(900), line(8),
        scene(say="Puis le paragraphe.", show=["p"]),
        wait(900), line(9),
        scene(say="Une balise `<script>` : il s'arrête de lire et charge `script.js`.",
              set=[{"id": "js", "dim": False}], hud=[hud("lecture du HTML", "en pause", "r")]),
        send(["js", "moteur"], kind="read", tone="y", label="script.js",
             explain=["Il confie le fichier au **moteur JavaScript**, qui l'exécute tout de suite."]),
        send(["moteur", "console"], label="console.log"),
        scene(say="Le moteur exécute le fichier : sa ligne s'écrit dans la console.",
              set=[{"id": "console", "label": "Bonjour depuis la page"}]),
        wait(1000), line(10),
        scene(say="Puis la lecture reprend, jusqu'à `</html>`.", hud=[hud("lecture du HTML", "reprise", None)]),
        wait(500), line(11),
        scene(say="À chaque chargement de la page, tout recommence, et le script se rejoue.",
              hud=[hud("lecture du HTML", "terminée", "g")]),
        line(0), wait(2200),
    ],
})

# ---------- 2. trop tôt : null
steps.append({
    "id": "trop-tot", "label": "Trop tôt", "title": "Un script dans le head : la page est encore vide",
    "body": ["Le script s'exécute au moment où le navigateur le lit : dans le `<head>`, le `<body>` n'existe pas encore."],
    "hud": [{"label": "body lu", "value": "non", "tone": "r"}],
    "show": BASE + ["js"],
    "links": LINKS + [L("moteur", "page")],
    "widgets": [{"kind": "editor", "title": "index.html", "lang": "text", "lines": page_lines(False)}],
    "script": [
        wait(700), line(2),
        send(["js", "moteur"], kind="read", tone="y", label="script.js",
             explain=["Le `<script>` est dans le `<head>` : le moteur l'exécute avant que le `<body>` soit lu."]),
        send(["moteur", "page"], label="#compteur", reply="null", tone="r",
             explain=["Il cherche `#compteur` dans la page…", "… encore vide : la recherche rend `null`."]),
        scene(say="La recherche ne trouve rien : `compteur` vaut `null`, sans erreur pour l'instant.",
              set=[{"id": "moteur", "label": "compteur = null"}]),
        wait(900),
        send(["moteur", "console"], label="TypeError", tone="r"),
        scene(say="Écrire dans `null` arrête le script, avec une TypeError, à la ligne qui écrit.",
              set=[{"id": "console", "label": "TypeError … of null"}]),
        wait(1100), line(5),
        scene(say="Le `<body>` arrive ensuite : le titre…", show=["h1"], hud=[hud("body lu", "en cours", None)]),
        line(6),
        scene(say="… et le paragraphe, trop tard : il garde son texte de départ.",
              show=[{"id": "p", "label": "En attente…"}], hud=[hud("body lu", "oui", "g")]),
        line(0), wait(2400),
    ],
})

# ---------- 3. defer
steps.append({
    "id": "defer", "label": "defer", "title": "defer : télécharger tout de suite, exécuter après",
    "body": ["Avec `defer`, la balise reste dans le `<head>`, mais le script attend que toute la page soit lue."],
    "hud": [{"label": "body lu", "value": "non", "tone": "r"}, {"label": "script", "value": "—"}],
    "show": BASE + [{"id": "js", "dim": True}],
    "links": LINKS + [L("moteur", "page")],
    "widgets": [{"kind": "editor", "title": "index.html", "lang": "text", "lines": page_lines(True)}],
    "script": [
        wait(700), line(2),
        scene(say="Avec `defer`, le navigateur télécharge `script.js` tout de suite, mais ne l'exécute pas encore.",
              set=[{"id": "js", "dim": False, "label": "téléchargé, attend"}], hud=[hud("script", "en attente", "y")]),
        wait(1000), line(5),
        scene(say="Il continue sa lecture : le titre…", show=["h1"], hud=[hud("body lu", "en cours", None)]),
        line(6),
        scene(say="… puis le paragraphe entrent dans la page.", show=[{"id": "p", "label": "En attente…"}]),
        wait(600), line(7),
        scene(say="Toute la page est lue : c'est le moment d'exécuter le script.",
              hud=[hud("body lu", "oui", "g"), hud("script", "exécuté", "g")], set=[{"id": "js", "label": None}]),
        send(["js", "moteur"], kind="read", tone="y", label="script.js"),
        send(["moteur", "p"], label="#compteur", reply="trouvé", tone="g",
             explain=["Le moteur cherche `#compteur`…", "… il existe : la recherche le trouve."]),
        scene(say="L'élément est trouvé : son texte change, sans erreur.",
              set=[{"id": "p", "label": "47 emprunts aujourd'hui", "tone": "g"}]),
        line(0), wait(2400),
    ],
})

lesson = {
    "format": "bl-scenes/0.3", "id": "js-in-page", "title": "Le JavaScript dans une page", "lang": "fr", "kit": "feuillete",
    "legend": [{"tone": "b", "label": "page affichée"}, {"tone": "y", "label": "fichier JavaScript"},
               {"tone": "r", "label": "null, erreur"}, {"tone": "g", "label": "trouvé"}],
    "entities": ents, "steps": steps,
}
write(lesson, *outputs(HERE, "in-page.scene.json", "js-in-page"))
