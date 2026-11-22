// Ce que le serveur a envoyé : du texte
const texte = '{"titre": "Dune", "auteur": "Frank Herbert", "pages": 900}';

const livre = JSON.parse(texte);
console.log("Titre :", livre.titre);
