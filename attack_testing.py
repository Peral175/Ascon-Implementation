import unittest
import pathlib
import AES_ExactMatch
import AES_LDA
import ASCON_ExactMatch
import ASCON_LDA


class TestStringMethods(unittest.TestCase):

    t = 150
    tr_aes_clear = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2_clear/")
    tr_ascon_clear = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/ascon128_2R_simplified-clear/")
    w = 128
    s = 64

    def test_aes_exact(self):
        r = AES_ExactMatch.attack(self.t, self.tr_aes_clear)
        self.assertEqual(True, r[0])

    def test_ascon_exact(self):
        r = ASCON_ExactMatch.attack(self.t, self.tr_ascon_clear)
        self.assertEqual(True, r[0])

    def test_aes_lda(self):
        r = AES_LDA.attack(self.t, self.tr_aes_clear, self.w, self.s)
        self.assertEqual(True, r[0])

    def test_ascon_lda(self):
        r = ASCON_LDA.attack(self.t, self.tr_ascon_clear, self.w, self.s)
        self.assertEqual(True, r[0])


if __name__ == '__main__':
    unittest.main()
