<template>
  <div class="container py-4">
    <!-- Hero — arcade marquee -->
    <header class="hero mb-4">
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

    <!-- Alert message -->
    <b-alert v-model="showMessage" variant="success" dismissible class="mb-3">
      <strong>✓</strong> {{ message }}
    </b-alert>

    <!-- Toolbar -->
    <div class="d-flex justify-content-between align-items-center mb-3 toolbar">
      <div class="toolbar-label">
        ► CARTRIDGE COUNT:
        <strong>{{ pad(games.length) }}</strong>
      </div>
      <button class="btn btn-primary btn-retro" v-b-modal.game-modal>
        + NEW CART
      </button>
    </div>

    <!-- Empty state -->
    <div v-if="games.length === 0" class="empty-state">
      <div class="empty-emoji">🕹️</div>
      <h3 class="empty-title">PRESS START</h3>
      <p class="empty-sub">No cartridges in the shelf yet.</p>
      <button class="btn btn-success btn-retro" v-b-modal.game-modal>
        + ADD YOUR FIRST GAME
      </button>
    </div>

    <!-- Games table — arcade cabinet display -->
    <div v-else class="card cabinet mb-4">
      <table class="table table-hover mb-0">
        <thead>
          <tr>
            <th scope="col">► TITLE</th>
            <th scope="col">GENRE</th>
            <th scope="col" class="text-center">STATUS</th>
            <th scope="col" class="text-right">CTRL</th>
          </tr>
        </thead>
        <TransitionGroup tag="tbody" name="row">
          <tr v-for="game in games" :key="game.id">
            <td class="title-cell">
              <span class="cursor">►</span>
              <strong>{{ game.title }}</strong>
            </td>
            <td>
              <span class="badge badge-genre">{{ game.genre }}</span>
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
                  @click="deleteGame(game.id)"
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
      title="Add a new game"
      hide-footer
    >
      <b-form @submit="onSubmit" @reset="onReset" class="w100">
        <b-form-group
          id="form-title-group"
          class="mb-4"
          label="Title:"
          label-for="form-title-input"
          floating
        >
          <b-form-input
            id="form-title-input"
            type="text"
            v-model="addGameForm.title"
            required
            placeholder="Enter Game"
          />
        </b-form-group>

        <b-form-group
          id="form-genre-group"
          class="mb-4"
          label="Genre:"
          label-for="form-genre-input"
          floating
        >
          <b-form-input
            id="form-genre-input"
            type="text"
            v-model="addGameForm.genre"
            required
            placeholder="Enter Genre"
          />
        </b-form-group>

        <b-form-group id="form-played-group" class="mb-4">
          <label class="check-row">
            <input
              id="form-checkbox"
              v-model="addGameForm.played"
              type="checkbox"
            />
            <span>Already played</span>
          </label>
        </b-form-group>

        <div class="d-flex justify-content-end">
          <b-button type="reset" variant="outline-secondary" class="mr-2">
            Cancel
          </b-button>
          <b-button type="submit" variant="primary">Add Game</b-button>
        </div>
      </b-form>
    </b-modal>

    <!-- Edit modal -->
    <b-modal
      ref="editGameModal"
      id="game-update-modal"
      title="Update the game"
      hide-footer
    >
      <b-form @submit="onSubmitUpdate" @reset="onCancelUpdate" class="w100">
        <b-form-group
          id="form-title-edit-group"
          class="mb-4"
          label="Title:"
          label-for="form-title-edit-input"
          floating
        >
          <b-form-input
            id="form-title-edit-input"
            type="text"
            v-model="editGameForm.title"
            required
            placeholder="Enter Game"
          />
        </b-form-group>

        <b-form-group
          id="form-genre-edit-group"
          class="mb-4"
          label="Genre:"
          label-for="form-title-edit-genre"
          floating
        >
          <b-form-input
            id="form-title-edit-genre"
            type="text"
            v-model="editGameForm.genre"
            required
            placeholder="Enter Genre"
          />
        </b-form-group>

        <b-form-group id="form-played-edit-group" class="mb-4">
          <label class="check-row">
            <input
              id="form-edit-checkbox"
              v-model="editGameForm.played"
              type="checkbox"
            />
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
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, computed, onMounted } from "vue";

const API_BASE = process.env.VUE_APP_API_URL || "http://localhost:5050";

