# 🕹️ This is a Games Library app. 🕹️

## Technologies / Libraries

Database:

- MongoDB

Backend:

- Python 3.9.6
- flask
- flask-cors
- pymongo

Frontend:

- Vue 3.2.13
- Bootstrap 5.3.3
- Bootswatch 4.5.2 Sketchy Theme

Docker

## Run the app

### Modify your docker-compose.yml

If you have already set up your mongodb:

- Copy docker-compose-with-db.yml to docker-compose.yml.
- Change docker-compose.yml variables MONGODB_URL, MONGO_INITDB_ROOT_USERNAME, MONGO_INITDB_ROOT_PASSWORD, with your credentials.
- Change /backend/Dockerfile CMD ["python", "main.py"] with CMD ["python", "mainWithDB.py"].
  Else:
- Copy docker-compose-no-db.yml to docker-compose.yml.

### Run the docker

```
docker compose up --build
```

### backend

### Change directory

```
cd ./backend
```

### Run the server

```
pipenv run python main.py
```

### frontend

### Change directory

```
cd ./frontend
```

### Project setup

```
npm install
```

### Compiles and hot-reloads for development

```
npm run serve
```

### Compiles and minifies for production

```
npm run build
```

### Lints and fixes files

```
npm run lint
```
