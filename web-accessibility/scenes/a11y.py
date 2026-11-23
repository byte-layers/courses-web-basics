"""Scènes 2D (kit plan) du bit « L'accessibilité web : une page lisible par tous » (web-accessibility).

Cinq étapes dans assets/a11y.scene.json :
  lecteur  (section « Qui lit votre page autrement ») : un lecteur d'écran lit le HTML dans l'ordre et annonce ce
           qu'est chaque élément ; sans alt, il ne lit que le nom du fichier.
  erreurs  (section « Cinq erreurs fréquentes ») : cinq erreurs à gauche, avec ce qu'elles donnent ; chacune reçoit
           sa correction à droite, avec le critère RGAA qui la détecte (le tableau de la v1, en scène).
  contraste (section « Le contraste ») : un texte gris clair sur blanc (2,3:1) refusé, le seuil 4,5:1, puis un
           texte foncé.
  focus    (section « Le focus visible ») : Tab fait avancer le focus ; outline: none le rend invisible ;
           :focus-visible rend un contour au clavier.
  lighthouse (section « Vérifier ») : Lighthouse trouve trois erreurs, on les corrige, score 100 ; trois défauts
           restent, qu'il ne sait pas voir, et que les gestes à la main trouvent.

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; entités au premier niveau.
Dessin : la page = layer ; un élément = node ; le lecteur d'écran, la personne au clavier = actor.
Couleurs : v un élément de la page ; r ce qui manque (image sans alt) ; b le focus ; g ce qui est corrigé.
"""
import sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "tools" / "scenes"))
from paths import outputs
from scene_kit import L, hud, scene, send, wait, write


def r(v):
    return round(v, 3)


def ent(id, kind, x0, y0, w=None, h=None, tone=None, **kw):
    if kind == "actor":
        d = {"id": id, "kind": kind, "at": [x0, y0]}
    else:
        d = {"id": id, "kind": kind, "at": [r(x0 + w / 2), r(y0 + h / 2)], "size": [r(w), r(h), 1]}
    if tone: d["tone"] = tone
    d.update({k: v for k, v in kw.items() if v is not None})
    return d


# ── Étape 1 : le lecteur d'écran ──────────────────────────────────────────────────────────────────────────────
ents = [
    ent("page", "layer", -9.0, -5.4, 11.6, 11.4, "n", title="page",
        detail="La même page : à l'écran, elle se regarde ; avec un lecteur d'écran, elle s'écoute."),
    ent("h1", "node", -8.4, -3.8, 10.4, 1.3, "v", title="h1 · Camille Martin"),
    ent("img", "node", -8.4, -2.0, 10.4, 3.4, "v", title="img", sub="IMG_2043.jpg",
        detail="Une image : sans attribut `alt`, rien ne la décrit à qui ne la voit pas."),
    ent("txt", "node", -8.4, 1.9, 10.4, 1.3, "v", title="p · Développeuse web à Toulouse"),
    ent("lnk", "node", -8.4, 3.8, 10.4, 1.3, "v", title="a · Mes projets"),
    ent("reader", "actor", 11.0, -0.6, tone="n", label="lecteur d'écran",
        detail="Un **lecteur d'écran** (NVDA, JAWS, VoiceOver, TalkBack) lit la page à voix haute, dans l'ordre du HTML."),
]

