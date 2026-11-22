const notes = [12, 15, 9, 18, 16];

let total = 0;
for (const note of notes) {
  total = total + note;
}
const moyenne = total / notes.length;
console.log("Moyenne :", moyenne);
