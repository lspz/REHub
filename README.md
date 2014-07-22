How To Use
-----

Install requirements:

    pip install -r requirements.txt
  
Create DB:

    cd django
    ./manage.py syncdb
    ./manage.py init_data

Run spiders:

    cd scrapy
    scrapy crawl <spidername>

Run Django:

    cd django
    ./manage.py runserver
