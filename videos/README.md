# Vidéos live coding : navigateur + DevTools

Variante « navigateur » de la chaîne de `courses-ansible-intro/videos`
(voir son `PROCESS.md`) : même scénario, même narration (`tts.cjs`), même
montage (`assemble.cjs`). Seul `record.cjs` change.

```
bash make-video.sh html-css-basics-01-onglet-reseau            # tout (voix + scène + montage)
bash make-video.sh html-css-basics-01-onglet-reseau revoice    # texte ou voix changés
SHOTS=1 bash make-video.sh <nom> record                        # captures par segment pour régler les gestes
TTS=say bash make-video.sh <nom>                               # brouillon gratuit, voix macOS
```

Installation : `npm install` ; `.env` (hors git, `chmod 600`) comme pour Ansible,
plus `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY` et `R2_ENDPOINT` pour publier.

## Publier

```
bash publish-media.sh out/<nom>/<nom>.mp4   # → https://media.byte-layers.com/v/<sha256>.mp4
```

L'adresse affichée se cite dans l'étape : `![Live coding : …](https://media.byte-layers.com/v/<sha256>.mp4)`.
Un fichier publié ne change jamais ; une vidéo refaite a une autre adresse. Décision :
`byte-layers-monorepo/docs/ETAPES_CHOIX_VIDEOS.md`.

## La scène

Playwright ne capture que le contenu d'une page : ni barre d'adresse, ni
DevTools. `record.cjs` enregistre donc trois pages en même temps et les
juxtapose (ffmpeg, 1920×1080) :

| Zone | Page | Contenu |
|---|---|---|
| haut gauche | `bar` | barre d'adresse dessinée, qui suit la page (redirections comprises) |
| bas gauche | `site` | la page visitée |
| droite | `dt` | les **vrais** DevTools de Chromium (`/devtools/inspector.html` servi par le port de débogage 9333), branchés sur `site` |

Avant `openDevtools()`, la colonne de droite affiche « Outils de
développement fermés », puis les touches F12 / ⌘⌥I.

## Aides du scénario (`ctx`)

| Aide | Effet |
|---|---|
| `go(url, { delay })` | clic dans la barre, frappe de l'adresse, navigation |
| `reload()` | clic sur ⟳ et rechargement |
| `openDevtools({ keysMs })` | montre les touches, ouvre les DevTools |
| `point(page, locator, { hold })` / `click(page, locator)` | curseur dessiné, anneau, clic réel |
| `moveTo(x, y, ms)`, `pulse()` | coordonnées de la scène (1280×720 px CSS, DevTools à partir de x = 640) |
| `bar`, `site`, `dt` | les pages Playwright |

Option de scénario `disableCache: true` : désactive le cache de `site`, pour
que le rechargement montre 200 et non 304.

## Pièges

| Symptôme | Cause | Solution |
|---|---|---|
| Écran miniature de la page à gauche des DevTools | « screencast » du frontal distant | `localStorage['screencast-enabled'] = 'false'` |
| Bandeau « DevTools is now available in French » | locale fr-FR ; Chromium ne livre que l'anglais | locale `en-US` pour la page `dt` |
| Clic sur une ligne sans ouvrir le volet Headers | clic au centre de la ligne (colonne Initiator) | cliquer la cellule Name (`td` 0) |
| La première ligne n'est pas la page | liste virtualisée, défilée vers le bas | `gridTop()` (molette) avant de pointer |
| `drawtext` échoue au carton titre | apostrophe droite dans `subtitle` | apostrophe typographique ’ |
