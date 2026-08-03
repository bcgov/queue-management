# Back-end Development Guide

Sync the project environment

```
uv sync --group dev
```

Generate new migrations

```bash
uv run python manage.py db migrate
uv run python manage.py db upgrade
```
