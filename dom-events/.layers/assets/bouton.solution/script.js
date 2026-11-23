const bouton = document.querySelector("#saluer");
const reponse = document.querySelector("#reponse");

function repondre() {
  reponse.textContent = "Bonjour, visiteur !";
}

bouton.addEventListener("click", repondre);
