/**
 * Narration : un fichier audio par segment, et leurs durées dans tts.json.
 * Lancé avant l'enregistrement, pour que chaque segment de la vidéo dure au
 * moins sa narration. Deux moteurs :
 *
 *   node tts.cjs <scenario.cjs> <outdir>
 *     TTS=say (défaut)  voix macOS, VOICE=Thomas RATE=175
 *     TTS=eleven        ElevenLabs, ELEVENLABS_API_KEY et VOICE=<voice_id>
 *                       (un clone fait par clone-voice.cjs) ; MODEL=eleven_v3
 *                       par défaut, qui lit les mots anglais tels quels
 *
 * Dans les deux cas, les mots anglais (noms d'outils, de marques) sont
 * réécrits phonétiquement d'après lexique.json (say) ou lexique-eleven.json : lus tels quels dans une
 * phrase française, les deux moteurs les francisent. ONLY=intro,ping ne
 * régénère que ces segments (les autres gardent leur audio).
 */
const { execFileSync } = require('child_process');
require('./env.cjs');
const fs = require('fs');
const path = require('path');

const scenario = require(path.resolve(process.argv[2]));
const out = path.resolve(process.argv[3]);
const engine = process.env.TTS || 'say';
const voice = process.env.VOICE || (engine === 'say' ? 'Thomas' : '');
const rate = process.env.RATE || '175';
const model = process.env.MODEL || 'eleven_v3';
// Avec ElevenLabs v3, les mots anglais sont bien lus tels quels : le lexique
// ne s'applique qu'à `say`, ou à ElevenLabs si LEXIQUE=1.
const useLexique = engine === 'say' || process.env.LEXIQUE === '1';
if (engine === 'eleven' && !(process.env.ELEVENLABS_API_KEY && voice)) {
  console.error('TTS=eleven demande ELEVENLABS_API_KEY et VOICE=<voice_id>');
  process.exit(2);
}
fs.mkdirSync(path.join(out, 'tts'), { recursive: true });

const durationOf = (file) =>
  Math.round(
    parseFloat(
      execFileSync('ffprobe', ['-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', file]).toString(),
    ) * 1000,
  );

// Les mots anglais que la voix lit mal sont remplacés par leur graphie phonétique.
const lexique = Object.entries(JSON.parse(fs.readFileSync(path.join(__dirname, engine === 'eleven' ? 'lexique-eleven.json' : 'lexique.json'), 'utf8')))
  .filter(([k]) => k !== '_')
  .sort((a, b) => b[0].length - a[0].length);
const escape = (s) => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
function prononce(text) {
  for (const [mot, lu] of lexique) {
    text = text.replace(new RegExp(`(?<![\\p{L}_])${escape(mot)}(?![\\p{L}_])`, 'giu'), lu);
  }
  return text;
}

async function eleven(text, file) {
  const r = await fetch(`https://api.elevenlabs.io/v1/text-to-speech/${voice}?output_format=mp3_44100_128`, {
    method: 'POST',
    headers: { 'xi-api-key': process.env.ELEVENLABS_API_KEY, 'content-type': 'application/json' },
    body: JSON.stringify({
      text,
      model_id: model,
      voice_settings: { stability: 0.5, similarity_boost: 0.8, style: 0.2, use_speaker_boost: true },
    }),
  });
  if (!r.ok) throw new Error(`ElevenLabs ${r.status} : ${await r.text()}`);
  fs.writeFileSync(file, Buffer.from(await r.arrayBuffer()));
}

(async () => {
  const only = process.env.ONLY ? new Set(process.env.ONLY.split(',')) : null;
  const previous = fs.existsSync(path.join(out, 'tts.json')) ? JSON.parse(fs.readFileSync(path.join(out, 'tts.json'), 'utf8')) : {};
  const result = {};
  for (const seg of scenario.segments) {
    if (only && !only.has(seg.id) && previous[seg.id]) {
      result[seg.id] = previous[seg.id];
      continue;
    }
    let file;
    if (engine === 'eleven') {
      file = path.join(out, 'tts', `${seg.id}.mp3`);
      await eleven(useLexique ? prononce(seg.say) : seg.say, file);
    } else {
      file = path.join(out, 'tts', `${seg.id}.aiff`);
      execFileSync('say', ['-v', voice, '-r', rate, '-o', file, prononce(seg.say)]);
    }
    result[seg.id] = { file, ms: durationOf(file) };
    console.log(`  ${seg.id.padEnd(12)} ${(result[seg.id].ms / 1000).toFixed(1)} s`);
  }
  fs.writeFileSync(path.join(out, 'tts.json'), JSON.stringify(result, null, 2));
  const total = Object.values(result).reduce((s, r) => s + r.ms, 0);
  console.log(`narration : ${(total / 1000).toFixed(0)} s, ${engine === 'eleven' ? `ElevenLabs ${model}` : `voix ${voice}`}`);
})().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
