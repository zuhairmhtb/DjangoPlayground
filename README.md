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

```
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', '')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
origins = os.getenv('TRUSTED_ORIGINS', '').split(',')

if origins and len(origins) > 0 and origins[0] != '':
    CSRF_TRUSTED_ORIGINS = origins

    CORS_ALLOWED_ORIGINS = origins

CORS_ALLOW_CREDENTIALS = True
CSRF_COOKIE_SAMESITE = 'LAX'
CSRF_COOKIE_SECURE = not DEBUG

# CSRF_COOKIE_HTTPONLY=True
# Add allowed headers
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# Application definition

INSTALLED_APPS = [

    "daphne", # must be placed before django.contrib.staticfiles    
    'django.contrib.staticfiles',
    'corsheaders', # Manages CORS when interacting through a separate frontend
    'django_playground',
]

# Enable ASGI
WSGI_APPLICATION = 'django_playground.wsgi.application'
ASGI_APPLICATION = 'django_playground.asgi.application'

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'mydb'),
        'USER': os.getenv('POSTGRES_USER', 'postgres'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'postgres'),
        'HOST': os.getenv("POSTGRES_HOST", "localhost"),
        'PORT': int(os.getenv("POSTGRES_PORT", "5432")),
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'sass_processor.finders.CssFinder',
]

# SCSS settings
SASS_PROCESSOR_ROOT = STATIC_ROOT
SASS_PROCESSOR_ENABLED = True
SASS_PRECISION = 8
SASS_OUTPUT_STYLE = 'compressed'

# Compress settings
COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.rCSSMinFilter'
]

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
```

12. Create a folder called 'static' inside the app/ directory. It will contain all the static assets and css generated from our scss.

13. Rerun the docker compose file and start the application.

14. Check the browser to make sure that the application is running. Unless you change the .env file, the application should run on [http://localhost:8000/](http://localhost:8000/).

15. Go to the terminal of the running Django container. If you are using Docker Desktop, you can access the terminal using the GUI. To access it from a terminal, first fetch the hash of the running container by inspecting the list of running containers. The following command:

```
docker container ls
```
should display all the running containers. Note down the hash of your django container and run the following command:

```
docker exec -ti 5f28db17eda1 bash
```
Replace '5f28db17eda1' with hash ID of your container. To make sure that you are in the correct folder, after logging into your container, type 'ls' to see the list of current files. If manage.py exists in your current directory, you are in the correct folder. Run migration using the command:

```
python manage.py makemigrations
python manage.py migrate
```
If your migrations run successfully, your application is connected to the database. Otherwise, make sure that you provided the right database configuration in both your .env files (infrastructure and django). Also make sure that you have configured the external docker network correctly. You can view the list of existing networks using the command:

```
docker network ls
```

Finally, make sure that both your docker-compose files are correctly configured and point to the correct environment variables. One way to make sure that the django container can communicate with the database container is to first login to your django container using the 'exec' command provided above. Then do a ping to your database container to make sure that the containers can reach each other. To ping the database container, run the following command from inside your django container:

```
apt-get update
apt-get upgrade
apt-get install 
apt-get install iputils-ping
ping postgres
```
Here we are installing the iputils-ping package for Ubuntu so that we can do a ping test. In the last line we are doing a ping to the postgres container. In my docker-compose.development.yml file inside infrastructure/ folder, the name of my postgres container is 'postgres'. Replace this with the name that you provided for your container (if you have updated the docker-compose file).

```
services:

  postgres:
    image: postgres:16.4-alpine
    container_name: postgres-playground
```

If you receive a reply similar to the following:

```
64 bytes from postgres-playground.my-playground-network (172.22.0.2): icmp_seq=1 ttl=64 time=0.050 ms
```
Your network connection is working fine and both containers are up and running. This probably means that your environment variable configuration is incorrect or you have provided the name of a database that does not exist.

16. Create a superadmin user for your django application. Login to your container's terminal and run the following command from inside 'app/' folder (or wherever your manage.py file is inside the container):

```
python manage.py createsuperuser
```

Make sure that your superuser was created successfully by logging in from the admin panel. That's it! you have a running container ready for development and ready to be configured for deployment to production. You can see that with this approach we still have to perform about 16 manual tasks - each can be automated on its own. That is the plan! To automate the entire process. However, I am reluctant to automate the entire thing because as the number of abstractions increase the probability to forget the fundamentals by not being in touch with it becomes more likely.

This django application comes with a built-in scss compiler and a GraphQL library 'strawberry'. It is also configured to handle CORS and CSRF. The settings are available in settings.py and the authorized domains can be configured from .env file of the main django application. It also has daphne installed and asgi enabled to perform async operations. If you do not need these, you can selectively uninstall the redundant packages from inside your django container and update the requirements.txt file using 'pip freeze' command. Cheers!

## References

1. [Deploying Django with Docker](https://medium.com/powered-by-django/deploy-django-using-docker-compose-windows-3068f2d981c4)

2. [Authentication and authorization of Django with Keycloak](https://medium.com/@robertjosephk/setting-up-keycloak-in-django-with-django-allauth-cfc84fdbfee2)

3. [Debugging Django application running in docker](https://dev.to/ferkarchiloff/how-to-debug-django-inside-a-docker-container-with-vscode-4ef9)

4. [Debugging Django application running in docker 2](https://testdriven.io/blog/django-debugging-vs-code/)