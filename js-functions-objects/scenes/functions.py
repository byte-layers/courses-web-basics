"""Scènes du bit « Fonctions et objets » (courses-web-basics/js-functions-objects), kit Feuilleté.

Dessin, une règle par sorte (le même pour tout le stack JavaScript) :
- une valeur = un bloc « fichier » ; un nombre est bleu (b), un texte jaune (y), undefined neutre (n), NaN rose (r) ;
- une fonction = un plateau pervenche (v) qui porte ses paramètres (blocs valeur) et son bloc de code (bloc programme) ;
- un objet = un plateau neutre (n) qui porte une case par clé (bloc valeur) ;
- l'appel (le code qui appelle) = un bloc pervenche devant ; la console = un bloc encre (i, >_), comme dans tout le stack.
Lecture de bas en haut : l'appel devant, la fonction derrière (ses paramètres au fond, son return devant, vers l'appel) ;
la console à gauche de l'appel.
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
    # étape 1 : addition
    {"id": "appel", "kind": "node", "at": G(-3, 9), "size": [2.0, 2.0, 0.9], "tone": "v", "title": "addition(5, 3)",
     "detail": "L'**appel** : le nom de la fonction, puis les **arguments** entre parenthèses."},
    {"id": "fadd", "kind": "layer", "at": G(4, -3), "size": [5.0, 5.0, 0.55], "tone": "v", "title": "function addition(a, b)",
     "detail": "La **fonction** déclarée une fois : ses **paramètres** `a` et `b`, et son bloc de code."},
    {"id": "pa", "kind": "file", "in": "fadd", "at": rel(-2.0, -1.4), "size": [1.4, 1.4, 0.4], "tone": "b", "title": "a",
     "detail": "Un **paramètre** : un nom qui reçoit la valeur donnée à l'appel."},
    {"id": "pb", "kind": "file", "in": "fadd", "at": rel(2.0, -1.4), "size": [1.4, 1.4, 0.4], "tone": "b", "title": "b"},
    {"id": "ret", "kind": "program", "in": "fadd", "at": rel(0, 1.8), "size": [1.6, 1.6, 0.7], "tone": "n", "title": "return a + b"},
    {"id": "cons", "kind": "node", "at": G(-9, 7), "size": [1.8, 1.8, 0.9], "tone": "i", "title": "console", "icon": ">_"},
    # étape 2 : prixTTC
    {"id": "appel2", "kind": "node", "at": G(-3, 9), "size": [2.0, 2.0, 0.9], "tone": "v", "title": "prixTTC(25) * 2",
     "detail": "Le code qui appelle `prixTTC(25)` et veut **se servir** du résultat : le multiplier par 2."},
    {"id": "fttc", "kind": "layer", "at": G(4, -3), "size": [4.4, 4.4, 0.55], "tone": "v", "title": "function prixTTC(prix)"},
    {"id": "corps", "kind": "program", "in": "fttc", "at": rel(0, 0), "size": [1.8, 1.8, 0.7], "tone": "n",
     "title": "console.log(prix * 1.2)"},
    # étape 3 : objet
    {"id": "livre", "kind": "layer", "at": G(0, -3), "size": [6.2, 6.2, 0.55], "tone": "n", "title": "livre",
     "detail": "Un **objet** : des paires **clé : valeur** qui décrivent une même chose."},
    {"id": "k-titre", "kind": "file", "in": "livre", "at": rel(-3.4, 0), "size": [1.4, 1.4, 0.4], "tone": "y", "title": "titre",
     "label": "\"Dune\"", "detail": "Une **clé** et sa valeur. Une case par clé."},
    {"id": "k-auteur", "kind": "file", "in": "livre", "at": rel(0, -1.8), "size": [1.4, 1.4, 0.4], "tone": "y", "title": "auteur",
     "label": "\"Frank Herbert\""},
    {"id": "k-pages", "kind": "file", "in": "livre", "at": rel(3.4, 0), "size": [1.4, 1.4, 0.4], "tone": "b", "title": "pages",
     "label": "900"},
    {"id": "k-editeur", "kind": "file", "in": "livre", "at": rel(0, 2.0), "size": [1.4, 1.4, 0.4], "tone": "y", "title": "editeur",
     "label": "\"Pocket\""},
    {"id": "lire", "kind": "program", "at": G(-6, 9), "tone": "v", "title": "livre.titre",
     "detail": "Une **expression** qui lit l'objet : son nom, un point, la clé."},
]
steps = []

# ---------- 1. appeler une fonction
V = "l'appel vaut"
steps.append({
    "id": "appel", "label": "L'appel", "title": "Un appel donne des valeurs, return rend le résultat",
    "body": ["Les arguments de l'appel vont dans les paramètres ; `return` rend la valeur calculée à celui qui a appelé."],
    "hud": [{"label": V, "value": "—"}],
    "labels": "left",
    "show": ["appel", "fadd", "pa", "pb", "ret", "cons"],
    "links": [L("appel", "pa"), L("appel", "pb"), L("ret", "appel", dashed=True), L("appel", "cons")],
    "script": [
        wait(800),
        send(["appel", "pa"], tone="b", label="5"),
        send(["appel", "pb"], tone="b", label="3"),
        scene(say="L'appel `addition(5, 3)` donne ses **arguments** : 5 va dans `a`, 3 dans `b`.",
              set=[{"id": "pa", "label": "5"}, {"id": "pb", "label": "3"}]),
        wait(1000),
        scene(say="La fonction exécute son bloc : `a + b` vaut 8.", set=[{"id": "ret", "label": "8"}]),
        wait(700),
        scene(link=[L("ret", "appel")], ms=300),
        send(["ret", "appel"], tone="b", label="8"),
        scene(say="`return` **rend** 8 à celui qui a appelé : l'appel vaut 8.", hud=[hud(V, 8, "b")]),
        send(["appel", "cons"], tone="b", label="8"),
        scene(say="`console.log` reçoit cette valeur et l'affiche.", set=[{"id": "cons", "label": "8"}]),
        wait(1300),
        scene(say="Le même geste resert avec d'autres valeurs : `addition(2, 2)`.",
              set=[{"id": "appel", "title": "addition(2, 2)"}, {"id": "pa", "label": None}, {"id": "pb", "label": None},
                   {"id": "ret", "label": None}],
              link=[L("ret", "appel", dashed=True)], hud=[hud(V, "—", None)]),
        send(["appel", "pa"], tone="b", label="2"),
        send(["appel", "pb"], tone="b", label="2"),
        scene(set=[{"id": "pa", "label": "2"}, {"id": "pb", "label": "2"}, {"id": "ret", "label": "4"}],
              link=[L("ret", "appel")], ms=400),
        send(["ret", "appel"], tone="b", label="4"),
        scene(say="Elle rend 4 : la formule est écrite une seule fois.", hud=[hud(V, 4, "b")], set=[{"id": "cons", "label": "8, puis 4"}]),
        wait(2400),
    ],
})

# ---------- 2. afficher n'est pas rendre
steps.append({
    "id": "return", "label": "return", "title": "Afficher n'est pas rendre",
    "body": ["`console.log` écrit le résultat pour toi ; seul `return` le donne au code qui a appelé."],
    "hud": [{"label": V, "value": "—"}],
    "labels": "left",
    "show": ["appel2", "fttc", "corps", "cons"],
    "links": [L("appel2", "corps"), L("corps", "cons"), L("corps", "appel2", dashed=True)],
    "script": [
        wait(800),
        send(["appel2", "corps"], tone="b", label="25"),
        scene(say="`prixTTC(25)` donne 25 à la fonction, qui calcule 30.", set=[{"id": "corps", "label": "30"}]),
        wait(600),
        send(["corps", "cons"], tone="b", label="30"),
        scene(say="Elle l'**affiche** avec `console.log` : la console montre 30, pour toi.", set=[{"id": "cons", "label": "30"}]),
        wait(1000),
        scene(link=[L("corps", "appel2")], ms=300),
        send(["corps", "appel2"], tone="n", label="undefined"),
        scene(say="Mais elle ne rend rien : l'appel vaut `undefined`, et `undefined * 2` donne `NaN`.",
              set=[{"id": "appel2", "label": "NaN", "tone": "r"}], hud=[hud(V, "undefined", "n")]),
        wait(1200),
        scene(say="La console montre 30, mais le code qui appelle n'a rien reçu : à toi de trouver ce qui manque.", hud=[hud(V, "rien reçu", "r")], ms=300),
        wait(2400),
    ],
})

# ---------- 3. un objet
def lecture(title, key, value, tone, say, prev=None):
    acts = [scene(set=[{"id": "lire", "title": title, "label": None, "tone": "v"}], link=[L("lire", key)],
                  unlink=[L("lire", prev)] if prev else [], ms=400),
            send(["lire", key], kind="read", reply=value, tone=tone),
            scene(say=say, set=[{"id": "lire", "label": value}])]
    return acts


steps.append({
    "id": "objet", "label": "Un objet", "title": "Un objet range des valeurs sous des clés",
    "body": ["On lit une valeur par sa clé ; une clé absente rend `undefined`, une clé nouvelle s'ajoute."],
    "labels": "left",
    "show": ["livre", "k-titre", "k-auteur", "k-pages", "lire"],
    "links": [],
    "script": [
        wait(800),
        *lecture("livre.titre", "k-titre", "\"Dune\"", "y", "`livre.titre` : le point va chercher la valeur de la clé `titre`."),
        wait(900),
        *lecture("livre[\"auteur\"]", "k-auteur", "\"Frank Herbert\"", "y",
                 "`livre[\"auteur\"]` fait la même chose, la clé écrite comme un texte.", prev="k-titre"),
        wait(900),
        scene(say="`livre.editeur` : aucune clé de ce nom, la réponse est `undefined`, sans erreur.",
              set=[{"id": "lire", "title": "livre.editeur", "label": "undefined", "tone": "n"}], unlink=[L("lire", "k-auteur")]),
        wait(1400),
        scene(say="`livre.editeur = \"Pocket\"` range une valeur sous une clé nouvelle : elle s'ajoute à l'objet.",
              set=[{"id": "lire", "title": "livre.editeur = \"Pocket\"", "label": None, "tone": "v"}],
              show=["k-editeur"], link=[L("lire", "k-editeur")]),
        wait(2400),
    ],
})

# ---------- 4. un tableau d'objets parcouru par for…of
# Trois objets (plateaux neutres) en rangée, une case titre et une case pages chacun ; la boucle devant, la console à gauche.
LIVRES = [("Dune", 900), ("Le Hobbit", 320), ("Fondation", 280)]
OX = [-10, 0, 10]
for k, (t, p) in enumerate(LIVRES):
    ents += [
        {"id": f"o{k}", "kind": "layer", "at": G(OX[k], -2), "size": [3.4, 3.4, 0.5], "tone": "n", "title": f"livres[{k}]",
         **({"detail": "Une **case** du tableau `livres` : elle contient un objet entier, avec ses deux clés."} if k == 0 else {})},
        {"id": f"o{k}t", "kind": "file", "in": f"o{k}", "at": rel(-1.5, 0), "size": [1.1, 1.1, 0.4], "tone": "y",
         "title": "titre", "label": f"\"{t}\""},
        {"id": f"o{k}p", "kind": "file", "in": f"o{k}", "at": rel(1.5, 0), "size": [1.1, 1.1, 0.4], "tone": "b",
         "title": "pages", "label": str(p)},
    ]
ents += [
    {"id": "boucle", "kind": "node", "at": G(0, 9), "size": [2.2, 2.2, 0.9], "tone": "v", "title": "for (const livre of livres)",
     "detail": "À chaque tour, la variable **`livre`** reçoit l'objet suivant du tableau, toutes ses clés comprises."},
    {"id": "cons4", "kind": "node", "at": G(-10, 8), "size": [1.8, 1.8, 0.9], "tone": "i", "title": "console", "icon": ">_"},
]
OBJ = ["o0", "o1", "o2"]
LV = "livre"


def tour(k, say_recoit, say_lit):
    t = LIVRES[k][0]
    prev = [{"id": f"o{k-1}", "dim": True}] if k else []
    return [
        send([f"o{k}", "boucle"], tone="n", label="{ titre, pages }"),
        scene(say=say_recoit, set=prev + [{"id": "boucle", "label": f"livre = livres[{k}]"}],
              hud=[hud("tour", k + 1, "v"), hud(LV, f"livres[{k}], entier", "v")]),
        wait(700),
        send(["boucle", f"o{k}t"], kind="read", reply=f"\"{t}\"", tone="y"),
        send(["boucle", "cons4"], tone="y", label=t),
        scene(say=say_lit, set=[{"id": "cons4", "label": ", ".join(x[0] for x in LIVRES[:k + 1])}]),
        wait(900),
    ]


steps.append({
    "id": "liste", "label": "Tableau d'objets", "title": "À chaque tour, un objet entier",
    "body": ["`for…of` donne à `livre` l'objet suivant du tableau ; `livre.titre` lit la clé de l'objet du tour."],
    "hud": [{"label": "tour", "value": "—"}, {"label": LV, "value": "—"}],
    "labels": "left",
    "show": OBJ + [f"o{k}{c}" for k in range(3) for c in "tp"] + ["boucle", "cons4"],
    "links": [L(o, "boucle") for o in OBJ] + [L("boucle", "cons4")],
    "script": [
        wait(900),
        *tour(0, "Premier tour : `livre` reçoit l'objet **entier** de la case 0, ses deux clés comprises.",
              "`livre.titre` lit la clé `titre` de cet objet : la console affiche Dune."),
        *tour(1, "Deuxième tour : `livre` reçoit l'objet suivant.", "Même ligne, autre objet : Le Hobbit."),
        *tour(2, "Dernier tour : le troisième objet.", "Fondation. Plus d'objet, la boucle s'arrête."),
        scene(say="Trois tours, un par objet : la ligne `console.log(livre.titre)` est écrite une fois, pour toute la liste.",
              set=[{"id": o, "dim": False} for o in OBJ] + [{"id": "boucle", "label": None}],
              hud=[hud("tour", "fini", None), hud(LV, "—", None)]),
        wait(2600),
    ],
})

lesson = {
    "format": "bl-scenes/0.3", "id": "js-functions-objects", "title": "Fonctions et objets", "lang": "fr", "kit": "feuillete",
    "legend": [{"tone": "b", "label": "nombre"}, {"tone": "y", "label": "texte"}, {"tone": "n", "label": "undefined"},
               {"tone": "r", "label": "NaN"}, {"tone": "v", "label": "fonction, appel"}],
    "entities": ents, "steps": steps,
}
write(lesson, *outputs(HERE, "functions.scene.json", "js-functions-objects"))
