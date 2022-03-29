<!-- activate -->
./virtualenv-folder-name/Scripts/activate

<!-- install requirements.txt -->
pip install -r requirements.txt

<!-- migrate if database is not present -->
python manage.py migrate

<!-- has to be together to create database -->
<!-- transform python models to database -->
python manage.py makemigrations
<!-- register database into sql language -->
python manage.py migrate

<!-- create ROOT / admin user who can control everthing -->
python manage.py createsuperuser

<!-- runserver -->
python mange.py runserver (port: optional)
