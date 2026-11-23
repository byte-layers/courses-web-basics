"""Scènes 2D (kit plan) du bit « Le web partout » (courses-web-basics/web-everywhere), suite d'everywhere.py.

Quatre étapes, une idée chacune (cibles.scene.json) :
- responsive : une seule page ; sur un écran large, trois blocs côte à côte ; sur un téléphone, l'écran rétrécit
  et les mêmes blocs glissent les uns sous les autres ; c'est la feuille de style qui choisit selon la largeur ;
- mobile : le même code JavaScript, deux façons de faire une app : React Native affiche les composants du système,
  Capacitor glisse une vraie page web dans l'app ;
- electron : un logiciel Electron porte Chromium (l'interface) et Node.js (le système) ; la page n'a pas le droit
  de lire le disque, Node.js le fait pour elle ;
- cibles : les mêmes trois langages, quatre cibles : le navigateur, la PWA, le téléphone, le bureau.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Une règle par sorte : ton code est un file (ou une boîte jaune) ; un écran ou un logiciel est un layer qui porte ce
qu'il affiche ou fait tourner ; le disque est un store.
Couleurs : y ton code ; v le web, ce que le navigateur affiche ; g ce qui est natif, au système ; b tes fichiers.
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


# ---------- 1. responsive : une page, deux largeurs
WIDE = [(-7.6, 1.2), (0, 1.2), (7.6, 1.2)]
NARROW = [(0, -2.6), (0, 1.4), (0, 5.4)]
R = [
    ent("r-css", "file", (-20, 0), (8.5, 2.6), "y", title="style.css",
        detail="Une seule **feuille de style** pour tous les écrans. Ses règles peuvent dépendre de la largeur de l'écran."),
    ent("r-screen", "layer", (0, 0), (24, 11), "v", title="écran d'ordinateur"),
    ent("r-a", "node", WIDE[0], (6.8, 6), "v", parent="r-screen", title="dossiers"),
    ent("r-b", "node", WIDE[1], (6.8, 6), "v", parent="r-screen", title="messages"),
    ent("r-c", "node", WIDE[2], (6.8, 6), "v", parent="r-screen", title="message ouvert"),
]
responsive = {
    "id": "responsive", "label": "Responsive", "title": "Une seule page, toutes les largeurs",
    "body": ["La même page s'ouvre sur un grand écran et sur un téléphone. La feuille de style range les blocs selon la largeur."],
    "hud": [{"label": "largeur", "value": "1 600 px"}, {"label": "disposition", "value": "trois colonnes"}],
    "show": ["r-css", "r-screen", "r-a", "r-b", "r-c"],
    "links": [L("r-css", "r-screen")],
    "script": [
        wait(1000),
        scene(set=[{"id": "r-css", "label": "écran large : côte à côte"}],
              say="Sur un ordinateur, l'écran est large : la feuille de style place les trois blocs **côte à côte**."),
        wait(1500),
        scene(set=[{"id": "r-screen", "size": [11, 15, 1], "title": "écran de téléphone"},
                   {"id": "r-a", "at": list(NARROW[0]), "size": [8.6, 3.2, 1]},
                   {"id": "r-b", "at": list(NARROW[1]), "size": [8.6, 3.2, 1]},
                   {"id": "r-c", "at": list(NARROW[2]), "size": [8.6, 3.2, 1]},
                   {"id": "r-css", "label": "écran étroit : l'un sous l'autre"}],
              hud=[hud("largeur", "360 px"), hud("disposition", "une colonne")], ms=1100,
              say="Sur un téléphone, c'est **la même page** : les mêmes blocs, rangés les uns sous les autres."),
        wait(1600),
        scene(set=[{"id": "r-css", "label": "une règle selon la largeur"}],
              say="Pas deux sites : une page, et une feuille de style qui choisit selon la largeur. C'est le **responsive design**."),
        wait(2600),
    ],
}

# ---------- 2. mobile : React Native ou Capacitor
M = [
    ent("m-code", "file", (-10, 0), (9, 2.6), "y", title="ton code JavaScript"),
    ent("m-rn", "layer", (6, -5), (13, 7.5), "g", title="app React Native", sub="iOS ou Android"),
    ent("m-rn-btn", "node", (0, 0.3), (10.5, 1.8), "g", parent="m-rn", title="un vrai bouton du système"),
    ent("m-rn-list", "node", (0, 2.4), (10.5, 1.8), "g", parent="m-rn", title="une vraie liste du système"),
    ent("m-cap", "layer", (6, 5), (13, 7.5), "n", title="app Capacitor", sub="iOS ou Android"),
    ent("m-cap-web", "layer", (0, 1.1), (11, 4.2), "v", parent="m-cap", title="une page web"),
    ent("m-cap-btn", "node", (0, 0.7), (8, 1.6), "v", parent="m-cap-web", title="<button>"),
]
mobile = {
    "id": "mobile", "label": "Mobile", "title": "Du JavaScript, deux façons de faire une app",
    "body": ["React Native affiche les composants du système. Capacitor glisse une vraie page web dans l'app."],
    "hud": [{"label": "à l'écran", "value": "—"}],
    "show": ["m-code"],
    "links": [],
    "script": [
        wait(900),
        scene(show=["m-rn"], link=[L("m-code", "m-rn")],
              say="Avec **React Native**, tu écris ton app en JavaScript, une seule fois pour iOS et pour Android."),
        wait(1300),
        scene(show=["m-rn-btn", "m-rn-list"], hud=[hud("à l'écran", "composants natifs", "g")],
              say="À l'écran, pas de page web : React Native affiche les **vrais** boutons et les vraies listes du système."),
        wait(1700),
        scene(show=["m-cap", "m-cap-web", "m-cap-btn"], link=[L("m-code", "m-cap")],
              hud=[hud("à l'écran", "une page web", "v")],
              say="Avec **Capacitor**, c'est l'inverse : une vraie page HTML, CSS et JavaScript, glissée dans une app."),
        wait(1700),
        scene(set=[{"id": "m-rn", "label": "publiée sur les boutiques"}, {"id": "m-cap", "label": "publiée sur les boutiques"}],
              say="Les deux se publient sur les boutiques d'applications, et ce que tu sais du web sert dans les deux cas."),
        wait(2600),
    ],
}

# ---------- 3. electron : Chromium pour l'interface, Node.js pour le système
X = [
    ent("x-you", "actor", (-19, 0.8), label="toi"),
    ent("x-app", "layer", (0, 0), (24, 11), "n", title="un logiciel Electron", sub="VS Code, Slack, Discord…"),
    ent("x-chr", "layer", (-5.5, 1.3), (11, 7), "v", parent="x-app", title="Chromium", sub="affiche l'interface"),
    ent("x-ui", "node", (0, 1.4), (9, 2.4), "v", parent="x-chr", title="l'interface", sub="HTML, CSS, JavaScript"),
    ent("x-node", "node", (6, 1.3), (8.5, 3), "g", parent="x-app", title="Node.js", sub="fichiers et système",
        detail="**Node.js** fait tourner du JavaScript hors du navigateur, avec accès aux fichiers et au système."),
    ent("x-disk", "store", (19, 0.8), (7, 3.6), "b", title="ton disque", sub="rapport.txt"),
]
electron = {
    "id": "electron", "label": "Bureau", "title": "Chromium pour l'interface, Node.js pour le système",
    "body": ["Un logiciel Electron emporte deux programmes : Chromium affiche l'interface, Node.js accède aux fichiers."],
    "hud": [{"label": "fichier", "value": "—"}],
    "show": ["x-you", "x-app", "x-chr", "x-ui", "x-disk"],
    "links": [L("x-you", "x-ui")],
    "script": [
        wait(1000),
        scene(set=[{"id": "x-ui", "label": "clic : Ouvrir un fichier"}],
              say="L'interface est une page web, affichée par **Chromium**. Tu cliques sur « Ouvrir un fichier »."),
        wait(1300),
        scene(link=[L("x-ui", "x-disk", dashed=True, label="interdit")], hud=[hud("fichier", "pas d'accès", "r")],
              say="Une page web n'a **pas le droit** de lire ton disque : c'est une protection du navigateur."),
        wait(1600),
        scene(show=["x-node"], unlink=[L("x-ui", "x-disk")], link=[L("x-ui", "x-node"), L("x-node", "x-disk")],
              say="Electron ajoute **Node.js**, qui, lui, accède aux fichiers et au système."),
        send(["x-ui", "x-node", "x-disk"], kind="read", label="lire rapport.txt", reply="contenu"),
        scene(set=[{"id": "x-ui", "label": "rapport.txt affiché"}], hud=[hud("fichier", "ouvert", "g")],
              say="Node.js lit le fichier et le rend à l'interface, qui l'affiche."),
        wait(1400),
        scene(set=[{"id": "x-app", "label": "emporte son propre Chromium"}],
              say="Le prix : chaque logiciel Electron emporte son propre Chromium, et pèse plus lourd qu'un logiciel natif."),
        wait(2600),
    ],
}

# ---------- 4. cibles : trois langages, quatre cibles
TGT = [
    ("t-web", (-13, -7.5), "le navigateur", "une application web"),
    ("t-pwa", (13, -7.5), "une PWA", "installée, hors connexion"),
    ("t-mob", (-13, 7.5), "le téléphone", "React Native, Capacitor"),
    ("t-desk", (13, 7.5), "le bureau", "Electron"),
]
T = [ent("t-code", "node", (0, 0), (12, 3.2), "y", title="HTML, CSS, JavaScript", sub="les mêmes langages")]
T += [ent(id, "node", at, (10.5, 3), "v", title=title, sub=sub) for id, at, title, sub in TGT]
SAY = [
    "Dans le **navigateur** : une application web, sans rien installer.",
    "Installée depuis le navigateur : une **PWA**, qui marche aussi hors connexion.",
    "Sur le **téléphone** : React Native ou Capacitor.",
    "Sur le **bureau** : Electron, avec Chromium et Node.js.",
]
script = [wait(900)]
for i, ((id, *_), say) in enumerate(zip(TGT, SAY)):
    script += [scene(show=[id], link=[L("t-code", id)], hud=[hud("cibles", str(i + 1))], say=say), wait(1100)]
script += [
    scene(set=[{"id": "t-code", "label": "un standard de fait"}],
          say="Quatre cibles, trois langages. Aucune loi ne l'impose, l'usage s'est installé : c'est un **standard de fait**."),
    wait(2800),
]
cibles = {
    "id": "cibles", "label": "Quatre cibles", "title": "Trois langages, quatre cibles",
    "body": ["Les mêmes langages, et souvent une bonne part du même code, du navigateur au bureau."],
    "hud": [{"label": "langages", "value": "3"}, {"label": "cibles", "value": "0"}],
    "show": ["t-code"],
    "links": [],
    "script": script,
}

write({
    "format": "bl-scenes/0.3", "id": "web-everywhere-cibles", "title": "Le web partout : écrans et cibles (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "y", "label": "ton code"}, {"tone": "v", "label": "le web, la page"},
               {"tone": "g", "label": "natif, système"}, {"tone": "b", "label": "tes fichiers"}],
    "entities": R + M + X + T, "steps": [responsive, mobile, electron, cibles],
}, *outputs(HERE, "cibles.scene.json", "web-everywhere-cibles"))