const games = ref([]);
const addGameForm = ref({
  title: "",
  genre: "",
  played: false,
});
const editGameForm = ref({
  title: "",
  genre: "",
  played: false,
});

const addGameModal = ref(null);
const editGameModal = ref(null);

const message = ref("");
const showMessage = ref(false);

const playedCount = computed(() => games.value.filter((g) => g.played).length);
const todoCount = computed(() => games.value.filter((g) => !g.played).length);
const year = computed(() => new Date().getFullYear());

// Pad numbers to 2 digits for that arcade high-score look.
const pad = (n) => String(n).padStart(2, "0");

let toastTimer = null;
const flash = (text) => {
  message.value = text;
  showMessage.value = true;
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => (showMessage.value = false), 3000);
};

// GET function
const getGames = () => {
  axios
    .get(`${API_BASE}/games`)
    .then((res) => (games.value = res.data.games))
    .catch((err) => console.log(err));
};

// POST function
const addGame = (payload) => {
  axios
    .post(`${API_BASE}/games`, payload)
    .then(() => {
      getGames();
      flash("Game added to your library");
    })
    .catch((err) => {
      console.log(err);
      getGames();
    });
};

// PUT function
const updateGame = (payload, gameID) => {
  axios
    .put(`${API_BASE}/games/${gameID}`, payload)
    .then(() => {
      getGames();
      flash("Game updated");
    })
    .catch((err) => {
      console.log(err);
      getGames();
    });
};

const deleteGame = (gameID) => {
  axios
    .delete(`${API_BASE}/games/${gameID}`)
    .then(() => {
      getGames();
      flash("Game removed");
    })
    .catch((err) => {
      console.log(err);
      getGames();
    });
};

const onSubmit = (e) => {
  e.preventDefault();
  addGameModal.value.hide();

  const payload = {
    title: addGameForm.value.title,
    genre: addGameForm.value.genre,
    played: addGameForm.value.played ? true : false,
  };

  addGame(payload);
  initForm();
};

const onSubmitUpdate = (e) => {
  e.preventDefault();
  editGameModal.value.hide();

  const payload = {
    title: editGameForm.value.title,
    genre: editGameForm.value.genre,
    played: editGameForm.value.played ? true : false,
  };

  updateGame(payload, editGameForm.value.id);
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
  getGames();
};

const editGame = (game) => {
  editGameForm.value = { ...game };
};

const initForm = () => {
  addGameForm.value = { title: "", genre: "", played: false };
  editGameForm.value = { id: "", title: "", genre: "", played: false };
};

onMounted(getGames);
</script>

<style scoped>
/* ===== RETRO ARCADE PALETTE =====
   Neon pink:    #ff2d95
   Neon cyan:    #00e0ff
   Neon yellow:  #ffe945
   Neon green:   #39ff7d
   Neon purple:  #a259ff
   Cabinet dark: #0c0c1a
   Phosphor mono font: 'Press Start 2P' (titles), 'VT323' (CRT text)
*/

.container {
  max-width: 900px;
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

/* Scanlines */
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

/* CRT glow vignette */
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

/* ============ TOOLBAR ============ */
.toolbar {
  padding: 0.5rem 0;
}

.toolbar-label {
  font-family: "VT323", monospace;
  font-size: 1.15rem;
  color: #6c757d;
  letter-spacing: 0.05em;
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

.cabinet .table tbody td {
  border-color: rgba(255, 255, 255, 0.06);
  vertical-align: middle;
  padding: 0.85rem 0.75rem;
}

.cabinet .table tbody tr:hover {
  background: rgba(255, 45, 149, 0.08);
}

.cursor {
  color: #ffe945;
  margin-right: 0.4rem;
  animation: blink 1s infinite step-end;
}

.title-cell strong {
  font-family: "VT323", monospace;
  font-size: 1.35rem;
  color: #fff;
  letter-spacing: 0.02em;
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
  background: #14142a;
  color: #00e0ff;
  border: 1px solid #00e0ff;
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

/* Action buttons inside table */
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

/* ============ ROW TRANSITIONS ============ */
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

/* ============ MODAL FORM ============ */
.check-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0;
  cursor: pointer;
  font-family: "VT323", monospace;
  font-size: 1.2rem;
}
.check-row input[type="checkbox"] {
  cursor: pointer;
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
  .stat-card .stat-number {
    font-size: 1.1rem;
  }
  .stat-card .stat-label {
    font-size: 0.5rem;
  }
}
</style>
