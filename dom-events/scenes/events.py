"""Scènes du bit « Les événements : réagir aux actions du visiteur » (courses-web-basics/dom-events), kit Feuilleté.

Dessin, une règle par sorte (le même pour tout le stack JavaScript) :
- la page affichée = un plateau bleu (b) qui porte ses éléments (petits blocs bleus, le nom de la balise en titre) ;
- le navigateur = un bloc neutre (n) : il reçoit les événements et garde les écouteurs (« click → direBonjour ») ;
- une fonction = un bloc programme pervenche (v) ; le fichier script.js = un bloc fichier jaune (y) ;
- la console = un bloc encre (i, >_) ; le visiteur = un acteur devant la page.
Couleurs des paquets : l'événement est rose (r, ce qui arrive), l'appel de la fonction pervenche (v), undefined neutre (n).
Ce qui est allumé ou affiché grâce à l'écouteur (la lampe, le message) est vert (g).
Lecture de bas en haut : le visiteur et la page devant, le navigateur au milieu, la fonction derrière.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import G, L, scene, send, wait, write, hud

H = 0.35
EL = [1.5, 1.5, 0.4]


def rel(sx, sy, z=H):
    x, y = G(sx, sy)
    return [x, y, z]


ents = [
    {"id": "vous", "kind": "actor", "at": G(-10, 8), "label": "visiteur"},
    {"id": "page", "kind": "layer", "at": G(-3.5, 3), "size": [4.2, 4.2, 0.35], "tone": "b", "title": "page affichée"},
    {"id": "bouton", "kind": "file", "in": "page", "at": rel(-1.4, 0.4), "size": EL, "tone": "b", "title": "<button>"},
    {"id": "lampe", "kind": "file", "in": "page", "at": rel(1.4, -0.4), "size": EL, "tone": "b", "title": "lampe"},
    {"id": "form", "kind": "file", "in": "page", "at": rel(-1.4, 0.4), "size": EL, "tone": "b", "title": "<form>"},
    {"id": "msg", "kind": "file", "in": "page", "at": rel(1.4, -0.4), "size": EL, "tone": "g", "title": "message",
     "label": "Bonjour Ada !"},
    {"id": "nav", "kind": "node", "at": G(3.5, -2.5), "tone": "n", "title": "navigateur",
     "detail": "Le **navigateur** reçoit chaque événement et appelle les fonctions qu'on lui a confiées, les **écouteurs**."},
    {"id": "fn", "kind": "program", "at": G(9, -9), "tone": "v", "title": "direBonjour",
     "detail": "La fonction confiée au navigateur : un **écouteur**. Ce n'est pas toi qui l'appelles, c'est le navigateur."},
    {"id": "cons", "kind": "node", "at": G(13, -2), "size": [1.8, 1.8, 0.9], "tone": "i", "title": "console", "icon": ">_"},
    {"id": "js", "kind": "file", "at": G(-6, -7), "tone": "y", "title": "script.js",
     "detail": "Le script s'exécute une fois, au chargement de la page."},
]
steps = []

# ---------- 1. écouter
E = "écouteur"
steps.append({
    "id": "ecouter", "label": "Écouter", "title": "Le navigateur appelle la fonction, à chaque clic",
    "body": ["Le script confie une fonction au navigateur ; c'est le navigateur qui l'appelle, à chaque événement."],
    "hud": [{"label": "script", "value": "au chargement"}, {"label": "clics", "value": 0}],
    "labels": "left",
    "show": ["vous", "page", "bouton", "nav", "fn", "cons", "js"],
    "links": [L("js", "nav"), L("vous", "bouton"), L("bouton", "nav"), L("nav", "fn"), L("fn", "cons")],
    "script": [
        wait(800),
        send(["js", "nav"], tone="y", label="addEventListener"),
        scene(say="Au chargement, le script confie la fonction au navigateur : « au clic sur le bouton, appelle `direBonjour` ».",
              set=[{"id": "nav", "label": "click → direBonjour"}]),
        wait(1200),
        scene(say="Le script est terminé. La page **attend** : rien ne se passe sans le visiteur.",
              set=[{"id": "js", "dim": True}], hud=[hud("script", "terminé", None)]),
        wait(1300),
        send(["vous", "bouton", "nav"], tone="r", label="click",
             explain=["Le visiteur clique sur le bouton…", "… qui produit un **événement** `click`, reçu par le navigateur."]),
        send(["nav", "fn", "cons"], tone="v", label="appelle",
             explain=["Le navigateur appelle l'écouteur, `direBonjour`.", "La fonction écrit `Bonjour !` dans la console."]),
        scene(say="Le navigateur a appelé la fonction : `Bonjour !` s'écrit dans la console.",
              set=[{"id": "cons", "label": "Bonjour !"}], hud=[hud("clics", 1, "r")]),
        wait(1100),
        send(["vous", "bouton", "nav"], tone="r", label="click"),
        send(["nav", "fn", "cons"], tone="v", label="appelle"),
        scene(say="Un autre clic, un autre appel : autant de fois que l'événement se produit.",
              set=[{"id": "cons", "label": "Bonjour ! (2 fois)"}], hud=[hud("clics", 2, "r")]),
        wait(2400),
    ],
})

# ---------- 2. f contre f()
steps.append({
    "id": "f-ou-f", "label": "f ou f()", "title": "basculer() appelle tout de suite, basculer désigne",
    "body": ["Avec des parenthèses, la fonction s'exécute au chargement ; le navigateur ne reçoit que ce qu'elle a rendu."],
    "hud": [{"label": "lampe", "value": "éteinte"}],
    "labels": "left",
    "show": ["vous", "page", "bouton", "lampe", "nav", {"id": "fn", "title": "basculer"},
             {"id": "js", "label": "basculer()"}],
    "links": [L("js", "nav"), L("js", "fn"), L("vous", "bouton"), L("bouton", "nav"), L("nav", "fn"), L("fn", "lampe")],
    "script": [
        wait(900),
        send(["js", "fn"], tone="v", label="basculer()"),
        scene(say="Avec des parenthèses, `basculer()` **appelle** la fonction tout de suite, au chargement.",
              set=[{"id": "fn", "label": "exécutée au chargement"}]),
        send(["fn", "lampe"], tone="v"),
        scene(say="La lampe s'allume toute seule, avant tout clic.",
              set=[{"id": "lampe", "tone": "g", "label": "allumée"}], hud=[hud("lampe", "allumée", "g")]),
        wait(1000),
        send(["js", "nav"], tone="n", label="undefined"),
        scene(say="Le navigateur reçoit ce que la fonction a rendu : `undefined`. Rien à appeler au clic.",
              set=[{"id": "nav", "label": "click → undefined"}]),
        wait(900),
        send(["vous", "bouton", "nav"], tone="r", label="click"),
        scene(say="Le visiteur clique : le navigateur n'a rien à exécuter, la lampe ne bouge plus.",
              set=[{"id": "nav", "label": "click → rien"}]),
        wait(1500),
        scene(say="Sans parenthèses, `basculer` **désigne** la fonction, sans l'exécuter.",
              set=[{"id": "js", "label": "basculer"}, {"id": "fn", "label": None}, {"id": "lampe", "tone": "b", "label": None},
                   {"id": "nav", "label": None}],
              unlink=[L("js", "fn")], hud=[hud("lampe", "éteinte", None)], ms=900),
        send(["js", "nav"], tone="v", label="basculer"),
        scene(say="Le navigateur la garde pour le clic : la lampe reste éteinte au chargement.",
              set=[{"id": "nav", "label": "click → basculer"}]),
        wait(900),
        send(["vous", "bouton", "nav"], tone="r", label="click"),
        send(["nav", "fn", "lampe"], tone="v", label="appelle"),
        scene(say="Au clic, et seulement au clic, le navigateur l'appelle : la lampe s'allume.",
              set=[{"id": "lampe", "tone": "g", "label": "allumée"}], hud=[hud("lampe", "allumée", "g")]),
        wait(2400),
    ],
})

# ---------- 3. submit et preventDefault
steps.append({
    "id": "submit", "label": "preventDefault", "title": "Un formulaire envoyé recharge la page, sauf preventDefault",
    "body": ["L'écouteur de `submit` s'exécute, puis le formulaire recharge la page, sauf si l'écouteur l'en empêche."],
    "hud": [{"label": "page", "value": "affichée"}],
    "labels": "left",
    "show": ["vous", "page", "form", "nav", {"id": "fn", "title": "écouteur de submit"}],
    "links": [L("vous", "form"), L("form", "nav"), L("nav", "fn"), L("fn", "page")],
    "script": [
        wait(800),
        send(["vous", "form", "nav"], tone="r", label="submit"),
        send(["nav", "fn"], tone="v", label="appelle"),
        scene(say="Le visiteur envoie le formulaire : le navigateur appelle l'écouteur de `submit`, qui écrit le message.",
              show=["msg"]),
        wait(1000),
        scene(say="Puis le formulaire fait ce qu'il fait par défaut : il **recharge** la page. Le message disparaît.",
              hide=["msg"], hud=[hud("page", "rechargée", "r")], ms=900),
        wait(1500),
        scene(say="Avec `evenement.preventDefault()`, l'écouteur coupe ce comportement par défaut.",
              set=[{"id": "fn", "label": "preventDefault(), puis message"}], hud=[hud("page", "affichée", None)]),
        wait(900),
        send(["vous", "form", "nav"], tone="r", label="submit"),
        send(["nav", "fn"], tone="v", label="appelle"),
        scene(say="Même envoi : le message s'affiche, et la page ne se recharge pas.",
              show=["msg"], hud=[hud("page", "pas rechargée", "g")]),
        wait(2600),
    ],
})

lesson = {
    "format": "bl-scenes/0.3", "id": "js-dom-events", "title": "Les événements", "lang": "fr", "kit": "feuillete",
    "legend": [{"tone": "b", "label": "page affichée"}, {"tone": "r", "label": "événement"}, {"tone": "v", "label": "fonction, appel"},
               {"tone": "y", "label": "fichier JavaScript"}],
    "entities": ents, "steps": steps,
}
write(lesson, *outputs(HERE, "events.scene.json", "js-dom-events"))
