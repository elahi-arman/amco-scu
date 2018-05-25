import argparse

from utils import info, warn, success, error

from courseavail import endpoints
from courseavail import constants

def createCLIParser():
    """
    Creates a argparse.ArgumentParser with quarter, year, and classes parameters.

    Returns:
    parser -- argparse.ArgumentParser to be used for CLI scripts
    """
    parser = argparse.ArgumentParser(description='Check if your classes are still open.')
    parser.add_argument('quarter', type=str, help='One of ["FALL", "SPRING", "WINTER", "SUMMER"]')
    parser.add_argument('year', type=int, help='Some year >= 2017')
    parser.add_argument('classes', type=str, nargs='+', help="Classes that you're trying to verify are open")
    return parser



def lookupCourses(endpoint, courses):
    """
    Using the courseavail package to determine if classes are open, printing them onto stdout

    Positional Arguments:
    endpoint (string) - the endpoint for courseavail where the request should be sent
    courses  (list)   - the list of courses to send to lookup
    
    Returns:
    None
    """
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


def main():
    parser = createCLIParser()
    args = parser.parse_args()
    endpoint = constants.BASE_URL + str(endpoints.get_quarter(args.quarter, args.year))
    courses = endpoints.get_course_form_data(args.classes)
    lookupCourses(endpoint, courses)


if __name__ == '__main__':
  main()
