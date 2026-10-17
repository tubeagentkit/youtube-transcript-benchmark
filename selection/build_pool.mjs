// Builds a candidate pool of public videos from the YouTube Data API v3.
// Usage: YOUTUBE_DATA_API_KEY=... node build_pool.mjs > pool.json
// Queries are fixed and listed here so the sample can be audited and repeated.
const key = process.env.YOUTUBE_DATA_API_KEY;
if (!key) { console.error('set YOUTUBE_DATA_API_KEY'); process.exit(1); }
const get = async (path, params) => {
  const u = new URL('https://www.googleapis.com/youtube/v3/' + path);
  for (const [k, v] of Object.entries({ ...params, key })) u.searchParams.set(k, v);
  const r = await fetch(u); const j = await r.json();
  if (!r.ok) throw new Error(String(j.error?.message || JSON.stringify(j)).slice(0, 140));
  return j;
};
const iso = d => { const m = /PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?/.exec(d) || []; return (+m[1] || 0) * 3600 + (+m[2] || 0) * 60 + (+m[3] || 0); };

// [label, query, extra search params]
const QUERIES = [
  ['en_short', 'how to explained quickly', { videoDuration: 'short', relevanceLanguage: 'en' }],
  ['en_short', 'science fact animation', { videoDuration: 'short', relevanceLanguage: 'en' }],
  ['en_medium', 'tutorial for beginners', { videoDuration: 'medium', relevanceLanguage: 'en' }],
  ['en_medium', 'history documentary', { videoDuration: 'medium', relevanceLanguage: 'en' }],
  ['en_long', 'full lecture university course', { videoDuration: 'long', relevanceLanguage: 'en' }],
  ['en_long', 'podcast full episode interview', { videoDuration: 'long', relevanceLanguage: 'en' }],
  ['en_long', 'live stream recording conference talk', { videoDuration: 'long', relevanceLanguage: 'en' }],
  ['es', 'tutorial en español', { relevanceLanguage: 'es' }],
  ['es', 'explicación documental español', { relevanceLanguage: 'es' }],
  ['hi', 'हिंदी में समझाइए', { relevanceLanguage: 'hi' }],
  ['hi', 'हिंदी ट्यूटोरियल', { relevanceLanguage: 'hi' }],
  ['ja', '解説 初心者 日本語', { relevanceLanguage: 'ja' }],
  ['ja', '講義 日本語', { relevanceLanguage: 'ja' }],
  ['de', 'Tutorial auf Deutsch erklärt', { relevanceLanguage: 'de' }],
  ['de', 'Dokumentation Deutsch', { relevanceLanguage: 'de' }],
  ['shorts', 'shorts #shorts', { videoDuration: 'short', relevanceLanguage: 'en' }],
  ['shorts', 'quick tip #shorts', { videoDuration: 'short', relevanceLanguage: 'en' }],
  ['age', 'horror movie scene graphic', { order: 'viewCount' }],
  ['age', 'violent video game trailer mature', { order: 'viewCount' }],
  ['age', 'true crime documentary graphic footage', { order: 'viewCount' }],
  ['nocap', 'ambient music no talking', { videoDuration: 'medium' }],
  ['nocap', 'kids nursery rhymes songs', { videoDuration: 'medium' }],
];
const pool = new Map();
for (const [label, q, extra] of QUERIES) {
  const s = await get('search', { part: 'id', q, type: 'video', maxResults: '50', ...extra });
  const ids = s.items.map(i => i.id.videoId).filter(Boolean);
  const v = await get('videos', { part: 'contentDetails,snippet,status', id: ids.join(',') });
  for (const it of v.items) {
    if (pool.has(it.id)) continue;
    pool.set(it.id, {
      id: it.id,
      source_label: label,
      query: q,
      duration_s: iso(it.contentDetails.duration),
      audio_lang: it.snippet.defaultAudioLanguage || it.snippet.defaultLanguage || '',
      caption_flag: it.contentDetails.caption,
      live: it.snippet.liveBroadcastContent,
      age_restricted: it.contentDetails.contentRating?.ytRating === 'ytAgeRestricted',
      published: it.snippet.publishedAt.slice(0, 10),
    });
  }
}
console.log(JSON.stringify({ built: new Date().toISOString(), queries: QUERIES.length, videos: [...pool.values()] }, null, 1));
