const onglets = document.querySelectorAll(".tab");
const panneaux = document.querySelectorAll(".tab-content");

function ouvrir(onglet) {
  for (const panneau of panneaux) {
    panneau.classList.remove("active");
  }
  for (const autre of onglets) {
    autre.classList.remove("tab-active");
  }
  onglet.classList.add("tab-active");
  const id = onglet.getAttribute("data-content-id");
  document.querySelector("#" + id).classList.add("active");
}

for (const onglet of onglets) {
  onglet.addEventListener("click", function () {
    ouvrir(onglet);
  });
}
