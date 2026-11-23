"""Scènes du bit « Le web : une adresse, une requête, une page » (courses-web-basics/web-request-response).

Kit Feuilleté. Trois étapes, une idée chacune :
- url : ce que le navigateur fait de chaque morceau d'une URL (le domaine devient une adresse, le chemin part
  dans la requête, le `#` reste chez lui) ;
- plusieurs : une page = une requête par fichier (le HTML d'abord, puis ce qu'il cite) ;
- disque : `file://` lit le disque sans serveur ; un petit serveur local rend les codes de statut.

Une règle par sorte : le navigateur est un bloc devant (il demande) ; un serveur est un plateau (layer) derrière,
qui porte les fichiers qu'il sert ; l'annuaire des noms est un bloc. Lecture de bas en haut : ce qui demande devant,
ce qui répond derrière.
Couleurs : v ce qui est chez toi (navigateur, disque, petit serveur local), b ce qui est sur Internet (annuaire,
serveur web), y les fichiers (du texte). Les paquets gardent les couleurs du type (requête, réponse).
Grille d'écran G(sx, sy) : navigateur en sy 8, serveurs en sy -4.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import G, L, scene, send, wait, write, hud

Y_FRONT, Y_BACK = 8, -4

ents = [
    {"id": "you", "kind": "actor", "at": G(-6.5, 12), "label": "toi"},
    {"id": "nav", "kind": "node", "at": G(0, Y_FRONT), "tone": "v", "title": "navigateur", "icon": "◧",
     "detail": "Le **navigateur** (Chrome, Firefox, Safari…) est le **client** : il envoie les requêtes et dessine la page qu'il reçoit."},
    {"id": "dns", "kind": "node", "at": G(-8, Y_BACK), "tone": "b", "title": "annuaire des noms", "sub": "DNS",
     "detail": "Le **DNS** (*Domain Name System*) est l'annuaire d'Internet : on lui donne un nom de domaine, il répond l'adresse de la machine qui le sert."},
    {"id": "srv", "kind": "node", "at": G(4, Y_BACK), "tone": "b", "icon": "⇄", "title": "serveur web",
     "sub": "byte-layers.com",
     "detail": "Le **serveur web** est un programme qui attend les requêtes HTTP sur une machine, et renvoie les fichiers demandés."},
    {"id": "f-html", "kind": "file", "at": G(-0.5, Y_BACK - 10.5), "tone": "y", "title": "la page",
     "detail": "Le **HTML** de la page : du texte."},
    {"id": "f-css", "kind": "file", "at": G(4, Y_BACK - 10.5), "tone": "y", "title": "style.css",
     "detail": "La **feuille de style** de la page, citée dans son HTML."},
    {"id": "f-logo", "kind": "file", "at": G(8.5, Y_BACK - 10.5), "tone": "y", "title": "logo.svg",
     "detail": "Une **image**, citée elle aussi dans le HTML."},
    # page ouverte depuis le disque
    {"id": "disk", "kind": "store", "at": G(-3, Y_BACK - 2), "tone": "v", "title": "ton disque", "sub": "index.html",
     "detail": "Le **disque** de ta machine. Avec `file://`, le navigateur y lit le fichier lui-même : aucun programme ne lui répond."},
    {"id": "live", "kind": "node", "at": G(5, 1), "tone": "v", "title": "petit serveur local", "sub": "Live Preview",
     "detail": "Une extension comme **Live Preview** lance un serveur web sur ta machine, à l'adresse `127.0.0.1`. Il lit les fichiers sur ton disque et les sert en HTTP."},
]

steps = []

# ---------- 1. l'URL, morceau par morceau
steps.append({
    "id": "url", "label": "Une URL", "title": "Ce que le navigateur fait d'une URL",
    "body": ["Le navigateur découpe l'adresse : le nom de domaine lui dit quelle machine joindre, le chemin quelle ressource demander."],
    "hud": [{"label": "protocole", "value": "https"}, {"label": "domaine", "value": "byte-layers.com"},
            {"label": "chemin", "value": "/fr/bits/…"}, {"label": "ancre #", "value": "#section1"}],
    "show": ["you", "nav"],
    "links": [L("you", "nav")],
    "script": [
        wait(900),
        scene(say="Tu tapes une adresse. Le navigateur la découpe : protocole, nom de domaine, chemin, et une **ancre** `#section1` à la fin.",
              set=[{"id": "nav", "label": "https://byte-layers.com/…#section1"}]),
        wait(1300),
        scene(say="Un nom ne suffit pas pour se connecter : il demande d'abord à l'annuaire l'adresse de la machine.",
              show=["dns"], link=[L("nav", "dns")], hud=[hud("domaine", "byte-layers.com")]),
        send(["nav", "dns"], label="byte-layers.com ?", reply="203.0.113.10"),
        scene(say="Avec cette adresse, il se connecte au serveur web. `https` : la connexion est chiffrée.",
              show=["srv", "f-html"], link=[L("nav", "srv"), L("srv", "f-html")], hud=[hud("protocole", "https, chiffré")]),
        wait(900),
        send(["nav", "srv"], label="GET /fr/bits/…", reply="200, la page",
             explain=["Seul le **chemin** part dans la requête : il dit quelle ressource donner.",
                      "Le serveur répond par le texte de la page."]),
        scene(say="L'ancre `#section1` n'est jamais partie : c'est un **repère** dans la page reçue, et le navigateur y descend.",
              set=[{"id": "nav", "label": "descend à #section1"}], hud=[hud("ancre #", "repère dans la page")]),
        wait(2600),
    ],
})

# ---------- 2. une page, plusieurs requêtes
steps.append({
    "id": "plusieurs", "label": "Une par fichier", "title": "Une page, une requête par fichier",
    "body": ["Le HTML arrive seul. Le navigateur y trouve les adresses des autres fichiers, et les demande un par un."],
    "hud": [{"label": "requêtes", "value": 0}],
    "show": ["you", "nav", "srv", "f-html", "f-css", "f-logo"],
    "links": [L("you", "nav"), L("nav", "srv"), L("srv", "f-html"), L("srv", "f-css"), L("srv", "f-logo")],
    "script": [
        wait(900),
        send(["nav", "srv"], label="GET la page", reply="200, le HTML",
             explain=["Le navigateur demande la page.", "Il reçoit son HTML, et rien d'autre."]),
        scene(hud=[hud("requêtes", 1)], ms=300),
        scene(say="Il lit le HTML et y trouve deux adresses : `style.css` et `logo.svg`.",
              set=[{"id": "nav", "label": "cite style.css, logo.svg"}]),
        wait(1200),
        send(["nav", "srv"], label="GET /style.css", reply="200",
             explain=["Une deuxième requête, pour la feuille de style.", "Le serveur la renvoie."]),
        scene(hud=[hud("requêtes", 2)], ms=300),
        send(["nav", "srv"], label="GET /logo.svg", reply="200",
             explain=["Une troisième, pour l'image.", "Le serveur la renvoie aussi."]),
        scene(hud=[hud("requêtes", 3)], ms=300),
        scene(say="Trois fichiers, trois requêtes : le navigateur peut dessiner la page.",
              set=[{"id": "nav", "label": "dessine la page"}]),
        wait(2600),
    ],
})

# ---------- 3. file:// ou http://
steps.append({
    "id": "disque", "label": "Depuis le disque", "title": "file:// : pas de serveur",
    "body": ["Par un double-clic, le navigateur lit le fichier sur ton disque. Personne ne lui répond, donc pas de code de statut."],
    "hud": [{"label": "adresse", "value": "file:///…/index.html"}, {"label": "serveur", "value": "aucun"},
            {"label": "code de statut", "value": "aucun"}],
    "show": ["you", "nav", "disk"],
    "links": [L("you", "nav"), L("nav", "disk")],
    "script": [
        wait(900),
        send(["nav", "disk"], kind="read", label="lit index.html",
             explain=["Avec `file://`, le navigateur lit le fichier lui-même, sur ton disque."]),
        scene(say="Aucun serveur entre les deux : pas de requête HTTP, pas de code de statut.",
              set=[{"id": "nav", "label": "le fichier existe, ou non"}]),
        wait(1500),
        scene(say="Une extension comme Live Preview lance un petit serveur web sur ta machine.",
              show=["live"], unlink=[L("nav", "disk")], link=[L("nav", "live"), L("live", "disk")],
              set=[{"id": "nav", "label": None}],
              hud=[hud("adresse", "http://127.0.0.1:3000/"), hud("serveur", "sur ta machine")]),
        wait(900),
        send(["nav", "live", "disk"], label="GET /index.html", reply="200",
             explain=["Le navigateur envoie une vraie requête HTTP au petit serveur.",
                      "Le serveur lit le fichier sur ton disque.",
                      "Il répond avec un code de statut, comme un serveur en ligne."]),
        scene(say="La page est maintenant servie : tu vois de vrais codes de statut, comme en ligne.",
              hud=[hud("code de statut", "200")]),
        wait(2600),
    ],
})
lesson = {
    "format": "bl-scenes/0.3", "id": "web-request-response", "title": "Une adresse, une requête, une page",
    "lang": "fr", "kit": "feuillete",
    "legend": [{"tone": "v", "label": "chez toi"}, {"tone": "b", "label": "sur Internet"},
               {"kind": "req", "label": "requête"}, {"kind": "res", "label": "réponse"}],
    "entities": ents, "steps": steps,
}
write(lesson, *outputs(HERE, "http.scene.json", "web-http"))
