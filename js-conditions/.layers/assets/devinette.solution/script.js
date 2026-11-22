const secret = 7;

function verdict(saisie) {
  const proposition = Number(saisie);
  if (proposition === secret) {
    console.log(proposition, "Gagné !");
  } else if (proposition < secret) {
    console.log(proposition, "Trop petit.");
  } else {
    console.log(proposition, "Trop grand.");
  }
}

// Trois saisies, du texte comme ce que rend prompt()
verdict("7");
verdict("3");
verdict("9");
