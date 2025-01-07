### INSTALLATION

- Clone This Repository
```
git clone https://github.com/VyacheslavShrot/ManagingStrategiesService.git
```

- Create an .env File at the Project Level
```
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
```

- Run Database and Create Database Name
```
docker-compose up -d postgres

docker exec -it postgres bash

psql -U $POSTGRES_USER -h postgres -c 'CREATE DATABASE default_name;'
```

### START

- Run Application -> WSGI
```
docker-compose up -d backend
```
