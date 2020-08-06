import unittest
import hrflow as hf
from tests import config


class TestHelper:
    def __init__(self):
        self.api_secret = config.API_SECRET
        self.webhook_secret = config.WEBHOOK_SECRET
        self.source_key = config.SOURCE_KEY
        self.board_key = config.BOARD_KEY
        self.profile_key = config.PROFILE_KEY
        self.job_key = config.JOB_KEY
        self.profile_reference = config.PROFILE_REFERENCE

    def gen_err_msg(self, resp):
        return "Response invalid: " + str(resp)


class TestSource(unittest.TestCase):
    def setUp(self):
        self.helper = TestHelper()
        # init client and profile objects
        self.client = hf.Client(api_secret=self.helper.api_secret)

    def test_get_sources(self):
        # get all sources
        resp = self.client.source.list()
        self.assertEqual(resp["code"], 200, msg="Response invalid: " + str(resp))

    def test_get_source(self):
        # get one source by id
        resp = self.client.source.get(key=self.helper.source_key)
        self.assertEqual(resp["code"], 200, msg="Response invalid: " + str(resp))


class TestProfile(unittest.TestCase):

    def setUp(self):
        self.helper = TestHelper()
        # init client and profile objects
        self.client = hf.Client(api_secret=self.helper.api_secret)

    def test_searching_profiles(self):
        # get all profiles
        res = self.client.profile.searching.list(source_keys=[self.helper.source_key])

        # print(res)
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_filter_by_limit_response_size(self):
        # filter profiles by seniority and limit
        # other params can be tested in the same manner
        res = self.client.profile.searching.list(
            source_keys=[self.helper.source_key],
            sort_by='created_at', order_by="desc",
            limit=5
        )
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))
        self.assertLessEqual(len(res["data"]["profiles"]), 5)

    def test_post_profile_file(self):
        with open('cvs/cv_test.pdf', "rb") as f:
            profile_file = f.read()
        res = self.client.profile.parsing.add_file(
            source_key=self.helper.source_key,
            profile_file=profile_file,
        )
        self.assertEqual(res["code"], 202, msg=self.helper.gen_err_msg(res))

    def test_post_profiles(self):
        dir_path = "cvs/"
        res = self.client.profile.parsing.add_folder(source_key=self.helper.source_key, dir_path=dir_path,
                                                     is_recurcive=True)
        if len(res['fail']) > 0:
            for kf, failed in res['fail'].items():
                print('failed send: {}->{}\n', kf, failed)
        self.assertEqual(len(res['success']), 1)

    def test_get_profile_parsing(self):
        res = self.client.profile.parsing.get(
            source_key=self.helper.source_key,
            key=self.helper.profile_key,
        )
        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_get_profile_ref(self):
        res = self.client.profile.parsing.get(
            source_key=self.helper.source_key,
            reference=self.helper.profile_reference,
        )
        errMessage = ""
        if not self.helper.profile_reference:
            errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
        self.assertEqual(res["code"], 200, msg=errMessage)

    def test_get_attachment(self):
        res = self.client.profile.attachment.list(
            source_key=self.helper.source_key,
            key=self.helper.profile_key,
        )

        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_get_attachment_ref(self):
        res = self.client.profile.attachment.list(
            source_key=self.helper.source_key,
            reference=self.helper.profile_reference,
        )
        errMessage = ""
        if not self.helper.profile_reference:
            errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
        self.assertEqual(res["code"], 200, msg=errMessage)

    def test_get_profile(self):
        res = self.client.profile.indexing.get(
            source_key=self.helper.source_key,
            key=self.helper.profile_key,
        )

        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_get_parsing_ref(self):
        res = self.client.profile.indexing.get(
            source_key=self.helper.source_key,
            reference=self.helper.profile_reference,
        )
        errMessage = ""
        if not self.helper.profile_reference:
            errMessage = "No profile reference found: " + self.helper.gen_err_msg(res)
        self.assertEqual(res["code"], 200, msg=errMessage)

    def test_scoring_profiles(self):
        res = self.client.profile.scoring.list(
            source_keys=[self.helper.source_key],
            board_key=self.helper.board_key,
            job_key=self.helper.job_key,
            use_agent=1
        )

        self.assertEqual(res["code"], 200, msg=self.helper.gen_err_msg(res))

    def test_index_profile_json(self):
        profile_json = {
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
            "info": {
                "full_name": "Harry Potter",
                "first_name": "Harry",
                "last_name": "Potter",
                "email": "harry.potter@gmail.com",
                "phone": "0202",
                "gender": None,
                "urls": {
                    "from_resume": [],
                    "linkedin": "",
                    "twitter": "",
                    "facebook": "",
                    "github": "",
                    "picture": ""},
                "picture": None,
                "location": {"text": None},
                "summary": "Brief summary"
            },
            "text": "test text",
            "experiences": [{
                "date_start": "15/02/1900",
                "date_end": "",
                "title": "Lead",
                "company": "Mathematic Departement",
                "location": {"text": "Paris"},
                "description": "Developping."
            }],
            "experiences_duration": 5,
            "educations": [{
                "date_start": "12540",
                "date_end": "12550",
                "title": "Mathematicien",
                "school": "University",
                "description": "Description",
                "location": {"text": "Scotland"}
            }],
            "educations_duration": 4,
            "skills": [{"name": "manual skill", "value": None}, {"name": "Creative spirit", "value": None},
                       {"name": "Writing skills", "value": None}, {"name": "Communication", "value": None}],
            "languages": [{"name": "english", "value": None}],
            "interests": [{"name": "football", "value": None}],
            "tags": [{"name": "archive", "value": True}],
            "metadatas": [],
            "labels": [{"stage": "yes", "job_id": "job_id"}],
            "attachments": []
        }

        res = self.client.profile.indexing.add_json(source_key=self.helper.source_key, profile_json=profile_json)
        self.assertEqual(res["code"], 201, msg=self.helper.gen_err_msg(res))


if __name__ == '__main__':
    unittest.main()
