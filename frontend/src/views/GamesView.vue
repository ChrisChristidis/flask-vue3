<template>
  <div class="container py-4" :class="{ 'konami-mode': konamiActive }">
    <!-- Hero — arcade marquee -->
    <header class="hero mb-4">
      <button
        class="hero-mute"
        :title="muted ? 'Unmute sounds (M)' : 'Mute sounds (M)'"
        @click="onToggleMute"
      >
        {{ muted ? "🔇" : "🔊" }}
      </button>
      <button
        class="hero-help"
        title="Keyboard shortcuts (?)"
        @click="showHelp = !showHelp"
      >
        ?
      </button>

      <div class="hero-marquee">
        <span class="hero-coin">●</span>
        <span class="hero-press">INSERT COIN</span>
        <span class="hero-coin">●</span>
      </div>
      <h1 class="hero-title">GAMES&nbsp;LIBRARY</h1>
      <p class="hero-sub">A QUARTER FOR EVERY GAME ON THE SHELF</p>
      <div class="hero-controls">
        <span class="hero-key">▲</span>
        <span class="hero-key">▼</span>
        <span class="hero-key">◀</span>
        <span class="hero-key">▶</span>
        <span class="hero-btn">A</span>
        <span class="hero-btn">B</span>
      </div>
    </header>

    <!-- Stats row — HIGH SCORE panel -->
    <div class="row stats-row mb-4">
      <div class="col">
        <div class="stat-card">
          <div class="stat-label">TOTAL</div>
          <div class="stat-number">{{ pad(games.length) }}</div>
        </div>
      </div>
      <div class="col">
        <div class="stat-card stat-played">
          <div class="stat-label">CLEARED</div>
          <div class="stat-number">{{ pad(playedCount) }}</div>
        </div>
      </div>
      <div class="col">
        <div class="stat-card stat-todo">
          <div class="stat-label">QUEUE</div>
          <div class="stat-number">{{ pad(todoCount) }}</div>
        </div>
      </div>
    </div>

    <!-- Alert toast (Konami too) -->
    <b-alert v-model="showMessage" variant="success" dismissible class="mb-3">
      <strong>✓</strong> {{ message }}
    </b-alert>

    <!-- Toolbar: search + add -->
    <div class="toolbar mb-3">
      <div class="search-wrap">
        <span class="search-icon">▶</span>
        <input
          ref="searchInput"
          v-model="search"
          type="text"
          class="search-input"
          placeholder="SEARCH CARTRIDGES… (PRESS / TO FOCUS)"
          @keydown.esc="search = ''"
        />
        <button
          v-if="search"
          class="search-clear"
          title="Clear (Esc)"
          @click="search = ''"
        >
          ×
        </button>
      </div>
      <div class="toolbar-label">
        ► COUNT: <strong>{{ pad(filtered.length) }}</strong>
      </div>
      <button class="btn btn-primary btn-retro" v-b-modal.game-modal>
        + NEW CART
      </button>
    </div>

    <!-- Empty state -->
    <div v-if="filtered.length === 0" class="empty-state">
      <div class="empty-emoji">🕹️</div>
      <h3 class="empty-title">
        {{ search ? "NO MATCH" : "PRESS START" }}
      </h3>
      <p class="empty-sub">
        {{
          search
            ? `No cartridges match "${search}".`
            : "No cartridges in the shelf yet."
        }}
      </p>
      <button
        v-if="!search"
        class="btn btn-success btn-retro"
        v-b-modal.game-modal
      >
        + ADD YOUR FIRST GAME
      </button>
      <button v-else class="btn btn-success btn-retro" @click="search = ''">
        CLEAR SEARCH
      </button>
    </div>

    <!-- Games table — arcade cabinet display -->
    <div v-else class="card cabinet mb-4">
      <table class="table table-hover mb-0">
        <thead>
          <tr>
            <th scope="col" class="th-sort" @click="setSort('title')">
              ► TITLE {{ sortGlyph("title") }}
            </th>
            <th scope="col" class="th-sort" @click="setSort('genre')">
              GENRE {{ sortGlyph("genre") }}
            </th>
            <th
              scope="col"
              class="text-center th-sort"
              @click="setSort('played')"
            >
              STATUS {{ sortGlyph("played") }}
            </th>
            <th scope="col" class="text-right">CTRL</th>
          </tr>
        </thead>
        <TransitionGroup tag="tbody" name="row">
          <tr v-for="game in filtered" :key="game.id">
            <td class="title-cell">
              <span class="cursor">►</span>
              <img
                v-if="game.cover_url"
                :src="game.cover_url"
                class="cover-thumb"
                :alt="`${game.title} cover`"
                @error="onCoverError($event)"
              />
              <span v-else class="cover-thumb cover-placeholder">🎮</span>
              <strong>{{ game.title }}</strong>
            </td>
            <td>
              <span class="badge badge-genre" :style="genreStyle(game.genre)">
                {{ game.genre }}
              </span>
            </td>
            <td class="text-center">
              <span
                class="badge badge-retro"
                :class="game.played ? 'badge-cleared' : 'badge-new'"
              >
                {{ game.played ? "✓ CLEARED" : "NEW GAME" }}
              </span>
            </td>
            <td class="text-right">
              <div class="btn-group" role="group">
                <button
                  class="btn btn-info btn-sm"
                  @click="editGame(game)"
                  v-b-modal.game-update-modal
                >
                  EDIT
                </button>
                <button
                  class="btn btn-danger btn-sm"
                  @click="onDelete(game.id)"
                >
                  DEL
                </button>
              </div>
            </td>
          </tr>
        </TransitionGroup>
      </table>
    </div>

    <!-- Footer -->
    <footer class="app-footer text-center">
      <span class="footer-blink">●</span>
      &nbsp;BUILT WITH VUE 3 · FLASK · DOCKER · RENDER&nbsp;
      <span class="footer-blink">●</span>
      <div class="footer-sub">© {{ year }} · GAME OVER</div>
    </footer>

    <!-- Add modal -->
    <b-modal
      ref="addGameModal"
      id="game-modal"
      title="Insert New Cartridge"
      hide-footer
      @shown="onModalShown"
    >
      <b-form @submit="onSubmit" @reset="onReset" class="w100">
        <b-form-group class="mb-3" label="Title:" label-for="form-title-input">
          <b-form-input
            id="form-title-input"
            type="text"
            v-model="addGameForm.title"
            required
            placeholder="e.g. Hades"
          />
        </b-form-group>

        <b-form-group class="mb-3" label="Genre:" label-for="form-genre-input">
          <b-form-input
            id="form-genre-input"
            type="text"
            v-model="addGameForm.genre"
            required
            placeholder="e.g. roguelike"
          />
        </b-form-group>

        <b-form-group
          class="mb-3"
          label="Cover URL (optional):"
          label-for="form-cover-input"
        >
          <b-form-input
            id="form-cover-input"
            type="url"
            v-model="addGameForm.cover_url"
            placeholder="https://…/cover.png"
          />
        </b-form-group>

        <b-form-group class="mb-3">
          <label class="check-row">
            <input v-model="addGameForm.played" type="checkbox" />
            <span>Already played</span>
          </label>
        </b-form-group>

        <div class="d-flex justify-content-end">
          <b-button type="reset" variant="outline-secondary" class="mr-2">
            Cancel
          </b-button>
          <b-button type="submit" variant="primary">Insert Cart</b-button>
        </div>
      </b-form>
    </b-modal>

    <!-- Edit modal -->
    <b-modal
      ref="editGameModal"
      id="game-update-modal"
      title="Update Cartridge"
      hide-footer
      @shown="onModalShown"
    >
      <b-form @submit="onSubmitUpdate" @reset="onCancelUpdate" class="w100">
        <b-form-group
          class="mb-3"
          label="Title:"
          label-for="form-title-edit-input"
        >
          <b-form-input
            id="form-title-edit-input"
            type="text"
            v-model="editGameForm.title"
            required
          />
        </b-form-group>

        <b-form-group
          class="mb-3"
          label="Genre:"
          label-for="form-title-edit-genre"
        >
          <b-form-input
            id="form-title-edit-genre"
            type="text"
            v-model="editGameForm.genre"
            required
          />
        </b-form-group>

        <b-form-group
          class="mb-3"
          label="Cover URL (optional):"
          label-for="form-cover-edit-input"
        >
          <b-form-input
            id="form-cover-edit-input"
            type="url"
            v-model="editGameForm.cover_url"
            placeholder="https://…/cover.png"
          />
        </b-form-group>

        <b-form-group class="mb-3">
          <label class="check-row">
            <input v-model="editGameForm.played" type="checkbox" />
            <span>Already played</span>
          </label>
        </b-form-group>

        <div class="d-flex justify-content-end">
          <b-button type="reset" variant="outline-secondary" class="mr-2">
            Cancel
          </b-button>
          <b-button type="submit" variant="primary">Save Changes</b-button>
        </div>
      </b-form>
    </b-modal>

    <!-- Help overlay (keyboard shortcuts) -->
    <Transition name="fade">
      <div
        v-if="showHelp"
        class="help-overlay"
        @click.self="showHelp = false"
        @keydown.esc="showHelp = false"
      >
        <div class="help-panel">
          <h2 class="help-title">KEYBOARD SHORTCUTS</h2>
          <table class="help-table">
            <tr>
              <td><kbd>A</kbd></td>
              <td>Add a new cart</td>
            </tr>
            <tr>
              <td><kbd>/</kbd></td>
              <td>Focus search</td>
            </tr>
            <tr>
              <td><kbd>Esc</kbd></td>
              <td>Close modal / clear search</td>
            </tr>
            <tr>
              <td><kbd>M</kbd></td>
              <td>Toggle sound</td>
            </tr>
            <tr>
              <td><kbd>?</kbd></td>
              <td>Toggle this help</td>
            </tr>
            <tr>
              <td>
                <kbd>↑</kbd><kbd>↑</kbd><kbd>↓</kbd><kbd>↓</kbd><kbd>←</kbd>
                <kbd>→</kbd><kbd>←</kbd><kbd>→</kbd><kbd>B</kbd><kbd>A</kbd>
              </td>
              <td>You know what.</td>
            </tr>
          </table>
          <button class="btn btn-primary btn-retro" @click="showHelp = false">
            CLOSE
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, computed, onMounted, onBeforeUnmount, nextTick } from "vue";
import { useSounds } from "@/composables/useSounds";

