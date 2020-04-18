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

``pip install falcon``
``pip install gunicorn``
``pip install httpie``
``pip install pytest``
``pip install requests``
``pip install requests-cache``

**Installation of the packages :**
In order to do that you can open the terminal in the project root folder "Rates-Web-Service" and using the Makefile of the project simply by entering ``make init`` in this terminal.

**Activation of work environments**
Once done you can activate your work environment in this terminal and in an other terminal in the project root folder "Rates-Web-Service" with this command : `source .venv/bin/activate``

**Server boot**
Now in the first terminal you can run the server by entering ``make run``

**Client simulation**
In the second terminal you can execute this command ``make demo`` which simulates several requests of a client to provide you a demo of this web service.

Authors and akcnowledgment
--------------------------

* Aurélie Beaugeard, Engineering sutdent at the INSA of Rouen

License
-------
`MIT
<https://choosealicense.com/licenses/mit/>`_

