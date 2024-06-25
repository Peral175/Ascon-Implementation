import unittest
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import timeit
import time
import AES_ExactMatch
import AES_LDA
import ASCON_ExactMatch
import ASCON_LDA


class TestStringMethods(unittest.TestCase):
    tr_aes_clear_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-clear/")
    tr_aes_isw_2_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-isw2/")
    tr_aes_isw_3_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-isw3/")
    tr_aes_isw_4_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-isw4/")
    tr_aes_isw_5_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-isw5/")
    tr_aes_clear_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-clear/")
    tr_aes_isw_2_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-isw2/")
    tr_aes_isw_3_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-isw3/")
    tr_aes_isw_4_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-isw4/")
    tr_aes_isw_5_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-isw5/")
    tr_aes = [tr_aes_clear_1, tr_aes_isw_2_1, tr_aes_isw_3_1, tr_aes_isw_4_1, tr_aes_isw_5_1,
              tr_aes_clear_2, tr_aes_isw_2_2, tr_aes_isw_3_2, tr_aes_isw_4_2, tr_aes_isw_5_2]
    tr_ascon_clear_1 = pathlib.PosixPath(
        "traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/ascon128_2R_simplified-clear/")
    tr_ascon_isw_2_1 = pathlib.PosixPath(
        "traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/ascon128_2R_simplified-isw_2/")
    tr_ascon_isw_3_1 = pathlib.PosixPath(
        "traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/ascon128_2R_simplified-isw_3/")
    tr_ascon_isw_4_1 = pathlib.PosixPath(
        "traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/ascon128_2R_simplified-isw_4/")
    tr_ascon_isw_5_1 = pathlib.PosixPath(
        "traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/ascon128_2R_simplified-isw_5/")
    tr_ascon_clear_2 = pathlib.PosixPath(
        "traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/ascon128_2R_simplified-clear/")
    tr_ascon_isw_2_2 = pathlib.PosixPath(
        "traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/ascon128_2R_simplified-isw_2/")
    tr_ascon_isw_3_2 = pathlib.PosixPath(
        "traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/ascon128_2R_simplified-isw_3/")
    tr_ascon_isw_4_2 = pathlib.PosixPath(
        "traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/ascon128_2R_simplified-isw_4/")
    tr_ascon_isw_5_2 = pathlib.PosixPath(
        "traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/ascon128_2R_simplified-isw_5/")
    tr_ascon = [tr_ascon_clear_1, tr_ascon_isw_2_1, tr_ascon_isw_3_1, tr_ascon_isw_4_1, tr_ascon_isw_5_1,
                tr_ascon_clear_2, tr_ascon_isw_2_2, tr_ascon_isw_3_2, tr_ascon_isw_4_2, tr_ascon_isw_5_2]

    t = 306

    def test_aes_exact(self):
        target1 = self.tr_aes_clear_1.parents[0].name  # secret key we want to find
        target1 = target1.encode('utf-8').hex()
        r = AES_ExactMatch.attack(self.t, self.tr_aes_clear_1)
        self.assertEqual(target1, r)
        r = AES_ExactMatch.attack(self.t, self.tr_aes_isw_2_1)
        self.assertNotEqual(target1, r)

        target2 = self.tr_aes_clear_2.parents[0].name  # secret key we want to find
        target2 = target2.encode('utf-8').hex()
        r = AES_ExactMatch.attack(self.t, self.tr_aes_clear_2)
        self.assertEqual(target2, r)
        r = AES_ExactMatch.attack(self.t, self.tr_aes_isw_2_2)
        self.assertNotEqual(target2, r)

    def test_ascon_exact(self):
        target1 = self.tr_ascon_clear_1.parents[0].name  # secret key we want to find
        target1 = target1.encode('utf-8').hex()
        r = ASCON_ExactMatch.attack(self.t, self.tr_ascon_clear_1)
        self.assertEqual(target1, r)
        r = ASCON_ExactMatch.attack(self.t, self.tr_ascon_isw_2_1)
        self.assertNotEqual(target1, r)

        target2 = self.tr_ascon_clear_2.parents[0].name  # secret key we want to find
        target2 = target2.encode('utf-8').hex()
        r = ASCON_ExactMatch.attack(self.t, self.tr_ascon_clear_2)
        self.assertEqual(target2, r)
        r = ASCON_ExactMatch.attack(self.t, self.tr_ascon_isw_2_2)
        self.assertNotEqual(target2, r)

    def test_lda_aes(self):
        nr_of_runs = 3
        nr_increments = 8
        timings = [[None] * nr_increments for _ in range(len(self.tr_aes))]
        for i in range(len(self.tr_aes)):  # all the implementations
            target = self.tr_aes[i].parents[0].name  # secret key we want to find
            target = target.encode('utf-8').hex()  # bytes.fromhex("61626364656667684142434445464748")
            for inc in range(nr_increments):
                times = []
                w_size = (inc + 1) * 64
                for j in range(nr_of_runs):  # average of 10 runs
                    t_start = time.time()
                    s_size = w_size // 2
                    # s_size = w_size // 4  # different window step size
                    tr = w_size + 50  # 2^50 chance of failure ?
                    # print("Run nr. {:2}/10  Traces:{:4}  Window:{:4}  Step:{:4}".format(j+1, tr, w_size, s_size))
                    r = AES_LDA.aes_lda(tr, self.tr_aes[i], w_size, s_size)
                    self.assertEqual(target, r)
                    t_stop = time.time()
                    elapsed_time = str(t_stop - t_start)[:6]
                    times.append(float(elapsed_time))
                timings[i][inc] = np.average(times)
                print(timings)

    def test_lda_ascon(self):
        nr_of_runs = 3
        nr_increments = 8
        timings = [[None] * nr_increments for _ in range(len(self.tr_aes))]
        for i in range(len(self.tr_ascon)):   # all the implementations
            target = self.tr_ascon[i].parents[0].name  # secret key we want to find
            target = target.encode('utf-8').hex()  # bytes.fromhex("61626364656667684142434445464748")
            for inc in range(nr_increments):
                times = []
                w_size = (inc+1)*64
                for j in range(nr_of_runs):         # average of 10 runs
                    t_start = time.time()
                    s_size = w_size // 2
                    # s_size = w_size // 4  # different window step size
                    tr = w_size + 50  # 2^50 chance of failure ?
                    # print("Run nr. {:2}/10  Traces:{:4}  Window:{:4}  Step:{:4}".format(j+1, tr, w_size, s_size))
                    r = ASCON_LDA.ascon_lda(tr, self.tr_ascon[i], w_size, s_size)
                    self.assertEqual(target, r)
                    t_stop = time.time()
                    elapsed_time = str(t_stop - t_start)[:6]
                    times.append(float(elapsed_time))
                timings[i][inc] = np.average(times)
                print(timings)


if __name__ == '__main__':
    unittest.main()