const API_BASE = process.env.VUE_APP_API_URL || "http://localhost:5050";
const { play, muted, toggleMute } = useSounds();

// ===== state =====
const games = ref([]);
const search = ref("");
const sortKey = ref("");
const sortDir = ref(1);
const showHelp = ref(false);
const konamiActive = ref(false);
const message = ref("");
const showMessage = ref(false);

const addGameForm = ref({ title: "", genre: "", played: false, cover_url: "" });
const editGameForm = ref({
  id: "",
  title: "",
  genre: "",
  played: false,
  cover_url: "",
});
const addGameModal = ref(null);
const editGameModal = ref(null);
const searchInput = ref(null);

// ===== computed =====
const playedCount = computed(() => games.value.filter((g) => g.played).length);
const todoCount = computed(() => games.value.filter((g) => !g.played).length);
const year = computed(() => new Date().getFullYear());

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase();
  let list = q
    ? games.value.filter(
        (g) =>
          g.title.toLowerCase().includes(q) ||
          (g.genre || "").toLowerCase().includes(q)
      )
    : [...games.value];

  if (sortKey.value) {
    const k = sortKey.value;
    const dir = sortDir.value;
    list.sort((a, b) => {
      const av = a[k];
      const bv = b[k];
      if (typeof av === "boolean") return (bv - av) * dir;
      return String(av).localeCompare(String(bv)) * dir;
    });
  }
  return list;
});

