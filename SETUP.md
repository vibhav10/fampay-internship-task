### Installation

1. Clone the repository to your local machine:

   ```
   $ git clone https://github.com/vibhav10/fampay-internship-task
   ```

2. Navigate to the project directory and change into the backend directory:

   ```
   $ cd famapy-internship-task
   ```

3. Build and run the Docker containers:

   ```
   $ docker-compose up --build
   ```

4. Open your web browser and visit [http://localhost:8000/](http://localhost:8000/) to see the project in action.


5. (Optional) Create a superuser to access the admin interface:

   Log into the Django container:
   ```
   $ docker exec -it django-fampay  bash

   ```
    Then, create a superuser:
    ```
    $ python manage.py createsuperuser
    ```
    Follow the prompts to create a superuser account.



### Configuration

- Modify the project settings in `settings.py` as needed, such as database settings, static files, etc.



### Deployment

- Refer to the official Django documentation for instructions on deploying Django projects to production environments.