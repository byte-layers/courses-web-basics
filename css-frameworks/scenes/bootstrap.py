"""Scènes 2D (kit plan) du bit « Bootstrap : des classes CSS toutes faites » (css-frameworks).

Quatre étapes dans assets/bootstrap.scene.json :
  classes  (section « Un framework CSS ») : le navigateur télécharge tout bootstrap.min.css ; une classe ajoutée à
           une balise suffit pour que la règle du fichier s'applique.
  grille   (section « La grille : container, row, col ») : la rangée a 12 parts, col-md-4 en prend 4 ; sous 768 px,
           la media query ne s'applique plus et les colonnes s'empilent. Les notes des blocs disent ce que chaque
           classe est en CSS (elles remplacent la colonne « Ce que c'est en CSS » du texte).
  fournit  (section « Ce que le framework fait à votre place ») : le fichier de Bootstrap découpé en blocs (remise
           à zéro, grille, composants, utilitaires), le script à part, et votre feuille chargée après ; chaque bloc
           dit ce qu'on écrirait sinon.
  lecteur  (section « Ce qu'il ne fait pas ») : un formulaire Bootstrap vu à l'écran, puis lu par un lecteur
           d'écran : un faux titre, un champ sans nom. Exemple différent de l'exercice (une carte), et sans la
           correction : la scène montre le défaut, l'exercice le fait corriger.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; entités au premier niveau.
Dessin : le CDN = store ; le navigateur, un conteneur = layer ; un fichier = file ; un élément = node ;
une part de la rangée = zone en pointillés ; ce qu'on voit et ce qu'on entend = deux layers côte à côte.
Couleurs : b le fichier de Bootstrap, n un élément sans style, g un élément stylé par une classe de Bootstrap ;
étape lecteur : g bien annoncé, r ce qui manque ; y votre feuille de style.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import L, hud, scene, send, wait, write


def r(v):
    return round(v, 3)


def box(id, x0, y0, w, h, zone=False, **kw):
    d = {"id": id, "at": [r(x0 + w / 2), r(y0 + h / 2)], "size": [r(w), r(h)] + ([] if zone else [1])}
    d.update(kw)
    return d


def ent(kind, b, tone=None, **kw):
    d = {"id": b["id"], "kind": kind, "at": b["at"], "size": b["size"]}
    if tone: d["tone"] = tone
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


# ── Étape 1 : un fichier qu'on utilise par ses classes ────────────────────────────────────────────────────────
ents = [
    ent("store", box("cdn", -14.0, -1.6, 4.4, 3.2), "n", title="CDN", sub="jsdelivr",
        detail="Un **CDN** : un serveur public qui distribue des bibliothèques, dont Bootstrap, version par version."),
    ent("layer", box("nav", -7.0, -5.0, 20.0, 10.0), "n", title="navigateur"),
    ent("file", box("bs", -5.8, -1.0, 7.4, 2.0), "b", title="bootstrap.min.css",
        detail="Quelques milliers de règles CSS, toutes écrites par Bootstrap. Environ 230 Ko, 30 Ko une fois compressé pour le transfert."),
    ent("node", box("btn", 5.0, -3.0, 6.8, 1.8), "n", title="a", sub="lien sans style"),
    ent("node", box("card", 5.0, 0.4, 6.8, 3.4), "n", title="div", sub="bloc sans style"),
]

classes = {
    "id": "classes", "label": "Des classes", "title": "Une feuille de style qu'on utilise par ses classes",
    "body": ["Une page avec un lien et un bloc, encore sans style. Elle charge Bootstrap depuis un CDN."],
    "show": ["cdn", "nav", "btn", "card"],
    "hud": [{"label": "téléchargé", "value": "0 Ko"}],
    "links": [L("cdn", "nav")],
    "script": [
        wait(900),
        send(["cdn", "nav"], label="bootstrap.min.css"),
        scene(say="La balise link fait télécharger bootstrap.min.css : tout le fichier, environ 230 Ko.",
              show=["bs"], hud=[hud("téléchargé", "230 Ko", "b")]),
        wait(1300),
        scene(say="Vous ajoutez les classes btn btn-primary au lien : les règles du fichier s'appliquent.",
              link=[L("bs", "btn")], set=[{"id": "btn", "tone": "g", "title": "a.btn.btn-primary", "sub": None}]),
        wait(1400),
        scene(say="Même chose pour card : vous n'avez écrit aucune règle.",
              link=[L("bs", "card")], set=[{"id": "card", "tone": "g", "title": "div.card", "sub": None}]),
        wait(1400),
        scene(say="Le fichier entier reste téléchargé, même si la page n'utilise qu'une poignée de ses classes.",
              set=[{"id": "bs", "label": "3 classes utilisées"}]),
        wait(2600),
    ],
}

# ── Étape 2 : la grille en 12 parts ───────────────────────────────────────────────────────────────────────────
GTOP = -5.0
PROJ = [("p1", "projet 1"), ("p2", "projet 2"), ("p3", "projet 3")]


def grid(width_u, md):
    """Conteneur de largeur width_u ; md : la media query min-width: 768px s'applique."""
    x0 = -width_u / 2
    out = [box("ctn", x0, GTOP, width_u, 0)]   # hauteur fixée plus bas
    rx0, rw = x0 + 0.6, width_u - 1.2
    part = rw / 12
    ry = GTOP + 1.5
    for k in range(12):
        out.append(box(f"z{k + 1}", rx0 + k * part, ry + 1.4, part, 0, zone=True))
    if md:
        for i, (pid, _) in enumerate(PROJ):
            out.append(box(pid, rx0 + i * 4 * part + 0.15, ry + 1.6, 4 * part - 0.3, 2.4))
        rows_h = 2.4
    else:
        for i, (pid, _) in enumerate(PROJ):
            out.append(box(pid, rx0 + 0.15, ry + 1.6 + i * 2.8, rw - 0.3, 2.4))
        rows_h = 3 * 2.4 + 2 * 0.4
    zh = rows_h + 0.4
    row_h = 1.4 + zh + 0.3
    for b in out:
        if b["id"].startswith("z"):
            b["size"][1] = r(zh)
            b["at"][1] = r(ry + 1.4 + zh / 2)
    out.append(box("row", rx0, ry, rw, row_h))
    ctn_h = 1.5 + row_h + 0.5
    out[0] = box("ctn", x0, GTOP, width_u, ctn_h)
    return {b["id"]: b for b in out}


