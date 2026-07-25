// Text-to-speech helper built on the browser's native Web Speech API
// (window.speechSynthesis). This is what was missing before: the app had
// voice INPUT (VoiceInput.jsx -> SpeechRecognition, speech-to-text) but no
// voice OUTPUT (speech synthesis, text-to-speech) — so the transcript
// matched what you said, but the AI's reply was never spoken back.

let cachedVoices = [];

function loadVoices() {
  return new Promise((resolve) => {
    if (!("speechSynthesis" in window)) return resolve([]);
    const synth = window.speechSynthesis;
    const existing = synth.getVoices();
    if (existing.length) {
      cachedVoices = existing;
      resolve(existing);
      return;
    }
    // Voices load asynchronously in some browsers (notably Chrome) —
    // they aren't ready on the very first call.
    synth.onvoiceschanged = () => {
      cachedVoices = synth.getVoices();
      resolve(cachedVoices);
    };
    // Fallback in case onvoiceschanged never fires
    setTimeout(() => resolve(synth.getVoices()), 300);
  });
}

export function isSpeechSynthesisSupported() {
  return typeof window !== "undefined" && "speechSynthesis" in window;
}

export async function speak(text, lang = "en-IN") {
  if (!text || !isSpeechSynthesisSupported()) return false;

  const synth = window.speechSynthesis;
  synth.cancel(); // stop any speech already in progress before starting new

  const voices = cachedVoices.length ? cachedVoices : await loadVoices();
  const utterance = new SpeechSynthesisUtterance(text);
  utterance.lang = lang;

  const langPrefix = lang.split("-")[0];
  const exactMatch = voices.find((v) => v.lang === lang);
  const looseMatch = voices.find((v) => v.lang?.startsWith(langPrefix));
  // If no Kannada voice is installed on this device/browser, this falls
  // back to the default voice, which will still read the English text
  // fine but may mispronounce Kannada script — that's a device/OS voice
  // pack limitation, not a bug in this code.
  utterance.voice = exactMatch || looseMatch || null;

  synth.speak(utterance);
  return true;
}

export function stopSpeaking() {
  if (isSpeechSynthesisSupported()) {
    window.speechSynthesis.cancel();
  }
}
