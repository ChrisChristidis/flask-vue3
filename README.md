# 🕹️ Games Library — Flask + Vue 3 + Docker

A tiny CRUD demo with an **arcade-cabinet retro UI**: a Vue 3 SPA backed by a
Flask JSON API, deployed on Render as two Docker containers. Bootstrap 5
(Sketchy theme) provides the hand-drawn chassis; pixel fonts + neon CRT
palette do the retro lift on top.

**Live:**
- Frontend → https://flask-vue3-frontend.onrender.com
- Backend  → https://flask-vue3-backend.onrender.com/games

> Free Render tier — first hit after 15 min idle takes ~30 s to cold-start.

---

## Stack

**Backend** — Python 3.9, Flask, Flask-CORS, PyMongo (optional)
**Frontend** — Vue 3 (Vue CLI / webpack), Vue Router 4, Bootstrap 5, Bootstrap-Vue-Next, Axios
**Styling** — Bootswatch Sketchy theme + retro overrides (Press Start 2P, VT323, neon palette, CRT scanlines)
**Database** — In-memory list by default; MongoDB (local or Atlas) optional
**Runtime** — Docker + Docker Compose locally; Render (Docker) in production

---

## Repo layout

```
flask-vue3/
├── backend/                    # Flask API
│   ├── main.py                 # In-memory store (default entrypoint)
│   ├── mainWithDB.py           # MongoDB-backed variant
│   ├── requirements.txt
│   ├── Pipfile
│   └── Dockerfile
├── frontend/                   # Vue 3 SPA
│   ├── src/
│   │   ├── views/GamesView.vue # Single CRUD page (retro UI lives here)
│   │   ├── router/
│   │   ├── App.vue
│   │   └── main.js
│   ├── public/index.html       # Bootswatch + retro Google Fonts loaded here
│   ├── package.json
│   ├── vue.config.js
│   ├── nginx.conf.template     # envsubst template for $PORT
│   └── Dockerfile              # Multi-stage: node build → nginx serve
├── docker-compose.yml          # Active: no-db prod-style (5050 / 8080)
├── docker-compose-no-db.yml    # Dev mode (hot reload, ports 5000 / 8080)
├── docker-compose-with-db.yml  # Adds MongoDB service + envs
├── render.yaml                 # Render Blueprint: two-service auto-deploy
└── README.md
```

---

## Quick start (Docker, no DB)

```bash
docker compose up --build
```

- Frontend → http://localhost:8080
- Backend  → http://localhost:5050/games

That's it. The default `docker-compose.yml` builds both images and starts them
with the in-memory game list. State resets every time the backend restarts.

### Stop / clean up

```bash
docker compose down            # stop + remove containers
docker compose down -v         # also drop named volumes (e.g. mongodb_data)
```

---

## The retro UI

The look is deliberately layered on top of Bootswatch Sketchy (whose
hand-drawn black borders give the "arcade cabinet" chassis). The retro lift
comes from a small set of overrides in [GamesView.vue](frontend/src/views/GamesView.vue):

- **Press Start 2P** — the iconic 8-bit arcade font, used for titles, badges,
  buttons, footer.
- **VT323** — CRT-monitor font, used for body copy and game titles.
- **Neon palette** — pink `#ff2d95`, cyan `#00e0ff`, yellow `#ffe945`,
  green `#39ff7d`, purple `#a259ff` on cabinet-dark `#0c0c1a`.
- **CRT scanlines + vignette** on the hero (pure CSS).
- **Blinking marquee, blinking cursor, blinking footer dots** — `@keyframes blink`.
- **Hard "Sketchy" drop shadows** (no blur, offset 4–6 px) on stats and cabinet.

Both Google Fonts and the Bootswatch CDN are loaded from `public/index.html`
with `preconnect` for faster paint.

To change the palette, edit the `/* ===== RETRO ARCADE PALETTE =====` block at
the top of the `<style>` in `GamesView.vue`.

---

## Mode B — with MongoDB

Use this when you want games to persist across restarts.

1. **Switch the compose file:**
   ```bash
   cp docker-compose-with-db.yml docker-compose.yml
   ```

2. **Switch the backend entrypoint.** In `backend/Dockerfile`, change:
   ```dockerfile
   # CMD ["python", "main.py"]
   CMD ["python", "mainWithDB.py"]
   ```

3. **Create `.env`** at the repo root (gitignored — see `.env.example`):
   ```env
   MONGODB_URL=mongodb://user:pass@mongodb:27017/
   MONGO_INITDB_ROOT_USERNAME=user
   MONGO_INITDB_ROOT_PASSWORD=<choose-a-strong-one>
   ```
   For MongoDB Atlas, use `mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/`
   in `MONGODB_URL` and drop the `mongodb` service from compose.

4. **Rebuild & up:**
   ```bash
   docker compose up --build
   ```

---

## Mode C — dev mode (hot reload, no Docker)

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py                 # serves on http://localhost:5000
```

### Frontend
```bash
cd frontend
npm install
npm run serve                  # http://localhost:8080
```

If you run the backend bare-metal on `:5000`, point the frontend at it:
```bash
VUE_APP_API_URL=http://localhost:5000 npm run serve
```

---

## Configuration

| Var | Used by | Default | Notes |
|---|---|---|---|
| `VUE_APP_API_URL` | frontend | `http://localhost:5050` | Baked into the bundle at build time via `Dockerfile ARG` |
| `CORS_ORIGINS` | backend | `*` | Comma-separated list; set to your frontend origin in prod |
| `PORT` | both | 5000 / 80 | Both services bind to `$PORT` (Render injects it) |
| `MONGODB_URL` | backend | _(required for DB mode)_ | Atlas URL or `mongodb://user:pass@mongodb:27017/` |
| `MONGO_INITDB_ROOT_USERNAME` | mongo | _(env-file)_ | Initial root user when volume comes up |
| `MONGO_INITDB_ROOT_PASSWORD` | mongo | _(env-file)_ | Set in `.env`, never commit |

---

## API surface

| Method | Path | Body | Response |
|---|---|---|---|
| GET | `/games` | — | `{ status, games: [...] }` |
| POST | `/games` | `{ title, genre, played }` | `{ status, message }` |
| PUT | `/games/<id>` | `{ title, genre, played }` | `{ status, message, games }` |
| DELETE | `/games/<id>` | — | `{ status, message, games }` |

---

## Common scripts

```bash
# Frontend
cd frontend
npm run serve      # dev server (hot reload)
npm run build      # production build into dist/
npm run lint       # eslint + prettier (lint-on-build is disabled in vue.config.js)

# Backend
cd backend
python main.py            # in-memory mode
python mainWithDB.py      # MongoDB mode (needs MONGODB_URL)
```

---

## Deploying

Already live on Render — the [`render.yaml`](render.yaml) Blueprint defines both
services. Push to `main` → Render auto-rebuilds and redeploys both containers.

See `HANDOFF.md` for the original deploy walkthrough and notes on upgrading
free tier to always-on, swapping to Mongo, or wiring a custom domain.
