import unittest
import hmac
import hashlib
import base64
import json

from hrflow import Hrflow
from test_assets import test_config
from hrflow.webhook import bytesutils


class TestHelper:

    instance = None

    def __init__(self):
        self.api_key = test_config.API_SECRET
        self.webhook_secret = test_config.WEBHOOK_SECRET
        self.source_id = None
        self.add_source_id = None
        self.profile_id = None
        self.profile_ref = None
        self.filter_id = None
        self.filter_ref = None
        self.rating = int(1)
        self.stage = 'NEW'
        self.source_type = 'api'
        # if source_name is empty no name is selected
        self.source_name = test_config.SOURCE_NAMES

    def getKey(self):
        return self.api_key

    def getWebhookSecret(self):
        return self.webhook_secret

    def setup(self):
        api = Hrflow(api_key=self.api_key)
        res = api.source.list()
        for source in res['data']:
            name = False
            type = False
            if source['type'] == self.source_type:
                source_type = True
            if self.source_name and source['name'] in self.source_name:
                name = True
            if name and source_type:
                self.add_source_id = str(source['source_id'])
                break
        if self.add_source_id is None:
            raise ValueError('no api test source found')
        self.source_id = self.add_source_id
        res = api.profile.list(source_ids=[self.source_id])
        if not res['data']['profiles']:
            raise ValueError('no profiles found')
        profiles = res['data']['profiles']
        for profile in profiles:
            profile_id = str(profile['profile_id'])
            res = api.profile.scoring.list(source_id=self.source_id, profile_id=profile_id)
            if res['code'] != 200 or not res['data']:
                continue
            for scoring in res['data']:
                if scoring['filter_reference'] is None:
                    continue
                self.profile_id = profile_id
                self.profile_ref = str(profile['profile_reference'])
                self.filter_id = str(scoring['filter_id'])
                self.filter_ref = str(scoring['filter_reference'])
                if scoring['rating'] is not None:
                    self.rating = int(scoring['rating'])
                if scoring['stage'] is not None:
                    self.stage = str(scoring['stage'])
                break
            # keep a valid profile but keep looking until one with a reference
            # is found.
            if not profile['profile_reference']:
                continue
            break
        if self.profile_id is None:
            raise ValueError('no valid profiles found...')

    def gen_err_msg(self, resp):
        return "Response invalid: " + str(resp)

    def gen_webhook_request(self, type):
        data = {
            'type': type,
            'message': 'pou lou lou',
            'profile': {'profile_id': '1', 'profile_reference': 'I\'m free'}
        }
        json_data = json.dumps(data)
        webhook_secret = bytesutils.strtobytes(self.webhook_secret, 'ascii')
        json_data = bytesutils.strtobytes(json_data, 'utf8')
        hasher = hmac.new(webhook_secret, json_data, hashlib.sha256)
        encoded_sign = bytesutils.strtobytes(hasher.hexdigest(), 'ascii')
        byte_encoded_sign = base64.b64encode(encoded_sign)
        byte_json_data = base64.b64encode(json_data)
        sign = '{}.{}'.format(byte_encoded_sign.decode('ascii'), byte_json_data.decode('ascii'))
        res = {'HTTP-HRFLOW-SIGNATURE': sign}
        return res

    @staticmethod
    def get_instance():
        if TestHelper.instance is None:
            TestHelper.instance = TestHelper()
            TestHelper.instance.setup()
        return TestHelper.instance


