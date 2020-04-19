Rates Web Service
==================
Undergraduate Research Opportunities Program
============================================


Description of the project
--------------------------

This project consists in a simple RESTFul web service thar queries the `Rates Api <https://ratesapi.io/>`_ and provides the following information :

* The base symbol
* Current symbol
* Current price of a symbol
* Price indicatior :
    + -1 if the price decreased compared to the previous day
    + 0 if the price stayed the same
    + 1 if the price increased

This project is implemented in Python 3 with Falcon.

Installation
------------

Use the package manager pip to install falcon, gunicorn, httpie, pytest, requests and requests-cache.

1) ``pip install falcon``
2) ``pip install gunicorn``
3) ``pip install httpie``
4) ``pip install pytest``
5) ``pip install requests``
6) ``pip install requests-cache``

**Installation of the packages :**
In order to do that you can open the terminal in the project root folder "Rates-Web-Service" and using the Makefile of the project simply by entering ``make init`` in this terminal.

**Activation of work environments :**
Once done you can activate your work environment in this terminal and in an other terminal in the project root folder "Rates-Web-Service" with this command : `source .venv/bin/activate``

**Server boot :**
Now in the first terminal you can run the server by entering ``make run``

**Client simulation :**
In the second terminal you can execute this command ``make demo`` which simulates several requests of a client to provide you a demo of this web service.

**Test execution :**
Please, enter ``make test`` in the terminal to execute the tests.

**DOCKER VERSION :**

Running the server:

1) ``sudo docker-compose up`` in the terminal in the project root folder

Running the demo:

2) ``sudo docker-compose up`` in the terminal in Rates-Web-Service/docker
3) ``sudo docker run --rm -it --network="host" my-demo`` in the terminal in Rates-Web-Service/docker


Authors and akcnowledgment
--------------------------

* Aurélie Beaugeard, Engineering sutdent at the INSA of Rouen

License
-------
`MIT
<https://choosealicense.com/licenses/mit/>`_

