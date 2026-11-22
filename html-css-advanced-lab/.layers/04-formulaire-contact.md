---
title: "04 - Un formulaire de contact, sans JavaScript"
description: "Écrire le formulaire de contact du portfolio, chaque champ relié à son étiquette et nommé, le faire contrôler par le navigateur, et voir dans la barre d'adresse ce qu'il envoie"
---

La page montre ; elle va maintenant recueillir. Vous écrivez le formulaire de contact du portfolio, sans une ligne de JavaScript, et vous voyez dans la barre d'adresse du navigateur ce qu'il envoie, champ par champ.

## 04.1 - Le formulaire et son premier champ

Un formulaire envoie ses données à l'adresse de son attribut `action`, de la façon que dit `method`. Ici, aucune adresse : sans `action`, le formulaire s'envoie **à la page elle-même**. Avec **`method="get"`**, les données sont ajoutées à l'adresse, après un `?`, sous la forme `nom=valeur`. C'est ce qui va vous permettre de les voir, sans serveur.

Collez cette section dans `index.html`, dans `main`, après les projets. Le champ Nom est complet : c'est le modèle des suivants.

🚧 **À compléter :**

```html
<section id="contact">
  <h2>Contact</h2>
  <form method="get">
    <p>
      <label for="nom">Votre nom</label>
      <input type="text" id="nom" name="nom" required>
    </p>
    <!-- TODO : les quatre champs du tableau ci-dessous, sur le même modèle -->
    <button type="submit">Envoyer</button>
  </form>
</section>
```

## 04.2 - Quatre champs, chacun relié et nommé

Chaque champ a son étiquette, dont le `for` reprend **exactement** son `id`, et un `name`, le nom sous lequel sa valeur part.

| Étiquette | Balise et type | `id` et `name` | Particularité |
|---|---|---|---|
| Votre e-mail | `<input type="email">` | `email` | obligatoire : `required` |
| Sujet | `<select>` avec trois `<option>` : Alternance, Projet, Autre | `sujet` | chaque option a une `value` : `alternance`, `projet`, `autre` |
| Votre message | `<textarea rows="5"></textarea>` | `message` | les deux balises collées, pour un champ vide au départ |
| Je souhaite recevoir des nouvelles | `<input type="checkbox">` | `newsletter` | l'étiquette se place **après** la case |

Enregistrez, rechargez, puis faites ces trois tests :

1. Cliquez sur chaque étiquette : le curseur va dans le champ, ou la case se coche. Une étiquette qui ne réagit pas n'est pas reliée.
2. Cliquez sur **Envoyer** sans rien remplir : le navigateur refuse, et affiche lui-même un message sur le champ Nom.
3. Tapez `camille` dans l'e-mail, sans `@`, remplissez le nom, et envoyez : le navigateur refuse encore.

```verify
H=$(tr -d '\n' < ~/byte-layers/web/advanced/index.html)
echo "$H" | grep -Eq '<form[^>]*method="get"' || { echo "index.html n'a pas de form avec method=\"get\"."; exit 1; }
for id in nom email sujet message newsletter; do
  echo "$H" | grep -Eq "<(input|select|textarea)[^>]*id=\"$id\"" || { echo "Il manque le champ d'id $id."; exit 1; }
  echo "$H" | grep -Eq "<(input|select|textarea)[^>]*name=\"$id\"" || { echo "Le champ $id n'a pas de name=\"$id\" : sa valeur ne serait pas envoyée."; exit 1; }
  echo "$H" | grep -Eq "<label[^>]*for=\"$id\"" || { echo "Aucune étiquette n'est reliée au champ $id : <label for=\"$id\">."; exit 1; }
done
echo "$H" | grep -Eq '<input[^>]*type="email"' || { echo "Le champ e-mail n'est pas de type email."; exit 1; }
echo "$H" | grep -Eq '<input[^>]*type="email"[^>]*required|<input[^>]*required[^>]*type="email"' || { echo "Le champ e-mail n'est pas obligatoire : ajoutez required."; exit 1; }
[ "$(echo "$H" | grep -o '<option' | wc -l)" -ge 3 ] || { echo "La liste Sujet doit avoir trois option."; exit 1; }
echo "Les cinq champs sont reliés à leur étiquette et nommés."
```

```hint
Pour la liste : `<select id="sujet" name="sujet">`, puis une ligne par choix, `<option value="alternance">Alternance</option>`. Pour la case : `<input type="checkbox" id="newsletter" name="newsletter">` suivi de `<label for="newsletter">…</label>`.
```

````solution
```html
<section id="contact">
  <h2>Contact</h2>
  <form method="get">
    <p>
      <label for="nom">Votre nom</label>
      <input type="text" id="nom" name="nom" required>
    </p>
    <p>
      <label for="email">Votre e-mail</label>
      <input type="email" id="email" name="email" required>
    </p>
    <p>
      <label for="sujet">Sujet</label>
      <select id="sujet" name="sujet">
        <option value="alternance">Alternance</option>
        <option value="projet">Projet</option>
        <option value="autre">Autre</option>
      </select>
    </p>
    <p>
      <label for="message">Votre message</label>
      <textarea id="message" name="message" rows="5"></textarea>
    </p>
    <p>
      <input type="checkbox" id="newsletter" name="newsletter">
      <label for="newsletter">Je souhaite recevoir des nouvelles</label>
    </p>
    <button type="submit">Envoyer</button>
  </form>
</section>
```
````

## 04.3 - Lire ce que le formulaire envoie

Remplissez tous les champs, cochez la case, et envoyez. La page se recharge, et la **barre d'adresse** montre ce qui est parti, après le `?` :

```text
index.html?nom=Camille&email=camille%40exemple.fr&sujet=alternance&message=Bonjour&newsletter=on
```

Chaque paire `name=valeur` est séparée de la suivante par `&`. Le `@` devient `%40` et une espace devient `+` : c'est l'encodage des adresses web. La case cochée envoie `on`. Un serveur qui recevrait cette adresse lirait exactement ces paires.

> **🧪 Manip — le champ sans name**
>
> 1. Retirez `name="message"` du `textarea`. Enregistrez, rechargez.
> 2. Remplissez le formulaire, écrivez un message, envoyez.
>
> *Observé : la barre d'adresse n'a plus de `message=`. Le champ s'affichait et se remplissait normalement, mais sa valeur n'est pas partie. Remettez `name="message"`.*

Avec `method="post"`, les données partent dans le corps de la requête au lieu de l'adresse : c'est ce qu'on utilise pour un vrai formulaire de contact, pour qu'un message n'apparaisse pas dans l'historique du navigateur. Le traitement, lui, demande un serveur ou du JavaScript.

> 📖 [Votre premier formulaire (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Extensions/Forms/Your_first_form) · [Envoyer les données d'un formulaire (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Extensions/Forms/Sending_and_retrieving_form_data) · [La validation côté client (MDN)](https://developer.mozilla.org/fr/docs/Learn_web_development/Extensions/Forms/Form_validation)
