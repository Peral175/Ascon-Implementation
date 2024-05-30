import unittest
import pathlib
import AES_ExactMatch
import AES_LDA
import ASCON_ExactMatch
import ASCON_LDA


class TestStringMethods(unittest.TestCase):

    t = 150
    tr_aes_clear = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-clear/")
    tr_aes_isw_2 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-isw2/")
    tr_ascon_clear = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/ascon128_2R_simplified-clear/")
    tr_ascon_isw_2 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/ascon128_2R_simplified-isw_2/")
    w = 128
    s = 64

    # todo: assertEqual False

    def test_aes_exact_clear(self):
        r = AES_ExactMatch.attack(self.t, self.tr_aes_clear)
        self.assertEqual(True, r[0])

    def test_ascon_exact_clear(self):
        r = ASCON_ExactMatch.attack(self.t, self.tr_ascon_clear)
        self.assertEqual(True, r[0])

    def test_aes_lda_clear(self):
        r = AES_LDA.attack(self.t, self.tr_aes_clear, self.w, self.s)
        self.assertEqual(True, r[0])

    def test_aes_lda_isw_2(self):
        r = AES_LDA.attack(self.t, self.tr_aes_isw_2, self.w, self.s)
        self.assertEqual(True, r[0])

    def test_ascon_lda_clear(self):
        r = ASCON_LDA.attack(self.t, self.tr_ascon_clear, self.w, self.s)
        self.assertEqual(True, r[0])

    # def test_ascon_lda_isw_2(self):
    #     r = ASCON_LDA.attack(512, self.tr_ascon_isw_2, 256, 128)
    #     self.assertEqual(True, r[0])


if __name__ == '__main__':
    unittest.main()
