"""Scènes du bit « Données JSON et fetch » (courses-web-basics/json-fetch), kit Feuilleté.

Dessin, une règle par sorte (le même pour tout le stack JavaScript) :
- un texte = un bloc fichier jaune (y) ; un objet = un plateau neutre (n) qui porte une case par clé, comme au bit sur les
  objets ; une expression qui lit = un bloc programme pervenche (v) devant ;
- le serveur = un bloc neutre (n) au fond ; le script = un bloc fichier jaune (y) ; une fonction (celle du .then) = un bloc
  programme pervenche (v) ; la console = un bloc encre (i, >_) ; la page affichée = un plateau bleu (b) et ses éléments.
Couleurs : undefined neutre (n) ; ce qui est arrivé et sert est vert (g) ; ce qui attend est estompé (dim).
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
    # étape 1 : du texte à l'objet
    {"id": "srv", "kind": "node", "at": G(-8, -8), "tone": "n", "title": "serveur",
     "detail": "Le **serveur** envoie les données sous forme de texte, au format JSON."},
    {"id": "texte", "kind": "file", "at": G(-8, 2), "size": [2.2, 2.2, 0.5], "tone": "y", "title": "texte",
     "label": "{\"titre\": \"Dune\", …}", "detail": "Un **texte** JSON : des caractères, pas encore un objet."},
    {"id": "parse", "kind": "program", "at": G(0, -1), "tone": "v", "title": "JSON.parse(texte)",
     "detail": "`JSON.parse` lit un texte JSON et rend l'objet ou le tableau qu'il décrit."},
    {"id": "obj", "kind": "layer", "at": G(8, -4), "size": [4.6, 4.6, 0.55], "tone": "n", "title": "objet"},
    {"id": "k-titre", "kind": "file", "in": "obj", "at": rel(-1.8, 0.8), "size": [1.4, 1.4, 0.4], "tone": "y", "title": "titre",
     "label": "\"Dune\""},
    {"id": "k-pages", "kind": "file", "in": "obj", "at": rel(1.8, -0.8), "size": [1.4, 1.4, 0.4], "tone": "b", "title": "pages",
     "label": "900"},
    {"id": "lire", "kind": "program", "at": G(0, 9), "tone": "v", "title": "texte.titre"},
    # étape 2 : fetch
    {"id": "script", "kind": "file", "at": G(-5, 2), "tone": "y", "title": "script.js",
     "detail": "Le script appelle `fetch`, puis continue à la ligne suivante sans attendre."},
    {"id": "then", "kind": "program", "at": G(4, 2), "tone": "v", "title": "fonction du .then",
     "detail": "La fonction donnée à `.then` : le navigateur l'appellera **plus tard**, quand la réponse sera là."},
    {"id": "srv2", "kind": "node", "at": G(-1, -8), "tone": "n", "title": "serveur", "sub": "projets.json"},
    {"id": "cons", "kind": "node", "at": G(-1, 10), "size": [1.8, 1.8, 0.9], "tone": "i", "title": "console", "icon": ">_"},
    {"id": "page", "kind": "layer", "at": G(9, 10), "size": [4.2, 4.2, 0.35], "tone": "b", "title": "page affichée"},
    {"id": "li1", "kind": "file", "in": "page", "at": rel(-1.6, 0, 0.35), "size": [1.1, 1.1, 0.3], "tone": "g", "title": "3 projets"},
    {"id": "li2", "kind": "file", "in": "page", "at": rel(0, 0, 0.35), "size": [1.1, 1.1, 0.3], "tone": "g"},
    {"id": "li3", "kind": "file", "in": "page", "at": rel(1.6, 0, 0.35), "size": [1.1, 1.1, 0.3], "tone": "g"},
]
steps = []

# ---------- 1. JSON : un texte, puis un objet
steps.append({
    "id": "parse", "label": "JSON.parse", "title": "Un JSON reçu est un texte, JSON.parse en fait un objet",
    "body": ["On ne lit pas une clé dans un texte : il faut d'abord le transformer en objet."],
    "labels": "left",
    "show": ["srv", "lire"],
    "links": [],
    "script": [
        wait(700),
        scene(show=["texte"], link=[L("srv", "texte")], ms=500),
        send(["srv", "texte"], tone="y", label="JSON"),
        scene(say="Le serveur envoie des données en JSON : la page reçoit un **texte**.", link=[L("lire", "texte")]),
        wait(900),
        send(["lire", "texte"], kind="read", reply="undefined", tone="n"),
        scene(say="`texte.titre` : un texte n'a pas de clé `titre`, la réponse est `undefined`.",
              set=[{"id": "lire", "label": "undefined", "tone": "n"}]),
        wait(1300),
        scene(show=["parse"], link=[L("texte", "parse")], unlink=[L("lire", "texte")], ms=500),
        send(["texte", "parse"], tone="y", label="texte"),
        scene(say="`JSON.parse(texte)` lit ce texte et fabrique l'**objet** qu'il décrit.",
              show=["obj", "k-titre", "k-pages"], link=[L("parse", "obj")]),
        wait(1200),
        scene(set=[{"id": "lire", "title": "objet.titre", "label": None, "tone": "v"}], link=[L("lire", "k-titre")], ms=500),
        send(["lire", "k-titre"], kind="read", reply="\"Dune\"", tone="y"),
        scene(say="Sur l'objet, la notation à point fonctionne : `objet.titre` vaut `\"Dune\"`.",
              set=[{"id": "lire", "label": "\"Dune\"", "tone": "g"}]),
        wait(2400),
    ],
})

# ---------- 2. fetch ne bloque pas
P = "promesse"
steps.append({
    "id": "fetch", "label": "fetch", "title": "fetch part, le code continue, la réponse arrive plus tard",
    "body": ["`fetch` rend tout de suite une promesse ; la fonction du `.then` ne s'exécute qu'à l'arrivée de la réponse."],
    "hud": [{"label": P, "value": "—"}, {"label": "projets", "value": "pas encore là"}],
    "labels": "left",
    "show": ["script", {"id": "then", "dim": True, "label": "attend la réponse"}, "srv2", "cons", "page"],
    "links": [L("script", "srv2"), L("script", "cons"), L("script", "then"), L("then", "cons"),
              L("then", "page")],
    "script": [
        wait(800),
        send(["script", "srv2"], tone="y", label="projets.json"),
        scene(say="`fetch(\"projets.json\")` envoie la demande et rend tout de suite une **promesse** : « la réponse arrivera ».",
              set=[{"id": "srv2", "label": "prépare la réponse…"}], hud=[hud(P, "en attente", "y")]),
        wait(800),
        send(["script", "cons"], tone="y", label="console.log"),
        scene(say="Le code n'attend pas : la ligne suivante s'exécute, et `Demande envoyée` s'écrit **d'abord**.",
              set=[{"id": "cons", "label": "Demande envoyée"}]),
        wait(1300),
        send(["srv2", "script"], tone="g", label="réponse"),
        scene(say="Plus tard, la réponse arrive : la promesse est tenue.",
              set=[{"id": "srv2", "label": None}], hud=[hud(P, "tenue", "g"), hud("projets", "3", "g")]),
        send(["script", "then"], tone="v", label="appelle"),
        scene(say="Le navigateur appelle alors la fonction du `.then` : c'est là, et seulement là, que les données servent.",
              set=[{"id": "then", "dim": False, "label": "reçoit 3 projets"}]),
        send(["then", "cons"], tone="g", label="console.log"),
        scene(say="`3 projets reçus` s'écrit **après** `Demande envoyée`, alors que sa ligne venait avant dans le code.",
              set=[{"id": "cons", "label": "Demande envoyée, 3 projets reçus"}]),
        wait(900),
        send(["then", "page"], tone="g", label="afficher"),
        scene(say="Tout ce qui dépend des données va dans le `.then` : la liste se remplit.", show=["li1", "li2", "li3"]),
        wait(2600),
    ],
})

# ---------- 3. async et await : la même chronologie, la fonction en pause
F = "charger()"
steps.append({
    "id": "await", "label": "async, await", "title": "await met la fonction en pause, pas la page",
    "body": ["Dans une fonction `async`, `await` attend la réponse ; le reste du script, lui, continue."],
    "hud": [{"label": F, "value": "—"}, {"label": "statut", "value": "—"}],
    "labels": "left",
    "show": ["script", {"id": "then", "title": "async function charger", "label": None,
                       "detail": "Une fonction déclarée `async` : à chaque `await`, elle se met en pause jusqu'à la réponse, sans bloquer la page."}, "srv2", "cons", "page"],
    "links": [L("script", "then"), L("then", "srv2"), L("script", "cons"), L("then", "cons"), L("then", "page")],
    "script": [
        wait(800),
        send(["script", "then"], tone="y", label="charger()"),
        send(["then", "srv2"], tone="v", label="projets.json"),
        scene(say="`charger()` démarre : `await fetch(\"projets.json\")` envoie la demande, puis met **la fonction** en pause.",
              set=[{"id": "then", "dim": True, "label": "en pause : await"}], hud=[hud(F, "en pause", "y")]),
        wait(700),
        send(["script", "cons"], tone="y", label="console.log"),
        scene(say="La page, elle, n'est pas bloquée : la ligne d'après l'appel s'exécute, `Chargement lancé` s'écrit d'abord.",
              set=[{"id": "cons", "label": "Chargement lancé"}]),
        wait(1300),
        send(["srv2", "then"], tone="g", label="réponse 200"),
        scene(say="La réponse arrive, statut `200` : `reponse.ok` vaut `true`, la fonction **reprend** à la ligne suivante.",
              set=[{"id": "then", "dim": False, "label": "reprend : reponse.ok"}],
              hud=[hud(F, "reprend", "g"), hud("statut", "200 : ok", "g")]),
        wait(900),
        scene(say="Second `await` : la lecture du JSON. Puis les données sont là, sur les lignes qui suivent.",
              set=[{"id": "then", "label": "await reponse.json()"}]),
        wait(800),
        send(["then", "page"], tone="g", label="afficher"),
        scene(say="Ce qui suit un `await` utilise les données : la liste se remplit.", show=["li1", "li2", "li3"]),
        wait(1700),
        scene(say="Si le fichier n'existe pas, le serveur répond quand même, avec le statut `404`.",
              hide=["li1", "li2", "li3"], set=[{"id": "srv2", "sub": "fichier absent"}, {"id": "then", "label": None}],
              hud=[hud(F, "—", None), hud("statut", "—", None)], ms=800),
        send(["srv2", "then"], tone="n", label="réponse 404"),
        scene(say="`fetch` n'échoue pas : c'est `reponse.ok`, ici `false`, qui signale l'erreur au code.",
              hud=[hud("statut", "404 : ok vaut false", "r")], set=[{"id": "then", "label": "reponse.ok : false"}]),
        send(["then", "cons"], tone="v", label="console.error"),
        scene(say="Le test de `reponse.ok` écrit l'erreur dans la console, et la fonction s'arrête.",
              set=[{"id": "cons", "label": "Erreur HTTP 404"}]),
        wait(2600),
    ],
})

lesson = {
    "format": "bl-scenes/0.3", "id": "js-json-fetch", "title": "JSON et fetch", "lang": "fr", "kit": "feuillete",
    "legend": [{"tone": "y", "label": "texte"}, {"tone": "v", "label": "fonction"},
               {"tone": "g", "label": "données reçues"}, {"tone": "b", "label": "page"}],
    "entities": ents, "steps": steps,
}
write(lesson, *outputs(HERE, "fetch.scene.json", "js-json-fetch"))
