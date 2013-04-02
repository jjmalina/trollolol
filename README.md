Hunting reddit trolls
===============================================================

Partially finished hackNY Fall 12 hackathon project. Crawls reddit for new comments and uses the sci-kit SVM package learn detect troll comments.

# Running it

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


MySQL:

    database: test
    user: root
    password: [none]
