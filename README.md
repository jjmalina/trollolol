A basic Django project set up with Celery and Django-Supervisor
===============================================================

Start celery:

python manage.py supervisor

Stop celery:

python manage.py supervisor stop celeryd celerycam celerybeat

Manually start celery:

python manage.py celeryd --setting=settings

Manually kill celery processes if hung:

ps ax | grep celery | cut -b1-5 | xargs kill -9

Rabbitmq setup:

rabbitmqctl add_user tester tester
rabbitmqctl add_vhost test_vhost
rabbitmqctl set_permissions -p test_vhost tester ".*" ".*" ".*"

Mysql:

database: test
user: root
password: [none]
