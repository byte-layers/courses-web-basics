"""Scènes du bit « Répéter : tableaux et boucles » (courses-web-basics/js-arrays-loops), kit Feuilleté.

Dessin, une règle par sorte (le même pour tout le stack JavaScript) :
- une valeur = un bloc « fichier » au sol ; un texte est jaune (y), un nombre bleu (b) ;
- un tableau = une rangée de cases (blocs fichier) de gauche à droite ; chaque case porte sa valeur en titre et son index
  en ligne d'action ([0], [1]…) ;
- ce qui lit (une expression, le compteur i, l'accumulateur) est devant la rangée ; un paquet de lecture (read) va de lui
  à la case, et revient avec la valeur ;
- une case déjà parcourue passe en vert (g) ; ce qui est faux ou absent est rose (r) ou neutre (n, undefined).
Grille d'écran G(sx, sy) : cases sur sy = 0, de sx = -10 à 10 (pas de 5) ; lecteur et compteur devant, sy = 9.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import G, L, scene, send, wait, write, hud

FRUITS = ["Pomme", "Banane", "Cerise", "Mangue", "Poire", "Kiwi"]
XS = [-10, -5, 0, 5, 10, 15]
# Essai d'une rangée le long d'un axe iso (pour le téléphone) : sur bureau la scène rapetissait, sur 390 px les cartes
# restaient minuscules ; la rangée horizontale est gardée.


def case_at(k):
    return G(XS[k], 0)


def i_at(k):
    return G(XS[k], 9)
ents = []
for i, f in enumerate(FRUITS):
    ents.append({"id": f"c{i}", "kind": "file", "at": case_at(i), "size": [1.9, 1.9, 0.45], "tone": "y",
                 "title": f, "label": f"[{i}]",
                 **({"detail": "Une **case** du tableau `fruits` : sa valeur, et son numéro, l'**index**, qui commence à 0."} if i == 0 else {})})
ents += [
    {"id": "lire", "kind": "program", "at": G(0, 9), "tone": "v", "title": "fruits[0]",
     "detail": "Une **expression** qui lit le tableau : le nom du tableau, puis l'index entre crochets."},
    {"id": "i", "kind": "file", "at": i_at(0), "size": [1.6, 1.6, 0.45], "tone": "b", "title": "i", "label": "0",
     "detail": "Le **compteur** de la boucle `for`. Il sert d'index : `fruits[i]`."},
    # étape 3
    {"id": "p0", "kind": "file", "at": G(-6, 0), "tone": "b", "title": "3", "label": "[0]",
     "detail": "Le tableau `[3, 5, 2]` : trois prix."},
    {"id": "p1", "kind": "file", "at": G(0, 0), "tone": "b", "title": "5", "label": "[1]"},
    {"id": "p2", "kind": "file", "at": G(6, 0), "tone": "b", "title": "2", "label": "[2]"},
    {"id": "total", "kind": "node", "at": G(0, 10), "size": [2.2, 2.2, 1.0], "tone": "b", "title": "total", "label": "0",
     "detail": "L'**accumulateur** : une variable créée avec `let` avant la boucle, à laquelle chaque tour ajoute une valeur."},
    # étape 4
    {"id": "compte", "kind": "file", "at": G(-6, 8), "size": [1.9, 1.9, 0.45], "tone": "b", "title": "compte", "label": "3",
     "detail": "La variable que teste la boucle `while`. Quelque chose dans le bloc doit la changer."},
    {"id": "test", "kind": "node", "at": G(0, 0), "size": [2.0, 2.0, 1.0], "tone": "v", "title": "while (compte > 0)",
     "detail": "`while` (« tant que ») refait le test **avant chaque tour** : vrai, le bloc s'exécute ; faux, la boucle s'arrête."},
    {"id": "bloc", "kind": "program", "at": G(6, 8), "tone": "n", "title": "bloc du while",
     "detail": "Le bloc : `console.log(\"Décollage dans \" + compte);` puis `compte = compte - 1;`."},
    {"id": "sortie", "kind": "program", "at": G(0, -8), "tone": "n", "title": "après la boucle",
     "detail": "La ligne qui suit la boucle : `console.log(\"Décollage !\");`."},
]
CASES = [f"c{i}" for i in range(5)]
steps = []

# ---------- 1. des cases numérotées à partir de 0
LEN = "fruits.length"


def read(k, title, value, say, prev=None):
    return [
        scene(set=[{"id": "lire", "title": title, "label": None}], link=[L("lire", f"c{k}")],
              unlink=[L("lire", f"c{prev}")] if prev is not None else [], ms=400),
        send(["lire", f"c{k}"], kind="read", reply=value, tone="y"),
        scene(say=say, set=[{"id": "lire", "label": value}]),
    ]


steps.append({
    "id": "tableau", "label": "Les cases", "title": "Un tableau : des cases numérotées à partir de 0",
    "body": ["Chaque valeur occupe une case ; on la lit par son numéro, l'index, qui commence à 0."],
    "hud": [{"label": LEN, "value": 5, "tone": "b"}],
    "labels": "left",
    "show": CASES + ["lire"],
    "links": [],
    "script": [
        wait(800),
        *read(0, "fruits[0]", "\"Pomme\"", "`fruits[0]` : la première case porte l'index **0**."),
        wait(1000),
        *read(2, "fruits[2]", "\"Cerise\"", "`fruits[2]` est donc la **troisième** case.", prev=0),
        wait(1000),
        *read(4, "fruits[4]", "\"Poire\"", "Cinq cases, numérotées de 0 à 4 : la dernière est `fruits[length - 1]`.", prev=2),
        wait(1000),
        scene(say="`fruits[5]` : cette case n'existe pas. Pas d'erreur, juste `undefined`.",
              set=[{"id": "lire", "title": "fruits[5]", "label": "undefined", "tone": "n"}], unlink=[L("lire", "c4")]),
        wait(1300),
        scene(say="`fruits.push(\"Kiwi\")` ajoute une case à la fin : `length` passe à 6.",
              show=["c5"], set=[{"id": "lire", "title": "fruits.push(\"Kiwi\")", "label": None, "tone": "v"}],
              hud=[hud(LEN, 6, "b")]),
        wait(2400),
    ],
})

# ---------- 2. la boucle for
TEST = "test i < length"


def tour(k, say=None, first=False):
    acts = []
    move = {"id": "i", "at": i_at(k), "label": str(k)}
    acts.append(scene(say=say if first else None, set=[move], link=[L("i", f"c{k}")],
                      unlink=[] if first else [L("i", f"c{k-1}")], hud=[hud("i", k, "b"), hud(TEST, "true", "g")], ms=700))
    acts.append(send(["i", f"c{k}"], kind="read", reply=FRUITS[k], tone="y"))
    acts.append(scene(say=None if first else say, set=[{"id": f"c{k}", "tone": "g"}], hud=[hud("console", f"case {k} : {FRUITS[k]}", None)]))
    return acts


steps.append({
    "id": "for", "label": "for", "title": "La boucle for avance son compteur, case après case",
    "body": ["Avant chaque tour, la boucle teste `i < fruits.length` ; après chaque tour, `i++` ajoute 1 au compteur."],
    "hud": [{"label": "i", "value": 0, "tone": "b"}, {"label": TEST, "value": "—"}, {"label": "console", "value": "—"}],
    "labels": "left",
    "show": CASES + ["i"],
    "links": [],
    "script": [
        wait(800),
        *tour(0, "Premier tour : `i` vaut 0, `0 < 5` est vrai, la boucle lit `fruits[0]`.", first=True),
        wait(900),
        *tour(1, "`i++` : `i` passe à 1, le test est refait, la boucle lit la case 1."),
        wait(600),
        *tour(2), *tour(3),
        *tour(4, "Et ainsi de suite jusqu'à la case 4, la dernière."),
        wait(900),
        scene(say="`i` passe à 5 : `5 < 5` est faux. La boucle s'arrête **avant** de lire une case qui n'existe pas.",
              set=[{"id": "i", "at": i_at(5), "label": "5", "tone": "r"}], unlink=[L("i", "c4")],
              hud=[hud("i", 5, "r"), hud(TEST, "false", "r")]),
        wait(2600),
    ],
})

# ---------- 3. for…of et accumulateur
P = ["p0", "p1", "p2"]
steps.append({
    "id": "for-of", "label": "for…of", "title": "for…of donne chaque valeur, l'accumulateur les additionne",
    "body": ["À chaque tour, `prix` reçoit la valeur suivante du tableau, sans compteur ; `total` en garde la somme."],
    "hud": [{"label": "prix", "value": "—"}, {"label": "total", "value": 0, "tone": "b"}],
    "labels": "left",
    "show": P + ["total"],
    "links": [L(p, "total") for p in P],
    "script": [
        wait(900),
        scene(say="`let total = 0` : l'accumulateur part de 0, **avant** la boucle.", set=[{"id": "total", "label": "0"}]),
        wait(900),
        send(["p0", "total"], tone="b", label="+ 3"),
        scene(say="Premier tour : `prix` reçoit 3, et `total = total + prix` donne 3.",
              set=[{"id": "total", "label": "3"}, {"id": "p0", "tone": "g"}], hud=[hud("prix", 3, "b"), hud("total", 3, "b")]),
        wait(800),
        send(["p1", "total"], tone="b", label="+ 5"),
        scene(say="Deuxième tour : `prix` reçoit 5, le total passe à 8.",
              set=[{"id": "total", "label": "8"}, {"id": "p1", "tone": "g"}], hud=[hud("prix", 5, "b"), hud("total", 8, "b")]),
        wait(800),
        send(["p2", "total"], tone="b", label="+ 2"),
        scene(say="Dernier tour : 2. Plus de valeur, la boucle s'arrête : `total` vaut 10.",
              set=[{"id": "total", "label": "10"}, {"id": "p2", "tone": "g"}], hud=[hud("prix", 2, "b"), hud("total", 10, "b")]),
        wait(2600),
    ],
})

# ---------- 4. while : le test avant chaque tour, et la boucle sans fin
CT, TW, CO = "compte", "test compte > 0", "console"


def tour_while(n, minus=True, say_test=None, say_bloc=None):
    acts = [
        send(["compte", "test"], tone="b", label=str(n)),
        scene(say=say_test, set=[{"id": "test", "tone": "g", "label": "true"}], hud=[hud(TW, "true", "g")], ms=400),
        send(["test", "bloc"], tone="g", label="true"),
        scene(say=say_bloc, set=[{"id": "bloc", "label": f"affiche Décollage dans {n}"}], hud=[hud(CO, f"Décollage dans {n}", None)], ms=400),
    ]
    if minus:
        acts += [
            send(["bloc", "compte"], tone="b", label="- 1"),
            scene(set=[{"id": "compte", "label": str(n - 1)}, {"id": "test", "tone": "v", "label": None}],
                  hud=[hud(CT, n - 1, "b"), hud(TW, "—", None)], ms=400),
        ]
    else:
        acts.append(scene(set=[{"id": "test", "tone": "v", "label": None}], hud=[hud(TW, "—", None)], ms=300))
    return acts


steps.append({
    "id": "while", "label": "while", "title": "while refait son test avant chaque tour",
    "body": ["Tant que `compte > 0` est vrai, le bloc s'exécute ; c'est `compte = compte - 1` qui finira par rendre le test faux."],
    "hud": [{"label": CT, "value": 3, "tone": "b"}, {"label": TW, "value": "—"}, {"label": CO, "value": "—"}],
    "labels": "left",
    "show": ["compte", "test", "bloc", "sortie"],
    "links": [L("compte", "test"), L("test", "bloc", label="true"), L("test", "sortie", label="false"),
              L("bloc", "compte", label="compte - 1")],
    "script": [
        wait(800),
        *tour_while(3, say_test="Avant le premier tour, le test : `3 > 0` est vrai.",
                    say_bloc="Le bloc affiche, puis `compte = compte - 1` fait passer `compte` à 2."),
        wait(500),
        *tour_while(2, say_test="Le test est refait : `2 > 0`, encore vrai."),
        *tour_while(1),
        send(["compte", "test"], tone="b", label="0"),
        scene(say="`compte` vaut 0 : `0 > 0` est faux. La boucle s'arrête.",
              set=[{"id": "test", "tone": "r", "label": "false"}], hud=[hud(TW, "false", "r")]),
        send(["test", "sortie"], tone="r", label="false"),
        scene(say="Le programme continue après la boucle : `Décollage !`.",
              set=[{"id": "sortie", "label": "affiche Décollage !"}], hud=[hud(CO, "Décollage !", None)]),
        wait(1800),
        scene(say="La même boucle, **sans** la ligne `compte = compte - 1`.",
              unlink=[L("bloc", "compte")],
              set=[{"id": "compte", "label": "3"}, {"id": "test", "tone": "v", "label": None},
                   {"id": "bloc", "title": "bloc sans compte - 1", "label": None}, {"id": "sortie", "label": None}],
              hud=[hud(CT, 3, "b"), hud(TW, "—", None), hud(CO, "—", None), hud("tours", 0, None)], ms=900),
        *tour_while(3, minus=False, say_test="`3 > 0` : vrai, le bloc s'exécute…"),
        scene(hud=[hud("tours", 1, None)], ms=200),
        *tour_while(3, minus=False, say_test="… et rien ne change `compte` : le test est encore vrai…"),
        scene(hud=[hud("tours", 2, None)], ms=200),
        *tour_while(3, minus=False),
        scene(hud=[hud("tours", 3, None)], ms=200),
        *tour_while(3, minus=False),
        scene(say="… pour toujours. La boucle ne s'arrête **jamais**, et l'onglet ne répond plus.",
              set=[{"id": "sortie", "dim": True}, {"id": "test", "tone": "g", "label": "true"}],
              hud=[hud(TW, "true", "g"), hud("tours", "sans fin", "r")]),
        wait(2600),
    ],
})

lesson = {
    "format": "bl-scenes/0.3", "id": "js-arrays-loops", "title": "Tableaux et boucles", "lang": "fr", "kit": "feuillete",
    "legend": [{"tone": "y", "label": "texte"}, {"tone": "b", "label": "nombre"}, {"tone": "g", "label": "case parcourue"},
               {"tone": "n", "label": "undefined"}, {"tone": "r", "label": "test faux"}],
    "entities": ents, "steps": steps,
}
write(lesson, *outputs(HERE, "loops.scene.json", "js-arrays-loops"))
