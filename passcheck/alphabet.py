from enum import Enum
import re
import unicodedata

# This is used to prevent regex DDoS attacks
MAXIMAL_PASSWORD_LENGTH = 1000

# Shorter passwords can not contain number, letter, and a special character
MINIMAL_PASSWORD_LENGTH = 3

WHITE_SPACE_RE = re.compile(r'\s+', re.MULTILINE)

NUMBER_RE = re.compile(r'\d+')

# See this one: https://en.wikipedia.org/wiki/Unicode_character_property
NON_PRINTABLE_CATEGORIES = ['Zs', 'Zl', 'Zp', 'Cc', 'Cf', 'Cs', 'Co', 'Cn']

def is_non_printable(c):
  return True if unicodedata.category(c) in NON_PRINTABLE_CATEGORIES else False

# See this one: https://en.wikipedia.org/wiki/Unicode_character_property
LETTER_CATEGORIES = ['Lu', 'Ll', 'Lt', 'Lo']

def is_letter(c):
  return True if unicodedata.category(c) in LETTER_CATEGORIES else False

# See this one: https://en.wikipedia.org/wiki/Unicode_character_property
SPECIAL_CATEGORIES = ['Lm', 'Mn', 'Mc', 'Pd', 'Pc', 'Ps', 'Pe', 'Pi', 'Pf', 'Po', 'Sm', 'Sc', 'Sk', 'So']

def is_special(c):
  return True if unicodedata.category(c) in SPECIAL_CATEGORIES else False

class AlphabetError(Enum):
  OK = 0
  NIL_STRING = 1
  TOO_LONG = 2
  SHORT_PASS = 3
  HAS_SPACES = 4
  NO_NUMBERS = 5
  NO_LETTERS = 6
  NO_SPECIALS = 7
  BAD_TYPE = 8
  HAS_NON_PRINTABLES = 9

def check_alphabet(password):
  """Verifies that the password has at least one letter, one number, one special symbol,
  no spaces, and is not empty.
  The return value is a tuple: (boolean success, AlphabetError error_code).

  OK - all is Ok
  NIL_STRING - the string provided is nil or empty
  TOO_LONG - the string provided is way too long, it might be a DDoS attack!
  SHORT_PASS - password provided is too short
  HAS_SPACES - password provided contains spaces
  NO_NUMBERS - password provided contains no numbers
  NO_LETTERS - password provided contains no letters
  NO_SPECIALS - password provided contains no special characters (_, punctuation, symbols)
  BAD_TYPE - password provided is not of string type
  HAS_NON_PRINTABLE - passwords contains new line sing or something else non-printable

  The only one good positive result is (True, AlphabetError.OK).
  """
  if not password:
    return (False, AlphabetError.NIL_STRING)

  if not isinstance(password, str):
    return (False, AlphabetError.BAD_TYPE)

  if MINIMAL_PASSWORD_LENGTH > len( password ):
    return (False, AlphabetError.SHORT_PASS)

  if MAXIMAL_PASSWORD_LENGTH <= len( password ):
    return (False, AlphabetError.TOO_LONG)

  if WHITE_SPACE_RE.search(password) is not None:
    return (False, AlphabetError.HAS_SPACES)

  if NUMBER_RE.search(password) is None:
    return (False, AlphabetError.NO_NUMBERS)

  for c in password:
    if is_non_printable(c):
      return (False, AlphabetError.HAS_NON_PRINTABLES)


  if any(is_non_printable(c) for c in password):
    return (False, AlphabetError.HAS_NON_PRINTABLES)

  if not any(is_special(c) for c in password):
    return (False, AlphabetError.NO_SPECIALS)

  return (True, AlphabetError.OK)
