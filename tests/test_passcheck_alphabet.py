# coding: utf8
import unittest
from passcheck.alphabet import check_alphabet as ca
from passcheck.alphabet import AlphabetError

class TestPasscheckPasswordAlphabet(unittest.TestCase):

  def test_nil_string(self):
    self.assertEqual(ca(None), (False, AlphabetError.NIL_STRING))

  def test_empty_string(self):
    self.assertEqual(ca(""), (False, AlphabetError.NIL_STRING))

  def test_not_string(self):
    self.assertEqual(ca(123496789012345678901), (False, AlphabetError.BAD_TYPE))

  def test_short_one(self):
    self.assertEqual(ca("a1"), (False, AlphabetError.SHORT_PASS))

  def test_short_two(self):
    self.assertEqual(ca("a "), (False, AlphabetError.SHORT_PASS))

  def test_short_three(self):
    self.assertEqual(ca("a"), (False, AlphabetError.SHORT_PASS))

  def test_short_four(self):
    self.assertEqual(ca("33"), (False, AlphabetError.SHORT_PASS))

  def test_short_five(self):
    self.assertEqual(ca(r"öÜ"), (False, AlphabetError.SHORT_PASS))

  def test_regex_ddos(self):
    self.assertEqual(ca("A"*15000), (False, AlphabetError.TOO_LONG))

  def test_no_num_one(self):
    self.assertEqual(ca("abc!@#"), (False, AlphabetError.NO_NUMBERS))

  def test_no_num_two(self):
    self.assertEqual(ca("abc"), (False, AlphabetError.NO_NUMBERS))

  def test_no_num_three(self):
    self.assertEqual(ca("abc&FDF<>,"*30), (False, AlphabetError.NO_NUMBERS))

  def test_multiline_one(self):
    self.assertEqual(ca("\n\n\n\n"), (False, AlphabetError.HAS_SPACES))

  def test_multiline_two(self):
    self.assertEqual(ca("123abc!\n\n"), (False, AlphabetError.HAS_SPACES))

  def test_multiline_three(self):
    self.assertEqual(ca("123abc!\n"), (False, AlphabetError.HAS_SPACES))

  def test_multiline_four(self):
    self.assertEqual(ca("\n123abc!"), (False, AlphabetError.HAS_SPACES))

  def test_multiline_five(self):
    self.assertEqual(ca("123 abc!"), (False, AlphabetError.HAS_SPACES))

  def test_multiline_six(self):
    self.assertEqual(ca("123\tabc!"), (False, AlphabetError.HAS_SPACES))

  def test_non_printables_one(self):
    self.assertEqual(ca("1ab!\x00"), (False, AlphabetError.HAS_NON_PRINTABLES))

  def test_non_printables_two(self):
    self.assertEqual(ca("\x071ab!"), (False, AlphabetError.HAS_NON_PRINTABLES))

  def test_non_printables_three(self):
    self.assertEqual(ca("1ab!\u2029"), (False, AlphabetError.HAS_SPACES))

  def test_non_printables_four(self):
    self.assertEqual(ca("\u20281ab!"), (False, AlphabetError.HAS_SPACES))

  def test_non_printables_five(self):
    self.assertEqual(ca("\u30001ab!"), (False, AlphabetError.HAS_SPACES))

  def test_non_printables_six(self):
    self.assertEqual(ca("\u00831ab!"), (False, AlphabetError.HAS_NON_PRINTABLES))

  def test_non_printables_seven(self):
    self.assertEqual(ca("\u009F1ab!"), (False, AlphabetError.HAS_NON_PRINTABLES))

  def test_specials_one(self):
    self.assertEqual(ca("123qweASD"), (False, AlphabetError.NO_SPECIALS))

  def test_specials_two(self):
    self.assertEqual(ca("qwe234dfg"), (False, AlphabetError.NO_SPECIALS))

  # Notice, _ is a special here
  def test_specials_three(self):
    self.assertEqual(ca("_asdas12312"), (True, AlphabetError.OK))

  def test_specials_four(self):
    self.assertEqual(ca("123avb"+chr(0x1D94A)), (True, AlphabetError.OK))

  def test_specials_five(self):
    self.assertEqual(ca("123asd\u273d"), (True, AlphabetError.OK))

  def test_easy_passwords(self):
    with open('seclists/best110.txt') as f:
      for p in f.readlines():
        p = p.strip('\n')
        self.assertNotEqual(ca(p), (True, AlphabetError.OK))

  def test_medium_passwords(self):
    with open('goodpasswords/medium.txt') as f:
      for p in f.readlines():
        p = p.strip('\n')
        self.assertNotEqual(ca(p), (True, AlphabetError.OK))

  def test_good_passwords(self):
    with open('goodpasswords/good.txt') as f:
      for p in f.readlines():
        p = p.strip('\n')
        self.assertEqual(ca(p), (True, AlphabetError.OK))

if __name__ == '__main__':
  unittest.main()