// ===== utils =====
const pad = (n) => String(n).padStart(2, "0");

const sortGlyph = (key) => {
  if (sortKey.value !== key) return "";
  return sortDir.value === 1 ? "▲" : "▼";
};

const setSort = (key) => {
  if (sortKey.value === key) {
    sortDir.value = -sortDir.value;
  } else {
    sortKey.value = key;
    sortDir.value = 1;
  }
  play("blip");
};

// Deterministic neon palette per genre — same genre always gets the same color.
const GENRE_PALETTE = [
  { fg: "#00e0ff", bg: "#0a1a2e" }, // cyan
  { fg: "#ff2d95", bg: "#2e0a1f" }, // pink
  { fg: "#ffe945", bg: "#2e2a0a" }, // yellow
  { fg: "#39ff7d", bg: "#0a2e1a" }, // green
  { fg: "#a259ff", bg: "#1a0a2e" }, // purple
  { fg: "#ff9148", bg: "#2e1a0a" }, // orange
];
const hashStr = (s) => {
  let h = 0;
  for (let i = 0; i < s.length; i++) {
    h = (h << 5) - h + s.charCodeAt(i);
    h |= 0;
  }
  return Math.abs(h);
};
const genreStyle = (genre) => {
  const p = GENRE_PALETTE[hashStr(genre || "") % GENRE_PALETTE.length];
  return {
    background: p.bg,
    color: p.fg,
    border: `1px solid ${p.fg}`,
    boxShadow: `0 0 6px ${p.fg}33`,
  };
};

