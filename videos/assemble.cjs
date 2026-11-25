/**
 * Assemble raw.mp4 + narration en <name>.mp4 : chaque segment audio est posé
 * à l'instant de son marqueur, un carton titre ouvre la vidéo.
 *
 *   node assemble.cjs <scenario.cjs> <outdir>
 */
const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const scenario = require(path.resolve(process.argv[2]));
const out = path.resolve(process.argv[3]);
const tts = JSON.parse(fs.readFileSync(path.join(out, 'tts.json'), 'utf8'));
const { markers } = JSON.parse(fs.readFileSync(path.join(out, 'markers.json'), 'utf8'));
const TITLE_S = 3;
const FONT = '/System/Library/Fonts/HelveticaNeue.ttc';
const esc = (s) => s.replace(/\\/g, '\\\\').replace(/:/g, '\\:').replace(/'/g, "\\'");

// 1. Carton titre (fond pervenche sombre, titre + sous-titre).
const title = path.join(out, 'title.mp4');
execFileSync('ffmpeg', ['-y', '-v', 'error',
  '-f', 'lavfi', '-i', `color=c=0x1b1d3a:s=1920x1080:d=${TITLE_S}:r=25`,
  '-f', 'lavfi', '-i', `anullsrc=r=44100:cl=stereo:d=${TITLE_S}`,
  '-vf', [
    `drawtext=fontfile=${FONT}:text='${esc(scenario.title)}':fontcolor=white:fontsize=84:x=(w-text_w)/2:y=(h-text_h)/2-70`,
    `drawtext=fontfile=${FONT}:text='${esc(scenario.subtitle)}':fontcolor=0xb7a6ff:fontsize=56:x=(w-text_w)/2:y=(h-text_h)/2+50`,
    `drawtext=fontfile=${FONT}:text='byte_layers  ·  live coding':fontcolor=0x8a8fb8:fontsize=34:x=(w-text_w)/2:y=h-120`,
    'fade=t=out:st=2.4:d=0.6',
  ].join(','),
  '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', title]);

// 2. Piste de narration alignée sur les segments. Quand une narration
// dépasse le créneau enregistré (voix plus lente, texte allongé), la vidéo
// gèle sur la dernière image du segment le temps qu'il faut : changer la voix
// ne demande jamais de réenregistrer VS Code.
const { duration } = JSON.parse(fs.readFileSync(path.join(out, 'markers.json'), 'utf8'));
const PAD_MS = 400;
let shift = 0; // temps ajouté par les gels, cumulé
const parts = []; // [début, fin] de chaque segment dans raw.webm, et gel à sa fin
const starts = []; // début de chaque narration dans la vidéo finale
markers.forEach((m, i) => {
  const end = markers[i + 1]?.ms ?? duration;
  const slot = end - m.ms;
  const need = tts[m.id].ms + PAD_MS;
  const freeze = Math.max(0, need - slot);
  if (freeze > 0) console.log(`  ${m.id} : narration ${(tts[m.id].ms / 1000).toFixed(1)} s > créneau ${(slot / 1000).toFixed(1)} s → gel ${(freeze / 1000).toFixed(1)} s`);
  starts.push(m.ms + shift);
  parts.push({ from: m.ms, to: end, freeze });
  shift += freeze;
});

const inputs = [];
const filters = [];
const vlabels = [];
parts.forEach((p, i) => {
  const trim = `[0:v]trim=start=${p.from / 1000}:end=${p.to / 1000},setpts=PTS-STARTPTS`;
  filters.push(p.freeze > 0 ? `${trim},tpad=stop_mode=clone:stop_duration=${p.freeze / 1000}[v${i}]` : `${trim}[v${i}]`);
  vlabels.push(`[v${i}]`);
});
filters.push(`${vlabels.join('')}concat=n=${parts.length}:v=1:a=0[vout]`);
markers.forEach((m, i) => {
  inputs.push('-i', tts[m.id].file);
  filters.push(`[${i + 1}:a]adelay=${starts[i]}|${starts[i]}[a${i}]`);
});
const mix = `${markers.map((_, i) => `[a${i}]`).join('')}amix=inputs=${markers.length}:normalize=0:dropout_transition=0,apad[narr]`;
const main = path.join(out, 'main.mp4');
execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', path.join(out, 'raw.mp4'), ...inputs,
  '-filter_complex', [...filters, mix].join(';'),
  '-map', '[vout]', '-map', '[narr]', '-shortest',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p', '-r', '25',
  '-c:a', 'aac', '-b:a', '128k', '-ar', '44100', '-ac', '2', main]);

// 3. Carton + vidéo.
const list = path.join(out, 'concat.txt');
fs.writeFileSync(list, `file '${title}'\nfile '${main}'\n`);
const master = path.join(out, 'master.mp4');
execFileSync('ffmpeg', ['-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', list, '-c', 'copy', master]);

// 4. Livrable léger : 1080p, 15 i/s (seuls le curseur et le défilement
// bougent), voix mono, lecture possible avant la fin du téléchargement.
// H.264 + AAC : lu partout, y compris Firefox et la webview de VS Code.
// Environ 8 Mo pour 2 min 30 (le master en fait 16).
const final = path.join(out, `${scenario.name}.mp4`);
execFileSync('ffmpeg', ['-y', '-v', 'error', '-i', master,
  '-r', '15',
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '26', '-tune', 'stillimage', '-pix_fmt', 'yuv420p',
  '-c:a', 'aac', '-b:a', '64k', '-ac', '1', '-movflags', '+faststart', final]);
const mo = (fs.statSync(final).size / 1048576).toFixed(1);
console.log(`✓ ${final} (${mo} Mo, 1080p)`);
