const codeSecret = "1234";
let saisie = "0000"; // ce que le visiteur a tapé

if (saisie === codeSecret) {
  console.log("Accès autorisé");
} else {
  console.log("Accès refusé");
}