const onCoverError = (e) => {
  // If the URL 404s or CORS-blocks, swap in the placeholder glyph.
  const el = e.target;
  el.style.display = "none";
};

const onModalShown = () => {
  // Focus the first input when a modal opens.
  nextTick(() => {
    const first = document.querySelector(".modal.show input");
    if (first) first.focus();
  });
};

// ===== API =====
const getGames = async () => {
  try {
    const res = await axios.get(`${API_BASE}/games`);
    games.value = res.data.games;
  } catch (err) {
    console.error(err);
  }
};

let toastTimer = null;
const flash = (text) => {
  message.value = text;
  showMessage.value = true;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (showMessage.value = false), 3000);
};

const addGame = (payload) => {
  axios
    .post(`${API_BASE}/games`, payload)
    .then(() => {
      getGames();
      flash("Game added to your library");
      play("powerup");
    })
    .catch((err) => {
      console.log(err);
      getGames();
    });
};

const updateGame = (payload, gameID) => {
  axios
    .put(`${API_BASE}/games/${gameID}`, payload)
    .then(() => {
      getGames();
      flash("Game updated");
      play(payload.played ? "success" : "blip");
    })
    .catch((err) => {
      console.log(err);
      getGames();
    });
};

const onDelete = (gameID) => {
  axios
    .delete(`${API_BASE}/games/${gameID}`)
    .then(() => {
      getGames();
      flash("Game removed");
      play("zap");
    })
    .catch((err) => {
      console.log(err);
      getGames();
    });
};

const onSubmit = (e) => {
  e.preventDefault();
  addGameModal.value.hide();
  const payload = { ...addGameForm.value, played: !!addGameForm.value.played };
  addGame(payload);
  initForm();
};

const onSubmitUpdate = (e) => {
  e.preventDefault();
  editGameModal.value.hide();
  const { id, ...payload } = editGameForm.value;
  updateGame({ ...payload, played: !!payload.played }, id);
  initForm();
};

const onReset = (e) => {
  e.preventDefault();
  addGameModal.value.hide();
  initForm();
};

const onCancelUpdate = (e) => {
  e.preventDefault();
  editGameModal.value.hide();
  initForm();
};

const editGame = (game) => {
  editGameForm.value = { ...game };
};

const initForm = () => {
  addGameForm.value = { title: "", genre: "", played: false, cover_url: "" };
  editGameForm.value = {
    id: "",
    title: "",
    genre: "",
    played: false,
    cover_url: "",
  };
};

const onToggleMute = () => {
  toggleMute();
  if (!muted.value) play("blip");
};

