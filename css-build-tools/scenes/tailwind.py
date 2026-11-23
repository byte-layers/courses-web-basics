"""Scènes 2D (kit plan) du bit « Tailwind, et pourquoi le CSS se compile » (css-build-tools).

Quatre étapes dans assets/tailwind.scene.json :
  utilitaires  (section « Des classes utilitaires ») : une classe, une propriété ; le style naît de leur assemblage.
  build        (section « Le CSS produit ») : la commande lit input.css et les classes du HTML, écrit output.css,
               que la page charge.
  photo        (section « Le piège ») : une classe ajoutée après le traitement n'a pas de règle ; --watch relance.
  bundle       (section « Une famille d'outils ») : des modules qui s'importent les uns les autres ; un outil de
               build les suit depuis main.js et les rassemble en deux fichiers, le bundle, que charge le navigateur.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; entités au premier niveau.
Dessin : un fichier = file ; Tailwind = node ; le navigateur = layer qui porte le bouton affiché.
Couleurs : y ce que vous écrivez (HTML, input.css), v Tailwind, g le fichier produit (output.css) ;
le bouton prend la couleur de son fond (n sans fond, b bleu, r rose).
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import L, hud, scene, send, wait, write


def r(v):
    return round(v, 3)


def ent(id, kind, cx, cy, w, h, tone=None, **kw):
    d = {"id": id, "kind": kind, "at": [r(cx), r(cy)], "size": [r(w), r(h), 1]}
    if tone: d["tone"] = tone
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


# ── Étape 1 : une classe, une propriété ───────────────────────────────────────────────────────────────────────
ents = [ent("lien", "node", 0, 0, 4.6, 0.9, "n", title="Me contacter",
            detail="Un lien `a`, qu'on habille en bouton avec des classes utilitaires, sans écrire de feuille de style."),
        ent("attr", "file", 0, 2.6, 13.0, 1.1, "y", title='class=""',
            detail="L'attribut `class` du lien, dans le HTML : c'est là que s'écrit tout le style.")]


def add(cls, prop, say, size=None, tone=None, classes=""):
    ch = {"id": "lien"}
    if size: ch["size"] = [size[0], size[1], 1]
    if tone: ch["tone"] = tone
    return scene(say=say, hud=[hud("classe", cls, "g"), hud("CSS écrit", prop, "g")], set=[ch, {"id": "attr", "title": f'class="{classes}"'}], ms=800)


utilitaires = {
    "id": "utilitaires", "label": "Une classe", "title": "Une classe, une propriété",
    "body": ["Un lien sans style. On lui ajoute des classes utilitaires, une à une."],
    "show": ["lien", "attr"],
    "hud": [{"label": "classe", "value": "—"}, {"label": "CSS écrit", "value": "—"}],
    "script": [
        wait(1000),
        add("px-4", "padding-inline: 1rem", "px-4 écrit une seule propriété : 16 px de padding à gauche et à droite.",
            size=(6.4, 0.9), classes="px-4"),
        wait(1100),
        add("py-2", "padding-block: 0.5rem", "py-2 : 8 px de padding en haut et en bas.",
            size=(6.4, 1.6), classes="px-4 py-2"),
        wait(1100),
        add("bg-blue-700", "background: bleu 700", "bg-blue-700 : un fond, la nuance 700 de la palette bleue.",
            tone="b", classes="px-4 py-2 bg-blue-700"),
        wait(1100),
        add("text-white", "color: #fff", "text-white : le texte en blanc. Le style naît de l'assemblage, écrit dans le HTML.",
            classes="px-4 py-2 bg-blue-700 text-white"),
        wait(2600),
    ],
}

# ── Étapes 2 et 3 : le traitement ─────────────────────────────────────────────────────────────────────────────
ents += [
    ent("html", "file", -12.0, -2.2, 6.4, 1.8, "y", title="index.html", note="vos classes",
        detail="Le HTML, avec les classes utilitaires dans ses attributs `class`."),
    ent("input", "file", -12.0, 2.2, 6.4, 1.8, "y", title="input.css", note='@import "tailwindcss";',
        detail="Le fichier d'entrée tient en une ligne : l'import de Tailwind."),
    ent("tw", "node", -2.6, 0, 6.0, 2.4, "v", title="Tailwind", sub="npx @tailwindcss/cli",
        detail="Tailwind **tourne sur votre machine**, comme un programme : il lit vos fichiers et écrit un fichier CSS."),
    ent("output", "file", 6.4, 0, 6.4, 1.8, "g", title="output.css",
        detail="Le fichier produit : du CSS ordinaire, lisible, avec seulement les règles des classes trouvées."),
    ent("nav", "layer", 15.6, 0, 7.6, 6.0, "n", title="navigateur"),
    ent("bouton", "node", 15.6, 0.6, 5.2, 1.5, "b", title="Me contacter"),
]
PIPE = [L("html", "tw"), L("input", "tw"), L("tw", "output"), L("output", "nav")]

build = {
    "id": "build", "label": "Le traitement", "title": "Du HTML et d'une ligne de CSS au fichier que charge la page",
    "body": ["Le HTML contient les classes du bouton ; `input.css`, l'import de Tailwind. On lance la commande."],
    "show": ["html", "input", "tw", {"id": "output", "dim": True, "note": "pas encore écrit"}, "nav"],
    "links": PIPE,
    "script": [
        wait(900),
        send(["input", "tw"], kind="read", label="@import",
             explain=["La commande lit `input.css` : une seule ligne, l'import de Tailwind."]),
        send(["html", "tw"], kind="read", label="les classes",
             explain=["Puis elle parcourt les fichiers du dossier à la recherche de noms de classes."]),
        scene(say="Elle trouve quatre classes : px-4, py-2, bg-blue-700, text-white.",
              set=[{"id": "tw", "label": "4 classes trouvées"}]),
        wait(800),
        scene(say="Elle écrit output.css : les règles de ces quatre classes, et aucune autre.",
              set=[{"id": "output", "dim": False, "note": "4 règles"}]),
        wait(800),
        send(["output", "nav"], label="<link>",
             explain=["La page charge `output.css` avec son `link` : c'est lui que lit le navigateur, pas `input.css`."]),
        scene(say="Le bouton s'affiche avec son style.", show=["bouton"]),
        wait(2400),
    ],
}

photo = {
    "id": "photo", "label": "Une photographie", "title": "output.css, une photographie du moment du traitement",
    "body": ["Le traitement a tourné une fois : `output.css` contient les quatre classes du bouton."],
    "show": ["html", "input", "tw", {"id": "output", "note": "4 règles"}, "nav", "bouton"],
    "links": PIPE,
    "hud": [{"label": "output.css", "value": "à jour", "tone": "g"}, {"label": "bouton", "value": "fond bleu"}],
    "script": [
        wait(1000),
        scene(say="Après le traitement, on change le bouton : bg-pink-600 et px-6 remplacent bg-blue-700 et px-4.",
              set=[{"id": "html", "note": "+ bg-pink-600 px-6"}], hud=[hud("output.css", "périmé", "r")]),
        wait(900),
        send(["output", "nav"], label="<link>"),
        scene(say="output.css n'a aucune règle pour ces classes : le bouton perd son fond et son padding, sans message.",
              hud=[hud("bouton", "ni fond ni padding", "r")],
              set=[{"id": "bouton", "tone": "n", "size": [4.6, 0.9, 1]}]),
        wait(1600),
        scene(say="En mode surveillance, avec --watch, Tailwind refait le traitement à chaque enregistrement.",
              set=[{"id": "tw", "label": "--watch"}]),
        send(["html", "tw"], kind="read", label="les classes"),
        send(["tw", "output"], label="+ 2 règles"),
        scene(say="output.css contient maintenant les nouvelles classes : le bouton retrouve un fond, rose cette fois.",
              hud=[hud("output.css", "à jour", "g"), hud("bouton", "fond rose", "g")],
              set=[{"id": "output", "note": "règles à jour"},
                   {"id": "bouton", "tone": "r", "size": [6.0, 1.5, 1]}]),
        wait(2400),
    ],
}

# ── Étape 4 : des modules au bundle ──────────────────────────────────────────────────────────────────────────
MODS = [("m-menu", "menu.js", -3.6), ("m-api", "api.js", 0.0), ("m-css", "style.css", 3.6)]
ents += [ent("m-main", "file", -18.0, 0, 5.4, 1.6, "y", title="main.js", note="le point de départ",
             detail="Le fichier de départ du projet. Il **importe** les autres, qui peuvent en importer d'autres à leur tour.")]
ents += [ent(mid, "file", -10.0, y, 5.4, 1.6, "y", title=t) for mid, t, y in MODS]
ents += [
    ent("b-tool", "node", -1.0, 0, 6.4, 2.4, "v", title="outil de build", sub="Webpack, Vite, Parcel…",
        detail="Un **outil de build** part du fichier de départ, suit chaque import, et rassemble tout en quelques fichiers prêts pour le navigateur."),
    ent("b-js", "file", 8.0, -1.6, 6.0, 1.6, "g", title="main.3f9a.js",
        detail="Le *bundle* : tous les scripts réunis en un seul fichier, compressé. Le code dans le nom change à chaque version, pour que le navigateur ne garde pas l'ancienne en cache."),
    ent("b-css", "file", 8.0, 1.6, 6.0, 1.6, "g", title="main.8c1d.css"),
    ent("b-nav", "layer", 17.0, 0, 6.4, 6.0, "n", title="navigateur"),
]
BUNDLE_LINKS = [L("m-main", mid, label="import") for mid, _, _ in MODS]

bundle = {
    "id": "bundle", "label": "Le bundle", "title": "Des modules qui s'importent, un bundle pour le navigateur",
    "body": ["Un petit projet : `main.js` importe un menu, un appel au serveur et une feuille de style."],
    "show": ["m-main"],
    "script": [
        wait(900),
        scene(say="Vos fichiers s'importent les uns les autres : main.js a besoin de menu.js, d'api.js et de style.css.",
              show=[m for m, _, _ in MODS], link=BUNDLE_LINKS),
        wait(1300),
        scene(say="L'outil de build part de main.js et suit chaque import.", show=["b-tool"],
              link=[L(mid, "b-tool") for mid, _, _ in MODS]),
        send(["m-main", "m-api", "b-tool"], kind="read", label="import"),
        scene(say="Il rassemble tout en deux fichiers, compressés : le bundle.", show=["b-js", "b-css"],
              link=[L("b-tool", "b-js"), L("b-tool", "b-css")]),
        wait(1100),
        scene(say="La page charge ces deux fichiers, pas les quatre que vous avez écrits.", show=["b-nav"],
              link=[L("b-js", "b-nav"), L("b-css", "b-nav")]),
        send(["b-js", "b-nav"], label="<script>"),
        scene(say="Comme avec Tailwind, ce que reçoit le navigateur n'est pas ce que vous avez écrit.",
              set=[{"id": "b-nav", "label": "2 fichiers prêts"}]),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "css-build-tools",
    "title": "Tailwind, et pourquoi le CSS se compile", "lang": "fr", "kit": "plan",
    "legend": [{"tone": "y", "label": "ce que vous écrivez"}, {"tone": "v", "label": "l'outil (Tailwind…)"}, {"tone": "g", "label": "fichier produit"}],
    "entities": ents, "steps": [utilitaires, build, photo, bundle],
}
write(lesson, *outputs(HERE, "tailwind.scene.json", "layout-tailwind"))
