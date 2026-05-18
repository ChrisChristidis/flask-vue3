# 🕹️ Games Library — Flask + Vue 3 + Docker

A tiny CRUD demo: a Vue 3 SPA backed by a Flask JSON API. Runs as two Docker
containers (frontend served by nginx, backend by Flask's dev server). Optional
MongoDB persistence is included for the "with DB" mode.

---

## Stack

**Backend** — Python 3.9, Flask, Flask-CORS, PyMongo
**Frontend** — Vue 3 (Vue CLI / webpack), Vue Router 4, Bootstrap 5, Bootstrap-Vue-Next, Axios
**Database** — In-memory list by default; MongoDB (local or Atlas) optional
**Runtime** — Docker + Docker Compose

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
│   │   ├── views/GamesView.vue # Single CRUD page
│   │   ├── router/             # Vue Router
│   │   ├── App.vue
│   │   └── main.js
│   ├── package.json
│   ├── vue.config.js
│   └── Dockerfile              # Multi-stage: node build → nginx serve
├── docker-compose.yml          # Active: no-db prod-style (5050 / 8080)
├── docker-compose-no-db.yml    # Dev mode (hot reload, ports 5000 / 8080)
├── docker-compose-with-db.yml  # Adds MongoDB service + envs
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

## Mode B — with MongoDB

Use this when you want games to persist across restarts.

1. **Switch the compose file.** Either run with `-f` or copy it over the default:
   ```bash
   cp docker-compose-with-db.yml docker-compose.yml
   ```

2. **Switch the backend entrypoint.** In `backend/Dockerfile`, change:
   ```dockerfile
   # CMD ["python", "main.py"]
   CMD ["python", "mainWithDB.py"]
   ```

3. **Create `.env`** at the repo root (gitignored):
   ```env
   MONGODB_URL=mongodb://christos:test1234@mongodb:27017/
   MONGO_INITDB_ROOT_USERNAME=christos
   MONGO_INITDB_ROOT_PASSWORD=<choose-a-strong-one>
   ```
   For MongoDB Atlas, use `mongodb+srv://<user>:<pass>@<cluster>.mongodb.net/`
   in `MONGODB_URL` and drop the `mongodb` service from compose if you don't
   need a local one.

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

| Var                  | Used by  | Default                  | Notes |
|----------------------|----------|--------------------------|-------|
| `VUE_APP_API_URL`    | frontend | `http://localhost:5050`  | Bake into the build (`docker build --build-arg` or env at `npm run build` time) |
| `MONGODB_URL`        | backend  | _(required for DB mode)_ | Atlas URL or `mongodb://user:pass@mongodb:27017/` |
| `MONGO_INITDB_ROOT_USERNAME` | mongo  | _(env-file)_     | Initial root user when first volume comes up |
| `MONGO_INITDB_ROOT_PASSWORD` | mongo  | _(env-file)_     | Same — set in `.env`, never commit |

---

## API surface

| Method | Path             | Body                                | Response                       |
|--------|------------------|-------------------------------------|--------------------------------|
| GET    | `/games`         | —                                   | `{ status, games: [...] }`     |
| POST   | `/games`         | `{ title, genre, played }`          | `{ status, message }`          |
| PUT    | `/games/<id>`    | `{ title, genre, played }`          | `{ status, message, games }`   |
| DELETE | `/games/<id>`    | —                                   | `{ status, message, games }`   |

CORS is wide-open (`*`) — fine for the tutorial, lock it down before any real
deploy.

---

## Common scripts

```bash
# Frontend
cd frontend
npm run serve      # dev server (hot reload)
npm run build      # production build into dist/
npm run lint       # eslint + prettier

# Backend
cd backend
python main.py            # in-memory mode
python mainWithDB.py      # MongoDB mode (needs MONGODB_URL)
```

---

## Deploying

See `HANDOFF.md` for a step-by-step Docker deploy guide (DigitalOcean, Fly.io,
or any VPS with Docker installed).
