# python-hrflow-api
🐍 hrflow API Python Wrapper

# Installation
The package is available for python >= 3.5
```sh
$ pip3 install hrflow
```

# Usage

**Source example**:

```sh
    >>> from hrflow import Hrflow
    >>> client = Hrflow(api_secret="YOUR_API_KEY")
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

**Profile example**

```sh
{
  "key": "8af2b7a0b48fbc936ace283ec020b0d6d4c4b018",
  "reference": null,
  "consent_algorithmic": {
    "owner": {
      "parsing": true,
      "revealing": false,
      "embedding": true,
      "searching": true,
      "scoring": true,
      "reasoning": false
    },
    "controller": {
      "parsing": true,
      "revealing": false,
      "embedding": true,
      "searching": true,
      "scoring": true,
      "reasoning": false
    }
  },
  "archived_at": null,
  "updated_at": "2021-12-10T15:18:46+0000",
  "created_at": "2021-12-10T15:18:46+0000",
  "info": {
    "full_name": "Harry James Potter",
    "first_name": "Harry James",
    "last_name": "Potter",
    "email": "harry.potter@hogwarts.net",
    "phone": "0747532699",
    "date_birth": "1997-06-26T00:00:00+0000",
    "location": {
      "text": "Number 4, Privet Drive, Little Whinging",
      "lat": null,
      "lng": null,
      "gmaps": null,
      "fields": null
    },
    "urls": [
      {"type": "from_resume", "url" : "https://hrflow.ai/"},
      {"type": "from_resume", "url" : "https://developers.hrflow.ai/"},
      {"type": "linkedin", "url" : "https://fr.linkedin.com/doe-john"},
      {"type": "linkedin", "url" : "https://fr.linkedin.com/doe-jane"},
      {"type": "twitter", "url" : "https://twitter.com/hrflowai"},
      {"type": "facebook", "url" : "https://www.facebook.com/hrflowai/"},  
      {"type": "github", "url" : "https://github.com/harry-james-potter"}
  ],
    "picture": null,
    "gender": "male",
    "summary": "Sorcerer Apprentice"
  },
  "text_language": "en",
  "text": "Harry James Potter\nSorcerer Apprentice\n\ndate of birth: June 26th 1997\nNumber 4, Privet Drive, Little Whinging\nemail: harry.potter@hogwarts.net\nphone: 0747532699\n\nExperiences\n\nApril 2002 - July 2002\tHogwarts School of Witchcraft and Wizardry\nMagic Investigator\nSolving mysteries about the Sorcerer's stone.\nteamplayer, empathy.\n\nEducations\n\nDecember 2001 - December 2002\tHogwarts School of Witchcraft and Wizardry\nSorcerer Apprentice\nFirst year of study.\nwitchcraft, levitation, lycanthropy.\n\nSkills\n\nwitchcraft\ndark arts\nperseverance\nempathy\n\nInterests\n\nquidditch\nwizard chess",
  "experiences_duration": 0.25,
  "educations_duration": 1,
  "experiences": [
    {
      "key": "8af2b7a0b48fbc936ace283ec020b0d6d4c4b019",
      "company": "Hogwarts School of Witchcraft and Wizardry",
      "logo": null,
      "title": "Magic Investigator",
      "description": "Solving mysteries about the Sorcerer's stone.",
      "location": {
        "text": "Hogwarts",
        "lat": null,
        "lng": null,
        "gmaps": null,
        "fields": null
      },
      "date_start": "2002-04-01T00:00:00tps://developers.hrflow.ai/reference/parse-a-resume+0000",
      "date_end": "2002-07-01T00:00:00+0000",
      "skills": [
        {
          "name": "teamplayer",
          "type": "soft",
          "value": null
        },
        {
          "name": "empathy",
          "type": "soft",
          "value": null
        }
      ],
      "certifications": [],
      "courses": [],
      "tasks": []
    }
  ],
  "educations": [
    {
      "key": "8af2b7a0b48fbc936ace283ec020b0d6d4c4b020",
      "school": "Hogwarts School of Witchcraft and Wizardry",
      "logo": null,
      "title": "Sorcerer Apprentice",
      "description": "First year of study.",
      "location": {
        "text": "Hogwarts",
        "lat": null,
        "lng": null,
        "gmaps": null,
        "fields": null
      },
      "date_start": "2001-12-01T00:00:00+0000",
      "date_end": "2002-12-01T00:00:00+0000",
      "skills": [
        {
          "name": "witchcraft",
          "type": "hard",
          "value": null
        },
        {
          "name": "levitation",
          "type": "hard",
          "value": null
        },
        {
          "name": "lycanthropy",
          "type": "hard",
          "value": null
        }
      ],
      "certifications": [],
      "courses": [],
      "tasks": []
    }
  ],
  "attachments": [],
  "skills": [
    {
      "name": "witchcraft",
      "type": "hard",
      "value": null
    },
    {
      "name": "dark arts",
      "type": "hard",
      "value": null
    },
    {
      "name": "perseverance",
      "type": "soft",
      "value": null
    },
    {
      "name": "empathy",
      "type": "soft",
      "value": null
    }
  ],
  "languages": [],
  "certifications": [],
  "courses": [],
  "tasks": [],
  "interests": [
    {
      "name": "quidditch",
      "value": null
    },
    {
      "name": "wizard chess",
      "value": null
    }
  ],
  "labels": [],
  "tags": [
    {
      "name": "contract_type",
      "value": "Full Time"
    }
  ],
  "metadatas": []
}
```
**Job example**

```sh
    {
    "name": "Data Scientist",
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
                    "description": "Bac+7"
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

```

# API

For any methods that needs `key` and `reference`
you need to provide at least one of them but not necessarily both, keep in mind that reference overrides id.
## Profile


### 📖 **The Profile Object**
JSON object with 5 required fields: `key`, `reference`, `info`, `text_language` and `text`. The JSON contains other optional fields that cannot be listed here. (See the examples above)
### 🧠 **Parse a Resume in a Source**
This endpoint allows you to parse a resume and make a profile object from it.
> 📘 **Real-time parsing**: To use the real-time parsing feature, you must have it enabled for the correponding source. In which case you just need to set `sync_parsing` to `1`.
- Open the file in `binary mode`
```python
with open('path/2/file', "rb") as f:
    profile_file = f.read()
```
- You can parse a resume without using a reference likr this:
```python
response = client.profile.parsing.add_file(source_key="source_key", 
                                  profile_file=profile_file, sync_parsing=0,
                                  sync_parsing_indexing=1,
                                  webhook_parsing_sending=0, 
                                  tags=[{"name":"archive", "value":True}])
```

- If you would like to specify a custom identifier that you can use later to retrieve the parsed profile more easily you can use the argument reference:
```python
response = client.profile.parsing.add_file(source_key="source_key", reference = "my_resume",
                                  profile_file=profile_file, sync_parsing=0,
                                  sync_parsing_indexing=1,
                                  webhook_parsing_sending=0, 
                                  tags=[{"name":"archive", "value":True}])
```
In both cases the output should look like this:
```
{'code': 202,
 'message': 'Your profile as been sent successfully to the Parsing Queue.',
 'data': []}
 ```
Note that the output above corresponds to a asynchronous profile parsing.
- To parse a profile synchronously you only need to set the parameter `sync-parsing` to `1`. The output should in this case look like this:
```
{'code': 201,
 'message': 'Profile parsed successfully. Profile extraction finished : 10.26 seconds.',
 ...}
```
Notice that you need to have real-time parsing enabled. In case you don't the parsing will be asynchronous by default. Check https://developers.hrflow.ai/reference/parse-a-resume for more information.
### 🧠 **Get a Resume Parsing from a Source**  
Retrieve Parsing information using source key and key/reference.
> ⚠️ **Query parameters**: `reference` and `key` cannot be null at the same time.
- Retrieve parsing information using source key
```python 
response = client.profile.parsing.get(source_key="source_key", key="profile_key")
```
- Retrieve parsing information using reference
```python
response = client.profile.parsing.get(source_key="source_key", reference="my_resume")
```
- The output should should look like this
```
{'code': 200,
 'message': 'Profile parsing',
 ...}
```
### 💾 **Index a Profile in a Source**
In order to add a JSON profile you can index it using HrFlow search engine
- Index a profile in a source using a JSON file `profile_json`
```python
response = client.profile.indexing.add_json(source_key="source_key", profile_json=profile_json)
```
- The output should be of this form:
```
{'code': 201,
 'message': 'Profile created',
 ...}
```

### 💾 **Edit a Profile indexed in a Source**
This enables you to edit the JSON of a profile in a source
>📘 JSON profile must include profile's key
- Edit a profile in a source
```python
response = client.profile.indexing.edit(source_key="source_key", key="profile_key", profile_json=profile_json)
```
- You should receive as output the following
```
{'code': 200,
 'message': 'Profile edited',
 ...}
```
### **💾 Get a Profile indexed in a Source**
Allows retrieving the profile information using source key and key/reference.
- Retrieve a profile object from a source this method
```python
response = client.profile.indexing.get(source_key="source_key", key="profile_key")
```
- The output should be
```
{'code': 200,
 'message': 'Profile details',
 ...}
```
### **💾 Get a Profile's attachment list**
- Retrieve a profile's attachment list from a source
```python
response = client.profile.attachment.list(source_key="source_key", key="profile_key")
```
- You should receive as output
```
{'code': 200,
 'message': 'Profile attachment list',
 ...}
```
### **🧠 Search Profiles indexed in Sources**     
This endpoint allows you to search profiles. 
- Search a profile using sources' keys 
```python
response = client.profile.searching.list(source_keys=["source_key"], page=1, 
                                    limit=30, sort_by='created_at',
                                    order_by="desc", text_keywords=['python'],
                                    created_at_min='2020-07-09T13:35:11+0000')
```
- The output should look like this
```
{'code': 200,
 'message': 'Profile searching results',
```
### 🧠 **Score Profiles indexed in sources for a Job**
This endpoint allows you to Score Profiles for a job.
- Score a profile using a list of `source_key`, a `board_key`, and a`job_key`
```python
response = client.profile.scoring.list(source_keys=["source_key"], 
                                  board_key="board_key", job_key="job_key",
                                  use_agent=1, page=1, limit=30,
                                  sort_by='created_at', order_by=None, 
                                  text_keywords=['python'])
```

## Job
### 📖 **The Job Object**
JSON object with 5 required fields: `key`, `reference`, `name`, `location` and `sections` . It contains other optional fields that cannot be listed here. 
Here is what a job JSON looks like:
```JSON
{
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
```
### 💾 **Index a Job in a Board**
This endpoint allows you to Index a Job object.
> ⚠️ **Job Input**: If your Job is an unstructured text, make sure to parse it first before indexing it. See how in 🧠 Parse a raw Text.
- Index a job in a board. This action requires a `board_key`
```python
response = client.job.indexing.add_json(board_key="board_key", job_json=job_json)
```
- The output should look like this
```
{'code': 201,
 'message': 'Job created',
...}
```
### 💾 **Edit a Job indexed in a Board**
This endpoint allows you to edit the of JSON of Job.
- Edit a job already indexed in a board. This action requires a `job_key`
```python
response = client.job.indexing.edit(board_key="board_key", key="job_key", job_json=job_json)
```
- You should receive the following output
```
{'code': 200,
 'message': 'Job edited',
 ...}
```
### 💾 **Get a Job indexed in a Board**
This endpoint allows retriving the job object from a board using the corresponding keys
- Retrieve a job indexed in a board
```python
response = client.job.indexing.get(board_key="board_key", key="job_key")
```
- The output
```
{'code': 200,
 'message': 'Job details',
 ...}
```
### 🧠 **Search for Jobs indexed in Boards**
This endpoint allows you to Search for Jobs.
- Search for jobs among a list of boards
```python
response = client.job.searching.list(board_keys=["board_key"], page=1, limit=30, 
                                sort_by='created_at', order_by=None)
```
- The output should be
```
{'code': 200,
 'message': 'Job searching results',
 ...}
```

 ### 🧠 **Score Jobs indexed in Boards for a Profile**
This endpoint allows you to Score Jobs for Profile.
- Score a job for a certain profile
```python
response = client.job.scoring.list(board_keys=["board_key"],source_key="source_key",profile_key="profile_key", use_agent=1,agent_key="agent_key", page=1, limit=30, sort_by='created_at', order_by=None)
```

## Text
### 🧠 **Parse a raw text**
Allows extracting over 50 data point from any raw input text.
- Parse a raw text given as argument
```python
resp = client.document.parsing.post(text="Your text here)
```
- It should return
```
{'code': 200,
 'message': 'Parsing results',
 'data':...}
```

### 🧠 **Reveal missing skills in a text**
Predict likely missing skills in a text
- Predict the skills using the method below
```python
resp = client.document.revealing.post(text="hello")
```
- The output should look like this:
```{'code': 200,
 'message': 'Revealing results',
 ...}
 ```

### 🧠 **Item embedding**
This endpoint allows profile/job 's embedding, it returns embedding encoded as base64.

In order to retrieve Item embeddings, you must decode response's body, and reshape the output as shown in below example.
 
```python
import base64
import numpy as np

dfloat32 = np.dtype('>f4')

response = client.document.embedding.post(item_type="profile", item=profile_json, return_sequences=True)

embeddings_reponse = response.get('data')
embeddings_decoded = base64.b64decode(embeddings_reponse)
embeddings_as_np = np.frombuffer(embeddings_decoded, dtype=dfloat32)

embeddings = np.reshape(embeddings_as_np, (-1, 1024)).tolist()
```

 ### 🧠 **Text Linking**    
```python
resp = client.document.linking.post(text="python", top_n=20)
```

## Source
### 📖 **The Source Object**
A JSON object with a `key`, a `name`, a `description`, a `type` and a `subtype` and other optional fields.
### 🔌 **Find Sources in a Workspace**
Retrieve all sources for a given team account
- List sources using this method
```python
resp = client.source.list(name='async')
```
- It should output something like this
```
{'code': 200,
 'message': 'Source list',
 ...}
```
### 🔌 **Get a Source from a Workspace**
Retrieve source's information with a source key
- Get a source's information for a given key using
```python
resp = client.source.get(key=key)
```
- The output should contain this message
```
{'code': 200,
 'message': 'Source info',
 ...}
```


## Board
### 📖 **The Board Object**
A JSON object representing a board containing many fields:  a `key`, a `name`, ``description`, a `description`, a `type` and a `subtype`
### 🔌 **Find Boards in a Workspace**
Retrieve all boads for given team account
- Get all boards for given team account using this method
```python
resp = client.board.list(name='compaign')
```
- The output should be as follows: 
```
{'code': 200,
 'message': 'Board list',
 ...}
```
### 🔌 **Get a Board from a Workspace**
Retrieve board's information for a given key.
- Get the board's information using this method
```python
resp = client.board.get(key=key)
```
- The output should be the same as below:
```
{'code': 200,
 'message': 'Board info',
 ...}
```

## Webhook

### 🔌 **Webhook Check**
Checks weither your webhook integration is enabled and works.
- Check if it is enabled using a  `url` and a `type`
```python
resp = client.webhooks.check("url","type")
```
- The output should look like this
```
{'code': 200,
 'message': 'ok',
 ...}
```

### **Set Handler**  
Add an handler of a webhook event
-  To set a handler, use the method below
```python
resp =  client.webhooks.setHandler(event_name, callback)
```
>  ⚠️ `event_name` and `callback` are required.

### **Handler presence check** 
- Check if a callback is bind to an event
```python
resp =  client.webhooks.isHandlerPresent(event_name)
```
>  ⚠️ `event_name` and `callback` are required.

### **Remove a handler**
Remove the handler for a webhook
- To do so, use the method below
```python
resp =  client.webhooks.removeHandler(event_name)
```
>  ⚠️ `event_name` and `callback` are required.

### **Start the handler** 
Start the handler for the given webhook request.

```python
resp =  client.webhooks.handle(request_headers, signature_header)
```
request_headers the headers of the webhook request while signature_header is the `HTTP-hrflow-SIGNATURE` header only, one of them is required.

event_name is required

### **Handle webhook requests**

Here is an example on how to handle webhooks

```python
from hrflow import Hrflow

def func_callback(event_name, webhook_data):
    print("{} {}".format(event_name, webhook_data)
    
    client = Hrflow(api_secret="YOUR_API_KEY", webhook_secret='webhook_key')

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
>>> from hrflow.hrflow.profile.parsing import ProfileParsing
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
