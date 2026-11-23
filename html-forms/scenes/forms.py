"""Scènes 2D (kit plan) du bit « Les formulaires HTML » (html-forms).

Quatre étapes dans assets/forms.scene.json :
  formulaire (section « Un formulaire ») : label for → id, le clic sur l'étiquette, puis name=valeur envoyé au serveur.
  methode    (section « Comment les données partent : method ») : avec get, les données s'ajoutent à l'adresse après
             un ? ; avec post, l'adresse reste la même et les données voyagent dans la requête.
  controle   (section « Contrôler la saisie : required et type ») : champ vide refusé, adresse sans @ refusée, adresse
             complète envoyée ; puis un script envoie au serveur sans passer par le formulaire : le serveur revérifie.
  envoi      (section « Les pièges ») : à l'envoi, le navigateur envoie chaque valeur sous le name de son champ ;
             un champ sans name (le téléphone, pas le message de l'exercice) ne part pas.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; entités au premier niveau.
Dessin : le formulaire, la page = layer ; un champ, l'adresse, un bouton = node ; le serveur = store.
Couleurs : y valeur saisie, v étiquette et bouton, r ce qui est refusé ou ne part pas, b le serveur.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import L, hud, scene, send, wait, write


def r(v):
    return round(v, 3)


def ent(id, kind, x0, y0, w, h, tone=None, **kw):
    d = {"id": id, "kind": kind, "at": [r(x0 + w / 2), r(y0 + h / 2)], "size": [r(w), r(h), 1]}
    if tone: d["tone"] = tone
    if kind == "actor": del d["size"]
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


ents = []

def sub_ent(id, kind, parent, at, size, tone=None, **kw):
    d = {"id": id, "kind": kind, "in": parent, "at": list(at)}
    if size: d["size"] = list(size) + ([] if kind == "zone" else [1])
    if tone: d["tone"] = tone
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


# ── Étape 5 : un champ relié, et ce qu'il envoie ──────────────────────────────────────────────────────────────
ents.append({"id": "fm-form", "kind": "layer", "at": [-4, 0], "size": [12, 9.6, 1], "tone": "n", "title": 'form action="/contact"',
             "detail": "`<form>` contient les champs ; `action` est l'adresse qui reçoit les données."})
ents.append(sub_ent("fm-label", "node", "fm-form", (0, -2.3), (10, 1.5), "v", title="label : Votre e-mail", sub='for="email"',
                    detail="L'**étiquette** : son `for` reprend exactement l'`id` du champ."))
ents.append(sub_ent("fm-input", "node", "fm-form", (0, 0.4), (10, 1.6), "y", title="input", sub='id="email" name="email"',
                    detail="Le **champ** : `id` pour la page (le `for` le vise), `name` pour le serveur."))
ents.append(sub_ent("fm-submit", "node", "fm-form", (3.0, 3.0), (3.6, 1.1), "v", title="Envoyer"))
ents.append({"id": "fm-server", "kind": "store", "at": [8.6, 0.4], "size": [4.0, 2.4, 1], "tone": "b", "title": "serveur"})

formulaire = {
    "id": "formulaire", "label": "for, id, name", "title": "Un champ relié, et ce qu'il envoie",
    "body": ["Un formulaire de contact réduit à un champ : l'e-mail, et son étiquette."],
    "show": ["fm-form", "fm-label", "fm-input", "fm-submit", "fm-server"],
    "hud": [{"label": "reçu", "value": "rien"}],
    "script": [
        wait(1000),
        scene(say="Le for de l'étiquette reprend l'id du champ : l'étiquette est reliée à ce champ.",
              link=[L("fm-label", "fm-input", label="for = id")]),
        wait(1300),
        {"do": "pulse", "at": "fm-label"},
        scene(say="Un clic sur l'étiquette met le curseur dans le champ ; un lecteur d'écran l'annonce en y arrivant.",
              set=[{"id": "fm-input", "label": "le curseur arrive ici"}]),
        wait(1300),
        scene(say="Le visiteur tape son adresse.", set=[{"id": "fm-input", "label": "camille@exemple.fr"}]),
        wait(1000),
        {"do": "pulse", "at": "fm-submit"},
        scene(say="À l'envoi, la valeur part sous le name du champ : email=…, le @ codé en %40.",
              link=[L("fm-input", "fm-server")]),
        send(["fm-input", "fm-server"], label="email=camille%40exemple", tone="y"),
        scene(hud=[hud("reçu", "email", "g")]),
        wait(2600),
    ],
}

# ── Étape 2 : ce que le formulaire envoie ─────────────────────────────────────────────────────────────────────
FX0, FW, FH = -8.0, 8.4, 1.5
# Le champ sans name est le téléphone : l'exercice qui suit a son propre champ sans name (le message), à trouver.
FIELDS = [("f-nom", "Nom", 'name="nom"', "Camille"), ("f-email", "E-mail", 'name="email"', "camille@exemple.fr"),
          ("f-tel", "Téléphone", 'id="tel"', "06 12 34 56 78")]
ents.append(ent("form", "layer", FX0 - 0.6, -4.6, FW + 1.2, 10.0, "n", title="form",
                detail="Un formulaire : tous ses champs vivent dans `<form>`, qui dit où envoyer les données."))
for k, (fid, title, sub, _) in enumerate(FIELDS):
    ents.append(ent(fid, "node", FX0, -3.0 + k * 2.1, FW, FH, "y", title=title, sub=sub,
                    detail="Un champ `input` : son attribut **`name`** est le nom sous lequel la valeur part au serveur." if k == 0 else None))
ents.append(ent("submit", "node", FX0 + FW - 3.6, 3.4, 3.6, 1.1, "v", title="Envoyer"))
ents.append(ent("server", "store", 6.4, -1.4, 4.0, 2.4, "b", title="serveur",
                detail="Le serveur reçoit les valeurs sous la forme `nom=valeur`, une par champ qui a un `name`."))

envoi = {
    "id": "envoi", "label": "Un champ sans name", "title": "Ce que le serveur reçoit",
    "body": ["Un formulaire de contact à trois champs. À l'écran, rien ne les distingue."],
    "show": ["form", "f-nom", "f-email", "f-tel", "submit", "server"],
    "hud": [{"label": "reçu", "value": "rien"}],
    "script": [
        wait(900),
        scene(say="Le visiteur remplit les trois champs : à l'écran, ils se comportent tous pareil.",
              set=[{"id": fid, "label": val} for fid, _, _, val in FIELDS]),
        wait(1300),
        {"do": "pulse", "at": "submit"},
        scene(say="Il clique sur Envoyer : le navigateur envoie chaque valeur sous le name de son champ.",
              link=[L("f-nom", "server"), L("f-email", "server")]),
        send(["f-nom", "server"], label="nom=Camille", tone="y"),
        scene(hud=[hud("reçu", "nom", "g")]),
        send(["f-email", "server"], label="email=camille…", tone="y"),
        scene(hud=[hud("reçu", "nom, email", "g")]),
        wait(600),
        scene(say="Le téléphone n'a pas d'attribut name : sa valeur ne part pas, et rien ne le signale.",
              set=[{"id": "f-tel", "tone": "r", "sub": "pas de name"}]),
        wait(2600),
    ],
}

# ── Étape : method, get ou post ───────────────────────────────────────────────────────────────────────────────
ents.append({"id": "mt-bar", "kind": "node", "at": [-1.5, -4.2], "size": [17, 1.3, 1], "tone": "n", "title": "adresse",
             "sub": "exemple.fr/contact",
             "detail": "La **barre d'adresse** du navigateur : l'adresse de la page demandée au serveur."})
ents.append({"id": "mt-form", "kind": "layer", "at": [-5, 0.8], "size": [10, 6, 1], "tone": "n", "title": 'form action="/contact"',
             "detail": "`action` donne l'adresse qui reçoit les données ; `method` dit comment elles partent."})
ents.append(sub_ent("mt-input", "node", "mt-form", (0, -0.8), (8.4, 1.6), "y", title="input", sub='name="email"',
                    label="camille@exemple.fr"))
ents.append(sub_ent("mt-submit", "node", "mt-form", (2.4, 1.6), (3.2, 1.1), "v", title="Envoyer"))
ents.append({"id": "mt-server", "kind": "store", "at": [8.4, 0.8], "size": [4.0, 2.4, 1], "tone": "b", "title": "serveur"})

methode = {
    "id": "methode", "label": "get ou post", "title": "Deux façons d'envoyer les données",
    "body": ["Le même formulaire, l'e-mail déjà saisi. Seul change l'attribut method de form."],
    "show": ["mt-bar", "mt-form", "mt-input", "mt-submit", "mt-server"],
    "hud": [{"label": "method", "value": "—"}, {"label": "données", "value": "—"}],
    "script": [
        wait(900),
        {"do": "pulse", "at": "mt-submit"},
        scene(say="Avec method=\"get\", le navigateur ajoute les données à l'adresse, après un ?.",
              set=[{"id": "mt-bar", "sub": "exemple.fr/contact?email=camille%40exemple.fr", "tone": "y"}],
              link=[L("mt-bar", "mt-server")], hud=[hud("method", "get", "y")]),
        send(["mt-bar", "mt-server"], label="GET ?email=camille…", tone="y"),
        wait(900),
        scene(say="Cette adresse s'affiche, reste dans l'historique et peut se partager : c'est fait pour une recherche.",
              hud=[hud("données", "visibles dans l'adresse", "y")]),
        wait(1500),
        {"do": "pulse", "at": "mt-submit"},
        scene(say="Avec method=\"post\", l'adresse reste /contact : les données voyagent dans la requête elle-même.",
              set=[{"id": "mt-bar", "sub": "exemple.fr/contact", "tone": "n"}],
              unlink=[{"from": "mt-bar", "to": "mt-server"}],
              link=[L("mt-input", "mt-server")], hud=[hud("method", "post", "v")]),
        send(["mt-input", "mt-server"], label="POST email=camille…", tone="v"),
        wait(900),
        scene(say="Un message, une inscription : on choisit post, pour que la saisie ne traîne pas dans une adresse.",
              hud=[hud("données", "dans la requête", "v")]),
        wait(2400),
    ],
}

# ── Étape : required et type, contrôlés par le navigateur ─────────────────────────────────────────────────────
ents.append({"id": "ct-form", "kind": "layer", "at": [-5, -0.6], "size": [11, 7.4, 1], "tone": "n", "title": "form",
             "detail": "Le navigateur contrôle les champs **avant** d'envoyer le formulaire."})
ents.append(sub_ent("ct-input", "node", "ct-form", (0, -1.2), (9.4, 1.6), "y", title="input", sub='type="email" required',
                    detail="`required` : le champ ne peut pas rester vide. `type=\"email\"` : la valeur doit contenir un `@`."))
ents.append(sub_ent("ct-submit", "node", "ct-form", (2.6, 1.6), (3.2, 1.1), "v", title="Envoyer"))
ents.append({"id": "ct-server", "kind": "store", "at": [8.4, -1.4], "size": [4.0, 2.4, 1], "tone": "b", "title": "serveur",
             "detail": "Le serveur reçoit aussi des données qui ne viennent pas du formulaire : il vérifie tout lui-même."})
ents.append({"id": "ct-script", "kind": "node", "at": [8.4, 3.6], "size": [5.0, 1.6, 1], "tone": "r", "title": "un script",
             "sub": "sans navigateur",
             "detail": "Un programme peut envoyer une requête au serveur sans jamais ouvrir la page ni son formulaire."})

controle = {
    "id": "controle", "label": "required, type", "title": "Le navigateur contrôle avant d'envoyer",
    "body": ["Un formulaire réduit à un champ e-mail, obligatoire."],
    "show": ["ct-form", "ct-input", "ct-submit", "ct-server"],
    "hud": [{"label": "envoi", "value": "—"}],
    "script": [
        wait(900),
        {"do": "pulse", "at": "ct-submit"},
        scene(say="Le champ est vide, le visiteur clique sur Envoyer : avec required, le navigateur refuse l'envoi.",
              set=[{"id": "ct-input", "tone": "r", "label": "Veuillez renseigner ce champ."}],
              hud=[hud("envoi", "refusé : vide", "r")]),
        wait(1600),
        {"do": "pulse", "at": "ct-submit"},
        scene(say="Il tape « camille » : type=\"email\" fait vérifier la présence d'un @. Refusé encore.",
              set=[{"id": "ct-input", "label": "camille : il manque un @"}],
              hud=[hud("envoi", "refusé : pas de @", "r")]),
        wait(1600),
        {"do": "pulse", "at": "ct-submit"},
        scene(say="Avec une adresse complète, le formulaire part.",
              set=[{"id": "ct-input", "tone": "y", "label": "camille@exemple.fr"}],
              link=[L("ct-input", "ct-server")], hud=[hud("envoi", "parti", "g")]),
        send(["ct-input", "ct-server"], label="email=camille%40…", tone="y"),
        wait(1000),
        scene(say="Mais un script peut écrire directement au serveur, sans formulaire : aucun de ces contrôles ne s'applique.",
              show=["ct-script"], link=[L("ct-script", "ct-server")]),
        send(["ct-script", "ct-server"], label="email=n'importe quoi", tone="r"),
        scene(say="Le serveur doit donc tout revérifier : les contrôles du navigateur rendent service au visiteur.",
              set=[{"id": "ct-server", "sub": "revérifie tout"}]),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "html-forms",
    "title": "Les formulaires HTML", "lang": "fr", "kit": "plan",
    "legend": [{"tone": "y", "label": "valeur saisie"}, {"tone": "v", "label": "étiquette, bouton"},
               {"tone": "r", "label": "refusé, perdu"}, {"tone": "b", "label": "serveur"}],
    "entities": ents, "steps": [formulaire, methode, controle, envoi],
}
write(lesson, *outputs(HERE, "forms.scene.json", "layout-html-forms"))
