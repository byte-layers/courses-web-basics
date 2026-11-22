const competences = ["HTML", "CSS", "JavaScript", "Git"];
const liste = document.querySelector("#competences");

for (const competence of competences) {
  const li = document.createElement("li");
  li.textContent = competence;
  liste.append(li);
}
