import requests, os
from datetime import datetime
from unittest import mock, TestCase, main
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env')

class TestAPI(TestCase):

  @classmethod
  def setUpClass(cls):

    cls.url = 'http://127.0.0.1:8000/test/'
  
  def api_struc_params(self):

    params_get_request = {
            "from_date": None,
            "to_date": None,
            "interval": None,
            "repository": "kubernetes/kubernetes",
            "sort": 1
        }
    
    return params_get_request
    

  def test_hour_metric(self):

    params_get_request = self.api_struc_params()

    params_get_request['from_date'] = '2021-10-18'
    params_get_request['to_date'] = '2021-10-18'
    params_get_request['interval'] = 'hour'

    api_response = requests.get(self.url,
      params=params_get_request
      ).json()['timestamps']

    first_obtained_api_response = api_response[0]

    expected_response = {'timestamp': '2021-10-18T01:00:00+00:00', 'count': 1}

    self.assertEqual(first_obtained_api_response, expected_response)

  
  def test_day_metric(self):

    params_get_request = self.api_struc_params()

    params_get_request['from_date'] = '2021-10-17'
    params_get_request['to_date'] = '2021-10-19'
    params_get_request['interval'] = 'day'

    api_response = requests.get(self.url,
      params=params_get_request).json()['timestamps']

    count_day_1 = api_response[0]['count']
    count_day_2 = api_response[1]['count']
    count_day_3 = api_response[2]['count']

    self.assertEqual(count_day_1, 3)
    self.assertEqual(count_day_2, 12)
    self.assertEqual(count_day_3, 14)


  def test_week_metric(self):

    params_get_request = self.api_struc_params()

    params_get_request['from_date'] = '2021-09-17'
    params_get_request['to_date'] = '2021-10-19'
    params_get_request['interval'] = 'week'

    api_response = requests.get(self.url,
      params=params_get_request).json()['timestamps']

    response_week_1 = api_response[0]
    response_week_2 = api_response[1]
    response_week_3 = api_response[2]
    response_week_4 = api_response[3]
    response_week_5 = api_response[4]

    expected_response_1 = {'timestamp': '2021-09-20T00:00:00+00:00', 'count': 20}
    expected_response_2 = {'timestamp': '2021-09-27T00:00:00+00:00', 'count': 32}
    expected_response_3 = {'timestamp': '2021-10-04T00:00:00+00:00', 'count': 47}
    expected_response_4 = {'timestamp': '2021-10-11T00:00:00+00:00', 'count': 37}
    expected_response_5 = {'timestamp': '2021-10-18T00:00:00+00:00', 'count': 52}

    self.assertEqual(response_week_1, expected_response_1)
    self.assertEqual(response_week_2, expected_response_2)
    self.assertEqual(response_week_3, expected_response_3)
    self.assertEqual(response_week_4, expected_response_4)
    self.assertEqual(response_week_5, expected_response_5)

  
  def test_month_metric(self):

    params_get_request = self.api_struc_params()

    params_get_request['from_date'] = '2021-06-01'
    params_get_request['to_date'] = '2021-09-30'
    params_get_request['interval'] = 'month'

    api_response = requests.get(self.url,
      params=params_get_request).json()['timestamps']

    response_month_06 = api_response[0]
    response_month_07 = api_response[1]
    response_month_08 = api_response[2]
    response_month_09 = api_response[3]

    expected_month_06 = {'timestamp': '2021-06-01T00:00:00+00:00', 'count': 102}
    expected_month_07 = {'timestamp': '2021-07-01T00:00:00+00:00', 'count': 84}
    expected_month_08 = {'timestamp': '2021-08-01T00:00:00+00:00', 'count': 86}
    expected_month_09 = {'timestamp': '2021-09-01T00:00:00+00:00', 'count': 143}

    self.assertEqual(response_month_06, expected_month_06)
    self.assertEqual(response_month_07, expected_month_07)
    self.assertEqual(response_month_08, expected_month_08)
    self.assertEqual(response_month_09, expected_month_09)


  def test_repository_non_existent(self):

    params_get_request = self.api_struc_params()
    params_get_request['from_date'] = '2021-10-01'
    params_get_request['to_date'] = '2021-10-17'
    params_get_request['interval'] = 'month'

    params_get_request['repository'] = 'Nonexistent_repository_for_testing'

    api_response = requests.get(self.url,
      params=params_get_request).json()
    
    success_response = api_response['success']
    reponse_code_not_200 = api_response['reponse_code_not_200']
    response_repository_not_found = api_response['repository_not_found']

    expected_success_response = False
    expected_reponse_code_not_200 = True
    expected_response_repository_not_found = True
    
    self.assertEqual(success_response, expected_success_response)
    self.assertEqual(reponse_code_not_200, expected_reponse_code_not_200)
    self.assertEqual(response_repository_not_found, expected_response_repository_not_found)


if __name__ == '__main__':
  main()