g0 = grid(20.0, True)
ents += [ent("layer", g0["ctn"], "n", title=".container", note="max-width selon l'écran",
             detail="`container` centre le contenu, avec une largeur maximale (`max-width`) qui change à chaque point de rupture."),
         ent("layer", g0["row"], "n", title=".row", note="display: flex; flex-wrap: wrap",
             detail="`row` : une rangée, en réalité `display: flex; flex-wrap: wrap;`.")]
ents += [ent("zone", g0[f"z{k}"], "b") for k in range(1, 13)]
ents[-12]["detail"] = "La rangée est découpée en **12 parts** égales."
ents += [ent("node", g0[pid], "g", title=t, sub="col-md-4" if pid == "p1" else None,
             note="width: 33.33 % dès 768 px" if pid == "p1" else None,
             detail="`col-md-4` : 4 parts sur 12, à partir de l'écran `md` (768 px) : `width: 33.33%` dans une media query `min-width: 768px`." if pid == "p1" else None) for pid, t in PROJ]
ZONES = [f"z{k}" for k in range(1, 13)]

grille = {
    "id": "grille", "label": "12 parts", "title": "Une rangée de 12 parts",
    "body": ["Trois projets dans un `container`, une `row` et trois colonnes `col-md-4`, sur un écran de 1000 px."],
    "show": ["ctn", "row"],
    "hud": [{"label": "largeur", "value": "1000 px"}, {"label": "min-width: 768px", "value": "oui", "tone": "g"}],
    "script": [
        wait(900),
        scene(say="La rangée est découpée en 12 parts égales.", show=ZONES),
        wait(1200),
        scene(say="Chaque col-md-4 en prend 4 : trois colonnes remplissent la rangée.", show=["p1", "p2", "p3"]),
        wait(1600),
        scene(say="Sous 768 px, la media query de col-md-4 ne s'applique plus : chaque colonne prend les 12 parts, et elles s'empilent.",
              hud=[hud("largeur", "600 px"), hud("min-width: 768px", "non", "r")],
              set=list(grid(12.0, False).values()), ms=1100),
        wait(2600),
    ],
}

