# courses-web-basics

Trois cours pour débuter le web avec byte_layers : HTML et CSS, puis HTML et CSS avancé, puis JavaScript. Le fil rouge est un portfolio, construit en trois versions. Il y a un dossier par contenu, à plat, chacun avec son `.layers/`.

Les cours insistent sur les pièges du débutant : chaque exercice les fait rencontrer avant de les expliquer.

## Les bases HTML CSS

Stack `html-css` : « Créer ses premières pages web ».

| Dossier | Contenu | Type |
|---|---|---|
| `web-request-response/` | Le web : une adresse, une requête, une page | bit |
| `web-page-languages/` | Une page web : HTML, CSS et JavaScript | bit |
| `web-standards-browsers/` | Les standards du web et les moteurs des navigateurs | bit |
| `web-everywhere/` | Le web partout : sites, applications, mobile et bureau | bit |
| `html-document/` | Le squelette d'une page HTML, son texte, ses liens et ses images | bit |
| `semantic-html/` | Le HTML sémantique : le sens avant la forme | bit |
| `css-rules-cascade/` | CSS : règles, sélecteurs et cascade | bit |
| `box-model/` | Le modèle de boîte : contenu, padding, bordure, marge | bit |
| `html-css-basics-lab/` | Les bases HTML et CSS, sur votre machine | lab |
| `portfolio-v1-challenge/` | Mon portfolio, version 1 : une page de liens | challenge |

## HTML CSS avancé

Stack `web-layout` : « Mettre en page pour tous les écrans ».

| Dossier | Contenu | Type |
|---|---|---|
| `normal-flow/` | Bloc, inline : le flux normal d'une page | bit |
| `flexbox/` | Flexbox : aligner des éléments sur une ligne | bit |
| `css-grid/` | CSS Grid : des lignes et des colonnes | bit |
| `html-tables/` | Les tableaux HTML | bit |
| `html-forms/` | Les formulaires HTML | bit |
| `responsive-design/` | Le responsive design : une page pour tous les écrans | bit |
| `web-accessibility/` | L'accessibilité web : une page lisible par tous | bit |
| `css-variables/` | Variables CSS : un choix écrit une fois | bit |
| `css-motion/` | Transitions et animations CSS | bit |
| `css-frameworks/` | Bootstrap : des classes CSS toutes faites | bit |
| `css-build-tools/` | Tailwind, et pourquoi le CSS se compile | bit |
| `html-css-advanced-lab/` | HTML et CSS avancé, sur votre machine | lab |
| `portfolio-v2-challenge/` | Mon portfolio v2 : adaptatif, accessible, avec un formulaire | challenge |

## Les bases de JavaScript

Stack `javascript` : « Rendre une page interactive avec JavaScript ».

| Dossier | Contenu | Type |
|---|---|---|
| `js-console/` | La console JavaScript : premier contact avec le moteur du navigateur | bit |
| `js-in-page/` | Où vit le JavaScript dans une page : script, fichier .js et defer | bit |
| `js-conditions/` | Décider : les conditions en JavaScript | bit |
| `js-arrays-loops/` | Répéter : tableaux et boucles en JavaScript | bit |
| `js-functions-objects/` | Fonctions et objets en JavaScript | bit |
| `dom/` | Le DOM : la page vue par JavaScript | bit |
| `dom-events/` | Les événements : réagir aux actions du visiteur | bit |
| `json-fetch/` | Données JSON et fetch : charger des données depuis un serveur | bit |
| `js-basics-lab/` | Les bases de JavaScript, sur votre machine | lab |
| `portfolio-v3-challenge/` | Mon portfolio, version 3 : une page qui réagit | challenge |

## Versions et fichiers

- Les contenus se lisent dans l'ordre des tableaux.
- Chaque contenu a son tag, de la forme `<dossier>/vN`. Chaque stack a son `stacks/<id>/stack.yml` et son tag `stacks/<id>/vN`.
- Les bits ont des schémas animés (format `bl-scenes/0.3`). Ceux qui ont un exercice de page web (playground `runtime: web` : éditeur, aperçu, console, contrôles sur la page rendue) demandent l'extension 0.9.0. Les deux autres bits demandent la 0.8.0. Les labs et les challenges demandent la 0.4.0.
- Dans VS Code, le playground web ne montre pas encore son aperçu : il s'ouvre sur le site.
- Les labs et les challenges écrivent dans `~/byte-layers/web/`.
- Chaque playground web a sa solution dans `.layers/assets/<nom>.solution/`. `layers-lint` la rejoue dans Chromium : les contrôles doivent échouer au départ et passer avec la solution.

