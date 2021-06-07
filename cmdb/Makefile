.PHONY: initial

install:
	pip install -r requirements.txt

db:
	python manage.py makemigrations
	python manage.py migrate
	ls */data/initial.yaml | xargs python manage.py loaddata

admin:
	echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin','', 'admin')" | python manage.py shell

hans:
	django-admin makemessages -l zh_hans
	django-admin compilemessages

run:
	python manage.py runserver 0.0.0.0:8000

uwsgi:
	uwsgi --ini ./uwsgi.ini

static:
	python manage.py collectstatic
