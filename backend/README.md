# Hotel Reservation Backend Module <Django Framework>

## Getting started

## Install

### Setup virtual environment

- At the backend folder run cmd
    ```sh
    python3 -m venv
  ```
- Execute follow CMD to active virtual environment
    ```shell
    source venv/bin/activate
    ```

### Setup dependencies packages

- Execute follow CMD to install dependencies packages
    ```shell
    pip3 install -r requirements.txt
    ```

### Migrations data

- Default we using SQLite to storage data
- Go to backend/app directory
    ```shell
        pip3 install -r requirements.txt
    ```
- Execute follow CMD to migrations data

```shell
python3 manage.py migrate
```

- We have poll application example, run follow CMD to

```shell
python3 manage.py makemigrations polls
python3 manage.py sqlmigrate polls 0001
python3 manage.py migrate
```

### Start backend webserver

- Run follow CMD to start webserver
    ```shell
    python3 manage.py runserver 
    ```

- We can also custom port for application via CMD:
    ```shell
    python3 manage.py runserver 0.0.0.0:8000 <8000: PORT>
    ```

- Now, we can access our application via URL:
    ```shell
    - http://localhost:8000/
    - http://localhost:8000/polls/
    - http://localhost:8000/admin
    ```

### Creating an admin user

- Run the following command:
    ```shell
    python3 manage.py createsuperuser
    ```
        