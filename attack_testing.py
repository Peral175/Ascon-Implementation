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

ascon_clear_obfus_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-clear_obfus/")
ascon_isw2_obfus_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-isw2_obfus/")
ascon_isw3_obfus_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-isw3_obfus/")
ascon_isw4_obfus_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-isw4_obfus/")
ascon_minq_obfus_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-minq_obfus/")
ascon_ql2_obfus_1 = pathlib.PosixPath("traces/abcdefghijklmnopqrstuvwxyz1234567890ABCD/asconP_2R_NCA-ql2_obfus/")

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

# targets of our attacks
aes_key_1 = aes_clear1.parents[0].name.encode('utf-8').hex()
aes_key_2 = aes_clear2.parents[0].name.encode('utf-8').hex()
ascon_key_1 = ascon_clear1.parents[0].name.encode('utf-8').hex()
ascon_key_2 = ascon_clear2.parents[0].name.encode('utf-8').hex()


class TestMethods(unittest.TestCase):

    def setUp(self):
        self.startTime = time.time()

    def tearDown(self):
        t = time.time() - self.startTime
        print('%s: %.3f seconds' % (self.id(), t))

    def test_exact(self):
        # Test duration around 2.5 minutes  (was 5)
        # AES       15 - 24 failed due to too few traces
        # Ascon needs only 16 traces (5-bit version)  -> but much slower
        aes_exact_array = [(aes_key_1, [aes_clear1, aes_isw2_1, aes_minq_1]),
                           # (aes_key_2, [aes_clear2, aes_isw2_2, aes_minq_2])
                           ]
        ascon_exact_array = [(ascon_key_1, [ascon_clear1, ascon_isw2_1, ascon_minq_1]),
                             # (ascon_key_2, [ascon_clear2, ascon_isw2_2, ascon_minq_2])
                             ]
        times = []
        for key, masks in aes_exact_array:
            for i in range(0, len(masks)):
                timings = [[], []]
                for t in range(15, 32, 1):
                    with self.subTest(name=(masks[i], t), T=t):
                        start = time.time()
                        r = AES_ExactMatch.attack(t, masks[i])  # non-masked
                        if i == 0:
                            self.assertEqual(key, r)  # should succeed
                        else:
                            self.assertNotEqual(key, r)  # should fail
                        end = time.time()
                        elapsed = end - start
                        timings[0].append(t)
                        timings[1].append(elapsed)
                        print("{} elapsed time: {} with {} traces".format(masks[i].name, elapsed, t))
                times.append(timings)
        for key, masks in ascon_exact_array:
            for i in range(0, len(masks)):
                timings = [[], []]
                for t in range(15, 32, 1):
                    with self.subTest(name=(masks[i], t), T=t):
                        start = time.time()
                        r = Ascon_ExactMatch.attack(t, masks[i])  # non-masked
                        if i == 0:
                            self.assertEqual(key, r)  # should succeed
                        else:
                            self.assertNotEqual(key, r)  # should fail
                        end = time.time()
                        elapsed = end - start
                        timings[0].append(t)
                        timings[1].append(elapsed)
                        print("{} elapsed time: {} with {} traces".format(masks[i].name, elapsed, t))
                times.append(timings)
        k1 = times[:3]
        plt.subplot(1, 2, 1)
        for x, y in k1:
            print(x, y)
            plt.plot(x, y, linestyle='-', marker='*')
        plt.title("AES")
        plt.grid(axis='y', alpha=0.25, color='grey')
        plt.xlabel("Nr. traces")
        plt.ylabel("Time (in seconds)")
        plt.legend(["Non-Masked", "ISW-2", "MINQ"], loc='upper left')
        k2 = times[3:]
        plt.subplot(1, 2, 2)
        for x, y in k2:
            plt.plot(x, y, linestyle='-', marker='*')
        plt.title("Em-Ascon-P")
        plt.grid(axis='y', alpha=0.5, color='grey')
        plt.xlabel("Nr. traces")
        plt.ylabel("Time (in seconds)")
        plt.legend(["Non-Masked", "ISW-2", "MINQ"], loc='upper left')
        plt.show()

    def test_Ascon_POC(self):
        # # Proof of concept
        # # test runs for approx. 15 mins for 6
        # ascon_array = [(ascon_key_1, [ascon_clear1, ascon_isw2_1,
        #                               ascon_isw3_1, ascon_isw4_1,
        #                               ascon_minq_1, ascon_ql2_1,
        #                               # ascon_ql3_1, ascon_ql4_1,
        #                               # ascon_cl2_1, ascon_cl3_1,
        #                               # ascon_cl4_1
        #                               ])]
        # window_size = 64
        # window_step = 16
        # nr_traces = window_size + 50  # 2^50
        # times = {}
        # KEY_BYTES = tuple(i for i in range(64))
        # for key, masks in ascon_array:
        #     for i in range(0, len(masks)):
        #         with self.subTest(name=(masks[i], nr_traces), T=nr_traces):
        #             start = time.time()
        #             r = Ascon_LDA.ascon_lda(traces=nr_traces, traces_dir=masks[i], window_size=window_size,
        #                                     window_step=window_step, KEY_BYTES=KEY_BYTES, verbose=False,
        #                                     RANKING=True)  # non-masked
        #             end = time.time()
        #             elapsed = end - start
        #             times[masks[i].name] = elapsed
        #             print("{} elapsed time: {} with {} traces".format(masks[i].name, elapsed, nr_traces))
        #             if i < 4:
        #                 self.assertEqual(key, r)  # should succeed
        #             else:
        #                 self.assertNotEqual(key, r)  # should fail
        # print(times)
        X = ["Non-Masked", "ISW-2", "ISW-3", "ISW-4", "MINQ", "QL-2"]
        # times = {'asconP_2R_NCA-clear': 5.526602745056152, 'asconP_2R_NCA-isw2': 16.88768172264099, 'asconP_2R_NCA-isw3': 51.91937470436096, 'asconP_2R_NCA-isw4': 144.25258374214172, 'asconP_2R_NCA-minq': 462.48216485977173, 'asconP_2R_NCA-ql2': 609.8035924434662}
        times = {'asconP_2R_NCA-clear': 5.050966739654541, 'asconP_2R_NCA-isw2': 16.82824683189392,
                 'asconP_2R_NCA-isw3': 35.9543673992157, 'asconP_2R_NCA-isw4': 54.096439361572266,
                 'asconP_2R_NCA-minq': 168.81626796722412, 'asconP_2R_NCA-ql2': 215.08399510383606}
        Y = list(times.values())
        for x, y in zip(X, Y):
            plt.bar(x, y)
        # plt.title("Ascon LDA (370 traces, 320 window size, 80 window step)")
        plt.title("Ascon LDA + Ranking (104 traces, 64 window size, 16 window step)")
        plt.grid(axis='y', alpha=0.25, color='grey')
        plt.xlabel("Implementations")
        plt.xticks(X)
        plt.ylabel("Time (in seconds)")
        # plt.legend(["Non-Masked", "ISW-2", "ISW-3", "ISW-4", "MINQ", "QL-2"], loc='upper left')
        plt.show()

    def test_Ascon_Obfuscation(self):
        # Impact of obfuscation
        # test runs for approx. 3 minutes [64 mins]
        # ascon_array = [(ascon_key_1, [ascon_clear1, ascon_clear_obfus_1,
        #                               ascon_isw2_1, ascon_isw2_obfus_1,
        #                               ascon_isw3_1, ascon_isw3_obfus_1,
        #                               ascon_isw4_1, ascon_isw4_obfus_1,
        #                               ascon_minq_1, ascon_minq_obfus_1,
        #                               ascon_ql2_1, ascon_ql2_obfus_1,
        #                               ])]
        # window_size = 256
        # window_step = 128
        # nr_traces = window_size + 50  # 2^50
        # times = {}
        # KEY_BYTES = tuple(i for i in range(64))
        # for key, masks in ascon_array:
        #     for i in range(0, len(masks)):
        #         with self.subTest(name=(masks[i], nr_traces), T=nr_traces):
        #             start = time.time()
        #             r = Ascon_LDA.ascon_lda(traces=nr_traces, traces_dir=masks[i], window_size=window_size,
        #                                     window_step=window_step, KEY_BYTES=KEY_BYTES, verbose=False,
        #                                     RANKING=True)  # non-masked
        #             if i < 8:
        #                 self.assertEqual(key, r)  # should succeed
        #             else:
        #                 self.assertNotEqual(key, r)  # should fail
        #             end = time.time()
        #             elapsed = end - start
        #             times[masks[i].name] = elapsed
        #             print("{} elapsed time: {} with {} traces".format(masks[i].name, elapsed, nr_traces))
        # print("Times:", times)
        times = {'asconP_2R_NCA-clear': 5.329787015914917, 'asconP_2R_NCA-clear_obfus': 39.920722246170044,
                 'asconP_2R_NCA-isw2': 13.455626964569092, 'asconP_2R_NCA-isw2_obfus': 128.6323697566986,
                 'asconP_2R_NCA-isw3': 24.097255229949950, 'asconP_2R_NCA-isw3_obfus': 243.27532172203064,
                 'asconP_2R_NCA-isw4': 38.605958461761475, 'asconP_2R_NCA-isw4_obfus': 393.8332350254059,
                 'asconP_2R_NCA-minq': 118.43666768074036, 'asconP_2R_NCA-minq_obfus': 1188.7132730484009,
                 'asconP_2R_NCA-ql2': 154.983089685440060, 'asconP_2R_NCA-ql2_obfus': 1509.6942660808563}
        # X = ["Clear", "Clear-obfus","ISW-2", "ISW-2-obfus","ISW-3", "ISW-3-obfus",
        #      "ISW-4", "ISW-4-obfus","MINQ", "MINQ-obfus", "QL-2", "QL-2-obfus"]
        X = ["Clear", "ISW-2", "ISW-3", "ISW-4", "MINQ", "QL-2"]
        Y = list(times.values())
        Y = [int(_) for _ in Y]
        Y1 = Y[::2]
        Y2 = Y[1::2]
        XX = np.arange(len(X), dtype=np.float64)
        fig, ax = plt.subplots()
        rects1 = ax.bar(XX - 0.35 / 2, Y1, 0.35)
        # ax.plot(XX-0.35/2, Y1, marker='*')
        rects2 = ax.bar(XX + 0.35 / 2, Y2, 0.35)
        # ax.plot(XX+0.35/2, Y2, marker='*')
        ax.set_ylabel('Time (in seconds)')
        ax.grid(axis='y', alpha=0.25, color='grey', which='both')
        ax.set_title('Obfuscation')
        ax.set_xticks(XX, X)
        ax.legend(["Masked", "Masked+Obfuscated"], loc='upper left')
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        fig.tight_layout()
        plt.show()
        # attack_testing.TestMethods.test_Ascon_Obfuscation: 3858.980 seconds

    def test_minimal_window(self):
        # # get the minimal window size for all
        # # compare LDA with RANKING
        # # it recovers some bits earlier than others --> we do full key
        # # clear requires a window of 1
        # # isw-2 200 128 32    2
        # # isw-3 300 192 48    16
        # # isw-4 400 257 64    16
        # KEY_BYTES = tuple(i for i in range(64))
        # # CLEAR
        # start = time.time()
        # r = Ascon_LDA.ascon_lda(traces=51, traces_dir=ascon_clear1, window_size=1, window_step=1, KEY_BYTES=KEY_BYTES,
        #                         verbose=False, RANKING=False)
        # elapsed = time.time() - start
        # print(ascon_clear1.name, elapsed, r, "\n", ascon_key_1)
        # self.assertEqual(r,ascon_key_1)
        # # CLEAR + RANKING
        # start = time.time()
        # r = Ascon_LDA.ascon_lda(traces=51, traces_dir=ascon_clear1, window_size=1, window_step=1, KEY_BYTES=KEY_BYTES,
        #                         verbose=False, RANKING=True)
        # elapsed = time.time() - start
        # print(ascon_clear1.name, elapsed, r, "\n", ascon_key_1)
        # self.assertEqual(r, ascon_key_1)
        # # ISW-2
        # # start = time.time()
        # # r = Ascon_LDA.ascon_lda(traces=178, traces_dir=ascon_isw2_1, window_size=127, window_step=1, KEY_BYTES=KEY_BYTES,
        # #                         verbose=False, RANKING=False)
        # # elapsed = time.time() - start
        # # print(ascon_isw2_1.name, elapsed, r, ascon_key_1)
        # start = time.time()
        # r = Ascon_LDA.ascon_lda(traces=178, traces_dir=ascon_isw2_1, window_size=128, window_step=1, KEY_BYTES=KEY_BYTES,
        #                         verbose=False, RANKING=False)
        # elapsed = time.time() - start
        # print(ascon_isw2_1.name, elapsed, r, "\n", ascon_key_1)
        # self.assertEqual(r, ascon_key_1)
        # # ISW-2 + RANKING
        # start = time.time()
        # r = Ascon_LDA.ascon_lda(traces=52, traces_dir=ascon_isw2_1, window_size=2, window_step=1, KEY_BYTES=KEY_BYTES,
        #                         verbose=False, RANKING=True)
        # elapsed = time.time() - start
        # print(ascon_isw2_1.name, elapsed, r, "\n", ascon_key_1)
        # self.assertEqual(r, ascon_key_1)
        #
        # # ISW-3
        # # start = time.time()
        # # r = Ascon_LDA.ascon_lda(traces=242, traces_dir=ascon_isw3_1, window_size=191, window_step=1, KEY_BYTES=KEY_BYTES,
        # #                         verbose=False, RANKING=False)
        # # elapsed = time.time() - start
        # # print(ascon_isw3_1.name, elapsed, r, ascon_key_1)
        # start = time.time()
        # r = Ascon_LDA.ascon_lda(traces=242, traces_dir=ascon_isw3_1, window_size=192, window_step=1, KEY_BYTES=KEY_BYTES,
        #                         verbose=False, RANKING=False)
        # elapsed = time.time() - start
        # print(ascon_isw3_1.name, elapsed, r, "\n", ascon_key_1)
        # self.assertEqual(r, ascon_key_1)
        # # ISW-3 + RANKING
        # # start = time.time()
        # # r = Ascon_LDA.ascon_lda(traces=66, traces_dir=ascon_isw3_1, window_size=15, window_step=1, KEY_BYTES=KEY_BYTES,
        # #                         verbose=False, RANKING=True)
        # # elapsed = time.time() - start
        # # print(ascon_isw3_1.name, elapsed, r, ascon_key_1)
        # start = time.time()
        # r = Ascon_LDA.ascon_lda(traces=66, traces_dir=ascon_isw3_1, window_size=16, window_step=1, KEY_BYTES=KEY_BYTES,
        #                         verbose=False, RANKING=True)
        # elapsed = time.time() - start
        # print(ascon_isw3_1.name, elapsed, r, "\n", ascon_key_1)
        # self.assertEqual(r, ascon_key_1)
        #
        # # ISW-4
        # start = time.time()
        # r = Ascon_LDA.ascon_lda(traces=307, traces_dir=ascon_isw4_1, window_size=255, window_step=1, KEY_BYTES=KEY_BYTES,
        #                         verbose=False, RANKING=False)
        # elapsed = time.time() - start
        # print(ascon_isw4_1.name, elapsed, r, "\n", ascon_key_1)
        # self.assertNotEqual(r, ascon_key_1)
        # start = time.time()
        # r = Ascon_LDA.ascon_lda(traces=307, traces_dir=ascon_isw4_1, window_size=256, window_step=1, KEY_BYTES=KEY_BYTES,
        #                         verbose=False, RANKING=False)
        # elapsed = time.time() - start
        # print(ascon_isw4_1.name, elapsed, r, "\n", ascon_key_1)
        # self.assertEqual(r, ascon_key_1)
        # # ISW-4 + RANKING
        # # start = time.time()
        # # r = Ascon_LDA.ascon_lda(traces=66, traces_dir=ascon_isw4_1, window_size=15, window_step=1, KEY_BYTES=KEY_BYTES,
        # #                         verbose=False, RANKING=True)
        # # elapsed = time.time() - start
        # # print(ascon_isw4_1.name, elapsed, r, ascon_key_1)
        # start = time.time()
        # r = Ascon_LDA.ascon_lda(traces=66, traces_dir=ascon_isw4_1, window_size=16, window_step=1, KEY_BYTES=KEY_BYTES,
        #                         verbose=False, RANKING=True)
        # elapsed = time.time() - start
        # print(ascon_isw4_1.name, elapsed, r, "\n", ascon_key_1)
        # self.assertEqual(r, ascon_key_1)
        # Testing started at 10: 54...
        # Launching unittests with arguments python -m unittest attack_testing.TestMethods.test_minimal_window in / mnt / h / Master / Thesis / Implementation
        # asconP_2R_NCA - clear
        # 45.333993673324585
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - clear
        # 45.29067778587341
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw2
        # 528.4037179946899
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw2
        # 146.19058322906494
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw3
        # 1721.6577894687653
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw3
        # 327.3436858654022
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw4
        # 4503.883012533188
        # 0110000101_0___00110001101__010001__0101011001100110011101______0110100101_0___00110101101__110001__1101011011100110111101______0111000101_1___00111001101__010001__0101011101100111011101______0111100101_1___00011000100__001000__0011001101000011010100______0011011100_1___00011100100__000001__0001010000100100001101______
        # asconP_2R_NCA - isw4
        # 4489.008816480637
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw4
        # 523.3566451072693
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # Ran 1 test in 12330.472 s OK#
        # attack_testing.TestMethods.test_minimal_window: 12330.471 seconds
        # Process finished with exit code 0
        labels = ["Clear", "ISW-2", "ISW-3", "ISW-4"]
        r_nr = [(45.333993673324585, 1), (528.4037179946899, 128), (1721.6577894687653, 192), (4489.008816480637, 256)]
        r_r = [(45.29067778587341, 1), (146.19058322906494, 2), (327.3436858654022, 16), (523.3566451072693, 16)]
        X_2 = list(zip(*r_nr))[1]
        Y_2 = list(zip(*r_r))[1]
        x = np.arange(4, dtype=np.float64)
        fig, ax = plt.subplots()
        rects1 = ax.bar(x - 0.35 / 2, X_2, 0.35)
        rects2 = ax.bar(x + 0.35 / 2, Y_2, 0.35)
        ax.set_ylabel('Window Size')
        ax.grid(axis='y', alpha=0.25, color='grey', which='both')
        ax.set_title('Minimal Window Size')
        ax.set_xticks(x, labels)
        ax.legend(["LDA", "LDA+Ranking"], loc='upper left')
        ax.bar_label(rects1, padding=3)
        ax.bar_label(rects2, padding=3)
        fig.tight_layout()
        plt.show()
        X_1 = list(zip(*r_nr))[0]
        Y_1 = list(zip(*r_r))[0]
        x = np.arange(4, dtype=np.float64)
        fig, ax = plt.subplots()
        rects1 = ax.plot(X_1, marker='*')
        rects2 = ax.plot(Y_1, marker='*')
        ax.set_ylabel('Time (in seconds)')
        ax.grid(axis='y', alpha=0.25, color='grey', which='both')
        ax.set_title('Minimal Window Size')
        ax.set_xticks(x, labels)
        ax.legend(["LDA", "LDA+Ranking"], loc='upper left')
        # ax.bar_label(rects1, padding=3)
        # ax.bar_label(rects2, padding=3)
        fig.tight_layout()
        plt.show()
        # Launching unittests
        # with arguments python -m unittest attack_testing.TestMethods.test_minimal_window in / mnt / h / Master / Thesis / Implementation
        #
        # asconP_2R_NCA - clear
        # 45.49471855163574
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - clear
        # 45.362316846847534
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw2
        # 534.5282273292542
        # 01100001011000100110001101100100011001010110011001100111011010_001101001011010100110101101101100011011010110111001101111011100_001110001011100100111001101110100011101010111011001110111011110_001111001011110100011000100110010001100110011010000110101001101_000110111001110000011100100110000010000010100001001000011010001_0
        # asconP_2R_NCA - isw2
        # 531.8086071014404
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw2
        # 145.47295308113098
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw3
        # 1738.102302312851
        # 0110000101100__00_10001101100100011001010110011001100111011___000110100101101__00_10101101101100011011010110111001101111011___000111000101110__00_11001101110100011101010111011001110111011___000111100101111__00_11000100110010001100110011010000110101001___100011011100111__00_11100100110000010000010100001001000011010___00
        # asconP_2R_NCA - isw3
        # 1729.2524342536926
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw3
        # 329.59919834136963
        # 61606164656465686968696c6d6c6d60616061646564656869682120212425242528292041404144
        # asconP_2R_NCA - isw3
        # 326.1257462501526
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw4
        # 4531.824024438858
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw4
        # 4528.478308439255 --> 4489.008816480637 [256]
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # asconP_2R_NCA - isw4
        # 532.0215246677399
        # 41404144454445404140414445444550515051545554555051501110111415141510111041404144
        # asconP_2R_NCA - isw4
        # 527.2801456451416
        # 6162636465666768696a6b6c6d6e6f707172737475767778797a3132333435363738393041424344
        # attack_testing.TestMethods.test_minimal_window: 15545.353
        # seconds
        # Ran 1 test in 15545.353 s
        # OK
        # Process finished with exit code 0

    def test_2v5bits(self):
        # # difference in performance for 2 vs 5 bits ascon
        # # test runs for around 6 mins
        # # 5 bit slower but decreasingly so
        # ascon_array = [(ascon_key_1, [
        #     # ascon_clear1,
        #     ascon_isw2_1,
        #     # ascon_isw3_1, ascon_isw4_1,
        #     # ascon_minq_1, ascon_ql2_1,
        #     # ascon_ql3_1, ascon_ql4_1,
        #     # ascon_cl2_1, ascon_cl3_1,
        #     # ascon_cl4_1
        # ])]
        # window_size = 32
        # window_step = 32
        # # nr_traces = window_size + 50  # 2^50
        # times1 = {}
        # times2 = {}
        # KEY_BYTES = tuple(i for i in range(64))
        # for key, masks in ascon_array:
        #     for i in range(0, len(masks)):
        #         for _ in range(5):
        #             for w in range(window_size, window_size * 15, window_step):
        #                 print("w", w)
        #                 with self.subTest(name=(masks[i], w + 50), T=w + 50):
        #                     start1 = time.time()
        #                     r1 = Ascon_LDA.ascon_lda(traces=w + 50, traces_dir=masks[i], window_size=w,
        #                                              window_step=w // 2, KEY_BYTES=KEY_BYTES,
        #                                              verbose=False,
        #                                              RANKING=False)
        #                     print("r1\t", r1)
        #                     end1 = time.time()
        #                     elapsed1 = end1 - start1
        #                     start2 = time.time()
        #                     r2 = Ascon_LDA.mini_ascon_lda(traces=w + 50, traces_dir=masks[i], window_size=w,
        #                                                   window_step=w // 2, KEY_BYTES=KEY_BYTES,
        #                                                   verbose=False,
        #                                                   RANKING=False)
        #                     print("r2\t", r2)
        #                     print("key\t", key)
        #                     end2 = time.time()
        #                     elapsed2 = end2 - start2
        #                     print("Times: ", (elapsed1, elapsed2))
        #                     times1[masks[i].name + "-e1-"+str(_)+"-" + str(w)] = elapsed1
        #                     times2[masks[i].name + "-e2-"+str(_)+"-" + str(w)] = elapsed2
        #                     print("{} elapsed time: {} with {} traces".format(masks[i].name, (elapsed1, elapsed2), w + 50))
        #                     self.assertEqual(key, r1)
        #                     self.assertEqual(key, r2)
        # print(times1)
        # print(times2)
        # print(len(times1))
        # times = {'asconP_2R_NCA-isw2-32': (9.321946382522583, 8.113517761230469),   # F T
        #          'asconP_2R_NCA-isw2-64': (6.98106575012207, 6.530013084411621),    # F T
        #          'asconP_2R_NCA-isw2-96': (6.663027763366699, 5.90791654586792),    # F T
        #          'asconP_2R_NCA-isw2-128': (6.661635398864746, 5.896665334701538),  # F T
        #          'asconP_2R_NCA-isw2-160': (6.546462535858154, 6.201824188232422),
        #          'asconP_2R_NCA-isw2-192': (6.993530035018921, 6.704261541366577),
        #          'asconP_2R_NCA-isw2-224': (7.583965063095093, 7.240850210189819),
        #          'asconP_2R_NCA-isw2-256': (8.283821821212769, 7.919913291931152),
        #          'asconP_2R_NCA-isw2-288': (8.885507345199585, 8.541930913925171),
        #          'asconP_2R_NCA-isw2-320': (9.613505125045776, 9.191009521484375),
        #          'asconP_2R_NCA-isw2-352': (10.15358853340149, 9.74407958984375),
        #          'asconP_2R_NCA-isw2-384': (10.850411653518677, 10.460332155227661),
        #          'asconP_2R_NCA-isw2-416': (11.724337816238403, 11.408489227294922),
        #          'asconP_2R_NCA-isw2-448': (12.32200288772583, 11.933516263961792)}
        # label = ["Non-Masked", "ISW-2", "ISW-3", "ISW-4", "MINQ", "QL-2"]
        times1 = {
            'asconP_2R_NCA-isw2e1-0-32': [9.353684902191162],
            'asconP_2R_NCA-isw2e1-0-64': [6.825925588607788],
            'asconP_2R_NCA-isw2e1-0-96': [6.308010578155518],
            'asconP_2R_NCA-isw2e1-0-128': [6.300734043121338],
            'asconP_2R_NCA-isw2e1-0-160': [6.642865896224976],
            'asconP_2R_NCA-isw2e1-0-192': [7.3873677253723145],
            'asconP_2R_NCA-isw2e1-0-224': [10.394385576248169],
            'asconP_2R_NCA-isw2e1-0-256': [20.601011753082275],
            'asconP_2R_NCA-isw2e1-0-288': [21.82456350326538],
            'asconP_2R_NCA-isw2e1-0-320': [23.44320559501648],
            'asconP_2R_NCA-isw2e1-0-352': [24.635647773742676],
            'asconP_2R_NCA-isw2e1-0-384': [26.37549901008606],
            'asconP_2R_NCA-isw2e1-0-416': [28.39501976966858],
            'asconP_2R_NCA-isw2e1-0-448': [30.516767740249634],
            'asconP_2R_NCA-isw2e1-1-32': [22.66486930847168],
            'asconP_2R_NCA-isw2e1-1-64': [16.82642412185669],
            'asconP_2R_NCA-isw2e1-1-96': [15.211930990219116],
            'asconP_2R_NCA-isw2e1-1-128': [15.157908201217651],
            'asconP_2R_NCA-isw2e1-1-160': [16.011788368225098],
            'asconP_2R_NCA-isw2e1-1-192': [17.11225938796997],
            'asconP_2R_NCA-isw2e1-1-224': [18.418660640716553],
            'asconP_2R_NCA-isw2e1-1-256': [20.20003390312195],
            'asconP_2R_NCA-isw2e1-1-288': [21.54514789581299],
            'asconP_2R_NCA-isw2e1-1-320': [23.172249794006348],
            'asconP_2R_NCA-isw2e1-1-352': [24.604676246643066],
            'asconP_2R_NCA-isw2e1-1-384': [26.488014221191406],
            'asconP_2R_NCA-isw2e1-1-416': [28.637735843658447],
            'asconP_2R_NCA-isw2e1-1-448': [29.72106623649597],
            'asconP_2R_NCA-isw2e1-2-32': [22.521564960479736],
            'asconP_2R_NCA-isw2e1-2-64': [16.668323516845703],
            'asconP_2R_NCA-isw2e1-2-96': [15.295588970184326],
            'asconP_2R_NCA-isw2e1-2-128': [15.219266891479492],
            'asconP_2R_NCA-isw2e1-2-160': [16.094303131103516],
            'asconP_2R_NCA-isw2e1-2-192': [17.17998456954956],
            'asconP_2R_NCA-isw2e1-2-224': [18.579587936401367],
            'asconP_2R_NCA-isw2e1-2-256': [20.215274333953857],
            'asconP_2R_NCA-isw2e1-2-288': [21.533568859100342],
            'asconP_2R_NCA-isw2e1-2-320': [23.205177783966064],
            'asconP_2R_NCA-isw2e1-2-352': [24.531989336013794],
            'asconP_2R_NCA-isw2e1-2-384': [26.378181219100952],
            'asconP_2R_NCA-isw2e1-2-416': [28.622577667236328],
            'asconP_2R_NCA-isw2e1-2-448': [29.83880090713501],
            'asconP_2R_NCA-isw2e1-3-32': [22.556459426879883],
            'asconP_2R_NCA-isw2e1-3-64': [17.11897563934326],
            'asconP_2R_NCA-isw2e1-3-96': [15.23517107963562],
            'asconP_2R_NCA-isw2e1-3-128': [15.183934926986694],
            'asconP_2R_NCA-isw2e1-3-160': [15.947891473770142],
            'asconP_2R_NCA-isw2e1-3-192': [17.07996416091919],
            'asconP_2R_NCA-isw2e1-3-224': [18.49725866317749],
            'asconP_2R_NCA-isw2e1-3-256': [20.13697624206543],
            'asconP_2R_NCA-isw2e1-3-288': [21.54644227027893],
            'asconP_2R_NCA-isw2e1-3-320': [23.202287435531616],
            'asconP_2R_NCA-isw2e1-3-352': [24.566598653793335],
            'asconP_2R_NCA-isw2e1-3-384': [26.263603925704956],
            'asconP_2R_NCA-isw2e1-3-416': [28.42494487762451],
            'asconP_2R_NCA-isw2e1-3-448': [29.836621522903442],
            'asconP_2R_NCA-isw2e1-4-32': [22.70076298713684],
            'asconP_2R_NCA-isw2e1-4-64': [16.53908371925354],
            'asconP_2R_NCA-isw2e1-4-96': [15.280580520629883],
            'asconP_2R_NCA-isw2e1-4-128': [15.24152135848999],
            'asconP_2R_NCA-isw2e1-4-160': [16.51780104637146],
            'asconP_2R_NCA-isw2e1-4-192': [17.112196922302246],
            'asconP_2R_NCA-isw2e1-4-224': [18.47835659980774],
            'asconP_2R_NCA-isw2e1-4-256': [20.723551511764526],
            'asconP_2R_NCA-isw2e1-4-288': [21.618741989135742],
            'asconP_2R_NCA-isw2e1-4-320': [23.204020261764526],
            'asconP_2R_NCA-isw2e1-4-352': [24.590930938720703],
            'asconP_2R_NCA-isw2e1-4-384': [26.54103922843933],
            'asconP_2R_NCA-isw2e1-4-416': [28.487539291381836],
            'asconP_2R_NCA-isw2e1-4-448': [30.01022696495056]}
        times2 = {'asconP_2R_NCA-isw2e2-0-32': [7.809126138687134],
                  'asconP_2R_NCA-isw2e2-0-64': [5.9967429637908936],
                  'asconP_2R_NCA-isw2e2-0-96': [5.742457866668701],
                  'asconP_2R_NCA-isw2e2-0-128': [5.867757320404053],
                  'asconP_2R_NCA-isw2e2-0-160': [6.243370294570923],
                  'asconP_2R_NCA-isw2e2-0-192': [7.543330669403076],
                  'asconP_2R_NCA-isw2e2-0-224': [18.758337020874023],
                  'asconP_2R_NCA-isw2e2-0-256': [20.315582036972046],
                  'asconP_2R_NCA-isw2e2-0-288': [21.135919094085693],
                  'asconP_2R_NCA-isw2e2-0-320': [22.743025541305542],
                  'asconP_2R_NCA-isw2e2-0-352': [24.04570770263672],
                  'asconP_2R_NCA-isw2e2-0-384': [25.75600004196167],
                  'asconP_2R_NCA-isw2e2-0-416': [28.054408311843872],
                  'asconP_2R_NCA-isw2e2-0-448': [29.320696115493774],
                  'asconP_2R_NCA-isw2e2-1-32': [19.861725330352783],
                  'asconP_2R_NCA-isw2e2-1-64': [15.200570821762085],
                  'asconP_2R_NCA-isw2e2-1-96': [14.273238182067871],
                  'asconP_2R_NCA-isw2e2-1-128': [14.443653583526611],
                  'asconP_2R_NCA-isw2e2-1-160': [15.317109823226929],
                  'asconP_2R_NCA-isw2e2-1-192': [16.535764932632446],
                  'asconP_2R_NCA-isw2e2-1-224': [17.871933937072754],
                  'asconP_2R_NCA-isw2e2-1-256': [19.540664434432983],
                  'asconP_2R_NCA-isw2e2-1-288': [20.870407342910767],
                  'asconP_2R_NCA-isw2e2-1-320': [22.60249662399292],
                  'asconP_2R_NCA-isw2e2-1-352': [23.95364761352539],
                  'asconP_2R_NCA-isw2e2-1-384': [25.87070107460022],
                  'asconP_2R_NCA-isw2e2-1-416': [28.18632435798645],
                  'asconP_2R_NCA-isw2e2-1-448': [29.2610342502594],
                  'asconP_2R_NCA-isw2e2-2-32': [19.981114864349365],
                  'asconP_2R_NCA-isw2e2-2-64': [15.180844068527222],
                  'asconP_2R_NCA-isw2e2-2-96': [14.346033811569214],
                  'asconP_2R_NCA-isw2e2-2-128': [14.39934229850769],
                  'asconP_2R_NCA-isw2e2-2-160': [15.39604139328003],
                  'asconP_2R_NCA-isw2e2-2-192': [16.558502435684204],
                  'asconP_2R_NCA-isw2e2-2-224': [17.807085514068604],
                  'asconP_2R_NCA-isw2e2-2-256': [19.881505727767944],
                  'asconP_2R_NCA-isw2e2-2-288': [21.298915147781372],
                  'asconP_2R_NCA-isw2e2-2-320': [22.62593984603882],
                  'asconP_2R_NCA-isw2e2-2-352': [24.056336879730225],
                  'asconP_2R_NCA-isw2e2-2-384': [26.571644067764282],
                  'asconP_2R_NCA-isw2e2-2-416': [27.97531819343567],
                  'asconP_2R_NCA-isw2e2-2-448': [29.40782380104065],
                  'asconP_2R_NCA-isw2e2-3-32': [20.171040534973145],
                  'asconP_2R_NCA-isw2e2-3-64': [15.138816356658936],
                  'asconP_2R_NCA-isw2e2-3-96': [15.398377895355225],
                  'asconP_2R_NCA-isw2e2-3-128': [14.404290676116943],
                  'asconP_2R_NCA-isw2e2-3-160': [15.292654514312744],
                  'asconP_2R_NCA-isw2e2-3-192': [16.5341899394989],
                  'asconP_2R_NCA-isw2e2-3-224': [17.928816080093384],
                  'asconP_2R_NCA-isw2e2-3-256': [19.646547317504883],
                  'asconP_2R_NCA-isw2e2-3-288': [20.910773992538452],
                  'asconP_2R_NCA-isw2e2-3-320': [22.65920329093933],
                  'asconP_2R_NCA-isw2e2-3-352': [25.07425856590271],
                  'asconP_2R_NCA-isw2e2-3-384': [25.76795983314514],
                  'asconP_2R_NCA-isw2e2-3-416': [27.909476041793823],
                  'asconP_2R_NCA-isw2e2-3-448': [29.255433082580566],
                  'asconP_2R_NCA-isw2e2-4-32': [19.861956119537354],
                  'asconP_2R_NCA-isw2e2-4-64': [15.309233665466309],
                  'asconP_2R_NCA-isw2e2-4-96': [14.281099557876587],
                  'asconP_2R_NCA-isw2e2-4-128': [14.566631317138672],
                  'asconP_2R_NCA-isw2e2-4-160': [15.675753116607666],
                  'asconP_2R_NCA-isw2e2-4-192': [16.613996028900146],
                  'asconP_2R_NCA-isw2e2-4-224': [17.81789994239807],
                  'asconP_2R_NCA-isw2e2-4-256': [20.10734534263611],
                  'asconP_2R_NCA-isw2e2-4-288': [20.969107151031494],
                  'asconP_2R_NCA-isw2e2-4-320': [22.621777057647705],
                  'asconP_2R_NCA-isw2e2-4-352': [24.024951696395874],
                  'asconP_2R_NCA-isw2e2-4-384': [25.927953004837036],
                  'asconP_2R_NCA-isw2e2-4-416': [28.06125521659851],
                  'asconP_2R_NCA-isw2e2-4-448': [29.27479362487793]}
        z = [32, 64, 96, 128, 160, 192, 224, 256, 288, 320, 352, 384, 416, 448]
        x = [9.321946382522583, 6.98106575012207, 6.663027763366699, 6.661635398864746, 6.546462535858154,
             6.993530035018921, 7.583965063095093, 8.283821821212769, 8.885507345199585, 9.613505125045776,
             10.15358853340149, 10.850411653518677, 11.724337816238403, 12.32200288772583]
        y = [8.113517761230469, 6.530013084411621, 5.90791654586792, 5.896665334701538, 6.201824188232422,
             6.704261541366577, 7.240850210189819, 7.919913291931152, 8.541930913925171, 9.191009521484375,
             9.74407958984375, 10.460332155227661, 11.408489227294922, 11.933516263961792]
        plt.fill_between(z, x, y, alpha=0.5, linewidth=0.1, linestyle='--')
        plt.plot(z, x, marker='*')
        plt.plot(z, y, marker='*')
        plt.title("Ascon LDA 5 bit vs 2 bit")
        plt.grid(axis='y', alpha=0.25, color='grey')
        plt.xlabel("Window Size")
        # plt.xticks(X)
        plt.ylabel("Time (in seconds)")
        plt.legend(["5-bit", "2-bit"], loc='upper left')
        plt.show()

    def test_ranking(self):
        # proof ranking -- no need
        ascon_array = [(ascon_key_1, [
            # ascon_clear1,
            ascon_isw2_1,
            # ascon_isw3_1, ascon_isw4_1,
            # ascon_minq_1, ascon_ql2_1,
            # ascon_ql3_1, ascon_ql4_1,
            # ascon_cl2_1, ascon_cl3_1,
            # ascon_cl4_1
        ])]
        window_size = 32
        window_step = 32
        # nr_traces = window_size + 50  # 2^50
        times = {}
        KEY_BYTES = tuple(i for i in range(64))
        for key, masks in ascon_array:
            for i in range(0, len(masks)):
                for w in range(window_size, window_size * 15, window_step):
                    print("w", w)
                    for _ in range(2):
                        if _ == 0:
                            ranking = True
                        else:
                            ranking = False
                        with self.subTest(name=(masks[i], w + 50), T=w + 50):
                            start = time.time()
                            r = Ascon_LDA.ascon_lda(traces=w + 50, traces_dir=masks[i], window_size=w,
                                                    window_step=w // 1, KEY_BYTES=KEY_BYTES,
                                                    verbose=True,
                                                    RANKING=ranking)
                            print(r)
                            end = time.time()
                            elapsed = end - start
                            times[masks[i].name + "-" + str(w)] = elapsed
                            print("{} elapsed time: {} with {} traces".format(masks[i].name, elapsed, w + 50))
                            self.assertEqual(key, r)
        print(times)


if __name__ == '__main__':
    unittest.main()
