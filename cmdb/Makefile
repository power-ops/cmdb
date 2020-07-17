.PHONY: initial

install:
	pip install -r requirements.txt

db:
	python manage.py makemigrations
	python manage.py migrate
	ls */data/initial.yaml | xargs python manage.py loaddata

admin:
	python manage.py createsuperuser

hans:
	django-admin makemessages -l zh_hans
	django-admin compilemessages

run:
	python manage.py runserver 0.0.0.0:8000