// ===== keyboard shortcuts =====
const KONAMI = [
  "ArrowUp",
  "ArrowUp",
  "ArrowDown",
  "ArrowDown",
  "ArrowLeft",
  "ArrowRight",
  "ArrowLeft",
  "ArrowRight",
  "b",
  "a",
];
let konamiIdx = 0;

const isTypingTarget = (el) => {
  if (!el) return false;
  const tag = el.tagName;
  return tag === "INPUT" || tag === "TEXTAREA" || el.isContentEditable;
};

const triggerKonami = () => {
  konamiActive.value = true;
  play("konami");
  flash("⬆ 30 LIVES UNLOCKED — PALETTE INVERSION ENGAGED ⬆");
  setTimeout(() => (konamiActive.value = false), 10_000);
};

const onKey = (e) => {
  // Konami code listens everywhere (even while typing)
  if (e.key === KONAMI[konamiIdx]) {
    konamiIdx++;
    if (konamiIdx === KONAMI.length) {
      konamiIdx = 0;
      triggerKonami();
      return;
    }
  } else if (e.key !== KONAMI[0]) {
    konamiIdx = 0;
  }

  // Other shortcuts: skip when typing
  if (isTypingTarget(e.target)) {
    if (e.key === "Escape") {
      if (showHelp.value) showHelp.value = false;
    }
    return;
  }

  if (e.key === "a" || e.key === "A") {
    e.preventDefault();
    document.querySelector('[data-bs-target="#game-modal"]')?.click();
    // Fallback: trigger the modal via bv-modal API by clicking the toolbar btn
    document
      .querySelector(".btn.btn-primary.btn-retro")
      ?.dispatchEvent(new MouseEvent("click", { bubbles: true }));
  } else if (e.key === "/") {
    e.preventDefault();
    searchInput.value?.focus();
  } else if (e.key === "?") {
    e.preventDefault();
    showHelp.value = !showHelp.value;
  } else if (e.key === "m" || e.key === "M") {
    e.preventDefault();
    onToggleMute();
  } else if (e.key === "Escape") {
    if (showHelp.value) showHelp.value = false;
  }
};

onMounted(() => {
  getGames();
  window.addEventListener("keydown", onKey);
  // Play the coin jingle on first user interaction (autoplay policy).
  const onFirstClick = () => {
    play("coin");
    window.removeEventListener("click", onFirstClick);
  };
  window.addEventListener("click", onFirstClick);
});

onBeforeUnmount(() => {
  window.removeEventListener("keydown", onKey);
});
</script>

<style scoped>
/* ===== RETRO ARCADE PALETTE =====
   Neon pink:    #ff2d95
   Neon cyan:    #00e0ff
   Neon yellow:  #ffe945
   Neon green:   #39ff7d
   Neon purple:  #a259ff
   Cabinet dark: #0c0c1a
*/

.container {
  max-width: 960px;
}