lecteur = {
    "id": "lecteur", "label": "Le lecteur d'écran", "title": "Un lecteur d'écran lit le HTML, dans l'ordre",
    "body": ["Le haut d'une page de portfolio, écouté avec un lecteur d'écran."],
    "show": ["page", "h1", "img", "txt", "lnk", "reader"],
    "links": [L("page", "reader")],
    "script": [
        wait(900),
        {"do": "pulse", "at": "h1"},
        send(["page", "reader"], label="titre 1, Camille Martin",
             explain=["Le lecteur d'écran lit la page dans l'ordre du HTML et dit ce qu'est chaque élément : « titre de niveau 1 »."]),
        {"do": "pulse", "at": "img"},
        send(["page", "reader"], label="IMG_2043.jpg", tone="r",
             explain=["Une image sans `alt` : il ne peut lire que le nom du fichier."]),
        scene(say="On écrit dans l'attribut alt ce que montre l'image…",
              set=[{"id": "img", "tone": "g", "sub": "alt=\"Le sommet du pic du Midi\""}]),
        {"do": "pulse", "at": "img"},
        send(["page", "reader"], label="image, Le sommet du pic…", tone="g",
             explain=["…et il la décrit à qui ne la voit pas."]),
        {"do": "pulse", "at": "txt"},
        send(["page", "reader"], label="Développeuse web…",
             explain=["Le texte est lu tel quel."]),
        {"do": "pulse", "at": "lnk"},
        send(["page", "reader"], label="lien, Mes projets",
             explain=["Un lien est annoncé comme un lien, avec son texte : c'est ce qui permet de le choisir."]),
        wait(2200),
    ],
}

# ── Étape 2 : le focus au clavier ─────────────────────────────────────────────────────────────────────────────
NAV = [("k-1", "Accueil"), ("k-2", "Projets"), ("k-3", "Contact")]
ents += [
    ent("page2", "layer", -7.8, -3.4, 15.6, 6.4, "n", title="page"),
    ent("kbd", "actor", -12.0, 0.0, tone="n", label="au clavier",
        detail="Une personne qui ne peut pas tenir une souris navigue au clavier : Tab pour passer d'un lien au suivant, Entrée pour l'activer."),
]
for i, (kid, t) in enumerate(NAV):
    ents.append(ent(kid, "node", -7.0 + i * 4.8, -1.4, 4.2, 1.4, "v", title=t,
                    detail="Le **focus** est l'élément qui reçoit les touches du clavier ; le navigateur l'entoure d'un contour, l'`outline`." if i == 0 else None))
ents.append(ent("k-btn", "node", -7.0, 0.8, 6.0, 1.4, "v", title="button · Me contacter"))

tab = lambda: send(["kbd", "page2"], label="Tab")
focus = {
    "id": "focus", "label": "Le focus", "title": "Le focus : où l'on est, au clavier",
    "body": ["Un menu de trois liens et un bouton, parcourus sans souris."],
    "show": ["page2", "kbd", "k-1", "k-2", "k-3", "k-btn"],
    "links": [L("kbd", "page2")],
    "hud": [{"label": "outline", "value": "par défaut"}],
    "script": [
        wait(900),
        tab(),
        scene(say="Tab donne le focus au premier lien : son contour montre où l'on est.",
              set=[{"id": "k-1", "tone": "b", "label": "focus"}]),
        wait(900),
        tab(),
        scene(say="Tab encore : le focus passe au lien suivant.",
              set=[{"id": "k-1", "tone": "v", "label": None}, {"id": "k-2", "tone": "b", "label": "focus"}]),
        wait(1100),
        scene(say="Avec outline: none, le contour disparaît pour tout le monde…",
              hud=[hud("outline", "none", "r")], set=[{"id": "k-2", "tone": "v", "label": None}]),
        wait(700),
        tab(),
        scene(say="…le focus avance toujours, mais plus rien ne dit où il est.",
              set=[{"id": "k-3", "note": "focus, invisible"}]),
        wait(1500),
        scene(say="Avec :focus-visible, un contour visible revient pour qui navigue au clavier.",
              hud=[hud("outline", ":focus-visible", "g")], set=[{"id": "k-3", "tone": "b", "note": None, "label": "focus"}]),
        wait(2600),
    ],
}

