# PodFeed
Podcast aggregator

!![ezgif com-gif-maker](https://github.com/shalini-bit/PodFeed/blob/main/ezgif.com-gif-maker.gif)
## How To Run The Project

Create and activate a Python virtual environment for your operating system and install the dependencies:
<ul>
  <li>Django==3.2.6</li>
  <li>django-apscheduler==0.6.0</li>
  <li>feedparser==6.0.8</li>
  <li>python-dateutil==2.8.2</li>
</ul>


First clone this repository from Github and switch to the new directory.

Activate the virtualenv for your project. 

#### Apply migrations:

1. `python manage.py makemigrations` 
2.  `python manage.py migrate`

#### Create a superuser:

`python manage.py createsuperuser`

#### Run the Server:

`python manage.py runserver`

You can now navigate to localhost:8000 in your browser and inspect the finished project. 

P.S -Many improvements are left to be done.






