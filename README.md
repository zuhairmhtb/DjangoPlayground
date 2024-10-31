# Containerized Django Development

**Read the full article at [https://vip3rtech6069.com](https://vip3rtech6069.com).**


## Create a Django application within Docker.

1. Create a new folder in services/ where the Django application will reside. Let the name of the app is 'my_django_playground'.

2. Copy Dockerfile and requirements.txt file in the base directory.

3. Copy the docker-compose.*.yml files. Copy only the development if you just need one. I usually do it for both. Open the file and make the following changes:

- Rename the django container from:

```
container_name: django-playground
```

to your preferred name.

- Change the name of the network from:

```
networks:
  playground_network:
    driver: bridge
    name: my-playground-network
    external: true
```

to your preferred name. Update 

```
networks:
      - playground_network
```

section of the file to the new network name.

4. Copy the infrastructure folder as it contains the docker compose file to run a postgres database inside the same network. We will also run pgadmin as it provides a simple dashboard for quick GUI view of the database. Make  the following changes to the docker-compose file of the infrastructure:

- Update the name of the posgres and pgadmin containers to your preferred container name.

```
container_name: postgres-playground
container_name: pgadmin-playground
```

- Update path of the volume where your database will persist the data. 

```
volumes:
      - ./development/postgres/data:/var/lib/postgresql/data
```

5. Make sure your docker compose files are accompanied by the .env file. So, there is one for the postgres config and one for the django config. Make the following changes to the .env file:

- Update the name of the database that you want to use for your django app. You can do this if you do not want to create a new database using pgadmin. Update the pgadmin email and password that you want to use.

```
# File playgorund/.env
POSTGRES_DB=djangoplayground

# Pgadmin
PGADMIN_EMAIL="admin@playground.com"
PGADMIN_PASSWORD="admin123"
PGADMIN_LOCAL_PORT=80
```

```
# File playground/infrastructure/postgres/.env

DJANGO_ADMIN_DB_NAME=djangoplayground
```

6. Create the external docker network network using the command:

```
docker network create -d bridge my-playground-network
```

Replace the name of the network with preferred network name. This network will be used for the communication between database and the application.

7. Start the infrastrucure container by navigation to the playground/infeastructure/postgres/ folder using terminal.


8. Make sure that the database server has started and the default database was created. Use pgadmin to check that. pgadmin by default should be running on [http://localhost:5050](http://localhost:5050). When connecting to the database server make sure to set the host name same as the name of your postgres docker container which in this case is 'postgres'.

```
services:

  postgres:
    image: postgres:16.4-alpine
    container_name: postgres-playground
```

Also make sure to use the correct username and password which in my case is also 'postgres'.

```
environment:
      POSTGRES_DB: ${POSTGRES_DB}
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
```


9. Run the following command using docker compose to create the django application.

```
docker-compose -f .\docker-compose.development.yml run django_admin django-admin startproject django_playground /app
```

10. Remove the temporary docker container created for email service once the django app files get copied over to the volume.

11. Update settings.py file to use the environment variables. Make sure to copy the secret key and update the environment file if you do not have a key in mind. You can use the settings.py in the app/ folder of this repository to copy the following information:

- Secret key
- Allowed hosts
- Debug Enabled
- Csrf trusted origins
- Cors allowed origins
- Cors allow credentials
- Csrf cookie samesite
- Csrf cookie secure
- Cors allow headers

All the above are present between line 20 and 58 in app/django_playground/settings.py file.

12. Rerun the docker compose file and start the application.



## References

1. [Deploying Django with Docker](https://medium.com/powered-by-django/deploy-django-using-docker-compose-windows-3068f2d981c4)

2. [Authentication and authorization of Django with Keycloak](https://medium.com/@robertjosephk/setting-up-keycloak-in-django-with-django-allauth-cfc84fdbfee2)

3. [Debugging Django application running in docker](https://dev.to/ferkarchiloff/how-to-debug-django-inside-a-docker-container-with-vscode-4ef9)

4. [Debugging Django application running in docker 2](https://testdriven.io/blog/django-debugging-vs-code/)