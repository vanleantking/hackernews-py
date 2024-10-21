### MIGRATE
1. SHOW MIGRATE:
    `python manage.py showmigrations`
2. GENERATE MIGRATIONS:
   - add models into **app**
   - `python manage.py makemigrations`
3. RUN MIGRATE:
   - `python manage.py migrate`
4. ROLLBACK MIGRATE:
   - `python manage.py showmigrations`
   - **rollback to a specific migration**: `python manage.py migrate` __app_name__ __id_file__
   - **rollback all migrations in single app**: `python manage.py migrate` __app_name__ `zero`