# ── Étape 3 : ce que le fichier fournit ──────────────────────────────────────────────────────────────────────
BLOCKS = [("f-reset", "remise à zéro", "aucune classe : il s'applique seul", "sinon : marges qui varient"),
          ("f-grid", "grille", "container, row, col-md-4", "sinon : Flexbox, gap, media queries"),
          ("f-comp", "composants", "btn, card, navbar, alert", "sinon : des dizaines de règles"),
          ("f-util", "utilitaires", "mt-3, text-center, d-flex", "sinon : une petite règle chaque fois")]
ents.append({"id": "f-css", "kind": "layer", "at": [-5.0, 0.0], "size": [14.0, 13.6, 1], "tone": "b",
             "title": "bootstrap.min.css",
             "detail": "Le fichier de Bootstrap, découpé ici en quatre blocs de règles."})
for i, (fid, t, sub, lab) in enumerate(BLOCKS):
    ents.append({"id": fid, "kind": "node", "in": "f-css", "at": [0.0, r(-4.4 + i * 3.0)], "size": [12.0, 2.4, 1],
                 "tone": "b", "title": t, "sub": sub, "label": lab})
ents += [
    {"id": "f-js", "kind": "file", "at": [9.5, -3.0], "size": [8.6, 1.8, 1], "tone": "b",
     "title": "bootstrap.bundle.min.js", "label": "sinon : script et clavier", "note": "menu repliable, modale",
     "detail": "Le fichier JavaScript de Bootstrap, pour les composants qui réagissent (menu repliable, fenêtre modale), avec leur gestion du clavier."},
    {"id": "f-own", "kind": "file", "at": [9.5, 2.6], "size": [8.6, 1.8, 1], "tone": "y",
     "title": "style.css", "label": "votre feuille, chargée après", "note": "ce qui est propre au site",
     "detail": "Votre propre feuille de style, chargée **après** celle de Bootstrap : à égalité de sélecteur, la dernière règle gagne."},
]

fournit = {
    "id": "fournit", "label": "Ce qu'il fournit", "title": "Ce que le fichier de Bootstrap écrit à votre place",
    "body": ["Le fichier de Bootstrap, ouvert et découpé en blocs. Chaque bloc dit ce que vous écririez sinon."],
    "show": ["f-css"],
    "script": [
        wait(900),
        scene(say="Une remise à zéro : les navigateurs ne donnent plus chacun leurs marges et leurs polices.", show=["f-reset"]),
        wait(1100),
        scene(say="La grille : Flexbox et une media query par point de rupture, déjà écrites.", show=["f-grid"]),
        wait(1100),
        scene(say="Les composants : boutons, cartes, menus, avec leurs états :hover et :focus.", show=["f-comp"]),
        wait(1100),
        scene(say="Les utilitaires : une classe pour une marge, un alignement, un display.", show=["f-util"]),
        wait(1100),
        scene(say="À part, un fichier JavaScript pour les composants qui réagissent : menu repliable, fenêtre modale.",
              show=["f-js"]),
        wait(1100),
        scene(say="Et votre feuille de style, chargée après la sienne, pour ce qui est propre au site.", show=["f-own"]),
        wait(2600),
    ],
}

