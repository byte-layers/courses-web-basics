const projets = [
  { titre: "Portfolio", annee: 2026, techno: "HTML" },
  { titre: "Météo", annee: 2025, techno: "JavaScript" },
  { titre: "Quiz", annee: 2024, techno: "CSS" }
];

function decrire(projet) {
  return projet.titre + " (" + projet.annee + ", " + projet.techno + ")";
}

for (const projet of projets) {
  console.log(decrire(projet));
}
