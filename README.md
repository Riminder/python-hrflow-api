# python-hrflow-api
🐍 hrflow API Python Wrapper

# Installation
The package is available for python >= 3.5
```sh
$ pip3 install hrflow
```

# Usage

Example Source

```sh
    >>> import hrflow as hf
    >>> client = hf.Client(api_secret="YOUR_API_KEY")
    >>> result = client.source.list(name='python', limit=1)
    >>> print(result)
    {
        'code': 200,
        'data': [{
            'archive': None,
            'consent': False,
            'consent_url': None,
            'created_at': '2020-07-22T09:11:32+0000',
            'description': None,
            'id': id,
            'key': 'source_key',
            'members': ['member@hrflow.ai'],
            'name': 'sync-php',
            'notification': False,
            'private': False,
            'stats': {'size': '0'},
            'status': True,
            'subtype': 'php',
            'type': 'api',
            'updated_at': '2020-07-22T09:11:32+0000',
            'user': {
                'avatarUrl': '/images/user.png',
                'email': 'member@hrflow.ai',
                'firstName': None,
                'id': id,
                'lastName': None,
                'locale': 'english',
                'phone': None,
                'position': None,
                'pseudo': None}},
            .
            .
            . ],
        'message': 'Source list',
        'meta': {'count': 11, 'maxPage': 1, 'page': 1, 'total': 11}}

```

Example Profile

```sh
    >>> import hrflow as hf
    >>> client = hf.Client(api_secret="YOUR_API_KEY")
    >>> result = client.profile.searching.list(source_keys=["source_key"],
                                              page=1, limit=30,
                                              sort_by='created_at',
                                              order_by="desc")

    >>> print(result)
    {
        'code': 200,
        'data': {'profiles': [{...},
                              {...},
                              {...}]
                }
    }

```
Example Job

```sh
    >>> import hrflow as hf
    >>> client = hf.Client(api_secret="YOUR_API_KEY")
    >>> result = client.job.searching.list(board_keys=["board_key"], page=1,
                                          limit=30, sort_by='created_at')
    >>> print(result)
    {
        'code': 200,
        'data': {'jobs': [{...},
                          {...},
                          {...}]
                }
    }

```

# API

For any methods that needs `key` and `reference`
you need to provide at least one of them but not necessarily both, keep in mind that reference override id.
## Profile


Retreive all profiles that match the query param, only source_ids are required

```python
client.profile.searching.list(source_keys=["source_key"], page=1, limit=30,.
                             sort_by='created_at', order_by="desc",
                             text_keywords=['python'], 
                             created_at_min='2020-07-09T13:35:11+0000')
```
source_keys is required

* Profile parsing:   
Add a profile resume as binary to a given source

```python
with open('path/2/file', "rb") as f:
    profile_file = f.read()

resp = client.profile.parsing.add_file(source_key="source_key", 
                                  profile_file=profile_file, sync_parsing=1,
                                  sync_parsing_indexing=1,
                                  webhook_parsing_sending=0, 
                                  tags=[{"name":"archive", "value":True}])
```

* Retrieve Parsing Object:     
Retrieve Parsing information using source key and key/reference.

```python
resp = client.profile.parsing.get(source_key="source_key", key="profile_key")
```
* Profile indexing:
In order to add Json profile you can index them using HrFlow search engine
```python
profile_json = {
  "source_key": "source_key",
  
  "consent_algorithmic": {
            "owner": {
                "parsing": True,
                "revealing": False,
                "embedding": True,
                "searching": False,
                "scoring": True,
                "reasoning": False
            },
            "controller": {
                "parsing": True,
                "revealing": False,
                "embedding": True,
                "searching": False,
                "scoring": True,
                "reasoning": False
            }
        },
  "info" : {
      "full_name":"Harry Potter",
      "first_name": "Harry",
      "last_name": "Potter",
      "email":"harry.potter@gmail.com",
      "phone":"0202",
      "gender": None,
      "urls": {
          "from_resume": [],
          "linkedin":"",
          "twitter":"",
          "facebook":"",
          "github":"",
          "picture":""},
      "picture":None,
  	  "location":{"text": None},
  	  "summary": "Brief summary"
  },
  "text": "test text",
  "experiences": [{
      "date_start": "15/02/1900",
      "date_end": "",
      "title": "Lead",
      "company": "Mathematic Departement",
      "location": {"text":"Paris"},
      "description": "Developping."
      }],
  "experiences_duration":5,
  "educations": [{
      "date_start": "12540",
      "date_end": "12550",
      "title": "Mathematicien",
      "school": "University",
      "description": "Description",
      "location": {"text":"Scotland"}
  }],
  "educations_duration":4,
  "skills": [{"name":"manual skill", "value": None}, {"name":"Creative spirit", "value": None},
             {"name":"Writing skills", "value": None}, {"name":"Communication", "value": None}],
  "languages" : [{"name":"english", "value": None}],
  "interests": [{"name":"football", "value": None}],
  "tags":[],
  "metadatas":[],
  "labels":[{"stage":"yes", "job_id":"job_id"}],
  "attachments": []
}
resp = client.profile.indexing.add_json(source_key="source_key", profile_json=profile_json)
```

* PUT Profile:
Json profile must include profile's key
```python
resp = client.profile.indexing.edit(source_key="source_key", key="profile_key", profile_json=profile_json)
```

* Retrieve Profile Object:
Retrieve Profile information using source key and key/reference.
```python
resp = client.profile.indexing.get(source_key="source_key", key="profile_key")
```

