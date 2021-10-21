from fastapi import FastAPI
import requests, os
from datetime import datetime, date, timezone, timedelta

from coding_challenge import calculate_datetimes_between

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict

from dotenv import load_dotenv
import main

load_dotenv(dotenv_path='.env')

"""
Use the following command to run the application:
<$ python -m uvicorn main:app --reload >
"""

app = FastAPI()

def define_response_structure():
  api_response_dict = {
    'repository': None,
    'url': None,
    'timestamps': [],
    'success': True,
    'reponse_code_not_200': False,
    'repository_not_found': False
  }

  return api_response_dict


class Interval(str, Enum):
    hour = "hour"
    day = "day"
    week = "week"
    month = "month"


def selection_interval(interval_str):

  interval_dict = {
    'hour': Interval.hour,
    'day': Interval.day,
    'week': Interval.week,
    'month': Interval.month
  }

  return interval_dict[interval_str]


def formatting_github_datetime_response(list_to_be_formatted, interval, from_date, to_date):

  date_limit = False
  list_of_formatted_dates = []

  if interval == 'hour':
    for single_entry in list_to_be_formatted:

      single_date = single_entry['created_at']

      year = int(single_date.split('-')[0])
      month = int(single_date.split('-')[1])
      day = int(single_date.split('-')[2][:2])
      hour = int(single_date.split('-')[2][3:5])

      final_single_date = datetime(year, month, day, hour, tzinfo=timezone.utc)

      if final_single_date.date() < from_date:
        date_limit = True
        break
      
      if final_single_date.date() <= to_date:
        list_of_formatted_dates.append(final_single_date)
    

  if interval == 'day':
    for single_entry in list_to_be_formatted:

      single_date = single_entry['created_at']

      year = int(single_date.split('-')[0])
      month = int(single_date.split('-')[1])
      day = int(single_date.split('-')[2][:2])

      final_single_date = datetime(year, month, day, tzinfo=timezone.utc)
  
      if final_single_date.date() < from_date:
        date_limit = True
        break
      
      if final_single_date.date() <= to_date:
        list_of_formatted_dates.append(final_single_date)
  

  if interval == 'week':
    for single_entry in list_to_be_formatted:

      single_date = single_entry['created_at']

      year = int(single_date.split('-')[0])
      month = int(single_date.split('-')[1])
      day = int(single_date.split('-')[2][:2])

      pre_final = datetime(year, month, day, tzinfo=timezone.utc)
      final_single_date = datetime(pre_final.year, pre_final.month, (pre_final - timedelta(pre_final.weekday())).day, tzinfo=timezone.utc)
  
      if final_single_date.date() < from_date:
        date_limit = True
        break

      if final_single_date.date() <= to_date:
        list_of_formatted_dates.append(final_single_date)


  if interval == 'month':
    for single_entry in list_to_be_formatted:

      single_date = single_entry['created_at']

      year = int(single_date.split('-')[0])
      month = int(single_date.split('-')[1])
      day = int(single_date.split('-')[2][:2])

      final_single_date = datetime(year, month, day, tzinfo=timezone.utc)
      if final_single_date.date() < from_date:
        date_limit = True
        break
      
      if final_single_date.date() <= to_date:
        final_single_date = datetime(year, month, 1, tzinfo=timezone.utc)
        list_of_formatted_dates.append(final_single_date)


  return list_of_formatted_dates, date_limit


@app.get('/test')
def connect(from_date, to_date, interval, repository, sort):

  timestamp_count_dict = {}

  url = f'https://api.github.com/repos/{repository}/pulls'

  number_of_returned_entries_api = 100
  
  params = { 'page': 1, 'per_page': 100 }
  headers = { 'Authorization': 'token %s' % os.getenv('github_auth_token') }

  api_response_dict = define_response_structure()
  api_response_dict['repository'] = repository
  api_response_dict['url'] = url

  from_date = date(int(from_date.split('-')[0]) ,int(from_date.split('-')[1]), int(from_date.split('-')[2]))
  to_date = date( int(to_date.split('-')[0]) ,int(to_date.split('-')[1]), int(to_date.split('-')[2]))

  calculate_datetimes = calculate_datetimes_between(from_date, to_date, selection_interval(interval))

  if not calculate_datetimes:
    return api_response_dict


  while(True):

    response = requests.get(url, params=params, headers=headers)
    if not response.ok:
      api_response_dict['success'] = False
      if response.status_code != 200:
        api_response_dict['reponse_code_not_200'] = True
      if response.status_code == 404:
        api_response_dict['repository_not_found'] = True
      return api_response_dict

    response_json = response.json()

    list_of_formatted_dates, date_limit = formatting_github_datetime_response(response_json, interval, from_date, to_date)

    for calculate_datetime in calculate_datetimes:
      count = list_of_formatted_dates.count(calculate_datetime)

      if count:
        if calculate_datetime in timestamp_count_dict:
          timestamp_count_dict[calculate_datetime] = timestamp_count_dict[calculate_datetime] + count
        else:
          timestamp_count_dict[calculate_datetime] = count

        #api_response_dict['timestamps'].append( {'timestamp': calculate_datetime, 'count': count } )

    if len(response_json) < number_of_returned_entries_api or date_limit:
      break
      
    params['page'] += 1
  
  for timestamp, count in timestamp_count_dict.items():
    api_response_dict['timestamps'].append( {'timestamp': timestamp, 'count': count } )

  if sort:
    api_response_dict['timestamps'] = sorted(api_response_dict['timestamps'], key = lambda i: i['timestamp']) 

  return api_response_dict
