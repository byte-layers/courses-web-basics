"""Scènes 2D (kit plan) du bit « Le responsive design : une page pour tous les écrans » (responsive-design).

Quatre étapes dans assets/responsive.scene.json :
  largeurs  (section « Une seule page, des largeurs très différentes ») : la même page dans une fenêtre qui
            s'élargit, du téléphone (375 px) au grand écran (1600 px) ; le contenu se range autrement, sans
            défilement horizontal.
  viewport  (section « La balise meta viewport ») : sans la balise, le téléphone met la page en page à 980 px puis la
            réduit ; avec elle, la page prend la vraie largeur de l'écran.
  media     (section « Les media queries, en mobile-first ») : la fenêtre s'élargit ; à 700 px, la condition
            min-width devient vraie et le menu passe en ligne.
  debord    (section « Le piège : des largeurs fixes ») : une boîte en width: 960px dépasse d'un écran de 375 px ;
            en max-width: 960px, elle rétrécit sur le téléphone et s'arrête à 960 px sur grand écran.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; 1 px CSS = 1/50 d'unité (980 px = 19,6 unités).
Dessin : l'écran ou la fenêtre = zone en pointillés (sa largeur) ; la page, le menu = layer ; un élément = node.
Les encarts disent la largeur de mise en page, le zoom, et si la media query s'applique.
Couleurs : v un élément de la page ; n la page ; g ce qui tient dans l'écran, la media query qui s'applique ;
r ce qui dépasse.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import hud, scene, wait, write

U = 1 / 50


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


# ── Étape 1 : la balise meta viewport ─────────────────────────────────────────────────────────────────────────
OX, OY = -3.9, -8.0          # coin haut gauche de l'écran du téléphone
TITLES = {"v-h1": "h1 · Camille Martin", "v-n1": "Projets", "v-n2": "À propos", "v-n3": "Contact",
          "v-txt": "texte", "v-img": "photo"}


def page(width, scale, wide):
    """Boîtes de la page (px CSS), mises à l'échelle (scale) et placées au coin de l'écran."""
    k = U * scale
    P = lambda id, x, y, w, h, **kw: box(id, OX + x * k, OY + 1.0 + y * k, w * k, h * k, **kw)
    out = []
    if wide:
        pad = 20
        out.append(P("v-h1", pad, 64, width - 2 * pad, 60))
        for i in range(3):
            out.append(P(f"v-n{i + 1}", pad + i * 180, 144, 160, 44))
        out.append(P("v-txt", pad, 208, 600, 260))
        out.append(P("v-img", pad + 620, 208, width - 2 * pad - 620, 260))
        height = 488
    else:
        pad = 16
        out.append(P("v-h1", pad, 64, width - 2 * pad, 60))
        for i in range(3):
            out.append(P(f"v-n{i + 1}", pad, 144 + i * 54, width - 2 * pad, 44))
        out.append(P("v-txt", pad, 316, width - 2 * pad, 200))
        out.append(P("v-img", pad, 532, width - 2 * pad, 160))
        height = 712
    out.append(P("v-page", 0, 0, width, height + 16))
    return {b["id"]: b for b in out}


wide = page(980, 1.0, True)
ents = [ent("zone", box("phone", OX, OY, 390 * U, 16.6, zone=True), label="écran du téléphone · 390 px")]
ents.append(ent("layer", wide["v-page"], "n", title="page",
                detail="Une page prévue pour les petits écrans : elle a ses règles CSS pour 390 px de large."))
ents += [ent("node", wide[i], "v", title=t) for i, t in TITLES.items()]
IDS = ["v-page"] + list(TITLES)


def shrink():
    st = page(980, 390 / 980, True)
    out = [st[i] for i in IDS]
    for b in out:
        b["title"] = None
    return out


def narrow():
    st = page(390, 1.0, False)
    out = [st[i] for i in IDS]
    out[0]["title"] = "page"
    for b, t in zip(out[1:], TITLES.values()):
        b["title"] = t
    return out


viewport = {
    "id": "viewport", "label": "La balise viewport", "title": "Sans la balise, le téléphone fait comme s'il mesurait 980 px",
    "body": ["Une page prévue pour les petits écrans, ouverte sur un téléphone de 390 px de large. Son `head` n'a pas la balise `meta viewport`."],
    "show": ["phone"],
    "hud": [{"label": "mise en page", "value": "—"}, {"label": "zoom", "value": "—"}],
    "script": [
        wait(1000),
        scene(say="Le navigateur ne sait pas si la page est prévue pour lui : il la met en page comme sur un écran de 980 px.",
              hud=[hud("mise en page", "980 px", "r")], show=IDS),
        wait(1500),
        scene(say="Puis il réduit le tout pour le faire tenir dans l'écran : le texte devient minuscule.",
              hud=[hud("zoom", "40 %", "r")], set=shrink(), ms=1100),
        wait(1700),
        scene(say="Avec la balise meta viewport, la page prend la vraie largeur de l'écran, sans zoom : ses règles pour petit écran s'appliquent.",
              hud=[hud("mise en page", "390 px", "g"), hud("zoom", "100 %", "g")], set=narrow(), ms=1100),
        wait(2600),
    ],
}

# ── Étape 2 : la media query min-width ────────────────────────────────────────────────────────────────────────
WX, WY = -11.0, -4.0         # coin haut gauche de la fenêtre
LINKS = [("m-1", "Projets"), ("m-2", "À propos"), ("m-3", "Contact")]


def window(width):
    k = U
    out = [box("win", WX, WY, width * k, 7.6, zone=True, label=f"fenêtre · {width} px")]
    pad = 16
    mw = width - 2 * pad
    row = width >= 700
    lh = 44 * k
    mx, my = WX + pad * k, WY + 1.2
    if row:
        lw = 150 * k
        for i, (lid, _) in enumerate(LINKS):
            out.append(box(lid, mx + 0.5 + i * (lw + 0.4), my + 1.3, lw, lh))
        mh = 1.3 + lh + 0.5
    else:
        for i, (lid, _) in enumerate(LINKS):
            out.append(box(lid, mx + 0.5, my + 1.3 + i * (lh + 0.3), mw * k - 1.0, lh))
        mh = 1.3 + 3 * lh + 2 * 0.3 + 0.5
    out.append(box("menu", mx, my, mw * k, mh))
    return out


w0 = {b["id"]: b for b in window(375)}
ents.append(ent("zone", w0["win"], label=w0["win"]["label"]))
ents.append(ent("layer", w0["menu"], "n", title=".menu",
                detail="Le menu : empilé par défaut (le style du téléphone), en ligne dans la media query `min-width: 700px`."))
ents += [ent("node", w0[lid], "v", title=t) for lid, t in LINKS]

media = {
    "id": "media", "label": "La media query", "title": "min-width: 700px, au moins 700 px de large",
    "body": ["Le menu est écrit pour le téléphone, empilé, puis enrichi par `@media (min-width: 700px)`. La fenêtre s'élargit."],
    "show": ["win", "menu", "m-1", "m-2", "m-3"],
    "hud": [{"label": "largeur", "value": "375 px"}, {"label": "min-width: 700px", "value": "non"}],
    "script": [
        wait(1400),
        scene(say="À 600 px, la fenêtre s'élargit, mais elle ne fait pas encore 700 px : le style du téléphone reste.",
              hud=[hud("largeur", "600 px")], set=window(600), ms=1000),
        wait(1500),
        scene(say="À 700 px, la condition devient vraie : la media query s'applique, et les liens passent en ligne.",
              hud=[hud("largeur", "700 px"), hud("min-width: 700px", "oui", "g")], set=window(700), ms=1000),
        wait(1500),
        scene(say="Au-delà, elle reste vraie : sur tous les grands écrans, le menu reste en ligne.",
              hud=[hud("largeur", "1100 px")], set=window(1100), ms=1000),
        wait(2600),
    ],
}

# ── Étape 0 : une seule page, des largeurs différentes ──────────────────────────────────────────────────────
K0 = 1 / 60                  # 1600 px = 26,7 unités
AX, AY = -13.4, -5.0         # coin haut gauche de la fenêtre
DEVICES = [(375, "téléphone"), (768, "tablette"), (1440, "ordinateur portable"), (1600, "grand écran")]


def adapt(width, device):
    """La même page dans une fenêtre de width px : empilée sous 700 px, sur deux colonnes au-delà (960 px au plus)."""
    k = K0
    out = [box("w0", AX, AY, width * k, 460 * k, zone=True, label=f"{device} · {width} px")]
    pad = 16
    cw = min(width - 2 * pad, 960)
    cx = (width - cw) / 2
    P = lambda id, x, y, w, h: box(id, AX + x * k, AY + y * k, w * k, h * k)
    out.append(P("a-h1", cx, 24, cw, 56))
    if width < 700:
        out.append(P("a-txt", cx, 96, cw, 150))
        out.append(P("a-img", cx, 262, cw, 150))
    else:
        half = (cw - 16) / 2
        out.append(P("a-txt", cx, 96, half, 220))
        out.append(P("a-img", cx + half + 16, 96, half, 220))
    return out


a0 = {b["id"]: b for b in adapt(375, "téléphone")}
ents.append(ent("zone", a0["w0"], label=a0["w0"]["label"]))
ents.append(ent("node", a0["a-h1"], "v", title="h1",
                detail="La même page HTML, à chaque largeur : seul le CSS range ses éléments autrement."))
ents.append(ent("node", a0["a-txt"], "v", title="texte"))
ents.append(ent("node", a0["a-img"], "v", title="photo"))

largeurs = {
    "id": "largeurs", "label": "Les largeurs", "title": "La même page, de 375 à 1600 px",
    "body": ["Une seule page, une seule adresse. La fenêtre qui l'affiche s'élargit, du téléphone au grand écran."],
    "show": ["w0", "a-h1", "a-txt", "a-img"],
    "hud": [{"label": "appareil", "value": "—"}, {"label": "largeur", "value": "—"},
            {"label": "défilement", "value": "—"}],
    "script": [
        wait(1400),
        scene(say="Sur un téléphone, 360 à 430 px de large : le titre, le texte et la photo s'empilent.",
              hud=[hud("appareil", "téléphone"), hud("largeur", "375 px"), hud("défilement", "aucun", "g")]),
        wait(1200),
        scene(say="Sur une tablette en portrait, 768 px : assez de place pour mettre la photo à côté du texte.",
              hud=[hud("appareil", "tablette"), hud("largeur", "768 px")], set=adapt(768, "tablette"), ms=1000),
        wait(1500),
        scene(say="Sur un ordinateur portable, 1280 à 1440 px : le contenu s'arrête à une largeur confortable, centré.",
              hud=[hud("appareil", "ordinateur portable"), hud("largeur", "1440 px")], set=adapt(1440, "ordinateur portable"), ms=1000),
        wait(1500),
        scene(say="Sur un grand écran, 1600 px et plus : toujours la même page, et jamais de barre de défilement horizontale.",
              hud=[hud("appareil", "grand écran"), hud("largeur", "1600 px")], set=adapt(1600, "grand écran"), ms=1000),
        wait(2600),
    ],
}

# ── Étape 3 : une largeur fixe déborde ────────────────────────────────────────────────────────────────────────
DX, DY = -9.6, -3.4          # coin haut gauche de l'écran


def screen(width, label):
    return box("sc", DX, DY, width * U, 6.0, zone=True, label=label)


def boite(width, title):
    b = box("fix", DX + 0.4, DY + 1.6, width * U - 0.8, 2.8)
    b["title"] = title
    return b


ents.append(ent("zone", screen(375, "écran du téléphone · 375 px"), label="écran du téléphone · 375 px"))
ents.append(ent("zone", box("out", DX + 375 * U, DY + 0.8, 585 * U, 4.4, zone=True), label="hors de l'écran · 585 px"))
ents.append(ent("node", boite(960, None), "r", title=".fiche · width: 960px",
                detail="Une largeur fixe ne rétrécit jamais, quelle que soit la largeur de l'écran."))

debord = {
    "id": "debord", "label": "Le débordement", "title": "960 px fixes sur un écran de 375 px",
    "body": ["Une fiche à largeur fixe, `width: 960px`, ouverte sur un téléphone de 375 px de large."],
    "show": ["sc", "fix"],
    "hud": [{"label": "dépasse de", "value": "—"}, {"label": "défilement", "value": "—"}],
    "script": [
        wait(1000),
        scene(say="La boîte garde ses 960 px : elle dépasse de l'écran de 585 px.", show=["out"],
              hud=[hud("dépasse de", "585 px", "r")]),
        wait(1400),
        scene(say="La page entière gagne une barre de défilement horizontale : il faut glisser de côté pour tout lire.",
              hud=[hud("défilement", "horizontal", "r")]),
        wait(1600),
        scene(say="Avec max-width: 960px, la boîte ne dépasse jamais 960 px, mais elle peut rétrécir : elle tient dans l'écran.",
              hide=["out"], set=[dict(boite(375, ".fiche · max-width: 960px"), tone="g")],
              hud=[hud("dépasse de", "0 px", "g"), hud("défilement", "aucun", "g")], ms=1000),
        wait(1600),
        scene(say="Sur un écran de 1200 px, la même règle laisse la boîte à 960 px : elle ne fait que rétrécir quand la place manque.",
              set=[screen(1200, "écran d'ordinateur · 1200 px"), boite(960, ".fiche · max-width: 960px")], ms=1100),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "responsive-design",
    "title": "Le responsive design", "lang": "fr", "kit": "plan",
    "legend": [{"tone": "v", "label": "élément de la page"}, {"tone": "r", "label": "dépasse"}, {"tone": "g", "label": "tient dans l'écran"}],
    "entities": ents, "steps": [largeurs, viewport, debord, media],
}
write(lesson, *outputs(HERE, "responsive.scene.json", "layout-responsive"))
