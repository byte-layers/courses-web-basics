"""Petits outils pour écrire une leçon bl-scenes en Python (skill byte-layers-scenes).

    import sys; sys.path.insert(0, "<chemin du skill>/scripts")
    from scene_kit import G, L, at, scene, send, wait, write

    lesson = {"format": "bl-scenes/0.3", "id": "demo", "title": "Démo", "lang": "fr", "kit": "feuillete",
              "entities": [...], "steps": [...]}
    write(lesson, "lessons/demo/lesson.json", "…/assets/demo.scene.json")
"""
import json
import os


def G(sx, sy):
    """Position par coordonnées d'écran : sx vers la droite, sy vers le bas.

    Une rangée horizontale = même sy. Une unité de sy vaut moitié moins de pixels qu'une unité de sx :
    écarter les rangées de 8 à 10 en sy, les blocs voisins de 3,5 à 4,5 en sx.
    """
    return [round((sy + sx) / 2, 3), round((sy - sx) / 2, 3)]


def at(id, sx, sy, **changes):
    """Élément de show (ou de set) qui place une entité du catalogue en G(sx, sy), avec des changements."""
    e = {"id": id, "at": G(sx, sy)}
    e.update(changes)
    return e


def L(a, b, **kw):
    """Lien de a vers b (label, dashed, weight : part du trafic spread)."""
    d = {"from": a, "to": b}
    d.update(kw)
    return d


def scene(say=None, ms=None, **kw):
    """Action scene : show, hide, set, link, unlink, hud ; say en fait un temps du pas à pas."""
    d = {"do": "scene"}
    d.update(kw)
    if say:
        d["say"] = say
    if ms:
        d["ms"] = ms
    return d


def send(path, label=None, reply=None, kind=None, explain=None, tone=None):
    """Un paquet sur le trajet ; explain : une phrase par saut, plus une pour la réponse ; tone : sa couleur."""
    d = {"do": "send", "path": path}
    for k, v in (("label", label), ("reply", reply), ("kind", kind), ("explain", explain), ("tone", tone)):
        if v is not None:
            d[k] = v
    return d


def wait(ms):
    return {"do": "wait", "ms": ms}


def hud(label, value, tone="keep"):
    """Encart pour scene(hud=[…]) : value None le retire ; tone None retire la couleur, omis la garde."""
    d = {"label": label, "value": value}
    if tone != "keep":
        d["tone"] = tone
    return d


def traffic(path, gap=380, fallback=None, only=None, **kw):
    """Trafic continu (flux spread) : le dernier saut suit les liens pleins vers des cibles non estompées."""
    d = {"path": path, "spread": only or True, "gap": gap}
    if fallback:
        d["fallback"] = fallback
    d.update(kw)
    return d


def write(lesson, *paths):
    """Écrit la leçon (JSON indenté, UTF-8) à chaque chemin."""
    for out in paths:
        d = os.path.dirname(out)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(out, "w", encoding="utf-8") as f:
            json.dump(lesson, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("écrit", out)
