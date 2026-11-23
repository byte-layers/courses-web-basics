const secret = 7;
const saisie = "7"; // ce que le joueur a tapé : du texte, comme ce que rend prompt()
const proposition = Number(saisie);

if (proposition === secret) {
  console.log(proposition, "Gagné !");
} else if (proposition < secret) {
  console.log(proposition, "Trop petit.");
} else {
  console.log(proposition, "Trop grand.");
}
