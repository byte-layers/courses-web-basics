"""Scènes du bit « Le web partout » (courses-web-basics/web-everywhere).

Kit Feuilleté. Trois étapes, une idée chacune :
- appli : sur un site, chaque clic rapporte une page entière ; dans une application web, le JavaScript ne demande
  que des données et met la page à jour sans la recharger ;
- installer : le navigateur lit le manifeste (manifest.json, dans un widget editor), propose « Installer » ; un clic
  pose une icône, l'icône ouvre l'application dans sa propre fenêtre, sans barre d'adresse ;
- pwa : le service worker se place entre la page et le réseau, garde une copie des fichiers et la sert hors connexion.

Une règle par sorte : le navigateur est un bloc devant (il demande), le serveur un bloc derrière (il répond) ; le
service worker est un petit programme entre les deux, sa réserve un cylindre (on y range des fichiers) ; le manifeste
est un fichier ; l'icône installée et la fenêtre de l'application sont des blocs chez toi.
Couleurs : v ce qui tourne chez toi (navigateur, service worker, réserve), b ce qui est sur Internet (serveur),
g les données (paquets d'une application web). Le trafic de la PWA est un flux continu : on voit où il va.
Grille d'écran G(sx, sy) : navigateur en sy 8, serveur en sy -9.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import G, L, scene, send, wait, write, hud, traffic


def line(n):
    return {"do": "line", "n": n}


ents = [
    {"id": "you", "kind": "actor", "at": G(-6.5, 12), "label": "toi"},
    {"id": "nav", "kind": "node", "at": G(0, 8), "tone": "v", "title": "navigateur", "icon": "◧",
     "detail": "Le **navigateur** affiche l'interface. Dans une application web, c'est le JavaScript de la page qui réagit à chaque clic."},
    {"id": "srv", "kind": "node", "at": G(6, -9), "tone": "b", "title": "serveur", "icon": "⇄",
     "detail": "Le **serveur** garde les données (les messages, les documents) et les fichiers de l'application."},
    {"id": "sw", "kind": "program", "at": G(3, 0), "tone": "v", "title": "service worker",
     "detail": "Le **service worker** est un fichier JavaScript que la page installe. Il tourne en arrière-plan, entre la page et le réseau."},
    {"id": "cache", "kind": "store", "at": G(-5, -5), "tone": "v", "title": "réserve", "sub": "copie des fichiers",
     "detail": "Une **réserve** gérée par le navigateur, où le service worker range une copie des fichiers de l'application."},
    {"id": "manifest", "kind": "file", "at": G(-6, 1), "tone": "v", "title": "manifest.json", "icon": "{ }",
     "detail": "Le **manifeste** : un petit fichier JSON qui donne le nom de l'application, son icône, ses couleurs et sa façon de s'ouvrir. La page le cite avec `<link rel=\"manifest\" href=\"manifest.json\">`."},
    {"id": "icon", "kind": "node", "at": G(-1, 15), "size": [1.6, 1.6, 0.85], "tone": "v", "title": "icône Messagerie", "icon": "✉",
     "detail": "L'**icône** posée par l'installation, sur l'écran d'accueil du téléphone ou dans le menu des applications de l'ordinateur."},
    {"id": "win", "kind": "node", "at": G(6, 6), "tone": "v", "title": "fenêtre Messagerie", "sub": "sans barre d'adresse", "icon": "▢",
     "detail": "L'application installée s'ouvre dans **sa propre fenêtre**, sans barre d'adresse ni onglets : on dirait une application du système."},
]

MANIFEST = [
    "{",
    '  "name": "Messagerie",',
    '  "icons": [{ "src": "icone-512.png", "sizes": "512x512" }],',
    '  "theme_color": "#6b72e8",',
    '  "start_url": "/",',
    '  "display": "standalone"',
    "}",
]

steps = []

# ---------- 1. site ou application web
steps.append({
    "id": "appli", "label": "Site ou appli", "title": "Un site recharge, une application met à jour",
    "body": ["Sur un site, chaque clic rapporte une page entière. Une application web ne demande que des données, et son JavaScript met la page à jour."],
    "hud": [{"label": "sorte", "value": "site"}, {"label": "à chaque clic", "value": "page entière"}],
    "show": ["you", "nav", "srv"],
    "links": [L("you", "nav"), L("nav", "srv")],
    "script": [
        wait(900),
        send(["nav", "srv"], label="clic : GET /page-2", reply="page entière",
             explain=["Sur un site, un clic sur un lien demande une nouvelle page au serveur.",
                      "Le serveur renvoie une page entière, que le navigateur redessine de zéro."]),
        wait(700),
        scene(say="Une application web charge sa page et son JavaScript une fois, au début.",
              set=[{"id": "nav", "label": "JavaScript chargé"}],
              hud=[hud("sorte", "application web"), hud("à chaque clic", "?")]),
        wait(1200),
        send(["nav", "srv"], tone="g", label="nouveaux messages ?", reply="données",
             explain=["Ensuite, à chaque clic, le JavaScript ne demande que des **données**.",
                      "Le serveur ne renvoie que ces données, pas de page."]),
        scene(say="Le JavaScript les place dans la page déjà affichée, sans la recharger.",
              set=[{"id": "nav", "label": "met la page à jour"}], hud=[hud("à chaque clic", "données seules", "g")]),
        wait(2600),
    ],
})

# ---------- 2. PWA : installer avec le manifeste
steps.append({
    "id": "installer", "label": "Installer", "title": "Le manifeste rend l'application installable",
    "body": ["Le navigateur lit le manifeste de l'application. Il y trouve un nom et une icône, et propose « Installer » : un clic, et l'application a son icône et sa fenêtre."],
    "hud": [{"label": "icône", "value": "aucune"}, {"label": "barre d'adresse", "value": "oui"}],
    "show": ["you", "nav", "srv"],
    "links": [L("you", "nav"), L("nav", "srv")],
    "widgets": [{"kind": "editor", "title": "manifest.json", "lang": "text", "lines": MANIFEST}],
    "script": [
        wait(900),
        send(["nav", "srv"], label="GET manifest.json", reply="manifest.json",
             explain=["La page cite son **manifeste** : le navigateur le demande au serveur.",
                      "Le serveur renvoie ce petit fichier de réglages, écrit en JSON."]),
        scene(show=["manifest"], link=[L("nav", "manifest", dashed=True)],
              say="Le navigateur lit le manifeste."),
        line(2),
        scene(set=[{"id": "manifest", "label": "nom : Messagerie"}],
              say="Il y trouve le **nom** de l'application…"),
        line(3),
        scene(say="… et son **icône**. Avec ces deux réglages, il propose un bouton « Installer ».",
              set=[{"id": "manifest", "label": "icône : icone-512.png"}, {"id": "nav", "label": "propose « Installer »"}]),
        wait(900), line(0),
        send(["you", "nav"], label="clic : Installer"),
        scene(show=["icon"], link=[L("nav", "icon", dashed=True)], hud=[hud("icône", "installée", "v")],
              set=[{"id": "nav", "label": None}, {"id": "manifest", "label": None}],
              say="Une **icône** apparaît sur l'écran d'accueil, ou dans le menu des applications."),
        wait(1200),
        send(["you", "icon"], label="clic sur l'icône"),
        line(6),
        scene(show=["win"], link=[L("icon", "win")], set=[{"id": "nav", "dim": True}],
              hud=[hud("barre d'adresse", "non", "v")],
              say="`\"display\": \"standalone\"` : l'application s'ouvre dans **sa propre fenêtre**, sans barre d'adresse."),
        wait(2600), line(0),
    ],
})

# ---------- 3. PWA hors connexion
steps.append({
    "id": "pwa", "label": "Hors connexion", "title": "Le service worker sert la réserve",
    "body": ["Le service worker se place entre la page et le réseau. Il garde une copie des fichiers, et la sert quand le réseau manque."],
    "hud": [{"label": "réseau", "value": "connecté"}, {"label": "application", "value": "s'affiche"}],
    "show": ["you", "nav", "sw", "srv"],
    "links": [L("you", "nav"), L("nav", "sw"), L("sw", "srv")],
    "flows": [traffic(["nav", "sw"], gap=700, fallback="erreur")],
    "script": [
        wait(1200),
        scene(say="Les requêtes de la page passent par le service worker, puis par le réseau jusqu'au serveur.",
              set=[{"id": "sw", "label": "entre la page et le réseau"}]),
        wait(1300),
        scene(show=["cache"], link=[L("sw", "cache", dashed=True)],
              say="Il garde une copie des fichiers de l'application dans une réserve."),
        send(["sw", "cache"], kind="read", label="copie"),
        wait(900),
        scene(unlink=[L("sw", "srv"), L("sw", "cache")], link=[L("sw", "cache")], set=[{"id": "srv", "dim": True}],
              hud=[hud("réseau", "coupé", "r")],
              say="Plus de réseau : le service worker répond avec la copie gardée en réserve."),
        wait(1600),
        scene(set=[{"id": "nav", "label": "s'ouvre hors connexion"}], hud=[hud("application", "s'affiche toujours", "g")],
              say="L'application s'ouvre et s'affiche, même dans le train."),
        wait(2600),
    ],
})

lesson = {
    "format": "bl-scenes/0.3", "id": "web-everywhere", "title": "Le web partout",
    "lang": "fr", "kit": "feuillete",
    "legend": [{"tone": "v", "label": "chez toi"}, {"tone": "b", "label": "sur Internet"},
               {"tone": "g", "label": "données"}, {"kind": "req", "label": "requête"}, {"kind": "res", "label": "réponse"}],
    "entities": ents, "steps": steps,
}
write(lesson, *outputs(HERE, "everywhere.scene.json", "web-everywhere"))
