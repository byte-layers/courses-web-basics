const liste = document.querySelector("#projets");

function afficher(projets) {
  for (const projet of projets) {
    const li = document.createElement("li");
    li.textContent = projet.titre + " (" + projet.annee + ")";
    liste.append(li);
  }
}

let projets = [];
fetch("projets.json")
  .then((reponse) => reponse.json())
  .then((donnees) => {
    projets = donnees;
    console.log("Projets chargés :", projets.length);
    afficher(projets);
  });
