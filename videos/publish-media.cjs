/**
 * Publie une vidéo sur https://media.byte-layers.com (Cloudflare R2), nommée
 * par son empreinte : v/<sha256>.<ext>. Un objet déjà présent n'est jamais
 * réécrit (même empreinte = même contenu). Décision :
 * byte-layers-monorepo/docs/ETAPES_CHOIX_VIDEOS.md.
 *
 *   bash publish-media.sh out/<nom>/<nom>.mp4
 *
 * Lit dans .env (hors git, chmod 600) : R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY,
 * R2_ENDPOINT (https://<account_id>.r2.cloudflarestorage.com) ; facultatifs :
 * R2_BUCKET (byte-layers-media), MEDIA_ORIGIN (https://media.byte-layers.com).
 * Aucune clé n'est jamais affichée. Signature S3 v4 faite ici, avec `crypto` :
 * pas de dépendance.
 */
require('./env.cjs');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const TYPES = { '.mp4': 'video/mp4', '.webm': 'video/webm' };
const CACHE = 'public, max-age=31536000, immutable';

const file = process.argv[2];
if (!file) {
  console.error('usage : bash publish-media.sh <fichier.mp4|fichier.webm>');
  process.exit(2);
}
const ext = path.extname(file).toLowerCase();
if (!TYPES[ext]) {
  console.error(`extension ${ext || '(aucune)'} : seules .mp4 et .webm se publient`);
  process.exit(2);
}
const { R2_ACCESS_KEY_ID: id, R2_SECRET_ACCESS_KEY: secret, R2_ENDPOINT: endpoint } = process.env;
if (!id || !secret || !endpoint) {
  console.error('R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY et R2_ENDPOINT sont attendus dans videos/.env');
  process.exit(2);
}
const bucket = process.env.R2_BUCKET || 'byte-layers-media';
const origin = (process.env.MEDIA_ORIGIN || 'https://media.byte-layers.com').replace(/\/$/, '');

const sha256 = (data) => crypto.createHash('sha256').update(data).digest('hex');
const hmac = (key, data) => crypto.createHmac('sha256', key).update(data).digest();

/** Une requête S3 signée (v4, région « auto » de R2). */
async function s3(method, key, { body, headers = {} } = {}) {
  const url = new URL(`${endpoint.replace(/\/$/, '')}/${bucket}/${key}`);
  const now = new Date().toISOString().replace(/[:-]|\.\d{3}/g, ''); // AAAAMMJJTHHMMSSZ
  const day = now.slice(0, 8);
  const payload = body ? sha256(body) : sha256('');
  const signed = { host: url.host, 'x-amz-content-sha256': payload, 'x-amz-date': now };
  const names = Object.keys(signed).sort();
  const canonical = [
    method,
    url.pathname.split('/').map(encodeURIComponent).join('/'),
    '',
    names.map((n) => `${n}:${signed[n]}\n`).join(''),
    names.join(';'),
    payload,
  ].join('\n');
  const scope = `${day}/auto/s3/aws4_request`;
  const toSign = ['AWS4-HMAC-SHA256', now, scope, sha256(canonical)].join('\n');
  const kSigning = hmac(hmac(hmac(hmac(`AWS4${secret}`, day), 'auto'), 's3'), 'aws4_request');
  const signature = crypto.createHmac('sha256', kSigning).update(toSign).digest('hex');
  return fetch(url, {
    method,
    body,
    headers: {
      ...headers,
      'x-amz-content-sha256': payload,
      'x-amz-date': now,
      authorization: `AWS4-HMAC-SHA256 Credential=${id}/${scope}, SignedHeaders=${names.join(';')}, Signature=${signature}`,
    },
  });
}

(async () => {
  const body = fs.readFileSync(file);
  const key = `v/${sha256(body)}${ext}`;
  const publicUrl = `${origin}/${key}`;
  const mo = (body.length / 1048576).toFixed(1);

  const head = await s3('HEAD', key);
  if (head.status === 200) {
    console.log(`déjà publié (${mo} Mo) : ${publicUrl}`);
    return;
  }
  if (head.status !== 404) throw new Error(`R2 HEAD ${key} : ${head.status}`);

  const put = await s3('PUT', key, {
    body,
    headers: { 'content-type': TYPES[ext], 'cache-control': CACHE, 'if-none-match': '*' },
  });
  if (!put.ok) throw new Error(`R2 PUT ${key} : ${put.status} ${(await put.text()).slice(0, 300)}`);
  console.log(`publié (${mo} Mo) : ${publicUrl}`);
})().catch((e) => {
  console.error(e.message);
  process.exit(1);
});