/* ============ HERO ============ */
.hero {
  position: relative;
  background:
    radial-gradient(
      circle at 30% 20%,
      rgba(255, 45, 149, 0.35) 0%,
      transparent 60%
    ),
    radial-gradient(
      circle at 70% 80%,
      rgba(0, 224, 255, 0.3) 0%,
      transparent 60%
    ),
    linear-gradient(180deg, #1a0033 0%, #0c0c1a 100%);
  color: #fff;
  padding: 2.5rem 2rem 2rem;
  border-radius: 12px;
  border: 3px solid #000;
  text-align: center;
  overflow: hidden;
  box-shadow: 6px 6px 0 #000;
}

.hero::before {
  content: "";
  position: absolute;
  inset: 0;
  background-image: repeating-linear-gradient(
    180deg,
    rgba(0, 0, 0, 0) 0px,
    rgba(0, 0, 0, 0) 2px,
    rgba(0, 0, 0, 0.18) 2px,
    rgba(0, 0, 0, 0.18) 4px
  );
  pointer-events: none;
}

.hero::after {
  content: "";
  position: absolute;
  inset: 0;
  box-shadow: inset 0 0 80px rgba(0, 0, 0, 0.7);
  pointer-events: none;
}

.hero > * {
  position: relative;
  z-index: 1;
}

.hero-mute,
.hero-help {
  position: absolute;
  top: 12px;
  z-index: 2;
  background: rgba(0, 0, 0, 0.5);
  border: 2px solid #00e0ff;
  border-radius: 6px;
  color: #00e0ff;
  width: 36px;
  height: 36px;
  font-size: 1rem;
  font-family: "Press Start 2P", monospace;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: all 0.15s;
}
.hero-mute {
  right: 56px;
}
.hero-help {
  right: 12px;
}
.hero-mute:hover,
.hero-help:hover {
  background: #00e0ff;
  color: #000;
  transform: translateY(-1px);
  box-shadow: 0 0 8px rgba(0, 224, 255, 0.6);
}

.hero-marquee {
  font-family: "Press Start 2P", monospace;
  font-size: 0.6rem;
  color: #ffe945;
  letter-spacing: 0.2em;
  margin-bottom: 1.25rem;
}

.hero-coin {
  display: inline-block;
  color: #ffe945;
  margin: 0 0.5rem;
  animation: blink 1.2s infinite step-end;
}

.hero-title {
  font-family: "Press Start 2P", monospace;
  font-size: 1.75rem;
  color: #fff;
  margin: 0 0 0.75rem;
  letter-spacing: 0.05em;
  text-shadow:
    3px 3px 0 #ff2d95,
    6px 6px 0 #00e0ff;
}

.hero-sub {
  font-family: "VT323", monospace;
  font-size: 1.3rem;
  color: #39ff7d;
  margin: 0 0 1.25rem;
  letter-spacing: 0.05em;
  text-shadow: 0 0 8px rgba(57, 255, 125, 0.6);
}

.hero-controls {
  display: inline-flex;
  gap: 0.4rem;
  align-items: center;
  background: rgba(0, 0, 0, 0.4);
  border: 2px solid rgba(255, 255, 255, 0.15);
  border-radius: 6px;
  padding: 0.4rem 0.7rem;
}

.hero-key,
.hero-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  font-family: "Press Start 2P", monospace;
  font-size: 0.6rem;
  border-radius: 4px;
}

.hero-key {
  background: #2a2a3e;
  color: #00e0ff;
  border: 1px solid #00e0ff;
}

.hero-btn {
  background: #ff2d95;
  color: #fff;
  border: 1px solid #fff;
  box-shadow: 0 0 6px rgba(255, 45, 149, 0.7);
}

.hero-btn:nth-of-type(2) {
  background: #ffe945;
  color: #000;
  box-shadow: 0 0 6px rgba(255, 233, 69, 0.7);
}

/* ============ STATS ============ */
.stats-row .col {
  padding: 0 0.5rem;
}

.stat-card {
  background: #0c0c1a;
  border: 3px solid #000;
  border-radius: 10px;
  padding: 1rem;
  text-align: center;
  transition:
    transform 0.15s ease-out,
    box-shadow 0.15s ease-out;
  box-shadow: 4px 4px 0 #000;
}

.stat-card:hover {
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 #000;
}

.stat-card .stat-label {
  font-family: "Press Start 2P", monospace;
  font-size: 0.55rem;
  color: #a259ff;
  margin-bottom: 0.6rem;
  letter-spacing: 0.15em;
}

.stat-card .stat-number {
  font-family: "Press Start 2P", monospace;
  font-size: 1.6rem;
  line-height: 1;
  color: #ffe945;
  text-shadow: 0 0 8px rgba(255, 233, 69, 0.6);
}

.stat-played .stat-number {
  color: #39ff7d;
  text-shadow: 0 0 8px rgba(57, 255, 125, 0.6);
}
.stat-played .stat-label {
  color: #39ff7d;
}
.stat-todo .stat-number {
  color: #ff2d95;
  text-shadow: 0 0 8px rgba(255, 45, 149, 0.6);
}
.stat-todo .stat-label {
  color: #ff2d95;
}

/* ============ TOOLBAR + SEARCH ============ */
.toolbar {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  flex-wrap: wrap;
  padding: 0.5rem 0;
}

