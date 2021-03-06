MoonBizGame
===========

A game simulating the bootstrapping of Lunar business.

Developed for the [International Space Apps Challlenge 2013](http://spaceappschallenge.org/), 
[Boostrapping of Space Industry](http://spaceappschallenge.org/challenge/affordable-rapid-bootstrapping-of-space-industry/) 
(AKA #moonville)

The game basically is like Civilization. You are running a company and you can buy launches to the moon and
put equipment there. There are several ways to make money, what will work for you?

The first version will be "Arcade style", with highly compressed timelines and each player in their own 
universe.

Setup
-----

Check out the code from git.

It is strongly recommended to use a virtual environment to develop in. Using virtualenvwrapper:

    mkvirtualenv moonbizgame

Install the required packages

    pip install -r requirements.txt
    
Create a localsettings.py file

    cp moonbizgame/localsettings.py.in moonbizgame/localsettings.py

Edit the localsettings.py file to suit. In particular, setting the `DATABASE`, `STATICFILES_DIRS`,
`TEMPLATE_DIRS`, and `SECRET_KEY`.

After setting up the database, you should be able to run the app.

    ./manage.py syncdb
    ./manage.py migrate
    
    ./manage.py runserver

The site is then available on http://localhost:8000/
