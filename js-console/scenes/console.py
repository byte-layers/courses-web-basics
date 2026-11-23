"""Scènes du bit « La console JavaScript » (courses-web-basics/js-console), kit Feuilleté.

Dessin, une règle par sorte (le même pour tout le stack JavaScript) :
- le navigateur = un plateau neutre (n) qui porte ce qui tourne dedans ;
- la console = un bloc encre (i, >_) devant, là où l'on tape ; le moteur JavaScript = un bloc pervenche (v, JS) derrière,
  qui exécute ; vous = un acteur devant le navigateur ;
- une valeur = un bloc « fichier » posé au sol : un texte est jaune (y), un nombre bleu (b) ;
- les réponses de la console prennent la couleur de leur sorte : une valeur verte (g), pas de valeur (undefined) neutre (n),
  une erreur rose (r).
Grille d'écran G(sx, sy) : vous (-6, 7), console (-2,3 ; 1,4), moteur (2,3 ; -1,4), en diagonale pour que les cartes ne s'empilent pas (sur le plateau).
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


ents = [
    {"id": "nav", "kind": "layer", "at": G(0, 0), "size": [5.2, 5.2, 0.55], "tone": "n", "title": "navigateur",
     "detail": "Le **navigateur** (Chrome, Firefox, Safari, Edge) dessine les pages, et il contient aussi un moteur JavaScript."},
    {"id": "console", "kind": "node", "in": "nav", "at": rel(-2.3, 1.4), "tone": "i", "title": "console", "icon": ">_",
     "detail": "La **console** fait partie des outils de développement du navigateur (F12). On y tape une instruction, le moteur répond sur la ligne suivante."},
    {"id": "moteur", "kind": "node", "in": "nav", "at": rel(2.3, -1.4), "tone": "v", "title": "moteur JavaScript", "icon": "JS",
     "detail": "Le **moteur JavaScript** lit une instruction et l'exécute tout de suite : c'est un **interpréteur**."},
    {"id": "vous", "kind": "actor", "at": G(-6, 7), "label": "vous"},
    # étape 3 : des valeurs
    {"id": "v5", "kind": "file", "at": G(-5, 8), "tone": "y", "title": "\"5\"",
     "detail": "Entre guillemets, `\"5\"` est un **texte** (type `string`) qui contient un chiffre."},
    {"id": "v3", "kind": "file", "at": G(5, 8), "tone": "b", "title": "3",
     "detail": "Sans guillemets, `3` est un **nombre** (type `number`)."},
    {"id": "plus", "kind": "program", "at": G(0, 0), "tone": "v", "title": "+",
     "detail": "Le `+` regarde le type de ses deux valeurs : deux nombres, il additionne ; un texte d'un côté, il **assemble**."},
    {"id": "res", "kind": "file", "at": G(0, -8), "tone": "y", "title": "\"53\""},
]
BASE = ["nav", "console", "moteur", "vous"]
LINKS = [L("vous", "console"), L("console", "moteur")]
steps = []

# ---------- 1. un moteur dans le navigateur
steps.append({
    "id": "moteur", "label": "Le moteur", "title": "La console parle au moteur JavaScript",
    "body": ["Tu tapes une instruction dans la console : le moteur JavaScript du navigateur l'exécute et répond aussitôt."],
    "labels": "left", "show": BASE, "links": LINKS,
    "script": [
        wait(800),
        send(["vous", "console", "moteur"], label="6 * 7", reply="42", tone="b",
             explain=["Tu tapes `6 * 7` dans la console et tu appuies sur Entrée.",
                      "La console passe l'instruction au **moteur JavaScript**, dans le navigateur.",
                      "Le moteur l'exécute tout de suite et répond : `42`."]),
        scene(say="La réponse s'affiche sur la ligne suivante : rien à installer, rien à compiler.",
              set=[{"id": "console", "label": "42"}]),
        wait(1300),
        send(["vous", "console", "moteur"], label="\"Bon\" + \"jour\"", reply="\"Bonjour\"", tone="y",
             explain=["Tu tapes deux textes reliés par un `+`.",
                      "Le moteur reçoit l'instruction.",
                      "Entre deux textes, le `+` assemble : `\"Bonjour\"`."]),
        scene(say="Entre deux textes, le `+` ne calcule pas : il assemble.",
              set=[{"id": "console", "label": "\"Bonjour\""}]),
        wait(1500),
        scene(say="Tu recharges la page : la console repart vide, rien n'a été enregistré.",
              set=[{"id": "console", "label": None, "note": "vide après rechargement"}], ms=900),
        wait(2200),
    ],
})

# ---------- 2. trois sortes de réponses
R = "réponse"
steps.append({
    "id": "reponses", "label": "Trois réponses", "title": "Une valeur, undefined ou une erreur",
    "body": ["Chaque instruction reçoit une réponse, et il n'en existe que trois sortes."],
    "hud": [{"label": R, "value": "—"}, {"label": "message rouge", "value": "—"}],
    "labels": "left", "show": BASE, "links": LINKS,
    "script": [
        wait(700),
        send(["vous", "console", "moteur"], label="2 + 3", reply="5", tone="g"),
        scene(say="`2 + 3` : le moteur répond par une **valeur**, le résultat.",
              set=[{"id": "console", "label": "5"}], hud=[hud(R, "une valeur", "g"), hud("message rouge", "non", None)]),
        wait(1300),
        send(["vous", "console", "moteur"], label="console.log(\"Salut\")", reply="undefined", tone="n"),
        scene(say="`console.log` écrit `Salut`, mais ne rend rien : la réponse est `undefined`, « pas de valeur ».",
              set=[{"id": "console", "label": "Salut, puis undefined"}], hud=[hud(R, "undefined", "n")]),
        wait(1500),
        send(["vous", "console", "moteur"], label="Bonjour", reply="ReferenceError", tone="r"),
        scene(say="`Bonjour` sans guillemets : le moteur cherche une variable de ce nom, et répond par une **erreur** en rouge.",
              set=[{"id": "console", "label": "Bonjour is not defined"}],
              hud=[hud(R, "une erreur", "r"), hud("message rouge", "oui", "r")]),
        wait(1500),
        send(["vous", "console", "moteur"], label="\"Bonjour", reply="SyntaxError", tone="r"),
        scene(say="`\"Bonjour` : le texte n'est jamais refermé. Le moteur ne sait pas lire la ligne : une **erreur de syntaxe**.",
              set=[{"id": "console", "label": "SyntaxError"}]),
        wait(1500),
        send(["vous", "console", "moteur"], label="3,5 + 1", reply="6", tone="g"),
        scene(say="Le pire : `3,5 + 1` répond `6`, sans message. La virgule n'est pas un séparateur décimal.",
              set=[{"id": "console", "label": "6, sans message"}],
              hud=[hud(R, "une valeur fausse", "g"), hud("message rouge", "non", None)]),
        wait(2400),
    ],
})

# ---------- 3. "5" + 3
steps.append({
    "id": "types", "label": "\"5\" + 3", "title": "Le + regarde le type des valeurs",
    "body": ["Un texte d'un côté, et le `+` assemble au lieu d'additionner."],
    "hud": [{"label": "à gauche", "value": "texte", "tone": "y"}, {"label": "à droite", "value": "nombre", "tone": "b"}],
    "show": ["v5", "v3", "plus"],
    "links": [L("v5", "plus"), L("v3", "plus")],
    "script": [
        wait(900),
        scene(say="Deux valeurs : `\"5\"`, entre guillemets, est un **texte** ; `3` est un **nombre**.",
              set=[{"id": "v5", "label": "texte"}, {"id": "v3", "label": "nombre"}]),
        wait(1200),
        send(["v5", "plus"], tone="y"),
        send(["v3", "plus"], tone="b"),
        scene(say="Le `+` voit un texte d'un côté : il **assemble**, `\"5\" + 3` donne `\"53\"`.",
              show=[{"id": "res", "title": "\"53\"", "tone": "y"}], link=[L("plus", "res")],
              set=[{"id": "plus", "label": "assemble"}]),
        wait(1800),
        scene(say="`Number(\"5\")` convertit le texte en nombre : le `5` perd ses guillemets.",
              hide=["res"], set=[{"id": "v5", "title": "5", "tone": "b", "label": "Number(\"5\")"}, {"id": "plus", "label": None}],
              hud=[hud("à gauche", "nombre", "b")], ms=900),
        wait(1200),
        send(["v5", "plus"], tone="b"),
        send(["v3", "plus"], tone="b"),
        scene(say="Deux nombres : cette fois, le `+` **additionne**, `5 + 3` donne `8`.",
              show=[{"id": "res", "title": "8", "tone": "b"}], link=[L("plus", "res")],
              set=[{"id": "plus", "label": "additionne"}]),
        wait(2400),
    ],
})

lesson = {
    "format": "bl-scenes/0.3", "id": "js-console", "title": "La console JavaScript", "lang": "fr", "kit": "feuillete",
    "legend": [{"tone": "g", "label": "une valeur"}, {"tone": "n", "label": "pas de valeur"}, {"tone": "r", "label": "une erreur"},
               {"tone": "y", "label": "texte"}, {"tone": "b", "label": "nombre"}],
    "entities": ents, "steps": steps,
}
write(lesson, *outputs(HERE, "console.scene.json", "js-console"))