# ── Étape : cinq erreurs fréquentes ───────────────────────────────────────────────────────────────────────────
ERR = [  # id, erreur, ce que ça donne, correction, critère
    ("alt", "image sans alt", "lue : « IMG_2043.jpg »", 'alt="Le sommet du pic du Midi"', "alt=\"\" si décorative · RGAA 1.1"),
    ("ctr", "texte gris clair sur blanc", "illisible : vue faible, soleil", "contraste d'au moins 4,5:1", "RGAA 3.2"),
    ("lng", "<html> sans lang", "lu avec un accent anglais", '<html lang="fr">', "RGAA 8.3"),
    ("hx", "h1, puis h4", "le plan des titres a des trous", "h1, h2, h3, sans sauter", "RGAA 9.1"),
    ("out", "outline: none sur le focus", "au clavier, on ne sait où l'on est", "garder un contour visible", "RGAA 10.7"),
]
EY0, EDY = -7.0, 2.9
for i, (k, e, eff, cor, crit) in enumerate(ERR):
    y = EY0 + i * EDY
    ents.append(ent(f"e-{k}", "node", -12.5, y, 11.0, 2.3, "r", title=e, sub=eff,
                    detail="Une erreur fréquente, et ce qu'elle donne pour qui lit la page autrement." if i == 0 else None))
    ents.append(ent(f"c-{k}", "node", 1.5, y, 11.0, 2.3, "g", title=cor, sub=crit,
                    detail="La correction, et le critère du RGAA qui détecte l'erreur." if i == 0 else None))

SAY = [
    "Une image sans alt : le lecteur d'écran lit le nom du fichier. On la décrit dans alt, ou alt=\"\" si elle ne fait que décorer.",
    "Un texte trop pâle ne se lit pas avec une vue faible, ni au soleil : il faut un contraste d'au moins 4,5:1.",
    "Sans lang, le lecteur d'écran choisit sa voix au hasard, souvent l'anglais : lang=\"fr\" la règle.",
    "Un niveau de titre sauté laisse un trou dans le plan qu'on parcourt au lecteur d'écran.",
    "Sans contour, la personne qui navigue au clavier ne sait plus où elle est.",
]
escript = [wait(1000)]
for (k, *_), say in zip(ERR, SAY):
    escript += [scene(say=say, show=[f"c-{k}"], link=[L(f"e-{k}", f"c-{k}")]), wait(1500)]
escript.append(wait(1500))
erreurs = {
    "id": "erreurs", "label": "Cinq erreurs", "title": "Cinq erreurs, cinq corrections d'une ligne",
    "body": ["À gauche, l'erreur et ce qu'elle donne ; à droite, sa correction et le critère RGAA qui la détecte."],
    "show": [f"e-{k}" for k, *_ in ERR],
    "links": [],
    "script": escript,
}

# ── Étape : le contraste ──────────────────────────────────────────────────────────────────────────────────────
ents += [
    ent("bg", "layer", -9.0, -4.0, 14.0, 8.0, "n", title="fond blanc",
        detail="Le **contraste** : le rapport de luminosité entre le texte et son fond, de `1:1` (blanc sur blanc) à `21:1` (noir sur blanc)."),
    ent("txt-c", "node", -8.0, -1.2, 12.0, 2.6, "n", title="Mis à jour en mars", sub="color: rgb(170, 170, 170)"),
    ent("seuil", "node", 8.0, -1.2, 9.0, 2.6, "v", title="seuil du RGAA : 4,5:1",
        sub="pour le texte courant"),
]
contraste = {
    "id": "contraste", "label": "Le contraste", "title": "Un rapport d'au moins 4,5:1",
    "body": ["Une petite ligne de texte gris clair, sur un fond blanc."],
    "show": ["bg", {"id": "txt-c", "dim": True}],
    "links": [],
    "hud": [{"label": "contraste", "value": "—"}, {"label": "critère 3.2", "value": "—"}],
    "script": [
        wait(1000),
        scene(say="Gris clair sur blanc : le rapport est de 2,3:1. Le texte se devine plus qu'il ne se lit.",
              hud=[hud("contraste", "2,3:1", "r"), hud("critère 3.2", "refusé", "r")], set=[{"id": "txt-c", "tone": "r"}]),
        wait(1500),
        scene(say="Pour le texte courant, le RGAA demande au moins 4,5:1.", show=["seuil"], link=[L("txt-c", "seuil", dashed=True)]),
        wait(1400),
        scene(say="Un gris plus foncé : le rapport monte au-dessus du seuil, le texte se lit.",
              hud=[hud("contraste", "5,9:1", "g"), hud("critère 3.2", "accepté", "g")],
              set=[{"id": "txt-c", "tone": "g", "dim": False, "sub": "color: rgb(100, 100, 100)"}]),
        wait(1500),
        scene(say="Le texte principal de la page, presque noir, va bien au-delà.",
              hud=[hud("contraste", "14,6:1", "g")], set=[{"id": "txt-c", "sub": "color: rgb(30, 41, 59)"}]),
        wait(2600),
    ],
}

