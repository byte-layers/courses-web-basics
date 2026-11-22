const champ = document.querySelector("#prenom");
const bouton = document.querySelector("#valider");
const message = document.querySelector("#message");

bouton.addEventListener("click", function () {
  const prenom = champ.value.trim();
  if (prenom === "") {
    message.textContent = "Remplissez le champ.";
    message.classList.add("erreur");
  } else {
    message.textContent = "Bonjour " + prenom + " !";
    message.classList.remove("erreur");
  }
});
