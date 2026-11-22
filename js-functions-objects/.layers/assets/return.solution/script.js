function prixTTC(prixHT) {
  return prixHT * 1.2;
}

const total = prixTTC(25) * 2;
console.log("Deux abonnements : " + total);