* Retrieve Profile's attachment:
```python
resp = client.profile.attachment.list(source_key="source_key", key="profile_key")
```

* Searching (ProfileAPI):     

```python
resp = client.profile.searching.list(source_keys=["source_key"], page=1, 
                                    limit=30, sort_by='created_at',
                                    order_by="desc", text_keywords=['python'],
                                    created_at_min='2020-07-09T13:35:11+0000')
```

* Scoring (ProfileAPI):     

```python
resp = client.profile.scoring.list(source_keys=["source_key"], 
                                  board_key="board_key", job_key="job_key",
                                  use_agent=1, page=1, limit=30,
                                  sort_by='created_at', order_by=None, 
                                  text_keywords=['python'])
```


## job
* Index Job    
Index json Job

```python
job_json = {
    "name": "Data Engineer",
    "agent_key": "agent_key",
    "reference": "Job's reference abc",
    "url": "https://www.pole-emploi.ai/jobs/data_engineer",
    "summary": "As an engineer for the Data Engineering Infrastructure team, you will design, build, scale, and evolve our data engineering  platform, services and tooling. Your work will have a critical  impact on all areas of business:supporting detailed internal analytics, calculating customer usage, securing our platform, and much more.",
    "location": {
                  "text": "Dampierre en Burly (45)",
                  "geopoint": {
                      "lat": 47.7667,
                      "lon": 2.5167
                  }
                 },
    "sections": [{
                    "name": "profile",
                    "title": "Searched Profile",
                    "description": "Bac+5"
                  }
                  ],
    "skills": [{
                  "name": "python",
                  "value": None
               },
               {
                  "name": "spark",
                  "value": 0.9
               }
               ],
    "languages": [{
                     "name": "english",
                     "value": 1
                  },
                 {  
                     "name": "french",
                     "value": 1
                  }
                  ],
    "tags": [{
                "name": "archive",
                "value": True
             },
             {  
                "name": "tag example",
                "value": "tag"
              }
              ],
    "ranges_date": [{
                       "name": "Dates",
                       "value_min": "2020-05-18T21:59",
                       "value_max": "2020-09-15T21:59"
                    }
                    ],
    "ranges_float": [{
                       "name": "salary",
                       "value_min": 30,
                       "value_max": 40,
                       "unit": "eur"
                    }
                    ],
    "metadatas": [{
                     "name": "metadata example",
                     "value": "metadata"
                  }
                  ]
}

resp = client.job.indexing.add_json(board_key="board_key", job_json=job_json)
```

* PUT Job:
Json profile must include job's key
```python
resp = client.job.indexing.edit(board_key="board_key", key="job_key", job_json=job_json)
```

* GET Job:    
Retrieve the job information associated with the job_id or job_reference

```python
resp = client.job.indexing.get(board_key="board_key", key="job_key")
```

* Search (JobAPI):     
```python
resp = client.job.searching.list(board_keys=["board_key"], page=1, limit=30, 
                                sort_by='created_at', order_by=None)
```

* Scoring (JobAPI):     
```python
resp = client.job.scoring.list(board_keys=["board_key"], source_key="source_key",
                              profile_key="profile_key", use_agent=1,
                              agent_key="agent_key", page=1, limit=30, 
                              sort_by='created_at', order_by=None)
```
## Source

* List sources:
```python
resp = client.source.list(name='async')
```

* GET source:     
Retrieve source's information for a given key

```python
resp = client.source.get(source_key=key)
```

## webhook

* webhook.check()
Checks weither your webhook integration is enabled and works.

```python
resp = client.webhooks.check()
```

* webhook.setHandler()     
Add an handler of a webhook event

```python
resp =  client.webhooks.setHandler(event_name, callback)
```
event_name and callback are required.

* webhook.isHandlerPresent(event_name).  
Checks if a callback is bind to an event

```python
resp =  client.webhooks.isHandlerPresent(event_name)
```
event_name and callback are required.

* webhook.removeHandler(event_name).    
Remove the handler for a webhook event_name

```python
resp =  client.webhooks.removeHandler(event_name)
```
event_name and callback are required.

* webhook.handleRequest(request_headers, signature_header)   
Start the handler for the given webhook request.

```python
resp =  client.webhooks.handle(request_headers, signature_header)
```
request_headers the headers of the webhook request while signature_header is the `HTTP-hrflow-SIGNATURE` header only, one of them is required.

event_name is required

* handle webhook request

Here is an example of how to handle webhooks

```python
import hrflow as hf

def func_callback(event_name, webhook_data):
print("{} {}".format(event_name, webhook_data)

client = hf.client(api_secret="YOUR_API_KEY", webhook_secret='webhook_key')

# Set an handler for webhook event.
callback = func_callback
resp = client.webhooks.setHandler('profile.parsing.success', callback)

# Get the header of the request sent by the webhook.
encoded_header = {HTTP-hrflow-SIGNATURE: 'some encoded datas'}

# Handle the webhook
client.webhooks.handle(request_headers=encoded_header)
```


# Help

* Here an example on how to get help:

 ```sh
>>> import hrflow
>>> from hrflow.profile.parsing import ProfileParsing
>>> help(ProfileParsing.get)

Help on function get in module hrflow.profile.parsing:

get(self, source_key=None, key=None, reference=None, email=None)
    Retrieve Parsing information.
    
    Args:
        source_key:             <string>
                                source_key
        key:                    <string>
                                key
        reference:              <string>
                                profile_reference
        email:                  <string>
                                profile_email
    
    Returns
        Get information

```

* More help ? see  [hrflow API Docs](https://developers.hrflow.ai/)