# ── Étape : Lighthouse, puis à la main ────────────────────────────────────────────────────────────────────────
AUTO = [("lh-alt", "img sans alt"), ("lh-ctr", "texte à 2,3:1"), ("lh-lng", "<html> sans lang")]
HAND = [("lh-pert", 'alt="photo"', "un alt qui ne dit rien"),
        ("lh-ord", "h2 « Divers », h2 « Suite »", "des titres qui ne disent rien"),
        ("lh-kbd", "menu qu'on ne quitte pas", "un piège au clavier")]
ents.append(ent("pg-l", "layer", -10.0, -7.0, 13.0, 15.6, "n", title="page"))
for i, (k, t) in enumerate(AUTO):
    ents.append(ent(k, "node", -9.2, -5.4 + i * 2.4, 11.4, 1.8, "v", title=t))
for i, (k, t, sub) in enumerate(HAND):
    ents.append(ent(k, "node", -9.2, 1.9 + i * 2.4, 11.4, 1.8, "v", title=t))
ents += [
    ent("lh", "actor", 12.0, -3.4, tone="n", label="Lighthouse",
        detail="**Lighthouse**, dans les outils de développement de Chrome et d'Edge, analyse la page et donne un score sur 100."),
    ent("hand", "actor", 12.0, 4.6, tone="n", label="à la main",
        detail="Tab sur toute la page, un zoom à 200 %, la liste des titres."),
]
lighthouse = {
    "id": "lighthouse", "label": "Vérifier", "title": "Ce que Lighthouse voit, et ce qu'il ne voit pas",
    "body": ["Une page avec six défauts, analysée d'abord par un outil automatique."],
    "show": ["pg-l"] + [k for k, _ in AUTO] + [k for k, *_ in HAND] + ["lh"],
    "links": [L("lh", "pg-l")],
    "hud": [{"label": "score", "value": "—"}, {"label": "non vus", "value": "—"}],
    "script": [
        wait(900),
        send(["lh", "pg-l"], label="analyse", explain=["Lighthouse parcourt le code de la page."]),
        scene(say="Il trouve ce qui se mesure : une image sans alt, un contraste trop faible, une langue absente.",
              hud=[hud("score", "moins de 100", "r")], set=[{"id": k, "tone": "r", "label": "trouvé"} for k, _ in AUTO]),
        wait(1500),
        scene(say="On corrige ces trois-là : le score passe à 100.",
              hud=[hud("score", "100", "g")],
              set=[{"id": k, "tone": "g", "label": None} for k, _ in AUTO]),
        wait(1500),
        scene(say="Mais trois défauts restent, que l'outil ne sait pas juger : un alt qui ne décrit rien, des titres qui ne disent rien, un piège au clavier.",
              hud=[hud("non vus", "3", "r")], set=[{"id": k, "tone": "r", "sub": sub} for k, _, sub in HAND]),
        wait(1800),
        scene(say="Tab sur toute la page, le zoom à 200 % et la liste des titres les trouvent : ce sont des vérifications à la main.",
              show=["hand"], link=[L("hand", "pg-l")],
              hud=[hud("non vus", "0", "g")],
              set=[{"id": k, "label": "trouvé à la main"} for k, *_ in HAND]),
        wait(2600),
    ],
}

lesson = {
    "format": "bl-scenes/0.3", "id": "web-accessibility",
    "title": "L'accessibilité web", "lang": "fr", "kit": "plan",
    "legend": [{"tone": "v", "label": "élément"}, {"tone": "r", "label": "erreur"}, {"tone": "b", "label": "focus"}, {"tone": "g", "label": "corrigé"}],
    "entities": ents, "steps": [lecteur, erreurs, contraste, focus, lighthouse],
}
write(lesson, *outputs(HERE, "a11y.scene.json", "layout-a11y"))
