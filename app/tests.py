from datetime import datetime, timedelta
from unittest import TestCase

import boto3
from fastapi.testclient import TestClient
from freezegun import freeze_time
from moto import mock_iam

from main import app


@mock_iam
class TestOrganizer(TestCase):
    def setUp(self):
        self.client = TestClient(app)

        self.iam = boto3.resource('iam')
        self.user_create_key_now = self.iam.create_user(UserName='user_create_key_now')
        self.user_create_key_1h_ago = self.iam.create_user(UserName='user_create_key_1h_ago')
        self.user_create_key_2h_ago = self.iam.create_user(UserName='user_create_key_2h_ago')
        self.user_create_key_3h_ago = self.iam.create_user(UserName='user_create_key_3h_ago')
        self.user_create_key_4h_ago = self.iam.create_user(UserName='user_create_key_4h_ago')
        self.user_create_key_5h_ago = self.iam.create_user(UserName='user_created_key_5h_ago')

        self.current_datetime = datetime.utcnow()
        with freeze_time(self.current_datetime - timedelta(hours=5)) as frozen_datetime:
            self.user_create_key_5h_ago.create_access_key_pair()

            frozen_datetime.tick(delta=timedelta(hours=1))
            self.user_create_key_4h_ago.create_access_key_pair()

            frozen_datetime.tick(delta=timedelta(hours=1))
            self.user_create_key_3h_ago.create_access_key_pair()

            frozen_datetime.tick(delta=timedelta(hours=1))
            self.user_create_key_2h_ago.create_access_key_pair()

            frozen_datetime.tick(delta=timedelta(hours=1))
            self.user_create_key_1h_ago.create_access_key_pair()

            frozen_datetime.tick(delta=timedelta(hours=1))
            self.user_create_key_now.create_access_key_pair()

    def test_when_no_parameter_is_given__raises_error(self):
        responses = self.client.get('/find')
        self.assertEqual(responses.status_code, 422)

    def test_when_wrong_type_of_parameters_are_given__raises_error(self):
        responses = self.client.get('/find', params={'age_hours': 'one'})
        self.assertEqual(responses.status_code, 422)

    def test_find(self):
        with freeze_time(self.current_datetime):
            with self.subTest('find access keys older than 1 hour'):
                response = self.client.get('/find', params={'age_hours': 1})

                json_response = response.json()
                result = json_response['result']
                self.assertEqual(response.status_code, 200)
                self.assertEqual({i['username'] for i in result},
                                 {self.user_create_key_1h_ago.user_name,
                                  self.user_create_key_2h_ago.user_name,
                                  self.user_create_key_3h_ago.user_name,
                                  self.user_create_key_4h_ago.user_name,
                                  self.user_create_key_5h_ago.user_name})

            with self.subTest('find access keys older than 2 hours'):
                response = self.client.get('/find', params={'age_hours': 2})

                json_response = response.json()
                result = json_response['result']
                self.assertEqual({i['username'] for i in result},
                                 {self.user_create_key_2h_ago.user_name,
                                  self.user_create_key_3h_ago.user_name,
                                  self.user_create_key_4h_ago.user_name,
                                  self.user_create_key_5h_ago.user_name})

            with self.subTest('find access keys older than 3 hours'):
                response = self.client.get('/find', params={'age_hours': 3})

                json_response = response.json()
                result = json_response['result']
                self.assertEqual({i['username'] for i in result},
                                 {self.user_create_key_3h_ago.user_name,
                                  self.user_create_key_4h_ago.user_name,
                                  self.user_create_key_5h_ago.user_name})

            with self.subTest('find access keys older than 4 hours'):
                response = self.client.get('/find', params={'age_hours': 4})

                json_response = response.json()
                result = json_response['result']
                self.assertEqual({i['username'] for i in result},
                                 {self.user_create_key_4h_ago.user_name,
                                  self.user_create_key_5h_ago.user_name})
