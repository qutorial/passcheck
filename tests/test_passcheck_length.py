import unittest
from passcheck.length import check_length as cl
from passcheck.length import LengthError

class TestPasscheckPasswordLength(unittest.TestCase):

  def test_nil_string(self):
    self.assertEqual(cl(None), (False, LengthError.NIL_STRING))

  def test_nil_req_length(self):
    self.assertEqual(cl(None, None), (False, LengthError.NIL_STRING))

  def test_nil_req_length_nones(self):
    self.assertEqual(cl("Hello", None), (False, LengthError.BAD_MIN))

  def test_short_one(self):
    self.assertEqual(cl("Hello"), (False, LengthError.SHORT_PASS))

  def test_short_two(self):
    self.assertEqual(cl("123456789012345"), (False, LengthError.SHORT_PASS))

  def test_ok_one(self):
    self.assertEqual(cl("1234567890123456"), (True, LengthError.OK))

  def test_ok_two(self):
    self.assertEqual(cl("12345678901234567"), (True, LengthError.OK))

  def test_ok_three(self):
    self.assertEqual(cl("123456789012", 12), (True, LengthError.SHORT_MIN))

  def test_ok_short_min(self):
    self.assertEqual(cl("12345678901", 11), (True, LengthError.SHORT_MIN))

  def test_not_ok_short_min(self):
    self.assertEqual(cl("1234", 4), (False, LengthError.SHORT_MIN))

  def test_not_ok_short_pass(self):
    self.assertEqual(cl("1234967890123456789", 20), (False, LengthError.SHORT_PASS))

  def test_ok_greater_min(self):
    self.assertEqual(cl("12349678901234567890", 20), (True, LengthError.OK))

  def test_ok_greater_min_more(self):
    self.assertEqual(cl("123496789012345678901", 20), (True, LengthError.OK))

  def test_not_string_one(self):
    self.assertEqual(cl(123496789012345678901, 20), (False, LengthError.BAD_TYPE))

  def test_not_string_two(self):
    self.assertEqual(cl(123496789012345678901, 0), (False, LengthError.BAD_TYPE))

  def test_not_string_three(self):
    self.assertEqual(cl(123496789012345678901, None), (False, LengthError.BAD_TYPE))

  def test_not_string_four(self):
    self.assertEqual(cl(123496789012345678901), (False, LengthError.BAD_TYPE))

if __name__ == '__main__':
  unittest.main()