.search-wrap {
  position: relative;
  flex: 1 1 280px;
  min-width: 0;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #ffe945;
  font-family: "Press Start 2P", monospace;
  font-size: 0.6rem;
  pointer-events: none;
}

.search-input {
  width: 100%;
  background: #0c0c1a;
  border: 2px solid #00e0ff;
  border-radius: 6px;
  padding: 0.55rem 2.25rem 0.55rem 2rem;
  color: #fff;
  font-family: "Press Start 2P", monospace;
  font-size: 0.55rem;
  letter-spacing: 0.05em;
  height: 42px;
  box-shadow: 3px 3px 0 #000;
  transition: all 0.15s;
}

.search-input::placeholder {
  color: #6c6a7a;
}

.search-input:focus {
  outline: none;
  border-color: #ff2d95;
  box-shadow:
    3px 3px 0 #000,
    0 0 10px rgba(255, 45, 149, 0.5);
}

.search-clear {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: #ff2d95;
  font-size: 1.4rem;
  cursor: pointer;
  line-height: 1;
  padding: 0 0.5rem;
}

.toolbar-label {
  font-family: "VT323", monospace;
  font-size: 1.15rem;
  color: #6c757d;
  letter-spacing: 0.05em;
  white-space: nowrap;
}

.toolbar-label strong {
  color: #ff2d95;
}

.btn-retro {
  font-family: "Press Start 2P", monospace;
  font-size: 0.65rem;
  letter-spacing: 0.05em;
  padding: 0.75rem 1.1rem;
}

/* ============ TABLE ============ */
.cabinet {
  background: #0c0c1a;
  border: 3px solid #000;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 4px 4px 0 #000;
}

.cabinet .table {
  color: #cdd5e0;
  margin-bottom: 0;
  background: #0c0c1a;
}

.cabinet .table thead th {
  font-family: "Press Start 2P", monospace;
  font-size: 0.55rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: #00e0ff;
  background: #14142a;
  border-top: none;
  border-bottom: 2px solid #000;
  padding: 0.9rem 0.75rem;
}

.th-sort {
  cursor: pointer;
  user-select: none;
  transition: color 0.15s;
}
.th-sort:hover {
  color: #ffe945;
}

.cabinet .table tbody td {
  border-color: rgba(255, 255, 255, 0.06);
  vertical-align: middle;
  padding: 0.85rem 0.75rem;
}

.cursor {
  color: #ffe945;
  margin-right: 0.4rem;
  animation: blink 1s infinite step-end;
}

.title-cell {
  display: flex;
  align-items: center;
  gap: 0.6rem;
}

.title-cell strong {
  font-family: "VT323", monospace;
  font-size: 1.35rem;
  color: #fff;
  letter-spacing: 0.02em;
}

/* Cover thumbnail */
.cover-thumb {
  width: 36px;
  height: 36px;
  object-fit: cover;
  border-radius: 4px;
  border: 2px solid #00e0ff;
  background: #14142a;
  image-rendering: pixelated;
  flex-shrink: 0;
}

.cover-placeholder {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  border-color: rgba(0, 224, 255, 0.3);
}

/* ============ BADGES ============ */
.badge {
  font-family: "Press Start 2P", monospace;
  font-size: 0.55rem;
  padding: 0.55em 0.7em;
  letter-spacing: 0.08em;
  font-weight: 400;
  border-radius: 4px;
}

.badge-genre {
  text-transform: uppercase;
}

.badge-retro {
  border: 1px solid currentColor;
}

.badge-cleared {
  background: #14142a;
  color: #39ff7d;
  box-shadow: 0 0 6px rgba(57, 255, 125, 0.4);
}

.badge-new {
  background: #14142a;
  color: #ffe945;
  box-shadow: 0 0 6px rgba(255, 233, 69, 0.3);
}

.cabinet .btn-sm {
  font-family: "Press Start 2P", monospace;
  font-size: 0.55rem;
  letter-spacing: 0.05em;
  padding: 0.4rem 0.7rem;
}

/* ============ EMPTY STATE ============ */
.empty-state {
  background: #0c0c1a;
  border: 3px dashed #00e0ff;
  border-radius: 12px;
  padding: 3rem 2rem;
  text-align: center;
  color: #cdd5e0;
}