# class TestProfile(unittest.TestCase):
#
#     def setUp(self):
#         self.helper = TestHelper.get_instance()
#         # init client and profile objects
#         self.client = Hrflow(api_key=self.helper.getKey())
#
#     def test_get_profiles(self):
#         # get all profiles
#         res = self.client.profile.list(source_ids=[self.helper.source_id])
#
#         # print(res)
#         self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
#
#     def test_filter_by_seniority_and_limit_response_size(self):
#         # filter profiles by seniority and limit
#         # other params can be tested in the same manner
#         res = self.client.profile.list(
#             source_ids=[self.helper.source_id],
#             seniority="junior",
#             limit=5
#             )
#         self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
#         self.assertLessEqual(len(res["data"]["profiles"]), 5)
#         for profile in res["data"]["profiles"]:
#             self.assertEqual(profile["seniority"], "junior")
#
#     def test_post_profile(self):
#         file_path = "test_assets/cv_test5.pdf"
#         res = self.client.profile.add(
#             source_id=self.helper.add_source_id,
#             file_path=file_path,
#         )
#         self.assertEqual(res["code"], 201, msg=self.helper.gen_err_msg(res))
#
#     def test_post_profile_with_metadata(self):
#         file_path = "test_assets/cv_test8.jpg"
#         metadata = [
#             {
#               "filter_reference": self.helper.filter_ref,
#               "stage": None,
#               "stage_timestamp": None,
#               "rating": 2,
#               "rating_timestamp": 1530607434
#             }
#           ]
#         res = self.client.profile.add(
#             source_id=self.helper.add_source_id,
#             file_path=file_path,
#             training_metadata=metadata,
#             profile_reference=str(random.randint(0, 999999)),
#             timestamp_reception=str(1530607434)
#         )
#         self.assertEqual(res["code"], 201, msg=self.helper.gen_err_msg(res))
#
#     def test_post_profile_with_bad_metadata(self):
#         file_path = "test_assets/cv_test8.jpg"
#         metadata = metadata = [
#             {
#               "filter_id": self.helper.filter_ref,
#               "stage": "None",
#               "stage_timestamp": None,
#               "rating": 2,
#               "rating_timestamp": 1530607434
#             }
#           ]
#         self.assertRaises(ValueError, self.client.profile.add,
#             self.helper.add_source_id,
#             file_path, str(random.randint(0, 999999)),
#             1530607434,
#             metadata)
#
#     def test_post_profiles(self):
#         dir_path = "test_assets/"
#         res = self.client.profile.addList(source_id=self.helper.add_source_id, dir_path=dir_path, is_recurcive=True)
#         if len(res['fail']) > 0:
#             for kf, failed in res['fail'].items():
#                 print('failed send: {}->{}\n', kf, failed)
#         self.assertEqual(len(res['success']), 3)
#
#     def test_get_profile(self):
#         res = self.client.profile.get(
#             source_id=self.helper.source_id,
#             profile_id=self.helper.profile_id,
#         )
#         self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
#
#     def test_get_profile_ref(self):
#         res = self.client.profile.get(
#             source_id=self.helper.source_id,
#             profile_reference=self.helper.profile_ref,
#         )
#         errMessage = ""
#         if not self.helper.profile_ref:
#             errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
#         self.assertEqual(res["code"], 200, msg=errMessage)
#
#     def test_get_documents(self):
#         res = self.client.profile.document.list(
#             source_id=self.helper.source_id,
#             profile_id=self.helper.profile_id,
#         )
#
#         self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
#
#     def test_get_documents_ref(self):
#         res = self.client.profile.document.list(
#             source_id=self.helper.source_id,
#             profile_reference=self.helper.profile_ref,
#         )
#         errMessage = ""
#         if not self.helper.profile_ref:
#             errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
#         self.assertEqual(res["code"], 200, msg=errMessage)
#
#     def test_get_parsing(self):
#         res = self.client.profile.parsing.get(
#             source_id=self.helper.source_id,
#             profile_id=self.helper.profile_id,
#         )
#
#         self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
#
#     def test_get_parsing_ref(self):
#         res = self.client.profile.parsing.get(
#             source_id=self.helper.source_id,
#             profile_reference=self.helper.profile_ref,
#         )
#         errMessage = ""
#         if not self.helper.profile_ref:
#             errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
#         self.assertEqual(res["code"], 200, msg=errMessage)
#
#     def test_get_scoring(self):
#         res = self.client.profile.scoring.list(
#             source_id=self.helper.source_id,
#             profile_id=self.helper.profile_id,
#         )
#
#         self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
#
#     def test_get_scoring_ref(self):
#         res = self.client.profile.scoring.list(
#             source_id=self.helper.source_id,
#             profile_reference=self.helper.profile_ref,
#         )
#         errMessage = ""
#         if not self.helper.profile_ref:
#             errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
#         self.assertEqual(res["code"], 200, msg=errMessage)
#
#     def test_update_stage(self):
#         res = self.client.profile.stage.set(
#             source_id=self.helper.source_id,
#             profile_id=self.helper.profile_id,
#             filter_id=self.helper.filter_id,
#             stage=self.helper.stage,
#         )
#         self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
#
#     def test_update_stage_ref(self):
#         res = self.client.profile.stage.set(
#             source_id=self.helper.source_id,
#             profile_reference=self.helper.profile_ref,
#             filter_reference=self.helper.filter_ref,
#             stage=self.helper.stage,
#         )
#         errMessage = self.helper.gen_err_msg(res)
#         if not self.helper.profile_ref or not self.helper.filter_ref:
#             errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
#         self.assertEqual(res["code"], 200, msg=errMessage)
#
#     def test_update_rating(self):
#         res = self.client.profile.rating.set(
#             source_id=self.helper.source_id,
#             profile_id=self.helper.profile_id,
#             filter_id=self.helper.filter_id,
#             rating=int(self.helper.rating),
#         )
#         self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
#
#     def test_update_rating_ref(self):
#         res = self.client.profile.rating.set(
#             source_id=self.helper.source_id,
#             profile_reference=self.helper.profile_ref,
#             filter_reference=self.helper.filter_ref,
#             rating=int(self.helper.rating),
#         )
#         errMessage = self.helper.gen_err_msg(res)
#         if not self.helper.profile_ref or not self.helper.filter_ref:
#             errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
#         self.assertEqual(res["code"], 200, msg=errMessage)
#
#     def test_check_profile_json(self):
#         metadata = [
#             {
#               "filter_reference": self.helper.filter_ref,
#               "stage": None,
#               "stage_timestamp": None,
#               "rating": 2,
#               "rating_timestamp": 1530607434
#             }
#           ]
#         profile_data = {
#             "name": "TESTSomone",
#             "phone": "+33689657412",
#             "email": "someone@someonelse.com",
#             "address": "1 rue de somexhereelse",
#             "location_details": {
#                 "text": "1 rue de somexhereelse",
#                 "lat": None,
#                 "lng": None,
#                 "gmaps": None
#             },
#             "summary": "I'm not just a test a a reel person!!!!",
#             "experiences": [
#               {
#                 "start": "15/02/2018",
#                 "end": "1/06/2018",
#                 "title": "Advisor",
#                 "company": "PwC luxembourg",
#                 "location_details": {
#                     "text": "Jupiter",
#                     "lat": None,
#                     "lng": None,
#                     "gmaps": None
#                 },
#                 "location": None,
#                 "description": "Doing IT integration and RPA"
#               }
#             ],
#             "educations": [
#               {
#                 "start": "2000",
#                 "end": "2018",
#                 "title": "Diplome d'ingenieur",
#                 "school": "UTT",
#                 "description": "Management des systemes d'information",
#                 "location_details": {
#                     "text": "Mars",
#                     "lat": None,
#                     "lng": None,
#                     "gmaps": None
#                 },
#                 "location": None,
#               }
#             ],
#             "skills": [
#               "manual skill",
#               "Creative spirit",
#               "Writing skills",
#               "Communication",
#               "Project management",
#               "French",
#               "German",
#               "Korean",
#               "English",
#               "Accounting",
#               "Human resources"
#             ],
#             "interests": [
#                 "Esquive",
#                 "Mathematiques",
#                 "Tennis",
#                 "Dors"
#             ],
#             "urls": {
#                 "from_resume": [],
#                 'linkedin': "",
#                 'twitter': "",
#                 'facebook': "",
#                 'github': "https://github.com/TESTSomone",
#                 'picture': ""
#             }
#           }
#         res = self.client.profile.json.check(
#             profile_data=profile_data,
#             training_metadata=metadata,
#         )
#         errMessage = self.helper.gen_err_msg(res)
#         self.assertEqual(res["code"], 200, msg=errMessage)
#
#     def test_check_profile_json_bad_metadata(self):
#         metadata = [
#             {
#               "filter_id": self.helper.filter_ref,
#               "stage": None,
#               "stage_timestamp": None,
#               "rating": 2,
#               "rating_timestamp": 1530607434
#             }
#           ]
#         profile_data = {
#             "name": "TESTSomone",
#             "phone": "+33689657412",
#             "email": "someone@someonelse.com",
#             "address": "1 rue de somexhereelse",
#             "location_details": {
#                 "text": "1 rue de somexhereelse",
#                 "lat": None,
#                 "lng": None,
#                 "gmaps": None
#             },
#             "summary": "I'm not just a test a a reel person!!!!",
#             "experiences": [
#               {
#                 "start": "15/02/2018",
#                 "end": "1/06/2018",
#                 "title": "Advisor",
#                 "company": "PwC luxembourg",
#                 "location_details": {
#                     "text": "Jupiter",
#                     "lat": None,
#                     "lng": None,
#                     "gmaps": None
#                 },
#                 "location": None,
#                 "description": "Doing IT integration and RPA"
#               }
#             ],
#             "educations": [
#               {
#                 "start": "2000",
#                 "end": "2018",
#                 "title": "Diplome d'ingenieur",
#                 "school": "UTT",
#                 "description": "Management des systemes d'information",
#                 "location_details": {
#                     "text": "Mars",
#                     "lat": None,
#                     "lng": None,
#                     "gmaps": None
#                 },
#                 "location": None,
#               }
#             ],
#             "skills": [
#               "manual skill",
#               "Creative spirit",
#               "Writing skills",
#               "Communication",
#               "Project management",
#               "French",
#               "German",
#               "Korean",
#               "English",
#               "Accounting",
#               "Human resources"
#             ],
#             "interests": [
#                 "Esquive",
#                 "Mathematiques",
#                 "Tennis",
#                 "Dors"
#             ],
#             "urls": {
#                 "from_resume": [],
#                 'linkedin': "",
#                 'twitter': "",
#                 'facebook': "",
#                 'github': "https://github.com/TESTSomone",
#                 'picture': ""
#             }
#           }
#         self.assertRaises(ValueError, self.client.profile.json.check,
#             profile_data,
#             metadata)
#
#     def test_check_profile_json_bad_profile_data(self):
#         metadata = [
#             {
#               "filter_reference": self.helper.filter_ref,
#               "stage": None,
#               "stage_timestamp": None,
#               "rating": 2,
#               "rating_timestamp": 1530607434
#             }
#           ]
#         profile_data = "Profile data !"
#         self.assertRaises(TypeError, self.client.profile.json.check,
#             profile_data,
#             metadata)
#
#     def test_add_profile_json(self):
#         metadata = [
#             {
#               "filter_reference": self.helper.filter_ref,
#               "stage": None,
#               "stage_timestamp": None,
#               "rating": 2,
#               "rating_timestamp": 1530607434
#             }
#           ]
#         profile_data = {
#             "name": "TESTSomone",
#             "phone": "+33689657412",
#             "email": "someone@someonelse.com",
#             "address": "1 rue de somexhereelse",
#             "location_details": {
#                 "text": "1 rue de somexhereelse",
#                 "lat": None,
#                 "lng": None,
#                 "gmaps": None
#             },
#             "summary": "I'm not just a test a a reel person!!!!",
#             "experiences": [
#               {
#                 "start": "15/02/2018",
#                 "end": "1/06/2018",
#                 "title": "Advisor",
#                 "company": "PwC luxembourg",
#                 "location_details": {
#                     "text": "Jupiter",
#                     "lat": None,
#                     "lng": None,
#                     "gmaps": None
#                 },
#                 "location": None,
#                 "description": "Doing IT integration and RPA"
#               }
#             ],
#             "educations": [
#               {
#                 "start": "2000",
#                 "end": "2018",
#                 "title": "Diplome d'ingenieur",
#                 "school": "UTT",
#                 "description": "Management des systemes d'information",
#                 "location_details": {
#                     "text": "Mars",
#                     "lat": None,
#                     "lng": None,
#                     "gmaps": None
#                 },
#                 "location": None,
#               }
#             ],
#             "skills": [
#               "manual skill",
#               "Creative spirit",
#               "Writing skills",
#               "Communication",
#               "Project management",
#               "French",
#               "German",
#               "Korean",
#               "English",
#               "Accounting",
#               "Human resources"
#             ],
#             "interests": [
#                 "Esquive",
#                 "Mathematiques",
#                 "Tennis",
#                 "Dors"
#             ],
#             "urls": {
#                 "from_resume": [],
#                 'linkedin': "",
#                 'twitter': "",
#                 'facebook': "",
#                 'github': "https://github.com/TESTSomone",
#                 'picture': ""
#             }
#           }
#         res = self.client.profile.json.add(
#             source_id=self.helper.add_source_id,
#             timestamp_reception=1530607434,
#             profile_data=profile_data,
#             training_metadata=metadata,
#             profile_reference=str(random.randint(0, 999999))
#         )
#         errMessage = self.helper.gen_err_msg(res)
#         self.assertEqual(res["code"], 201, msg=errMessage)
#
#
# def test_add_profile_json_bad_meta(self):
#     metadata = [
#         {
#           "zap": self.helper.filter_ref,
#           "stage": None,
#           "stage_timestamp": None,
#           "rating": 2,
#           "rating_timestamp": 1530607434
#         }
#       ]
#     profile_data = {
#         "name": "TESTSomone",
#         "phone": "+33689657412",
#         "email": "someone@someonelse.com",
#         "address": "1 rue de somexhereelse",
#         "location_details": {
#             "text": "1 rue de somexhereelse",
#             "lat": None,
#             "lng": None,
#             "gmaps": None
#         },
#         "summary": "I'm not just a test a a reel person!!!!",
#         "experiences": [
#           {
#             "start": "15/02/2018",
#             "end": "1/06/2018",
#             "title": "Advisor",
#             "company": "PwC luxembourg",
#             "location_details": {
#                 "text": "Jupiter",
#                 "lat": None,
#                 "lng": None,
#                 "gmaps": None
#             },
#             "location": None,
#             "description": "Doing IT integration and RPA"
#           }
#         ],
#         "educations": [
#           {
#             "start": "2000",
#             "end": "2018",
#             "title": "Diplome d'ingenieur",
#             "school": "UTT",
#             "description": "Management des systemes d'information",
#             "location_details": {
#                 "text": "Mars",
#                 "lat": None,
#                 "lng": None,
#                 "gmaps": None
#             },
#             "location": None,
#           }
#         ],
#         "skills": [
#           "manual skill",
#           "Creative spirit",
#           "Writing skills",
#           "Communication",
#           "Project management",
#           "French",
#           "German",
#           "Korean",
#           "English",
#           "Accounting",
#           "Human resources"
#         ],
#         "interests": [
#             "Esquive",
#             "Mathematiques",
#             "Tennis",
#             "Dors"
#         ],
#         "urls": {
#             "from_resume": [],
#             'linkedin': "",
#             'twitter': "",
#             'facebook': "",
#             'github': "https://github.com/TESTSomone",
#             'picture': ""
#         }
#       }
#     self.assertRaises(ValueError, self.client.profile.json.add,
#         self.helper.add_source_id,
#         profile_data,
#         metadata,
#         random.randint(0, 999999),
#         1530607434)
#
#
# def test_add_profile_json_bad_meta_null_ref(self):
#     metadata = [
#         {
#           "filter_reference": None,
#           "stage": None,
#           "stage_timestamp": None,
#           "rating": 2,
#           "rating_timestamp": 1530607434
#         }
#       ]
#     profile_data = {
#         "name": "TESTSomone",
#         "phone": "+33689657412",
#         "email": "someone@someonelse.com",
#         "address": "1 rue de somexhereelse",
#         "location_details": {
#             "text": "1 rue de somexhereelse",
#             "lat": None,
#             "lng": None,
#             "gmaps": None
#         },
#         "summary": "I'm not just a test a a reel person!!!!",
#         "experiences": [
#           {
#             "start": "15/02/2018",
#             "end": "1/06/2018",
#             "title": "Advisor",
#             "company": "PwC luxembourg",
#             "location_details": {
#                 "text": "Jupiter",
#                 "lat": None,
#                 "lng": None,
#                 "gmaps": None
#             },
#             "location": None,
#             "description": "Doing IT integration and RPA"
#           }
#         ],
#         "educations": [
#           {
#             "start": "2000",
#             "end": "2018",
#             "title": "Diplome d'ingenieur",
#             "school": "UTT",
#             "description": "Management des systemes d'information",
#             "location_details": {
#                 "text": "Mars",
#                 "lat": None,
#                 "lng": None,
#                 "gmaps": None
#             },
#             "location": None,
#           }
#         ],
#         "skills": [
#           "manual skill",
#           "Creative spirit",
#           "Writing skills",
#           "Communication",
#           "Project management",
#           "French",
#           "German",
#           "Korean",
#           "English",
#           "Accounting",
#           "Human resources"
#         ],
#         "interests": [
#             "Esquive",
#             "Mathematiques",
#             "Tennis",
#             "Dors"
#         ],
#         "urls": {
#             "from_resume": [],
#             'linkedin': "",
#             'twitter': "",
#             'facebook': "",
#             'github': "https://github.com/TESTSomone",
#             'picture': ""
#         }
#       }
#     self.assertRaises(ValueError, self.client.profile.json.add,
#         self.helper.add_source_id,
#         profile_data,
#         metadata,
#         random.randint(0, 999999),
#         1530607434)
#
#
# def test_add_profile_json_bad_profile_data(self):
#     metadata = [
#         {
#           "filter_reference": self.helper.filter_ref,
#           "stage": None,
#           "stage_timestamp": None,
#           "rating": 2,
#           "rating_timestamp": 1530607434
#         }
#       ]
#     profile_data = "Profile data !"
#     self.assertRaises(TypeError, self.client.profile.json.add,
#         self.helper.add_source_id,
#         profile_data,
#         metadata,
#         random.randint(0, 999999),
#         1530607434)


