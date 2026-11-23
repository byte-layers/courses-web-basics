# courses-web-basics

Trois cours pour débuter le web avec byte_layers : HTML et CSS, puis HTML et CSS avancé, puis JavaScript. Le fil rouge est un portfolio, construit en trois versions. Il y a un dossier par contenu, à plat, chacun avec son `.layers/`.

Les cours insistent sur les pièges du débutant : chaque exercice les fait rencontrer avant de les expliquer.

## Les bases HTML CSS

Stack `html-css` : « Créer ses premières pages web ».

| Dossier | Contenu | Type |
|---|---|---|
| `web-request-response/` | Le web : une adresse, une requête, une page | bit |
| `web-page-languages/` | Une page web : HTML, CSS et JavaScript | bit |
| `web-everywhere/` | Le web partout : sites, applications, mobile et bureau | bit |
| `html-document/` | Le squelette d'une page HTML, son texte, ses liens et ses images | bit |
| `semantic-html/` | Le HTML sémantique : le sens avant la forme | bit |
| `css-rules-cascade/` | CSS : règles, sélecteurs et cascade | bit |
| `box-model/` | Le modèle de boîte : contenu, padding, bordure, marge | bit |
| `html-css-basics-lab/` | Les bases HTML et CSS, sur votre machine | lab |
| `portfolio-v1-challenge/` | Mon portfolio, version 1 | challenge |

## HTML CSS avancé

Stack `web-layout` : « Mettre en page pour tous les écrans ».

| Dossier | Contenu | Type |
|---|---|---|
| `normal-flow/` | Bloc, inline : le flux normal d'une page | bit |
| `flexbox/` | Flexbox : aligner des éléments sur une ligne | bit |
| `css-grid/` | CSS Grid : des lignes et des colonnes | bit |
| `html-tables-forms/` | Tableaux et formulaires HTML | bit |
| `responsive-design/` | Le responsive design : une page pour tous les écrans | bit |
| `web-accessibility/` | L'accessibilité web : une page lisible par tous | bit |
| `css-variables-motion/` | Variables CSS et mouvement | bit |
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
- Les bits qui ont un exercice de page web (playground `runtime: web` : éditeur, aperçu, console, contrôles sur la page rendue) demandent l'extension 0.9.0. Les deux autres bits demandent la 0.8.0. Les labs et les challenges demandent la 0.4.0.
- Dans VS Code, le playground web ne montre pas encore son aperçu : il s'ouvre sur le site.
- Les labs et les challenges écrivent dans `~/byte-layers/web/`.
- Chaque playground web a sa solution dans `.layers/assets/<nom>.solution/`. `layers-lint` la rejoue dans Chromium : les contrôles doivent échouer au départ et passer avec la solution.

Licence : CC BY-NC-SA 4.0.
