IoToad - st_sp_ranking
-----------------------

.. image:: https://travis-ci.org/morelab/st_sp_ranking.svg?branch=master
    :target: https://travis-ci.org/morelab/st_sp_ranking

.. image:: https://codecov.io/gh/morelab/st_sp_ranking/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/morelab/st_sp_ranking

.. image:: https://img.shields.io/badge/python-3.8-blue.svg
    :target: https://www.python.org/downloads/release/python-380/

.. image:: https://img.shields.io/badge/code%20style-pep8-orange.svg
    :target: https://www.python.org/dev/peps/pep-0008/

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

.. image:: http://www.mypy-lang.org/static/mypy_badge.svg
    :target: http://mypy-lang.org/

IoToad hook that responds ranking REST queries, developed for SentientThings.

The REST API structure is:

* :code:`api/out/sp_ranking/<time-range>/<smartplug-id>`

Where...

* :code:`<time-range>`: can only be :code:`today`, :code:`week` and :code:`month`
* :code:`smartplug-id`: is the device id, e.g. sp_w.r1.c3


Examples
+++++++++



* :code:`api/out/sp_ranking/today/sp_w.r0.c1`
* :code:`api/out/sp_ranking/week/sp_w.r0.c1`
* :code:`api/out/sp_ranking/month/sp_w.r0.c1`

.. code-block:: json

    {
        "data": {
            "position": "1",  # ranking position
            "amount": "22"  # number of devices in ranking
        }
    }