class TestSource(unittest.TestCase):

    def setUp(self):
        self.helper = TestHelper.get_instance()
        # init client and profile objects
        self.client = Client(api_key=self.helper.getKey())

    def test_get_sources(self):
        # get all sources
        res = self.client.source.list()

        # print(res)
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_get_source(self):
        # get one source by id
        res = self.client.source.get(
            source_id=self.helper.source_id
        )
        # print(res)
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))


# class TestFilter(unittest.TestCase):
#
#     def setUp(self):
#         self.helper = TestHelper.get_instance()
#         # init client and filter objects
#         self.client = Hrflow(api_key=self.helper.getKey())
#
#     def test_get_filters(self):
#         # get all filters
#         res = self.client.filter.list()
#
#         # print(res)
#         self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
#
#     def test_get_filter(self):
#         # get one filter by id
#         res = self.client.filter.get(
#             filter_id=self.helper.filter_id
#         )
#         # print(res)
#         self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
#
#     def test_get_filter_ref(self):
#         # get one filter by ref
#         res = self.client.filter.get(
#             filter_reference=self.helper.filter_ref
#         )
#         # print(res)
#         self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
#
#
# class TestWebhook(unittest.TestCase):
#
#     last_evt_type = None
#     last_decoded_request = None
#
#     @staticmethod
#     def handler(decoded_request, event_type):
#         TestWebhook.last_evt_type = event_type
#         TestWebhook.last_decoded_request = decoded_request
#
#     @staticmethod
#     def handler_one_arg(decoded_request):
#         TestWebhook.last_decoded_request = decoded_request
#
#     @staticmethod
#     def reset_test_value():
#         TestWebhook.last_evt_type = None
#         TestWebhook.last_decoded_request = None
#
#     def setUp(self):
#         self.helper = TestHelper.get_instance()
#         self.client = Hrflow(api_key=self.helper.getKey(), webhook_secret=self.helper.getWebhookSecret())
#
#     def test_post_check(self):
#         self.reset_test_value()
#         res = self.client.webhooks.check()
#         self.assertEqual(res['code'], 200, msg=self.helper.gen_err_msg(res))
#
#     def test_handle_request(self):
#         self.reset_test_value()
#         self.client.webhooks.setHandler(EVENT_FILTER_SCORE_ERROR, TestWebhook.handler)
#         webhook_req = self.helper.gen_webhook_request(EVENT_FILTER_SCORE_ERROR)
#         self.client.webhooks.handle(signature_header=webhook_req['HTTP-HRFLOW-SIGNATURE'])
#         self.assertEqual(TestWebhook.last_evt_type, EVENT_FILTER_SCORE_ERROR)
#         if 'profile' not in TestWebhook.last_decoded_request:
#             self.fail('Resquest is not full.')
#
#     def test_handle_request_with_full_header(self):
#         self.reset_test_value()
#         self.client.webhooks.setHandler(EVENT_FILTER_SCORE_ERROR, TestWebhook.handler)
#         webhook_req = self.helper.gen_webhook_request(EVENT_FILTER_SCORE_ERROR)
#         self.client.webhooks.handle(webhook_req)
#         self.assertEqual(TestWebhook.last_evt_type, EVENT_FILTER_SCORE_ERROR)
#         if 'profile' not in TestWebhook.last_decoded_request:
#             self.fail('Resquest is not full.')
#
#     def test_handle_request_with_full_header_one_arg(self):
#         self.reset_test_value()
#         self.client.webhooks.setHandler(EVENT_FILTER_SCORE_ERROR, TestWebhook.handler_one_arg)
#         webhook_req = self.helper.gen_webhook_request(EVENT_FILTER_SCORE_ERROR)
#         self.client.webhooks.handle(webhook_req)
#         if 'profile' not in TestWebhook.last_decoded_request:
#             self.fail('Resquest is not full.')
#
#     def test_handle_request_with_no_handler(self):
#         self.reset_test_value()
#         self.client.webhooks.setHandler(EVENT_FILTER_SCORE_START, TestWebhook.handler_one_arg)
#         webhook_req = self.helper.gen_webhook_request(EVENT_FILTER_SCORE_ERROR)
#         self.client.webhooks.handle(webhook_req)
#         self.assertEqual(TestWebhook.last_evt_type, None)
#         self.assertEqual(TestWebhook.last_decoded_request, None)


if __name__ == '__main__':
    unittest.main()