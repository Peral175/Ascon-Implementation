import unittest
import pathlib
import numpy as np
import matplotlib.pyplot as plt
import timeit
import time
import AES_ExactMatch
import AES_LDA
import Ascon_ExactMatch
import Ascon_LDA

aes_clear1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-clear/")
aes_isw2_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-isw2/")
aes_isw3_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-isw3/")
aes_isw4_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-isw4/")
aes_minq_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-minq/")
aes_ql2_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-ql2/")
aes_ql3_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-ql3/")
aes_ql4_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-ql4/")
aes_cl2_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-cl2/")
aes_cl3_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-cl3/")
aes_cl4_1 = pathlib.PosixPath("traces/abcdefghABCDEFGH/aes2-cl4/")

aes_clear2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-clear/")
aes_isw2_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-isw2/")
aes_isw3_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-isw3/")
aes_isw4_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-isw4/")
aes_minq_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-minq/")
aes_ql2_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-ql2/")
aes_ql3_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-ql3/")
aes_ql4_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-ql4/")
aes_cl2_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-cl2/")
aes_cl3_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-cl3/")
aes_cl4_2 = pathlib.PosixPath("traces/0123456789:;<=>?/aes2-cl4/")

ascon_clear1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-clear/")
ascon_isw2_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-isw2/")
ascon_isw3_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-isw3/")
ascon_isw4_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-isw4/")
ascon_minq_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-minq/")
ascon_ql2_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-ql2/")
ascon_ql3_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-ql3/")
ascon_ql4_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-ql4/")
ascon_cl2_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-cl2/")
ascon_cl3_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-cl3/")
ascon_cl4_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-cl4/")

ascon_clear2 = pathlib.PosixPath("traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/asconP_2R_NCA-clear/")
ascon_isw2_2 = pathlib.PosixPath("traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/asconP_2R_NCA-isw2/")
ascon_isw3_2 = pathlib.PosixPath("traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/asconP_2R_NCA-isw3/")
ascon_isw4_2 = pathlib.PosixPath("traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/asconP_2R_NCA-isw4/")
ascon_minq_2 = pathlib.PosixPath("traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/asconP_2R_NCA-minq/")
ascon_ql2_2 = pathlib.PosixPath("traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/asconP_2R_NCA-ql2/")
ascon_ql3_2 = pathlib.PosixPath("traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/asconP_2R_NCA-ql3/")
ascon_ql4_2 = pathlib.PosixPath("traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/asconP_2R_NCA-ql4/")
ascon_cl2_2 = pathlib.PosixPath("traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/asconP_2R_NCA-cl2/")
ascon_cl3_2 = pathlib.PosixPath("traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/asconP_2R_NCA-cl3/")
ascon_cl4_2 = pathlib.PosixPath("traces/0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVW/asconP_2R_NCA-cl4/")

tr_aes_1 = [aes_clear1, aes_isw2_1, aes_isw3_1, aes_isw4_1,
            aes_minq_1, aes_ql2_1, aes_ql3_1, aes_ql4_1,
            aes_cl2_1, aes_cl3_1, aes_cl4_1]
tr_aes_2 = [aes_clear2, aes_isw2_2, aes_isw3_2, aes_isw4_2,
            aes_minq_2, aes_ql2_2, aes_ql3_2, aes_ql4_2,
            aes_cl2_2, aes_cl3_2, aes_cl4_2]
tr_ascon_1 = [ascon_clear1, ascon_isw2_1, ascon_isw3_1, ascon_isw4_1,
              ascon_minq_1, ascon_ql2_1, ascon_ql3_1, ascon_ql4_1,
              ascon_cl2_1, ascon_cl3_1, ascon_cl4_1]
tr_ascon_2 = [ascon_clear2, ascon_isw2_2, ascon_isw3_2, ascon_isw4_2,
              ascon_minq_2, ascon_ql2_2, ascon_ql3_2, ascon_ql4_2,
              ascon_cl2_2, ascon_cl3_2, ascon_cl4_2]