.empty-emoji {
  font-size: 3rem;
  margin-bottom: 0.75rem;
}

.empty-title {
  font-family: "Press Start 2P", monospace;
  font-size: 1.1rem;
  color: #ffe945;
  margin-bottom: 0.75rem;
  letter-spacing: 0.05em;
  animation: blink 1.2s infinite step-end;
}

.empty-sub {
  font-family: "VT323", monospace;
  font-size: 1.25rem;
  color: #cdd5e0;
  margin-bottom: 1.5rem;
}

/* ============ TRANSITIONS ============ */
.row-enter-active,
.row-leave-active {
  transition: all 0.25s ease-out;
}
.row-enter-from {
  opacity: 0;
  transform: translateY(-6px);
}
.row-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* ============ FOOTER ============ */
.app-footer {
  margin-top: 2rem;
  padding: 1.25rem 0;
  font-family: "Press Start 2P", monospace;
  font-size: 0.55rem;
  color: #6c757d;
  letter-spacing: 0.1em;
  border-top: 2px dashed rgba(0, 224, 255, 0.3);
}

.footer-blink {
  color: #ff2d95;
  animation: blink 0.8s infinite step-end;
}

.footer-sub {
  margin-top: 0.5rem;
  font-family: "VT323", monospace;
  font-size: 1.05rem;
  color: #a259ff;
  letter-spacing: 0.15em;
}

/* ============ HELP OVERLAY ============ */
.help-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.85);
  z-index: 1080;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1.5rem;
}

.help-panel {
  background: #0c0c1a;
  border: 3px solid #00e0ff;
  border-radius: 12px;
  box-shadow: 6px 6px 0 #000;
  padding: 2rem;
  max-width: 480px;
  width: 100%;
  color: #fff;
}

.help-title {
  font-family: "Press Start 2P", monospace;
  font-size: 0.85rem;
  color: #ffe945;
  margin-bottom: 1.5rem;
  letter-spacing: 0.08em;
  text-shadow: 2px 2px 0 #ff2d95;
  text-align: center;
}

.help-table {
  width: 100%;
  margin-bottom: 1.5rem;
  font-family: "VT323", monospace;
}

.help-table td {
  padding: 0.5rem 0.25rem;
  font-size: 1.1rem;
  color: #cdd5e0;
}

.help-table td:first-child {
  text-align: right;
  white-space: nowrap;
  padding-right: 1rem;
}

.help-table kbd {
  display: inline-block;
  background: #14142a;
  border: 1px solid #00e0ff;
  border-radius: 4px;
  padding: 0.2rem 0.45rem;
  margin: 0 0.1rem;
  font-family: "Press Start 2P", monospace;
  font-size: 0.55rem;
  color: #00e0ff;
}

.help-panel .btn {
  width: 100%;
}

.check-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0;
  cursor: pointer;
  font-family: "VT323", monospace;
  font-size: 1.25rem;
  color: #cdd5e0;
}

/* ============ ANIMATIONS ============ */
@keyframes blink {
  0%,
  49% {
    opacity: 1;
  }
  50%,
  100% {
    opacity: 0;
  }
}

/* ============ RESPONSIVE ============ */
@media (max-width: 575.98px) {
  .hero {
    padding: 1.75rem 1rem 1.25rem;
  }
  .hero-title {
    font-size: 1.1rem;
    text-shadow:
      2px 2px 0 #ff2d95,
      4px 4px 0 #00e0ff;
  }
  .hero-sub {
    font-size: 1.05rem;
  }
  .hero-mute,
  .hero-help {
    width: 30px;
    height: 30px;
    font-size: 0.85rem;
  }
  .hero-mute {
    right: 48px;
  }
  .stat-card .stat-number {
    font-size: 1.1rem;
  }
  .stat-card .stat-label {
    font-size: 0.5rem;
  }
  .toolbar {
    gap: 0.5rem;
  }
  .search-input {
    font-size: 0.5rem;
  }
}
</style>
