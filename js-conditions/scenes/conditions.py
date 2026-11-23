"""Scènes du bit « Décider : les conditions en JavaScript » (courses-web-basics/js-conditions), kit Feuilleté.

Dessin, une règle par sorte (le même pour tout le stack JavaScript) :
- une valeur = un bloc « fichier » au sol ; un nombre est bleu (b), son nom en titre, sa valeur en ligne d'action ;
- une comparaison (une condition) = un bloc pervenche (v) qui porte la question ;
- un texte est jaune (y) : `"5"` n'est pas `5` ;
- un bloc de code (ce qu'exécute un if, un else) = un bloc « programme » neutre (n) ; ce qu'il affiche en ligne d'action ;
- la réponse d'une comparaison est verte (g) pour true, rose (r) pour false : paquets, encarts et conditions déjà testées.
Ce qui est sauté est estompé (dim). Lecture de bas en haut : la valeur devant, la condition, puis les blocs derrière.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import G, L, scene, send, wait, write, hud

ents = [
    # étape 1
    {"id": "age", "kind": "file", "at": G(-5, 8), "tone": "b", "title": "age", "label": "20",
     "detail": "Une variable `age` qui contient un **nombre**."},
    {"id": "dix8", "kind": "file", "at": G(5, 8), "tone": "b", "title": "18"},
    {"id": "cmp", "kind": "node", "at": G(0, 0), "size": [2.0, 2.0, 1.0], "tone": "v", "title": "age >= 18", "icon": ">=",
     "detail": "Une **comparaison** pose une question au moteur ; il répond par un **booléen** : `true` ou `false`."},
    {"id": "rep", "kind": "file", "at": G(0, -8), "tone": "g", "title": "true"},
    # étape 2
    {"id": "age2", "kind": "file", "at": G(0, 9), "tone": "b", "title": "age", "label": "20"},
    {"id": "cond", "kind": "node", "at": G(0, 0), "size": [2.0, 2.0, 1.0], "tone": "v", "title": "if (age >= 18)", "icon": "?",
     "detail": "Le `if` évalue la comparaison entre parenthèses : `true`, son bloc s'exécute ; `false`, c'est celui du `else`."},
    {"id": "bif", "kind": "program", "at": G(-5, -8), "tone": "n", "title": "bloc du if",
     "detail": "Le bloc entre les accolades du `if` : `console.log(\"Majeur\")`."},
    {"id": "belse", "kind": "program", "at": G(5, -8), "tone": "n", "title": "bloc du else",
     "detail": "Le bloc entre les accolades du `else` : `console.log(\"Mineur\")`."},
    # étape 3
    {"id": "age3", "kind": "file", "at": G(-13, 7), "tone": "b", "title": "age", "label": "70"},
    {"id": "t1", "kind": "node", "at": G(-8, 0), "size": [1.8, 1.8, 0.9], "tone": "v", "title": "age < 12"},
    {"id": "t2", "kind": "node", "at": G(-2.5, 0), "size": [1.8, 1.8, 0.9], "tone": "v", "title": "else if (age < 18)"},
    {"id": "t3", "kind": "node", "at": G(3, 0), "size": [1.8, 1.8, 0.9], "tone": "v", "title": "else if (age < 65)"},
    {"id": "t4", "kind": "node", "at": G(8.5, 0), "size": [1.8, 1.8, 0.9], "tone": "n", "title": "else"},
    {"id": "b1", "kind": "program", "at": G(-8, -8), "tone": "n", "title": "\"enfant\""},
    {"id": "b2", "kind": "program", "at": G(-2.5, -8), "tone": "n", "title": "\"jeune\""},
    {"id": "b3", "kind": "program", "at": G(3, -8), "tone": "n", "title": "\"adulte\""},
    {"id": "b4", "kind": "program", "at": G(8.5, -8), "tone": "n", "title": "\"senior\""},
    # étape 4
    {"id": "age4", "kind": "file", "at": G(0, 9), "tone": "b", "title": "age", "label": "70",
     "detail": "Un visiteur de 70 ans : il n'a **pas** entre 18 et 64 ans."},
    {"id": "ca", "kind": "node", "at": G(-5, 0), "size": [1.9, 1.9, 0.9], "tone": "v", "title": "18 <= age",
     "detail": "Le moteur lit `18 <= age < 65` de gauche à droite : d'abord cette comparaison."},
    {"id": "cb", "kind": "node", "at": G(5, 0), "size": [1.9, 1.9, 0.9], "tone": "v", "title": "(…) < 65",
     "detail": "Puis il compare **la réponse** de la première, `true` ou `false`, à 65."},
    {"id": "res4", "kind": "file", "at": G(0, -8), "tone": "g", "title": "true"},
    {"id": "et", "kind": "node", "at": G(0, -8), "size": [1.9, 1.9, 0.9], "tone": "v", "title": "&&", "icon": "&&",
     "detail": "`&&` (et) vaut `true` seulement si **les deux** conditions sont vraies ; `||` (ou), si l'une au moins l'est ; `!` (non) inverse."},
    # étape 5
    {"id": "txt5", "kind": "file", "at": G(-5, 8), "tone": "y", "title": "\"5\"", "label": "texte",
     "detail": "Un **texte** qui ressemble à un nombre, comme ce que rend `prompt()`."},
    {"id": "num5", "kind": "file", "at": G(5, 8), "tone": "b", "title": "5", "label": "nombre"},
    {"id": "eq", "kind": "node", "at": G(0, 0), "size": [2.0, 2.0, 1.0], "tone": "v", "title": "\"5\" == 5", "icon": "==",
     "detail": "Deux égalités : `==` convertit les valeurs avant de comparer, `===` compare aussi le **type**."},
    {"id": "res5", "kind": "file", "at": G(0, -8), "tone": "g", "title": "true"},
]
steps = []

# ---------- 1. une comparaison rend true ou false
Q, R = "question posée", "réponse"
steps.append({
    "id": "comparer", "label": "Comparer", "title": "Une comparaison répond true ou false",
    "body": ["Une comparaison pose une question au moteur, qui répond par un booléen. Un seul `=` ne pose aucune question."],
    "hud": [{"label": Q, "value": "—"}, {"label": R, "value": "—"}],
    "show": ["age", "dix8", "cmp"],
    "links": [L("age", "cmp"), L("dix8", "cmp")],
    "script": [
        wait(800),
        send(["age", "cmp"], tone="b", label="20"),
        send(["dix8", "cmp"], tone="b", label="18"),
        scene(say="`age >= 18` pose une question : 20 est-il plus grand ou égal à 18 ? Le moteur répond `true`.",
              show=[{"id": "rep", "title": "true", "tone": "g"}], link=[L("cmp", "rep")],
              hud=[hud(Q, "oui", None), hud(R, "true", "g")]),
        wait(1500),
        scene(say="`age` vaut maintenant 15.", hide=["rep"], set=[{"id": "age", "label": "15"}], hud=[hud(R, "—", None)]),
        send(["age", "cmp"], tone="b", label="15"),
        scene(say="La même question répond `false` : une comparaison rend toujours un **booléen**.",
              show=[{"id": "rep", "title": "false", "tone": "r"}], link=[L("cmp", "rep")], hud=[hud(R, "false", "r")]),
        wait(1500),
        scene(say="Avec un seul `=`, `age = 18` ne compare rien…", hide=["rep"],
              set=[{"id": "cmp", "title": "age = 18", "icon": "="}], hud=[hud(Q, "non", "r"), hud(R, "aucune", None)]),
        send(["dix8", "cmp", "age"], tone="b", label="18"),
        scene(say="… il **range** 18 dans `age`. Pour comparer, il faut `===`, `>=`, `<`…",
              set=[{"id": "age", "label": "18 (rangé)"}]),
        wait(2400),
    ],
})

# ---------- 2. if / else : un seul bloc
C = "condition"
steps.append({
    "id": "if-else", "label": "if / else", "title": "Un seul des deux blocs s'exécute",
    "body": ["Le `if` évalue sa condition ; selon la réponse, il exécute son bloc ou celui du `else`, jamais les deux."],
    "hud": [{"label": C, "value": "—"}, {"label": "console", "value": "—"}],
    "show": ["age2", "cond", "bif", "belse"],
    "links": [L("age2", "cond"), L("cond", "bif", label="true"), L("cond", "belse", label="false")],
    "script": [
        wait(800),
        send(["age2", "cond"], tone="b", label="20"),
        scene(say="Le moteur évalue la condition : `20 >= 18` vaut `true`.", hud=[hud(C, "true", "g")]),
        wait(700),
        send(["cond", "bif"], tone="g", label="true"),
        scene(say="`true` : le bloc du `if` s'exécute, celui du `else` est sauté.",
              set=[{"id": "bif", "label": "affiche Majeur"}, {"id": "belse", "dim": True}], hud=[hud("console", "Majeur", None)]),
        wait(1500),
        scene(say="On rejoue avec `age` à 15.",
              set=[{"id": "age2", "label": "15"}, {"id": "bif", "label": None}, {"id": "belse", "dim": False}],
              hud=[hud(C, "—", None), hud("console", "—", None)]),
        send(["age2", "cond"], tone="b", label="15"),
        scene(say="`15 >= 18` vaut `false`.", hud=[hud(C, "false", "r")]),
        wait(600),
        send(["cond", "belse"], tone="r", label="false"),
        scene(say="Cette fois, seul le bloc du `else` s'exécute : un seul des deux, jamais les deux.",
              set=[{"id": "belse", "label": "affiche Mineur"}, {"id": "bif", "dim": True}], hud=[hud("console", "Mineur", None)]),
        wait(2400),
    ],
})

# ---------- 3. else if : la première condition vraie gagne
T = ["t1", "t2", "t3"]
steps.append({
    "id": "else-if", "label": "else if", "title": "Le premier cas vrai, puis on s'arrête",
    "body": ["Le moteur teste les conditions dans l'ordre et exécute le premier bloc dont la condition est vraie."],
    "hud": [{"label": "age", "value": 70, "tone": "b"}, {"label": "console", "value": "—"}],
    "labels": "left",
    "show": ["age3", "t1", "t2", "t3", "t4", "b1", "b2", "b3", "b4"],
    "links": [L("age3", "t1"), L("t1", "t2"), L("t2", "t3"), L("t3", "t4"),
              L("t1", "b1"), L("t2", "b2"), L("t3", "b3"), L("t4", "b4")],
    "script": [
        wait(800),
        send(["age3", "t1"], tone="b", label="70"),
        scene(say="Le moteur teste la première condition : `70 < 12` ? `false`.", set=[{"id": "t1", "tone": "r", "label": "false"}]),
        wait(500),
        send(["t1", "t2"], tone="r"),
        scene(say="Il passe à la suivante : `70 < 18` ? `false`.", set=[{"id": "t2", "tone": "r", "label": "false"}]),
        wait(400),
        send(["t2", "t3"], tone="r"),
        scene(say="`70 < 65` ? Toujours `false`.", set=[{"id": "t3", "tone": "r", "label": "false"}]),
        send(["t3", "t4"], tone="r"),
        send(["t4", "b4"], tone="g"),
        scene(say="Aucune n'est vraie : le bloc du `else` s'exécute.",
              set=[{"id": "b4", "label": "affiche senior"}], hud=[hud("console", "senior", None)]),
        wait(1600),
        scene(say="Avec 8 ans, on rejoue.",
              set=[{"id": t, "tone": "v", "label": None} for t in T] + [{"id": "b4", "label": None}, {"id": "age3", "label": "8"}],
              hud=[hud("age", 8, "b"), hud("console", "—", None)]),
        send(["age3", "t1"], tone="b", label="8"),
        scene(say="`8 < 12` vaut `true` : la première condition gagne.", set=[{"id": "t1", "tone": "g", "label": "true"}]),
        send(["t1", "b1"], tone="g"),
        scene(say="Son bloc s'exécute, et le moteur s'arrête là : les autres cas ne sont même pas testés.",
              set=[{"id": "b1", "label": "affiche enfant"}] + [{"id": i, "dim": True} for i in ["t2", "t3", "t4", "b2", "b3", "b4"]],
              hud=[hud("console", "enfant", None)]),
        wait(2600),
    ],
})

# ---------- 4. un intervalle : 18 <= age < 65 contre &&
A = "attendu"
steps.append({
    "id": "intervalle", "label": "et, ou, non", "title": "Un intervalle se lit en deux comparaisons",
    "body": ["`18 <= age < 65` ne pose pas la question des maths : le moteur compare `true` à 65. Avec `&&`, chaque comparaison répète `age`."],
    "hud": [{"label": A, "value": "false", "tone": "r"}, {"label": R, "value": "—"}],
    "show": ["age4", "ca", "cb"],
    "links": [L("age4", "ca"), L("ca", "cb")],
    "script": [
        wait(800),
        send(["age4", "ca"], tone="b", label="70"),
        scene(say="Le moteur lit `18 <= age < 65` de gauche à droite : d'abord `18 <= 70`, qui vaut `true`.",
              set=[{"id": "ca", "tone": "g", "label": "true"}]),
        wait(600),
        send(["ca", "cb"], tone="g", label="true"),
        scene(say="Puis il compare **ce `true`** à 65. Dans un calcul, `true` vaut 1, et `1 < 65`…",
              set=[{"id": "cb", "title": "true < 65"}]),
        wait(500),
        scene(say="… vaut `true`. On attendait `false` : le visiteur de 70 ans passe, sans aucune erreur.",
              show=[{"id": "res4", "title": "true", "tone": "g"}], link=[L("cb", "res4")], hud=[hud(R, "true", "g")]),
        wait(1800),
        scene(say="La bonne écriture répète `age` dans chaque comparaison, et les relie par `&&` (et).",
              hide=["res4"], unlink=[L("ca", "cb")],
              set=[{"id": "ca", "title": "age >= 18", "tone": "v", "label": None},
                   {"id": "cb", "title": "age < 65", "tone": "v", "label": None}],
              hud=[hud(R, "—", None)], ms=900),
        scene(show=["et"], link=[L("age4", "cb"), L("ca", "et"), L("cb", "et")], ms=500),
        send(["age4", "ca"], tone="b", label="70"),
        scene(say="`70 >= 18` vaut `true`…", set=[{"id": "ca", "tone": "g", "label": "true"}]),
        send(["age4", "cb"], tone="b", label="70"),
        scene(say="… et `70 < 65` vaut `false`.", set=[{"id": "cb", "tone": "r", "label": "false"}]),
        send(["ca", "et"], tone="g", label="true"),
        send(["cb", "et"], tone="r", label="false"),
        scene(say="`&&` ne vaut `true` que si **les deux** sont vraies : ici `false`, la bonne réponse.",
              set=[{"id": "et", "tone": "r", "label": "false"}], hud=[hud(R, "false", "r")]),
        wait(2600),
    ],
})

# ---------- 5. == convertit, === compare aussi le type
TY = "types comparés"
steps.append({
    "id": "egalite", "label": "== ou ===", "title": "== convertit, === compare aussi le type",
    "body": ["`==` convertit le texte en nombre avant de comparer ; `===` compare la valeur **et** le type, sans rien convertir."],
    "hud": [{"label": TY, "value": "—"}, {"label": R, "value": "—"}],
    "show": ["txt5", "num5", "eq"],
    "links": [L("txt5", "eq"), L("num5", "eq")],
    "script": [
        wait(800),
        send(["txt5", "eq"], tone="y", label="\"5\""),
        send(["num5", "eq"], tone="b", label="5"),
        scene(say="`==` commence par **convertir** : le texte `\"5\"` devient le nombre 5.",
              set=[{"id": "txt5", "title": "5", "tone": "b", "label": "converti"}], hud=[hud(TY, "non", None)]),
        wait(700),
        scene(say="Puis il compare 5 et 5 : `true`. La différence entre texte et nombre a disparu.",
              show=[{"id": "res5", "title": "true", "tone": "g"}], link=[L("eq", "res5")], hud=[hud(R, "true", "g")]),
        wait(1800),
        scene(say="Même question avec `===`.", hide=["res5"],
              set=[{"id": "txt5", "title": "\"5\"", "tone": "y", "label": "texte"},
                   {"id": "eq", "title": "\"5\" === 5", "icon": "==="}],
              hud=[hud(TY, "—", None), hud(R, "—", None)], ms=900),
        send(["txt5", "eq"], tone="y", label="\"5\""),
        send(["num5", "eq"], tone="b", label="5"),
        scene(say="`===` compare aussi le **type** : un texte d'un côté, un nombre de l'autre.", hud=[hud(TY, "oui", None)]),
        wait(600),
        scene(say="Réponse : `false`, sans rien convertir. La différence reste visible.",
              show=[{"id": "res5", "title": "false", "tone": "r"}], link=[L("eq", "res5")], hud=[hud(R, "false", "r")]),
        wait(2600),
    ],
})

lesson = {
    "format": "bl-scenes/0.3", "id": "js-conditions", "title": "Les conditions en JavaScript", "lang": "fr", "kit": "feuillete",
    "legend": [{"tone": "b", "label": "nombre"}, {"tone": "y", "label": "texte"}, {"tone": "v", "label": "condition"},
               {"tone": "g", "label": "true"}, {"tone": "r", "label": "false"}],
    "entities": ents, "steps": steps,
}
write(lesson, *outputs(HERE, "conditions.scene.json", "js-conditions"))
