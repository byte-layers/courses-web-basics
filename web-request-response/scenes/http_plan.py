"""Scène 2D (kit plan) de la section « Une requête, une réponse : le protocole HTTP »
(courses-web-basics/web-request-response).

Quatre étapes, une idée chacune :
- message : la requête et la réponse sont du texte, ligne par ligne ; le corps est du HTML, que le navigateur dessine ;
- cascade : le chargement d'une page vu comme l'onglet Réseau, une ligne par requête, son code, sa durée ;
- codes : les quatre codes de statut à connaître, par famille (le tableau est dans la scène) ;
- https : la même conversation, d'abord lisible par le trajet, puis chiffrée après le certificat.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Une règle par sorte : une machine (navigateur, serveur) est un plateau layer ; un message HTTP est un layer
qui porte ses lignes (des node) ; la page dessinée est un node dans le navigateur.
Couleurs (message, https) : v le navigateur ; n le serveur ou le trajet ; b la requête ; g la réponse, ce qui est sûr.
Couleurs (cascade) : b la page HTML, y les fichiers qu'elle cite, g les données chargées ensuite.
Couleurs (codes) : une famille, une couleur : g 2xx, b 3xx, y 4xx, r 5xx.
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


XM, YM = 13.5, 6.2          # colonnes des machines, rangées des messages
MSG = (15, 11)              # taille d'un message
LINE = (13, 1.9)            # taille d'une ligne
ROWS = [-2.7, -0.5, 1.7, 3.9]

ents = [
    ent("nav", "layer", (-XM, 0), (8, 13), "v", title="navigateur", sub="le client"),
    ent("page", "node", (0, 2.2), (6, 4), "v", parent="nav", title="la page", sub="dessinée"),
    ent("srv", "layer", (XM, 0), (8, 13), "n", title="serveur web", sub="byte-layers.com"),
    ent("req", "layer", (0, -YM), MSG, "b", title="la requête"),
    ent("q1", "node", (0, ROWS[0]), LINE, "b", parent="req", title="GET /fr/bits/… HTTP/1.1", sub="méthode, chemin, version"),
    ent("q2", "node", (0, ROWS[1]), LINE, "b", parent="req", title="Host: byte-layers.com", sub="le serveur visé"),
    ent("q3", "node", (0, ROWS[2]), LINE, "b", parent="req", title="User-Agent: Mozilla/5.0 …", sub="le navigateur qui demande"),
    ent("q4", "node", (0, ROWS[3]), LINE, "b", parent="req", title="Accept: text/html", sub="le format qu'il préfère"),
    ent("resp", "layer", (0, YM), MSG, "g", title="la réponse"),
    ent("r1", "node", (0, ROWS[0]), LINE, "g", parent="resp", title="HTTP/1.1 200 OK", sub="le code de statut"),
    ent("r2", "node", (0, ROWS[1]), LINE, "g", parent="resp", title="Content-Type: text/html", sub="ce que contient le corps"),
    ent("r3", "node", (0, ROWS[2] + 1.1), LINE, "g", parent="resp", title="<!DOCTYPE html> <html> …", sub="le corps : la page, en texte"),
]

step = {
    "id": "message", "label": "Requête, réponse", "title": "Une requête, une réponse : du texte",
    "body": ["Le navigateur envoie une requête écrite en texte ; le serveur répond en texte, et le corps de la réponse est la page en HTML."],
    "hud": [{"label": "requête", "value": "—"}, {"label": "statut", "value": "—"}],
    "show": ["nav", "srv"],
    "links": [],
    "script": [
        wait(900),
        scene(show=["req", "q1"], link=[L("nav", "req")], hud=[hud("requête", "GET", "b")],
              say="Le navigateur écrit sa **requête**, en texte. Première ligne : la méthode `GET`, le chemin, la version de HTTP."),
        wait(1300),
        scene(show=["q2", "q3", "q4"],
              say="Puis des **en-têtes** : le serveur visé, le navigateur qui demande, le format qu'il préfère."),
        wait(1300),
        scene(link=[L("req", "srv")], ms=300),
        send(["nav", "req", "srv"], label="requête", tone="b"),
        scene(set=[{"id": "srv", "label": "cherche la page"}],
              say="Le serveur lit la requête et cherche la ressource que désigne le chemin."),
        wait(1000),
        scene(show=["resp", "r1"], link=[L("srv", "resp")], set=[{"id": "srv", "label": None}],
              hud=[hud("statut", "200 OK", "g")],
              say="Il répond, lui aussi en texte. Première ligne : le **code de statut**, `200 OK` : la page existe."),
        wait(1300),
        scene(show=["r2", "r3"],
              say="Un en-tête dit ce que contient la réponse ; après une ligne vide vient le **corps** : la page, écrite en HTML."),
        wait(1300),
        scene(link=[L("resp", "nav")], ms=300),
        send(["srv", "resp", "nav"], label="réponse", tone="g"),
        scene(show=["page"], set=[{"id": "nav", "label": "lit le HTML"}],
              say="Le navigateur ne reçoit pas une image : il **lit ce texte** et dessine la page lui-même."),
        wait(2800),
    ],
}


# ---------- 2. la cascade : le chargement vu comme l'onglet Réseau
X0, U = -8.5, 1.55          # début de l'axe du temps, largeur d'une unité de temps
RY = [-5, -2.8, -0.6, 1.6, 3.8]


def bar(id, start, dur, y, tone, title="200"):
    return ent(id, "node", (X0 + (start + dur / 2) * U, y), (dur * U, 1.6), tone, title=title)


def row(id, y, tone, title, sub):
    return ent(id, "node", (-14, y), (8.4, 1.7), tone, title=title, sub=sub)


ents += [
    ent("axe", "zone", (X0 + 9.2 * U, -7.2), (19 * U, 1.1), None, label="temps →"),
    row("w-html", RY[0], "b", "la page", "document HTML"), bar("b-html", 0, 4, RY[0], "b"),
    row("w-css", RY[1], "y", "style.css", "feuille de style"), bar("b-css", 4.3, 2.4, RY[1], "y"),
    row("w-js", RY[2], "y", "script.js", "script"), bar("b-js", 4.3, 2, RY[2], "y"),
    row("w-logo", RY[3], "y", "logo.svg", "image"), bar("b-logo", 4.6, 3, RY[3], "y"),
    row("w-data", RY[4], "g", "/api/projets", "données, en JSON"), bar("b-data", 8.6, 3, RY[4], "g"),
]

cascade = {
    "id": "cascade", "label": "Le chargement", "title": "Le chargement d'une page, requête par requête",
    "body": ["Comme l'onglet Réseau du navigateur : une ligne par requête, avec son code de statut et sa durée."],
    "hud": [{"label": "requêtes", "value": 0}, {"label": "page", "value": "—"}],
    "show": ["axe"],
    "links": [],
    "script": [
        wait(800),
        scene(show=["w-html", "b-html"], hud=[hud("requêtes", 1), hud("page", "en cours", "b")],
              say="D'abord une seule requête, pour la page. La réponse arrive avec le code `200` : tout va bien."),
        wait(1400),
        scene(show=["w-css", "b-css", "w-js", "b-js", "w-logo", "b-logo"], hud=[hud("requêtes", 4)],
              say="Le navigateur lit le HTML, y trouve trois adresses, et les demande **en même temps**."),
        wait(1400),
        scene(set=[{"id": "b-css", "label": "CSS"}, {"id": "b-js", "label": "JS"}, {"id": "b-logo", "label": "image"}],
              hud=[hud("page", "affichée", "g")],
              say="Chaque ligne a son propre **code de statut** : ici, `200` partout. La page s'affiche."),
        wait(1400),
        scene(show=["w-data", "b-data"], hud=[hud("requêtes", 5)],
              say="Si la page charge des **données**, son JavaScript envoie encore des requêtes, après l'affichage."),
        wait(1400),
        scene(say="Une page, plusieurs requêtes, chacune avec son code : c'est ce qu'on lit dans l'onglet **Réseau**.", ms=300,
              set=[{"id": "b-data", "label": "fetch"}]),
        wait(2800),
    ],
}

# ---------- 3. les codes de statut, par famille
CY = [-5.4, -1.8, 1.8, 5.4]


def code(id, y, tone, title, sub):
    return ent(id, "node", (-9, y), (9, 2.6), tone, title=title, sub=sub)


def sens(id, y, tone, title, sub):
    return ent(id, "node", (6.5, y), (17, 2.6), tone, title=title, sub=sub)


ents += [
    code("c200", CY[0], "g", "200 OK", "2xx · succès"),
    sens("s200", CY[0], "g", "la ressource existe, la voici", "à l'écran : la page s'affiche"),
    code("c301", CY[1], "b", "301 Moved Permanently", "3xx · redirection"),
    sens("s301", CY[1], "b", "déménagée : voici la nouvelle adresse", "à l'écran : l'adresse change toute seule"),
    code("c404", CY[2], "y", "404 Not Found", "4xx · erreur du client"),
    sens("s404", CY[2], "y", "rien à cette adresse", "à l'écran : une page « introuvable »"),
    code("c500", CY[3], "r", "500 Internal Server Error", "5xx · erreur du serveur"),
    sens("s500", CY[3], "r", "le serveur a planté pendant la réponse", "à l'écran : une page d'erreur, pas ta faute"),
]

codes = {
    "id": "codes", "label": "Les codes", "title": "Quatre codes, quatre familles",
    "body": ["Le premier chiffre du code de statut donne la famille de la réponse."],
    "hud": [{"label": "famille", "value": "—"}],
    "show": ["c200", "c301", "c404", "c500"],
    "links": [],
    "script": [
        wait(900),
        scene(show=["s200"], link=[L("c200", "s200")], hud=[hud("famille", "2xx : succès", "g")],
              say="`200` : la ressource existe, le serveur l'envoie. C'est le code de presque toutes les lignes."),
        wait(1500),
        scene(show=["s301"], link=[L("c301", "s301")], hud=[hud("famille", "3xx : redirection", "b")],
              say="`301` : la ressource a déménagé. La réponse donne la nouvelle adresse, et le navigateur refait la requête tout seul."),
        wait(1500),
        scene(show=["s404"], link=[L("c404", "s404")], hud=[hud("famille", "4xx : côté client", "y")],
              say="`404` : rien à cette adresse. La demande est en cause : une faute de frappe, une page supprimée."),
        wait(1500),
        scene(show=["s500"], link=[L("c500", "s500")], hud=[hud("famille", "5xx : côté serveur", "r")],
              say="`500` : le serveur a planté en préparant la réponse. Là, ce n'est pas ta demande qui est en cause."),
        wait(3000),
    ],
}

# ---------- 4. HTTPS : la même conversation, chiffrée
ents += [
    ent("tunnel", "zone", (0, 0), (35, 6.5), "g", label="connexion chiffrée"),
    ent("h-nav", "node", (-13, 0), (7, 3.6), "v", title="navigateur", sub="le client"),
    ent("h-wifi", "node", (0, 0), (9, 3.6), "n", title="Wi-Fi du café", sub="une machine sur le trajet"),
    ent("h-srv", "node", (13, 0), (7, 3.6), "n", title="serveur web", sub="byte-layers.com"),
    ent("h-vu", "node", (0, -6.4), (16, 2.6), "r", title="GET /compte · mot de passe=…", sub="ce que lit le trajet"),
    ent("h-cert", "node", (13, 6.4), (10, 2.6), "g", title="certificat", sub="byte-layers.com, signé"),
]

https = {
    "id": "https", "label": "HTTPS", "title": "La même conversation, chiffrée",
    "body": ["HTTPS ne change pas les requêtes ni les réponses : il les fait passer dans une connexion chiffrée, après avoir vérifié le serveur."],
    "hud": [{"label": "adresse", "value": "http://"}, {"label": "le trajet lit", "value": "—"}],
    "show": ["h-nav", "h-wifi", "h-srv"],
    "links": [L("h-nav", "h-wifi"), L("h-wifi", "h-srv")],
    "script": [
        wait(800),
        send(["h-nav", "h-wifi", "h-srv"], label="GET /compte", tone="b"),
        scene(show=["h-vu"], link=[L("h-wifi", "h-vu", dashed=True)], hud=[hud("le trajet lit", "tout", "r")],
              say="Avec `http://`, la requête voyage **en clair** : chaque machine du trajet peut la lire."),
        wait(1600),
        scene(hide=["h-vu"], show=["h-cert"], link=[L("h-srv", "h-cert")], hud=[hud("adresse", "https://", "g"), hud("le trajet lit", "—", None)],
              say="Avec `https://`, le serveur commence par montrer son **certificat**, qui prouve qui il est."),
        wait(1200),
        scene(set=[{"id": "h-nav", "label": "certificat vérifié : cadenas"}],
              say="Le navigateur le vérifie : c'est le **cadenas** à côté de l'adresse."),
        wait(1200),
        scene(show=["tunnel"], say="Les deux établissent alors une **connexion chiffrée**."),
        wait(1000),
        send(["h-nav", "h-wifi", "h-srv"], label="GET /compte", tone="b"),
        scene(show=["h-vu"], link=[L("h-wifi", "h-vu", dashed=True)], ms=200),
        scene(set=[{"id": "h-vu", "title": "x9#fQ2…L7%k", "sub": "illisible", "tone": "g"}],
              hud=[hud("le trajet lit", "du bruit", "g")],
              say="La même requête passe : le trajet ne voit plus que du bruit. À l'intérieur, rien ne change."),
        wait(2800),
    ],
}

MSG_IDS = {"nav", "page", "srv", "req", "q1", "q2", "q3", "q4", "resp", "r1", "r2", "r3",
           "tunnel", "h-nav", "h-wifi", "h-srv", "h-vu", "h-cert"}

lesson = {
    "format": "bl-scenes/0.3", "id": "web-request-response-http", "title": "Une requête, une réponse (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "n", "label": "serveur, trajet"},
               {"tone": "b", "label": "requête"}, {"tone": "g", "label": "réponse, chiffré"},
               {"tone": "r", "label": "lu par le trajet"}],
    "entities": [e for e in ents if e["id"] in MSG_IDS], "steps": [step, https],
}
write(lesson, *outputs(HERE, "http-message.scene.json", "web-http-message"))

lesson_cascade = {
    "format": "bl-scenes/0.3", "id": "web-request-response-cascade", "title": "Le chargement d'une page (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "b", "label": "la page HTML"}, {"tone": "y", "label": "fichiers cités"},
               {"tone": "g", "label": "données, ensuite"}],
    "entities": [e for e in ents if e["id"] == "axe" or e["id"][:2] in ("w-", "b-")], "steps": [cascade],
}
write(lesson_cascade, *outputs(HERE, "http-cascade.scene.json", "web-http-cascade"))

lesson_codes = {
    "format": "bl-scenes/0.3", "id": "web-request-response-codes", "title": "Les codes de statut (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "g", "label": "2xx succès"}, {"tone": "b", "label": "3xx redirection"},
               {"tone": "y", "label": "4xx erreur client"}, {"tone": "r", "label": "5xx erreur serveur"}],
    "entities": [e for e in ents if e["id"][:1] in ("c", "s") and e["id"][1:].isdigit()], "steps": [codes],
}
write(lesson_codes, *outputs(HERE, "http-codes.scene.json", "web-http-codes"))
