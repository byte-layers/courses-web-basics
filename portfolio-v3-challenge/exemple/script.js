// Les projets : construits à partir de projets.json
const conteneur = document.querySelector("#liste-projets");

fetch("projets.json")
  .then((reponse) => reponse.json())
  .then((projets) => {
    for (const projet of projets) {
      const carte = document.createElement("article");
      carte.classList.add("projet");

      const image = document.createElement("img");
      image.src = projet.image;
      image.alt = projet.alt;

      const titre = document.createElement("h3");
      titre.textContent = projet.titre;

      const description = document.createElement("p");
      description.textContent = projet.description;

      carte.append(image, titre, description);
      conteneur.append(carte);
    }
  })
  .catch(() => {
    conteneur.textContent = "Les projets n'ont pas pu se charger. Réessayez dans un instant.";
    conteneur.classList.add("echec");
  });

// Le formulaire : valider, répondre dans la page, ajouter à la liste
const formulaire = document.querySelector("#formulaire-contact");
const retour = document.querySelector("#retour");
const envoyes = document.querySelector("#envoyes");

function afficher(texte, reussi) {
  retour.textContent = texte;
  if (reussi) {
    retour.classList.remove("refus");
    retour.classList.add("reussite");
  } else {
    retour.classList.remove("reussite");
    retour.classList.add("refus");
  }
}

function ajouterContact(evenement) {
  evenement.preventDefault();
  const nom = formulaire.nom.value.trim();
  const email = formulaire.email.value.trim();
  const message = formulaire.message.value.trim();

  if (nom === "") {
    afficher("Indiquez votre nom.", false);
    return;
  }
  if (!email.includes("@")) {
    afficher("Votre adresse e-mail doit contenir un @.", false);
    return;
  }

  const ligne = document.createElement("li");
  ligne.textContent = nom + " : " + (message || "(pas de message)");
  envoyes.append(ligne);

  afficher("Merci " + nom + ", votre message est bien parti.", true);
  formulaire.reset();
}

formulaire.addEventListener("submit", ajouterContact);
