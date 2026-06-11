# Notes App — Flask + MySQL

Просто уеб приложение за бележки, изградено с Flask и MySQL, контейнеризирано с Docker.

## Структура на проекта

```
app/
├── app.py                  # Flask уеб приложение
├── templates/
│   └── index.html          # HTML фронтенд
├── requirements.txt        # Python зависимости
├── Dockerfile              # Docker образ за уеб услугата
├── compose.yml             # Docker Compose конфигурация
├── init.sql                # SQL скрипт за инициализация на базата данни
└── README.md
```

## Компоненти

### web — Flask приложение
- **Образ:** изграден от `Dockerfile` (базиран на `python:3.9-slim`)
- **Порт:** `5000`
- Обслужва HTML страница, от която могат да се добавят и изтриват бележки
- Свързва се с MySQL базата данни чрез environment променливи

### db — MySQL база данни
- **Образ:** `mysql:8.0` (официален образ от Docker Hub)
- Съхранява бележките в таблица `notes`
- При първо стартиране изпълнява `init.sql`, за да създаде таблицата
- Има healthcheck — `web` услугата изчаква базата да е готова

## Комуникация между услугите

`web` се свързва с `db` по вътрешната Docker мрежа, използвайки hostname `db` (името на услугата в `compose.yml`). Credentials-ите се предават чрез environment променливи.

```
[Browser] → http://localhost:5000 → [web container] → db:3306 → [db container]
```

## Изграждане и стартиране

### Изисквания
- Docker Desktop (или Docker Engine + Docker Compose)

### Стартиране
```bash
docker compose up --build
```

Приложението ще е достъпно на [http://localhost:5000](http://localhost:5000).

### Спиране
```bash
docker compose down
```

За да изтриете и volume-а с данните:
```bash
docker compose down -v
```

## Docker Hub

Образът на уеб услугата е публикуван на Docker Hub:

```
docker pull kristiankostadinov14/notes-web
```

За да изградите и публикувате образа ръчно:
```bash
docker build -t kristiankostadinov14/notes-web .
docker push kristiankostadinov14/notes-web
```
