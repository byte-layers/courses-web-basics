const lampe = document.querySelector("#lampe");
const etat = document.querySelector("#etat");
const bouton = document.querySelector("#bouton");

function basculer() {
  lampe.classList.toggle("allumee");
  if (lampe.classList.contains("allumee")) {
    etat.textContent = "La lampe est allumée";
  } else {
    etat.textContent = "La lampe est éteinte";
  }
}

bouton.addEventListener("click", basculer);
