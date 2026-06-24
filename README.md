# Backend Django

API REST con Django + Django REST Framework.

Los modelos son **no gestionados** (`managed = False`): Django no crea ni migra las tablas,
las lee desde el esquema que ya aplicaste con `database/schema.sql`. Por eso **no hace falta
`migrate`** para las tablas del negocio.

## Requisitos

- Python 3.12

## Instalación

```bash
cd backtest

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env             # ajusta credenciales si es necesario
```

## Ejecución

```bash
python manage.py runserver 0.0.0.0:8000
```

El API queda en `http://localhost:8000/api`.

## Variables de entorno (`.env`)

| Variable               | Descripción                                       |
|------------------------|---------------------------------------------------|
| `DJANGO_SECRET_KEY`    | Clave de Django                                   |
| `DJANGO_DEBUG`         | `true` / `false`                                  |
| `DJANGO_ALLOWED_HOSTS` | Hosts permitidos, separados por coma              |
| `JWT_SECRET`           | Secreto de firma del JWT                          |
| `JWT_EXPIRATION_HOURS` | Vigencia del token                                |
| `DB_HOST` … `DB_PASSWORD` | Conexión a PostgreSQL                          |

En desarrollo, los defaults del código ya apuntan a un Postgres local, así que la app
corre incluso sin `.env`. El `.env` no se versiona (está en `.gitignore`). Más sobre el
manejo de secretos en [`SECRETS.md`](../SECRETS.md).

## Probar con curl

```bash
# Login
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"admin@demo.com","password":"Admin123!"}' | python -c "import sys,json;print(json.load(sys.stdin)['token'])")

# Listado con filtros y paginación
curl -s "http://localhost:8000/api/users?search=lucia&page=1&pageSize=10" \
  -H "Authorization: Bearer $TOKEN"

# Alta
curl -s -X POST http://localhost:8000/api/users \
  -H "Authorization: Bearer $TOKEN" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Alexis García","email":"nuevo@example.com","age":30,"country":"México"}'
```