class TestStringMethods(unittest.TestCase):

    t = 306
    nr_of_runs = 20
    nr_increments = 2

    def test_aes_exact(self):
        target1 = self.aes_clear1.parents[0].name  # secret key we want to find
        target1 = target1.encode('utf-8').hex()
        r = AES_ExactMatch.attack(self.t, self.aes_clear1)
        self.assertEqual(target1, r)
        r = AES_ExactMatch.attack(self.t, self.aes_isw2_1)
        self.assertNotEqual(target1, r)

        target2 = self.aes_clear2.parents[0].name  # secret key we want to find
        target2 = target2.encode('utf-8').hex()
        r = AES_ExactMatch.attack(self.t, self.aes_clear2)
        self.assertEqual(target2, r)
        r = AES_ExactMatch.attack(self.t, self.aes_isw2_2)
        self.assertNotEqual(target2, r)

    def test_ascon_exact(self):
        target1 = self.ascon_clear1.parents[0].name  # secret key we want to find
        target1 = target1.encode('utf-8').hex()
        r = ASCON_ExactMatch.attack(self.t, self.ascon_clear1)
        self.assertEqual(target1, r)
        r = ASCON_ExactMatch.attack(self.t, self.ascon_isw2_1)
        self.assertNotEqual(target1, r)

        target2 = self.ascon_clear2.parents[0].name  # secret key we want to find
        target2 = target2.encode('utf-8').hex()
        r = Ascon_ExactMatch.attack(self.t, self.ascon_clear2)
        self.assertEqual(target2, r)
        r = ASCON_ExactMatch.attack(self.t, self.ascon_isw2_2)
        self.assertNotEqual(target2, r)

    def test_lda_aes(self):
        timings = [[None] * self.nr_increments for _ in range(len(self.tr_aes))]
        for i in range(len(self.tr_aes)):  # all the implementations
            target = self.tr_aes[i].parents[0].name  # secret key we want to find
            target = target.encode('utf-8').hex()  # bytes.fromhex("61626364656667684142434445464748")
            for inc in range(self.nr_increments):
                times = []
                w_size = (inc + 1) * 64
                for j in range(self.nr_of_runs):  # average of 10 runs
                    t_start = time.time()
                    s_size = w_size // 2
                    # s_size = w_size // 4  # different window step size
                    tr = w_size + 50  # 2^50 chance of failure ?
                    # print("Run nr. {:2}/{:2}   Traces:{:4}  Window:{:4}  Step:{:4}".format(j+1, self.nr_increments, tr, w_size, s_size))
                    r = AES_LDA.aes_lda(tr, self.tr_aes[i], w_size, s_size)
                    self.assertEqual(target, r)
                    t_stop = time.time()
                    elapsed_time = str(t_stop - t_start)[:6]
                    times.append(float(elapsed_time))
                timings[i][inc] = np.average(times)
                print(timings)

    def test_lda_ascon(self):
        timings = [[None] * self.nr_increments for _ in range(len(self.tr_ascon))]
        for i in range(len(self.tr_ascon)):   # all the implementations
            target = self.tr_ascon[i].parents[0].name  # secret key we want to find
            target = target.encode('utf-8').hex()  # bytes.fromhex("61626364656667684142434445464748")
            for inc in range(self.nr_increments):
                times = []
                w_size = (inc+1)*64
                for j in range(self.nr_of_runs):         # average of 10 runs
                    t_start = time.time()
                    s_size = w_size // 2
                    # s_size = w_size // 4  # different window step size
                    tr = w_size + 50  # 2^50 chance of failure ?
                    print("Run nr. {:2}/{:2}  Traces:{:4}  Window:{:4}  Step:{:4}".format(j+1, self.nr_increments, tr, w_size, s_size))
                    print(self.tr_ascon[i])
                    r = Ascon_LDA.ascon_lda(tr, self.tr_ascon[i], w_size, s_size)
                    self.assertEqual(target, r)
                    t_stop = time.time()
                    elapsed_time = str(t_stop - t_start)[:6]
                    times.append(float(elapsed_time))
                timings[i][inc] = np.average(times)
                print(timings)


if __name__ == '__main__':
    unittest.main()
