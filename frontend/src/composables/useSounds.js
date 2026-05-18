// 8-bit arcade sound synthesizer.
// Generates retro sounds in real time via Web Audio API — no audio files needed,
// so nothing to bundle, host, or load. Honors a localStorage mute toggle.
//
// Usage:
//   const { play, muted, toggleMute } = useSounds();
//   play("blip");  // any of: coin, blip, success, zap, powerup, konami

import { ref, watch } from "vue";

const MUTE_KEY = "flask-vue3:muted";
const muted = ref(localStorage.getItem(MUTE_KEY) === "true");

watch(muted, (v) => localStorage.setItem(MUTE_KEY, String(v)));

let ctx = null;
const getCtx = () => {
  if (!ctx) {
    const Ctor = window.AudioContext || window.webkitAudioContext;
    if (!Ctor) return null;
    ctx = new Ctor();
  }
  // Some browsers suspend the context until a user gesture; resume on first use.
  if (ctx.state === "suspended") ctx.resume();
  return ctx;
};

// Play a sequence of "notes": [{ freq, duration, type, gain }]
const playSequence = (notes, masterGain = 0.18) => {
  if (muted.value) return;
  const ac = getCtx();
  if (!ac) return;
  let t = ac.currentTime;
  for (const n of notes) {
    const osc = ac.createOscillator();
    const g = ac.createGain();
    osc.type = n.type || "square";
    osc.frequency.setValueAtTime(n.freq, t);
    if (n.slideTo) {
      osc.frequency.exponentialRampToValueAtTime(n.slideTo, t + n.duration);
    }
    const peak = (n.gain ?? 1) * masterGain;
    g.gain.setValueAtTime(0, t);
    g.gain.linearRampToValueAtTime(peak, t + 0.005);
    g.gain.exponentialRampToValueAtTime(0.0001, t + n.duration);
    osc.connect(g).connect(ac.destination);
    osc.start(t);
    osc.stop(t + n.duration + 0.01);
    t += n.duration + (n.gap ?? 0.01);
  }
};

const SOUNDS = {
  // Coin-insert jingle (classic Mario coin: B5 -> E6)
  coin: [
    { freq: 988, duration: 0.08, type: "square" },
    { freq: 1319, duration: 0.18, type: "square" },
  ],
  // Quick UI confirmation
  blip: [{ freq: 880, duration: 0.07, type: "square" }],
  // Powerup / cleared (rising)
  success: [
    { freq: 523, duration: 0.06 },
    { freq: 659, duration: 0.06 },
    { freq: 784, duration: 0.06 },
    { freq: 1047, duration: 0.12 },
  ],
  // Delete / explode (descending sawtooth)
  zap: [
    {
      freq: 880,
      slideTo: 80,
      duration: 0.25,
      type: "sawtooth",
      gain: 0.8,
    },
  ],
  // 1-up
  powerup: [
    { freq: 392, duration: 0.05 },
    { freq: 523, duration: 0.05 },
    { freq: 659, duration: 0.05 },
    { freq: 784, duration: 0.05 },
    { freq: 1047, duration: 0.15 },
  ],
  // Konami easter egg — fanfare
  konami: [
    { freq: 523, duration: 0.08 },
    { freq: 659, duration: 0.08 },
    { freq: 784, duration: 0.08 },
    { freq: 1047, duration: 0.08 },
    { freq: 1319, duration: 0.08 },
    { freq: 1568, duration: 0.25 },
  ],
};

const play = (name) => {
  const seq = SOUNDS[name];
  if (!seq) return;
  playSequence(seq);
};

const toggleMute = () => (muted.value = !muted.value);

export function useSounds() {
  return { play, muted, toggleMute };
}
