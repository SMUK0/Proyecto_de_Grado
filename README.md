# 1) Clonar
cd $HOME\Desktop
git clone https://github.com/SMUK0/Proyecto_de_Grado.git
cd Proyecto_de_Grado

# 2) Backend
cd backend
py -3 -m venv .venv
.\.venv\Scripts\activate
if (Test-Path .\requirements.txt) { py -m pip install -r requirements.txt } `
else { py -m pip install "django~=5.2" djangorestframework django-cors-headers psycopg2-binary }

# — Opción Docker para Postgres —
docker run --name pg -e POSTGRES_PASSWORD=clave123 -p 5432:5432 -d postgres:16
docker exec -it pg psql -U postgres -c "CREATE DATABASE resol_db;"
docker exec -it pg psql -U postgres -c "CREATE USER resol_user WITH PASSWORD 'clave_segura';"
docker exec -it pg psql -U postgres -c "GRANT ALL PRIVILEGES ON DATABASE resol_db TO resol_user;"

# Migraciones y backend
python manage.py migrate
python manage.py runserver


# 3) Frontend
cd $HOME\Desktop\Proyecto_de_Grado\proyecto_de_grado
npm install
npm run dev
