const liste = document.querySelector("#livres");

function afficher(livres) {
  for (const livre of livres) {
    const li = document.createElement("li");
    li.textContent = livre.titre + ", " + livre.auteur;
    liste.append(li);
  }
}

async function charger() {
  const reponse = await fetch("livres.json");
  const livres = await reponse.json();
  console.log("Livres chargés :", livres.length);
  afficher(livres);
}

charger();
