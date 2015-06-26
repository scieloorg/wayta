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

+--------------+------------------------+-----------------------------+
| Paremeter    | Description            | Mandatory                   |
+==============+========================+=============================+
| **q**        | Country name           | Yes                         |
+--------------+------------------------+-----------------------------+
| **accuracy** | Match accuracy [1,2,3] | No                          |
+--------------+------------------------+-----------------------------+
| callback     | JSONP callback method  | No                          |
+--------------+------------------------+-----------------------------+

Accuracy could be: 1 (high), 2 (medium), 3 (low)

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

+--------------+------------------------+-----------------------------+
| Paremeter    | Description            | Mandatory                   |
+==============+========================+=============================+
| **q**        | Institution Name       | yes                         |
+--------------+------------------------+-----------------------------+
| **country**  | Country Name           | No                          |
+--------------+------------------------+-----------------------------+
| **accuracy** | Match accuracy [1,2,3] | No                          |
+--------------+-------------------------+----------------------------+
| callback     | JSONP callback method  | No                          |
+--------------+------------------------+-----------------------------+

Accuracy could be: 1 (high), 2 (medium), 3 (low)

``GET /api/v1/institution?q=Pontifícia%20Universidade%20Católica``


Response::

    {
        head: {
            match: "multiple"
        },
        choices: [
            {
                city: "Rio de Janeiro",
                country: "Brazil",
                value: "Pontifícia Universidade Católica do Rio de Janeiro",
                state: "Rio de Janeiro",
                score: 8.287096,
                iso3166: "BR"
            },
            {
                city: "São Paulo",
                country: "Brazil",
                value: "Pontifícia Universidade Católica de São Paulo",
                state: "São Paulo",
                score: 5.763332,
                iso3166: "BR"
            },
            {
                city: "Porto Alegre",
                country: "Brazil",
                value: "Pontifícia Universidade Católica do Rio Grande do Sul",
                state: "Rio Grande do Sul",
                score: 5.763332,
                iso3166: "BR"
            },
            {
                city: "Santiago",
                country: "Chile",
                value: "Pontificia Universidad Católica de Chile",
                state: "Santiago de Chile",
                score: 5.685427,
                iso3166: "CL"
            },
            {
                city: "Belo Horizonte",
                country: "Brazil",
                value: "Pontifícia Universidade Católica de Minas Gerais",
                state: "Minas Gerais",
                score: 4.7990766,
                iso3166: "BR"
            }
        ]
    }

``GET /api/v1/institution?q=Pontifícia%20Universidade%20Católica&country=Chile``

Response::

    {
        head: {
            match: "by_similarity"
        },
        choices: [
            {
                city: "Santiago",
                country: "Chile",
                value: "Pontificia Universidad Católica de Chile",
                state: "Santiago de Chile",
                score: 9.483286,
                iso3166: "CL"
            }
        ]
    }


``GET /api/v1/institution?q=Pontifícia%20Universidade%20Católica&country=Chile&callback=my_callback``

Response::

    my_callback({
        "head": {
            "match": "multiple"
        }, 
        choices: [
            {
                city: "Santiago",
                country: "Chile",
                value: "Pontificia Universidad Católica de Chile",
                state: "Santiago de Chile",
                score: 9.483286,
                iso3166: "CL"
            }
        ]
    });

