from enum import Enum

GOOD_MINIMAL_LENGTH = 16
SHORT_MINIMAL_LENGTH = 6

class LengthError(Enum):
  OK = 0
  NIL_STRING = 1
  SHORT_MIN = 2
  SHORT_PASS = 3
  BAD_MIN = 4
  BAD_TYPE = 5

def check_length(password, required_minimum_length = GOOD_MINIMAL_LENGTH):
  """Verifies that the password has at least the required_minimum_length.
  The return value is a tuple: (boolean success, LengthError error_code).

  OK - all is Ok
  NIL_STRING - the string provided is nil or empty
  SHORT_MIN - required password length is too short
  SHORT_PASS - password provided is too short
  BAD_MIN - the required minimum length parameter is not an integer
  BAD_TYPE - the passwords provided is not a string

  The only one good positive result is (True, LengthError.OK).

  """

  if not password:
    return (False, LengthError.NIL_STRING)

  if not isinstance(password, str):
    return (False, LengthError.BAD_TYPE)

  if not isinstance(required_minimum_length, int):
    return (False, LengthError.BAD_MIN)

  if SHORT_MINIMAL_LENGTH >= required_minimum_length:
    return (False, LengthError.SHORT_MIN)

  if len ( password ) >= required_minimum_length:
    return (True, LengthError.OK if required_minimum_length >= GOOD_MINIMAL_LENGTH else LengthError.SHORT_MIN)

  return (False, LengthError.SHORT_PASS)
