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
    >>> client = hf.Client(api_key="YOUR_API_KEY")
    >>> result = client.source.search(name='python', limit=1)
    >>> print(result)
    {
     'code': 200,
     'page': 1,
     'maxPage': 2,
     'count': 1,
     'total': 2,
     'message': 'Source list',
     'data': [{'source_id': 'a62ae2d5560fca7b34bb6c0c389a378f99bcdd52',
       'name': 'python',
       'type': 'api',
       'sub_type': 'api',
       'archive': False,
        ...

```

Example Profile

```sh
    >>> import hrflow as hf
    >>> client = hf.Client(api_key="YOUR_API_KEY")
    >>> result = client.profile.search(source_ids=["source_id"], limit=1)
    >>> print(result)
    {
     'code': 200,
     'message': 'Profiles list',
     'page': 1,
     'max_page': 3,
     'count': 1,
     'total': 3,
     'data': {'profiles': [{'date_creation': '2020-03-31T12:04:52.858408',
        'date_reception': '2020-03-31T12:04:42',
        'educations': [{'description': 'Master data',
          'end_date': {'date': None, 'text': '12550'},
          'id': 'b03c71f748a048f96bcda33397457a81d8bf1301',
          'location': {'geocoder': {'fields': {'category': None,
                ...

```
Example Job

```sh
    >>> import hrflow as hf
    >>> client = hf.Client(api_key="YOUR_API_KEY")
    >>> result = client.job.search()
    >>> print(result)
    {
        "code": 200,
        "message": "ok",
        "data": [
            {
            "job_id": "7c94e981cd23d16f5c549eea21a7554db0c927a7",
            "job_reference": "1248593",
            "name": "Talent Acquisition Specialist",
            "archive": false,
            "date_creation": {
                "date": "2017-07-27 18:49:41.000000",
                "timezone_type": 3,
                "timezone": "Europe/Paris"
            ...

```

# API

For any methods that needs `*_id` and `*_reference`
you need to provide at least one of them but not necessarily both, keep in mind that reference override id.
## Profile


Retreive all profiles that match the query param, only source_ids are required

```python
    client.profile.search(source_ids, seniority, stage, date_start, date_end, filter_id, page, limit, sort_by, order_by)
```
source_ids is required

* profile.add_file().   
Add a profile resume as binary or json to a source id

```python
    client.profile.add_file(source_id, profile_file, sync_parsing, profile_content_type, profile_tags, profile_labels, profile_metadas, timestamp_reception)
```
source_id and profile_file are required

* profile.add_json(). 
```python
    client.profile.add_json(source_id, profile_json, profile_tags, profile_labels, profile_metadas, timestamp_reception)
```
source_id and profile_json are required


* profile.get().     
Retrieve the profile information associated with profile id.

```python
    client.profile.get(source_id, profile_id, profile_reference)
```
source_id and whether profile_id or profile_reference are required.

* profile.attachments.get().     
Retrieve the profile information associated with profile id.

```python
    client.profile.attachments.get(source_id, profile_id, profile_reference)
```
source_id and whether profile_id or profile_reference are required.


* profile.parsing.get().     
Retrieve the profile parsing data path associated with profile id.

```python
    client.profile.parsing.get(source_id, profile_id, profile_reference)
```
source_id and whether profile_id or profile_reference are required.

* profile.scoring.search().     
Retrieve the profile scoring associated with profile id.

```python
    client.profile.scoring.search(source_ids, job_id, stage, limit, use_agent)
```
source_ids and job_id are required.

## Source

* source.search().     
get all sources

```python
    client.source.search(name)
```

* source.get().     
Retrieve the source information associated with source id

```python
    client.source.get(source_id)
```
source_id is required.

## job

* job.search().     
Retrieve all jobs for given team account

```python
    client.job.search(name)
```

* job.get().     
Retrieve the job information associated with the job_id or job_reference

```python
    client.job.get(job_id, job_reference)
```
job_id or job_reference is required.

## webhook

* webhook.check()
Checks weither your webhook integration is enabled and works.

```python
  client.webhooks.check()
```

* webhook.setHandler()     
Add an handler of a webhook event

```python
  client.webhooks.setHandler(event_name, callback)
```
event_name and callback are required.

* webhook.isHandlerPresent(event_name).  
Checks if a callback is bind to an event

```python
  client.webhooks.isHandlerPresent(event_name)
```
event_name and callback are required.

* webhook.removeHandler(event_name).    
Remove the handler for a webhook event_name

```python
  client.webhooks.removeHandler(event_name)
```
event_name and callback are required.

* webhook.handleRequest(request_headers, signature_header)   
Start the handler for the given webhook request.

```python
  client.webhooks.handle(request_headers, signature_header)
```
request_headers the headers of the webhook request while signature_header is the `HTTP-hrflow-SIGNATURE` header only, one of them is required.

event_name is required

* handle webhook request

Here is an example of how to handle webhooks

```python
  import hrflow as hf

  def func_callback(event_name, webhook_data):
    print("{} {}".format(event_name, webhook_data)

  client = hf.client('api_key', webhook_secret='webhook_key')

  # Set an handler for webhook event.
  callback = func_callback
  resp = client.webhooks.setHandler('profile.parse.success', callback)

  # Get the header of the request sent by the webhook.
  encoded_header = {HTTP-hrflow-SIGNATURE: 'some encoded datas'}

  # Handle the webhook
  client.webhooks.handle(request_headers=encoded_header)
```


# Help

* Here an example on how to get help:

 ```sh
    >>> import hrflow as hf
    >>> from hrflow.profile import Profile
    >>> help(Profile.update_rating)

    Help on function update_rating in module hrflow.profile:

    update_rating(self, source_id=None, profile_id=None, filter_id=None, rating=None)
    Edit the profile rating given a filter

    Args:
        profile_id:             <string>
                                profile id
    body params:
        source_id:              <string>
                                source id associated to the profile

        filter_id:                 <string>
                                filter id
        rating:                 <int32>
                                profile rating from 1 to 4 associated to the filter.

    Returns:
        Response that contains code 201 if successful
        Other status codes otherwise.
(END)

```

* More help ? see  [hrflow API Docs](https://developers.hrflow.net/v1.0/reference#authentication)
