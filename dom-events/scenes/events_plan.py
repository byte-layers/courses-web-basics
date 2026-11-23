"""Scènes 2D (kit plan) du bit « Les événements : réagir aux actions du visiteur » (courses-web-basics/dom-events), suite.

Deux étapes, une idée chacune (events-plan.scene.json) :
- onglets : trois boutons, trois panneaux ; chaque bouton nomme son panneau dans un attribut data- ; au clic, tout
  s'éteint, puis un seul onglet et un seul panneau se rallument. Aucun code montré : l'exercice qui suit fait
  écrire la fonction ;
- trim : un champ lu par value est toujours un texte ; trois espaces font un texte de 3 caractères ; trim les
  retire, il reste un texte vide, que la validation refuse. Exemple volontairement différent de l'exercice
  (une ville, pas un prénom ; pas de classe d'erreur montrée).

Kit plan : x vers la droite, y vers le bas, en unités de 28 px ; un enfant (in) est relatif au centre du parent.
Une règle par sorte : la page affichée est un layer bleu (b) qui porte ses éléments ; une expression qui lit ou
transforme est un node pervenche (v) ; le champ est un node bleu.
Couleurs : g allumé, affiché ou accepté ; r refusé ; n éteint (estompé) ; v ce que fait JavaScript.
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


# ---------- 1. onglets : tout éteindre, puis rallumer un seul
XS = (-9.5, 0, 9.5)
NAMES = ("Projets", "Compétences", "Contact")
O = [ent("o-page", "layer", (0, 0), (30, 15), "b", title="la page affichée")]
for i, (x, name) in enumerate(zip(XS, NAMES), start=1):
    O.append(ent(f"o-b{i}", "node", (x, -4.2), (8.4, 2.4), "b", parent="o-page", title=name,
                 sub=f"data-content-id=\"content{i}\""))
    O.append(ent(f"o-p{i}", "node", (x, 2.6), (8.4, 3.6), "b", parent="o-page", title=f"#content{i}",
                 sub="un panneau"))
O[1]["detail"] = ("Un attribut **`data-`** est un attribut qu'on invente soi-même. Ici, il dit quel panneau ce bouton "
                  "ouvre ; `getAttribute(\"data-content-id\")` le lit.")
ON_B = {"tone": "g", "dim": False}
ON_P = {"tone": "g", "dim": False, "label": "visible"}
OFF = {"tone": "n", "dim": True, "label": None}
LINKS_O = [L(f"o-b{i}", f"o-p{i}", dashed=True) for i in (1, 2, 3)]


def etat(actif):
    """set : un seul onglet et un seul panneau allumés."""
    out = []
    for i in (1, 2, 3):
        out.append({"id": f"o-b{i}", **(ON_B if i == actif else OFF), "label": "tab-active" if i == actif else None})
        out.append({"id": f"o-p{i}", **(ON_P if i == actif else OFF)})
    return out


def eteindre():
    return [{"id": f"o-{k}{i}", **OFF} for i in (1, 2, 3) for k in ("b", "p")]


onglets = {
    "id": "onglets", "label": "Les onglets", "title": "Tout éteindre, puis rallumer un seul",
    "body": ["Chaque bouton nomme son panneau dans un attribut data- ; au clic, tout s'éteint, puis un seul se rallume."],
    "hud": [{"label": "clic sur", "value": "—"}, {"label": "data-content-id", "value": "—"}],
    "labels": "left",
    "show": ["o-page"] + etat(1),
    "links": [],
    "script": [
        wait(900),
        scene(link=LINKS_O,
              say="Chaque bouton porte un **attribut** `data-content-id` : le nom du panneau qu'il ouvre."),
        wait(1500),
        {"do": "pulse", "at": "o-b2"},
        scene(hud=[hud("clic sur", "Compétences", "v")],
              say="Le visiteur clique sur « Compétences »."),
        wait(500),
        scene(set=eteindre(), ms=600,
              say="D'abord, **tout éteindre** : aucun onglet souligné, aucun panneau visible."),
        wait(1100),
        scene(hud=[hud("data-content-id", "content2", "v")],
              say="Puis lire le `data-content-id` du bouton cliqué : `content2`."),
        send(["o-b2", "o-p2"], tone="v", label="content2"),
        scene(set=etat(2),
              say="Et **rallumer un seul** : ce bouton, et le panneau qu'il nomme."),
        wait(1500),
        {"do": "pulse", "at": "o-b3"},
        scene(set=eteindre(), hud=[hud("clic sur", "Contact", "v"), hud("data-content-id", "—", None)], ms=600,
              say="Un clic sur « Contact » : tout s'éteint de nouveau…"),
        send(["o-b3", "o-p3"], tone="v", label="content3"),
        scene(set=etat(3), hud=[hud("data-content-id", "content3", "v")],
              say="… et seul « Contact » se rallume. Il n'y a jamais deux panneaux visibles à la fois."),
        wait(2600),
    ],
}

# ---------- 2. trim : trois espaces ne font pas un champ rempli
XF, XV, XT, XE = -15, -5, 5, 15
W = (8.6, 3.0)
T = [
    ent("t-field", "node", (XF, 0), W, "b", title="<input id=\"ville\">", sub="le visiteur a tapé 3 espaces",
        detail="Ce que le visiteur a tapé se lit dans la propriété **`value`** du champ."),
    ent("t-value", "node", (XV, 0), W, "v", title="champ.value", sub="toujours un texte",
        detail="`value` rend **toujours un texte**, même quand le visiteur tape un nombre."),
    ent("t-trim", "node", (XT, 0), W, "v", title=".trim()", sub="retire les espaces des bords",
        detail="`trim` (*rogner*) retire les espaces du **début** et de la **fin** du texte, pas ceux du milieu."),
    ent("t-test", "node", (XE, 0), W, "v", title="=== \"\"", sub="le texte est-il vide ?"),
    ent("t-msg", "node", (XE, 5.6), W, "r", title="Remplissez le champ.", sub="le message affiché"),
]
trim = {
    "id": "trim", "label": "value et trim", "title": "Trois espaces, ce n'est pas un champ rempli",
    "body": ["value lit le champ, toujours en texte ; trim retire les espaces des bords avant de valider."],
    "hud": [{"label": "longueur", "value": "—"}],
    "labels": "left",
    "show": ["t-field", "t-value", "t-trim", "t-test"],
    "links": [L("t-field", "t-value"), L("t-value", "t-trim"), L("t-trim", "t-test")],
    "script": [
        wait(900),
        send(["t-field", "t-value"], tone="b", label="lecture"),
        scene(set=[{"id": "t-value", "label": "\"   \""}], hud=[hud("longueur", 3, "r")],
              say="`champ.value` lit ce qui est tapé : trois espaces, un texte de **3 caractères**. Pour un test `=== \"\"`, le champ est rempli."),
        wait(1700),
        send(["t-value", "t-trim"], tone="v"),
        scene(set=[{"id": "t-trim", "label": "\"\""}], hud=[hud("longueur", 0, "v")],
              say="`.trim()` retire les espaces du début et de la fin : il ne reste **rien**, un texte vide."),
        wait(1500),
        send(["t-trim", "t-test"], tone="v"),
        scene(set=[{"id": "t-test", "label": "true", "tone": "r"}], show=["t-msg"], link=[L("t-test", "t-msg")],
              say="Le texte vide est refusé : la validation affiche son message."),
        wait(1900),
        scene(set=[{"id": "t-field", "sub": "tapé : « Lyon » et des espaces"},
                   {"id": "t-value", "label": "\"  Lyon  \""}, {"id": "t-trim", "label": None},
                   {"id": "t-test", "label": None, "tone": "v"}],
              hide=["t-msg"], hud=[hud("longueur", 8, None)], ms=800,
              say="Même chemin avec « Lyon », entouré d'espaces : `value` rend 8 caractères."),
        wait(1100),
        send(["t-value", "t-trim", "t-test"], tone="v"),
        scene(set=[{"id": "t-trim", "label": "\"Lyon\""}, {"id": "t-test", "label": "false", "tone": "g"}],
              hud=[hud("longueur", 4, "g")],
              say="`trim` garde le mot et retire les bords : `\"Lyon\"`, accepté, et propre à enregistrer."),
        wait(2600),
    ],
}

write({
    "format": "bl-scenes/0.3", "id": "js-dom-events-plan", "title": "Onglets et champs (2D)",
    "lang": "fr", "kit": "plan",
    "legend": [{"tone": "b", "label": "page affichée"}, {"tone": "v", "label": "JavaScript"},
               {"tone": "g", "label": "allumé, accepté"}, {"tone": "r", "label": "refusé"}],
    "entities": O + T, "steps": [onglets, trim],
}, *outputs(HERE, "events-plan.scene.json", "js-dom-events-plan"))
