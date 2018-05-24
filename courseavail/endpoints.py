import json
import re

import requests
from . import constants

COURSE_REGEX = re.compile(r'([a-zA-Z]*)\s*([0-9]*)')

def get_quarter(quarter, year):
  """ Returns the search parameter based on the quarters and the year or -1. """
  if quarter not in constants.QUARTERS.keys():
    return -1
  
  if year < 2017:
    return -1

  return ((year - 2017) * 100 + 3900) + constants.QUARTERS[quarter]

def get_course_form_data(courses):
  """ Returns a dictionary for each element of courses. """
  form_parameters = []
  
  for course in courses:
    split_course = re.match(COURSE_REGEX, course)
    if split_course is not None:
      form_parameters.append({
        'q': (None, '{} {}'.format(split_course.group(1), split_course.group(2))),
        'maxRes': (None, '30')      # form data needs to be a string
      })
    else:
      print('No match for {}'.format(course))
  return form_parameters

def is_class_open(url, formData):
  # https://franklingu.github.io/programming/2017/10/30/post-multipart-form-data-using-requests/
  response = requests.post(url, files=formData)
  
  if response.status_code == 200: 
    return convert_body_to_dict(response.json())
  else:
    return []


def extract_course_keys(search_result):
  """ Returns the relevant keys for the search result. """
  # refer to https://www.scu.edu/apps/ws/courseavail/search/3920/ for keys
  if int(search_result['seats_remaining']) >= 0 :
    seats = search_result['seats_remaining']
  else:
    seats = 0

  return {
    'class_number': search_result['class_nbr'],
    'class_time': '{} @ {}:{}'.format(search_result['mtg_days_1'], search_result['c_hrstart'], search_result['c_mnstart']),
    'class': search_result['mtg_facility_1'],
    'teacher': search_result['instr_1'],
    'is_open': search_result['has_seats'] == 1,
    'remaining_seats': seats
  }

def convert_body_to_dict(body):
  """ Converts a request body dictionary to the keys we actually care about. """
  courses = []
  search_results = body['results']
  for sr in search_results:
    courses.append(extract_course_keys(sr))
  return courses
