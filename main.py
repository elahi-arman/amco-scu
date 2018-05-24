import argparse

from utils import info, warn, success, error

from courseavail import endpoints
from courseavail import constants

parser = argparse.ArgumentParser(description='Check if your classes are still open.')
parser.add_argument('quarter', type=str, help='One of ["FALL", "SPRING", "WINTER", "SUMMER"]')
parser.add_argument('year', type=int, help='Some year >= 2017')
parser.add_argument('classes', type=str, nargs='+', help="Classes that you're trying to verify are open")

args = parser.parse_args()

endpoint = constants.BASE_URL + str(endpoints.get_quarter(args.quarter, args.year))
courses = endpoints.get_course_form_data(args.classes)

for course in courses:
  print('\n')  
  print('{}\n---\n'.format(course['q'][1]))
  print('ID\t|\tTIME\t|\tSEATS\t|\tTEACHER')
  for cd in endpoints.is_class_open(endpoint, course):
    formatted = '{}\t|  {}\t|\t{}\t|{}\t'.format(cd['class_number'], cd['class_time'], cd['remaining_seats'], cd['teacher'])
    if cd['is_open']:
      success(formatted)
    else:
      error(formatted)
  print('\n')


  