# ── Étape 4 : ce qu'on voit, ce qu'on entend ─────────────────────────────────────────────────────────────────
SEEN = [("v-title", "Newsletter", 'div class="h4"', "n"),
        ("v-field", "E-mail  [__________]", "label sans for, input.form-control", "n"),
        ("v-btn", "S'inscrire", "button.btn.btn-primary", "g")]
HEARD = [("h-title", "« Newsletter »", "du texte, pas un titre", "r"),
         ("h-field", "« zone de saisie »", "sans nom : que faut-il taper ?", "r"),
         ("h-btn", "« bouton, S'inscrire »", "bien annoncé", "g")]
ents += [{"id": "seen", "kind": "layer", "at": [-7.5, 0.0], "size": [13.0, 11.0, 1], "tone": "n", "title": "à l'écran"},
         {"id": "heard", "kind": "layer", "at": [7.5, 0.0], "size": [13.0, 11.0, 1], "tone": "n", "title": "au lecteur d'écran"}]
for i, (vid, t, sub, tone) in enumerate(SEEN):
    ents.append({"id": vid, "kind": "node", "in": "seen", "at": [0.0, r(-2.8 + i * 3.2)], "size": [11.0, 2.2, 1],
                 "tone": "g", "title": t, "sub": sub})
for i, (hid, t, sub, tone) in enumerate(HEARD):
    ents.append({"id": hid, "kind": "node", "in": "heard", "at": [0.0, r(-2.8 + i * 3.2)], "size": [11.0, 2.2, 1],
                 "tone": tone, "title": t, "sub": sub})
ents[-6]["detail"] = "Ce que la personne voit : un formulaire stylé par Bootstrap, net et cohérent."
ents[-3]["detail"] = "Ce qu'annonce un lecteur d'écran, élément par élément. Il lit le HTML, pas les classes."

lecteur = {
    "id": "lecteur", "label": "Vu, puis entendu", "title": "Un joli formulaire, lu par un lecteur d'écran",
    "body": ["Un formulaire d'inscription stylé par Bootstrap. À gauche ce qu'on voit, à droite ce qu'on entend."],
    "show": ["seen", "v-title", "v-field", "v-btn", "heard"],
    "hud": [{"label": "titres", "value": "1 à l'écran"}, {"label": "champs nommés", "value": "—"}],
    "script": [
        wait(1000),
        scene(say="« Newsletter » a l'air d'un titre : la classe h4 lui en donne la taille. Le lecteur d'écran, lui, lit une div.",
              show=["h-title"], link=[L("v-title", "h-title")], hud=[hud("titres", "0 annoncé", "r")]),
        wait(1500),
        scene(say="L'étiquette E-mail est bien affichée, mais rien ne la relie au champ : il est annoncé sans nom.",
              show=["h-field"], link=[L("v-field", "h-field")], hud=[hud("champs nommés", "0 sur 1", "r")]),
        wait(1500),
        scene(say="Le bouton, lui, est un vrai button : il est bien annoncé.", show=["h-btn"], link=[L("v-btn", "h-btn")]),
        wait(1300),
        scene(say="Les classes ont changé l'apparence, pas le sens : la balise et le lien label–champ restent à écrire.",
              set=[{"id": "heard", "label": "le HTML, pas les classes"}]),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "css-frameworks",
    "title": "Bootstrap : des classes CSS toutes faites", "lang": "fr", "kit": "plan",
    "legend": [{"tone": "b", "label": "Bootstrap"}, {"tone": "n", "label": "sans style"}, {"tone": "g", "label": "stylé, ou bien lu"}, {"tone": "r", "label": "ce qui manque"}],
    "entities": ents, "steps": [classes, grille, fournit, lecteur],
}
write(lesson, *outputs(HERE, "bootstrap.scene.json", "layout-bootstrap"))
