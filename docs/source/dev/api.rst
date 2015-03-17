Wayta RESTful API
=================

API URL: http://wayta.scielo.org

API Versioning:

+------------+---------+-----------------+
| Date       | Version | Changes         |
+============+=========+=================+
| 2015-03-17 | v1.0b   | Initial Version |
+------------+---------+-----------------+

Country
-------

Retrieve a list of normalized country name related with a given string.

Endpoint::

/api/v1/country

Parameters:

+------------+-----------------------+-----------------------------+
| Paremeter  | Description           | Mandatory                   |
+============+=======================+=============================+
| **q**      | Country name          | Yes                         |
+------------+-----------------------+-----------------------------+
| callback   | JSONP callback method | No                          |
+------------+-----------------------+-----------------------------+

``GET /api/v1/country/?q=AZIL``

Response::

    {

        "head": {
            "match": "by_similarity"
        },
        "choices": [
            {
                "score": 5.61512,
                "value": "Brazil"
            }
        ]

    }

``GET /api/v1/pid/?q=AZIL&callback=my_callback``

Response::

    my_callback({
        "head": {
            "match": "exact"
        }, 
        "choices": [
            {
                "country": "Brazil", 
                "score": 8.057689, 
                "value": "Universidade de S\u00e3o Paulo"
            }
        ]
    });


Institution
-----------

Retrieve a list of normalized institution names related with a given string.

Endpoint::

/api/v1/institution


Parameters:

+------------+-----------------------+-----------------------------+
| Paremeter  | Description           | Mandatory                   |
+============+=======================+=============================+
| **q**      | Institution Name      | yes                         |
+------------+-----------------------+-----------------------------+
| callback   | JSONP callback method | No                          |
+------------+-----------------------+-----------------------------+

``GET /api/v1/institution/?q=Católica``


Response::

    {
        "head": {
            "match": "multiple"
        }, 
        "choices": [
            {
                "country": "Colombia", 
                "score": 3.616078, 
                "value": "Pontificia Universidad Bolivariana"
            }, 
            {
                "country": "Brazil", 
                "score": 3.616078, 
                "value": "Pontif\u00edcia Universidade Cat\u00f3lica do Rio de Janeiro"
            }, 
            {
                "country": "Brazil", 
                "score": 3.616078, 
                "value": "Pontif\u00edcia Universidade Cat\u00f3lica de Campinas"
            }, 
            {
                "country": "Brazil", 
                "score": 3.616078, 
                "value": "Pontif\u00edcia Universidade Cat\u00f3lica de S\u00e3o Paulo"
            }, 
            {
                "country": "Chile", 
                "score": 3.616078, 
                "value": "Pontificia Universidad Cat\u00f3lica de Chile"
            }, 
            {
                "country": "Venezuela", 
                "score": 3.616078, 
                "value": "Universidad Cat\u00f3lica Cecilio Acosta"
            }
        ]
    }

``GET /api/v1/institution/?q=Católica&country=Chile``

Response::

    {
        "head": {
            "match": "multiple"
        }, 
        "choices": [
            {
                "country": "Chile", 
                "score": 8.139689, 
                "value": "Universidad Cat\u00f3lica Silva Henr\u00edquez"
            }, 
            {
                "country": "Chile", 
                "score": 8.139689, 
                "value": "Pontificia Universidad Cat\u00f3lica de Chile"
            }, 
            {
                "country": "Chile", 
                "score": 8.139689, 
                "value": "Pontificia Universidad Cat\u00f3lica de Valpara\u00edso"
            }, 
            {
                "country": "Chile", 
                "score": 7.900635, 
                "value": "Universidad Cat\u00f3lica del Norte"
            }
        ]
    }


``GET /api/v1/institution/?q=Católica&country=Chile&callback=my_callback``

Response::

    my_callback({
        "head": {
            "match": "multiple"
        }, 
        "choices": [
            {
                "country": "Chile", 
                "score": 8.139689, 
                "value": "Universidad Cat\u00f3lica Silva Henr\u00edquez"
            }, 
            {
                "country": "Chile", 
                "score": 8.139689, 
                "value": "Pontificia Universidad Cat\u00f3lica de Chile"
            }, 
            {
                "country": "Chile", 
                "score": 8.139689, 
                "value": "Pontificia Universidad Cat\u00f3lica de Valpara\u00edso"
            }, 
            {
                "country": "Chile", 
                "score": 7.900635, 
                "value": "Universidad Cat\u00f3lica del Norte"
            }
        ]
    });

