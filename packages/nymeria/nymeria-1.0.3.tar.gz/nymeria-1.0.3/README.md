# Nymeria

[![PyPI version](https://badge.fury.io/py/nymeria.svg)](https://badge.fury.io/py/nymeria)

The official python package to interact with the Nymeria service and API.

Nymeria makes it easy to enrich data with contact information such as email
addresses, phone numbers and social links. The ruby gem wraps Nymeria's [public
API](https://www.nymeria.io/developers) so you don't have to.

![Nymeria makes finding contact details a breeze.](https://www.nymeria.io/assets/images/marquee.png)

## Usage

#### Installation

```bash
$ pip install nymeria
```

#### Set and Check an API Key.

```python
from nymeria import api

client = api.Client('ny_apikey')

client.check_authentication() # => True | False
```

All API endpoints assume an api key has been set. You should set the api key
early in your program. The key will automatically be added to all future
requests.

#### Verify an Email Address

```python
from nymeria import api

client = api.Client('ny_apikey')

if client.check_authentication():
  client.verify('foo@bar.com') # => dict (see below)
```

```json
{
  'data': {
    'result': 'catchall',
    'tags': ['has_dns', 'has_dns_mx', 'smtp_connectable', 'accepts_all', 'has_dns']
  },

  'usage': {
    'used': 861,
    'limit': 10000
  }
}
```

#### Enrich a Profile

```python
from nymeria import api

client = api.Client('ny_apikey')

# Single Enrichment

if client.check_authentication():
  client.enrich({ 'url': 'linkedin.com/in/wozniaksteve' }) # => dict (see below)

  # Bulk Enrichment (pass n-queries to enrich)

  client.enrich({ 'email': 'woz@steve.org' }, { 'url': 'github.com/nymeriaio' }) # => dict (see below)
```

#### Single Enrichment Response

```json
{
  "usage": {
    "used": 4,
    "limit": 100
  },
  "data": {
    "bio": {
      "first_name": "Steve",
      "last_name": "Wozniak",
      "title": "Chief Scientist",
      "company": "Sandisk",
      "company_website": "sandisk.com"
    },
    "emails": [
      {
        "type": "professional",
        "name": "steve",
        "domain": "woz.org",
        "address": "steve@woz.org"
      },
      ...
    ],
    "phone_numbers": [
      ...
    ],
    "social": [
      {
        "type": "linkedin",
        "id": "wozniaksteve",
        "url": "https://www.linkedin.com/in/wozniaksteve"
      }
    ]
  }
}
```

#### Bulk Enrichment Response

```json
{
  "usage": {
    "used": 4,
    "limit": 100
  },
  "data": [
    {
      'meta': {
        'email': 'steve@woz.org'
      },
      'result': {
        "bio": {
          "first_name": "Steve",
          "last_name": "Wozniak",
          "title": "Chief Scientist",
          "company": "Sandisk",
          "company_website": "sandisk.com"
        },
        "emails": [
          {
            "type": "professional",
            "name": "steve",
            "domain": "woz.org",
            "address": "steve@woz.org"
          },
          ...
        ],
        "phone_numbers": [
          ...
        ],
        "social": [
          {
            "type": "linkedin",
            "id": "wozniaksteve",
            "url": "https://www.linkedin.com/in/wozniaksteve"
          }
        ]
      }
    },
    {
      'meta': {
        'url': 'github.com/nymeriaio'
      },
      'result': {
        ...
      }
    },
    ...
  ]
}
```

#### Search for People

You can query Nymeria's people database for people that match a certain
criteria. You can view previews for each person and "unlock" the complete
profile.

Currently, you can query using any of the following parameters:

1. `q` a raw query which will match keywords in a person's name, title, skills,
   etc.
2. `first_name`
3. `last_name`
4. `title`
5. `company`
6. `skills` a comma separated list of skills.
7. `location` city, state, country, etc.
8. `country` matches country only.

```python
from nymeria import api

client = api.Client('ny_apikey')

if client.check_authentication():
  # Query for people. Returns previews for each person.
  previews = client.people({ 'q': 'Ruby on Rails' }) # => dict (see above)

  # Given a person's UUID, unlock their details (including contact info).
  people = client.reveal([ r['uuid'] for r in previews['data'] ])

  print(people)
```

## License

MIT License

Copyright (c) 2022, Nymeria LLC.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
