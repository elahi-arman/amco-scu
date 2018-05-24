import unittest

from . import constants
from . import endpoints

class TestEndpoints(unittest.TestCase):
  def test_get_quarter_with_invalid_quarter(self):
    """ Test that -1 is returned with an invalid quarter. """
    self.assertEqual(endpoints.get_quarter('', 2017), -1)

  def test_get_quarter_with_invalid_year(self):
    """ Test that -1 is returned with an invalid year. """
    self.assertEqual(endpoints.get_quarter('FALL', 2016), -1)

  def test_get_quarter(self):
    """ Test that you can get the correct offset. """
    self.assertEqual(endpoints.get_quarter('FALL', 2017), 3900)

  def test_getting_form_for_courses(self):
    """ Test getting correct form parameters for all courses. """
    form_data = endpoints.get_course_form_data(['COEN12'])
    self.assertDictContainsSubset(form_data[0], {'q': 'COEN+12', 'maxRes': 30})
  
  def test_getting_form_for_empty_list(self):
    """ Test getting correct form parameters for all courses. """
    form_data = endpoints.get_course_form_data([])
    self.assertListEqual(form_data, [])