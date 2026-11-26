# Vidéos live coding du cours

Les **scénarios** sont ici, un dossier par vidéo (`<nom>/scenario.cjs`), avec
`lab-files.cjs` (les fichiers du lab posés avant chaque scène). Le **moteur**
(enregistrement VS Code + navigateur + DevTools, narration, montage, contrôle,
publication R2) est le skill `byte-layers-videos` :
`~/.claude/skills/byte-layers-videos/` (source :
`Deltavia/ai-work-automation/skills/byte-layers/byte-layers-videos/`).

```bash
V=~/.claude/skills/byte-layers-videos/scripts
bash $V/make-video.sh html-css-basics-03-squelette draft     # brouillon gratuit (voix macOS, captures)
bash $V/make-video.sh html-css-basics-03-squelette           # final : ElevenLabs, scène, montage, contrôle
bash $V/make-video.sh html-css-basics-03-squelette revoice   # texte changé, scène gardée
bash $V/make-video.sh html-css-basics-03-squelette publish   # R2 + ligne à citer dans l'étape
```

Sorties dans `out/<nom>/` (hors git). Clés (ElevenLabs, R2) :
`~/.config/byte-layers/videos.env`, jamais dans ce dépôt.

| Vidéo | Étape | Scènes |
|---|---|---|
| `html-css-basics-01-onglet-reseau` | 01 | navigateur + DevTools |
| `html-css-basics-02-inspecteur` | 02.1 | navigateur + DevTools |
| `html-css-basics-02-trois-fichiers` | 02.2 | VS Code + navigateur |
| `html-css-basics-03-squelette` | 03 | VS Code + navigateur |
| `html-css-basics-04-ville` | 04 | VS Code + navigateur |
| `html-css-basics-05-semantique` | 05 | VS Code + navigateur + DevTools |
| `html-css-basics-06-css` | 06 | VS Code + navigateur + DevTools |
| `html-css-basics-07-largeur` | 07 | VS Code + navigateur + DevTools |