## Régénérer un schéma animé

Les fichiers `.layers/assets/*.scene.json` sont écrits par des scripts Python, rangés dans le dossier `scenes/` du contenu (hors de `.layers/`, donc non publiés) :

| Contenu | Script | Fichier écrit |
|---|---|---|
| `box-model` | `scenes/box_plan.py` | `box.scene.json` |
| `css-build-tools` | `scenes/tailwind.py` | `tailwind.scene.json` |
| `css-frameworks` | `scenes/bootstrap.py` | `bootstrap.scene.json` |
| `css-grid` | `scenes/grid.py` | `grid.scene.json` |
| `css-rules-cascade` | `scenes/css_plan.py`, `scenes/syntaxe_plan.py` | `css.scene.json`, `syntaxe.scene.json` |
| `css-motion` | `scenes/motion.py` | `motion.scene.json` |
| `css-variables` | `scenes/variables.py` | `variables.scene.json` |
| `dom-events` | `scenes/events.py`, `scenes/events_plan.py` | `events.scene.json`, `events-plan.scene.json` |
| `dom` | `scenes/dom_plan.py` | `dom.scene.json` |
| `flexbox` | `scenes/flex.py` | `flex.scene.json` |
| `html-document` | `scenes/html_plan.py`, `scenes/texte_plan.py` | `chemin.scene.json`, `html.scene.json`, `texte.scene.json` |
| `html-forms` | `scenes/forms.py` | `forms.scene.json` |
| `html-tables` | `scenes/tables.py` | `tables.scene.json` |
| `js-arrays-loops` | `scenes/loops.py` | `loops.scene.json` |
| `js-conditions` | `scenes/conditions.py` | `conditions.scene.json` |
| `js-console` | `scenes/console.py`, `scenes/console_plan.py` | `console.scene.json`, `console-plan.scene.json` |
| `js-functions-objects` | `scenes/functions.py`, `scenes/fleche_plan.py` | `functions.scene.json`, `fleche.scene.json` |
| `js-in-page` | `scenes/in_page.py` | `in-page.scene.json` |
| `json-fetch` | `scenes/fetch.py`, `scenes/json_plan.py` | `fetch.scene.json`, `json.scene.json` |
| `normal-flow` | `scenes/flow.py`, `scenes/limites_plan.py` | `flow.scene.json`, `limites.scene.json` |
| `responsive-design` | `scenes/responsive.py` | `responsive.scene.json` |
| `semantic-html` | `scenes/semantic_plan.py` | `semantic.scene.json` |
| `web-accessibility` | `scenes/a11y.py` | `a11y.scene.json` |
| `web-everywhere` | `scenes/everywhere.py`, `scenes/cibles_plan.py` | `everywhere.scene.json`, `cibles.scene.json` |
| `web-page-languages` | `scenes/langages_plan.py`, `scenes/page_plan.py` | `langages.scene.json`, `page.scene.json` |
| `web-standards-browsers` | `scenes/standards_plan.py` | `standards.scene.json`, `moteurs.scene.json`, `histoire.scene.json` |
| `web-request-response` | `scenes/http.py`, `scenes/http_plan.py` | `http.scene.json`, `http-message.scene.json`, `http-cascade.scene.json`, `http-codes.scene.json` |

On corrige le script, jamais le JSON à la main, puis on le relance depuis la racine du dépôt : `python3 box-model/scenes/box_plan.py`. Les scripts importent `tools/scenes/scene_kit.py` (copie du kit de la skill byte-layers-scenes) et `tools/scenes/paths.py`, qui dit où écrire ; avec `BL_SCENES` pointant sur `packages/scenes` d'un worktree du monorepo, la scène est aussi écrite dans `lessons/zz-<id>/` pour la valider et la capturer.

Licence : CC BY-NC-SA 4.0.
