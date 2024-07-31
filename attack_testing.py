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

    aes_exact_array = [(aes_key_1, [aes_clear1, aes_isw2_1, aes_minq_1]),
                       (aes_key_2, [aes_clear2, aes_isw2_2, aes_minq_2])]

    ascon_exact_array = [(ascon_key_1, [ascon_clear1, ascon_isw2_1, ascon_minq_1]),
                         (ascon_key_2, [ascon_clear2, ascon_isw2_2, ascon_minq_2])]

    aes_lda_array = [(aes_key_1, tr_aes_1),
                     (aes_key_2, tr_aes_2), ]
    aes_lda_array_2 = [(aes_key_1, tr_aes_1[1:5])]
    ascon_lda_array = [(ascon_key_1, tr_ascon_1),
                       (ascon_key_2, tr_ascon_2)]

    def test_aes_exact(self):
        all_times = []
        for key, masks in self.aes_exact_array:
            for i in range(0, len(masks)):
                timings = [[], []]
                for t in range(32, 65, 8):
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
                all_times.append(timings)
        # print(all_times)
        # k1 = all_times[:3]
        # plt.subplot(1, 2, 1)
        # for x, y in k1:
        #     print(x, y)
        #     plt.plot(x, y, linestyle='-', marker='*')
        # plt.title("first key")
        # plt.legend(["1", "2", "3"])
        # k2 = all_times[3:]
        # plt.subplot(1, 2, 2)
        # for x, y in k2:
        #     plt.plot(x, y, linestyle='-', marker='*')
        # plt.title("second key")
        # plt.legend(["1", "2", "3"])
        # plt.show()
        """
        DONE:   key has no effect on performance
        Done:   proof of concept (works as intended)
                minimum traces
                show circuit size impacting performance
                success vs failure on performance
                show quickly become infeasible for lda
                show exponential growth
                ...
                make nice
                reboot pc
                improve ascon performance  maybe
        """

    def test_ascon_exact(self):
        for key, masks in self.ascon_exact_array:
            for i in range(0, len(masks)):
                for t in range(32, 65, 16):
                    with self.subTest(name=(masks[i], t), T=t):
                        start = time.time()
                        r = Ascon_ExactMatch.attack(t, masks[i])  # non-masked
                        if i == 0:
                            self.assertEqual(key, r)  # should succeed
                        else:
                            self.assertNotEqual(key, r)  # should fail
                        end = time.time()
                        elapsed = end - start
                        print("{} elapsed time: {} with {} traces".format(masks[i].name, elapsed, t))

    # todo: minimal window etc
    # todo: masking + obfuscation comparison

    def test_lda_aes(self):
        nr_traces = 32 + 50
        increment = 32
        nr_of_runs = 10

        KEY_BYTES = tuple(i for i in range(16))
        # for key, masks in self.aes_lda_array:
        for key, masks in self.aes_lda_array_2:
            # key = key[:2]
            for i in range(0, len(masks)):
                for t in range(nr_traces, 64 + 50 + 1, increment):
                    with self.subTest(name=(masks[i], t), T=t):
                        start = time.time()
                        for _ in range(nr_of_runs):
                            r = AES_LDA.aes_lda(traces=t, traces_dir=masks[i], window_size=t - 50,
                                                window_step=(t - 50) // 2, KEY_BYTES=KEY_BYTES)  # non-masked
                            if i < 3:
                                self.assertEqual(key, r)  # should succeed
                            else:
                                self.assertNotEqual(key, r)  # should fail
                        end = time.time()
                        elapsed = end - start
                        print("{} elapsed time: {} with {} traces".format(masks[i].name, elapsed, t))

        # timings = [[None] * nr_increments for _ in range(len(tr_aes_1))]
        # for i in range(len(tr_aes_1)):  # all the implementations
        #     target = tr_aes_1[i].parents[0].name  # secret key we want to find
        #     target = target.encode('utf-8').hex()  # bytes.fromhex("61626364656667684142434445464748")
        #     for inc in range(nr_increments):
        #         times = []
        #         w_size = (inc + 1) * 64
        #         for j in range(nr_of_runs):  # average of 10 runs
        #             t_start = time.time()
        #             s_size = w_size // 2
        #             tr = w_size + 50  # 2^50 chance of failure ?
        #             r = AES_LDA.aes_lda(tr, tr_aes_1[i], w_size, s_size)
        #             self.assertEqual(target, r)
        #             t_stop = time.time()
        #             elapsed_time = str(t_stop - t_start)[:6]
        #             times.append(float(elapsed_time))
        #         timings[i][inc] = np.average(times)
        #         print(timings)


if __name__ == '__main__':
    unittest.main()

# aes2-clear elapsed time: 5.520910739898682 with 114 traces
# aes2-clear elapsed time: 5.674640417098999 with 130 traces
# aes2-clear elapsed time: 5.86058497428894 with 146 traces
# aes2-clear elapsed time: 6.194171190261841 with 162 traces
# aes2-clear elapsed time: 6.575989246368408 with 178 traces
# aes2-clear elapsed time: 7.071808576583862 with 194 traces
# aes2-clear elapsed time: 7.388443231582642 with 210 traces
# aes2-clear elapsed time: 7.6459572315216064 with 226 traces
# aes2-clear elapsed time: 8.18288803100586 with 242 traces
# aes2-clear elapsed time: 8.520897388458252 with 258 traces
# aes2-clear elapsed time: 8.872462749481201 with 274 traces
# aes2-clear elapsed time: 9.432048320770264 with 290 traces
# aes2-clear elapsed time: 9.761123418807983 with 306 traces
# aes2-isw2 elapsed time: 15.296777486801147 with 114 traces
# aes2-isw2 elapsed time: 15.46338939666748 with 130 traces
# aes2-isw2 elapsed time: 15.881580591201782 with 146 traces
# aes2-isw2 elapsed time: 16.60208821296692 with 162 traces
# aes2-isw2 elapsed time: 17.273742198944092 with 178 traces
# aes2-isw2 elapsed time: 18.219271183013916 with 194 traces
# aes2-isw2 elapsed time: 19.09377670288086 with 210 traces
# aes2-isw2 elapsed time: 20.00856328010559 with 226 traces
# aes2-isw2 elapsed time: 21.2017343044281 with 242 traces
# aes2-isw2 elapsed time: 22.283329486846924 with 258 traces
# aes2-isw2 elapsed time: 23.36983561515808 with 274 traces
# aes2-isw2 elapsed time: 24.418556690216064 with 290 traces
# aes2-isw2 elapsed time: 25.453880071640015 with 306 traces
# aes2-isw3 elapsed time: 29.41950035095215 with 114 traces
# aes2-isw3 elapsed time: 29.292570114135742 with 130 traces
# aes2-isw3 elapsed time: 30.14198350906372 with 146 traces
# aes2-isw3 elapsed time: 31.051223516464233 with 162 traces
# aes2-isw3 elapsed time: 32.464845418930054 with 178 traces
# aes2-isw3 elapsed time: 33.69513511657715 with 194 traces
# aes2-isw3 elapsed time: 35.35506510734558 with 210 traces
# aes2-isw3 elapsed time: 37.163738489151 with 226 traces
# aes2-isw3 elapsed time: 39.77147197723389 with 242 traces
# aes2-isw3 elapsed time: 41.331775188446045 with 258 traces
# aes2-isw3 elapsed time: 43.45059823989868 with 274 traces
# aes2-isw3 elapsed time: 44.8979070186615 with 290 traces
# aes2-isw3 elapsed time: 47.347625494003296 with 306 traces
# aes2-isw4 elapsed time: 48.14706230163574 with 114 traces
# aes2-isw4 elapsed time: 47.70807886123657 with 130 traces
# aes2-isw4 elapsed time: 49.17772030830383 with 146 traces
# aes2-isw4 elapsed time: 50.43869185447693 with 162 traces
# aes2-isw4 elapsed time: 52.766879081726074 with 178 traces
# aes2-isw4 elapsed time: 54.52900505065918 with 194 traces
# aes2-isw4 elapsed time: 57.955275774002075 with 210 traces
# aes2-isw4 elapsed time: 60.04417824745178 with 226 traces
# aes2-isw4 elapsed time: 63.084022998809814 with 242 traces
# aes2-isw4 elapsed time: 65.65831160545349 with 258 traces
# aes2-isw4 elapsed time: 68.94679546356201 with 274 traces
# aes2-isw4 elapsed time: 71.91768765449524 with 290 traces
# aes2-isw4 elapsed time: 75.06888437271118 with 306 traces
# aes2-minq elapsed time: 120.32065200805664 with 114 traces
# aes2-minq elapsed time: 119.07404446601868 with 130 traces
# aes2-minq elapsed time: 120.71823835372925 with 146 traces
# aes2-minq elapsed time: 124.49672842025757 with 162 traces
# aes2-minq elapsed time: 128.613618850708 with 178 traces
# aes2-minq elapsed time: 132.31436562538147 with 194 traces
# aes2-minq elapsed time: 138.38968110084534 with 210 traces
# aes2-minq elapsed time: 143.63537788391113 with 226 traces
# aes2-minq elapsed time: 150.31783843040466 with 242 traces
# aes2-minq elapsed time: 156.75036883354187 with 258 traces
# aes2-minq elapsed time: 164.2995162010193 with 274 traces
# aes2-minq elapsed time: 171.07203030586243 with 290 traces
# aes2-minq elapsed time: 178.11124753952026 with 306 traces
# aes2-ql2 elapsed time: 157.20459866523743 with 114 traces
# aes2-ql2 elapsed time: 158.08742809295654 with 130 traces
# aes2-ql2 elapsed time: 158.14853048324585 with 146 traces
# aes2-ql2 elapsed time: 161.78663969039917 with 162 traces
# aes2-ql2 elapsed time: 166.98678851127625 with 178 traces
# aes2-ql2 elapsed time: 173.4004409313202 with 194 traces
# aes2-ql2 elapsed time: 179.7280077934265 with 210 traces
# aes2-ql2 elapsed time: 187.6796407699585 with 226 traces
# aes2-ql2 elapsed time: 194.8364701271057 with 242 traces
# aes2-ql2 elapsed time: 204.93873238563538 with 258 traces
# aes2-ql2 elapsed time: 213.20660710334778 with 274 traces
# aes2-ql2 elapsed time: 221.3427414894104 with 290 traces
# aes2-ql2 elapsed time: 230.69302463531494 with 306 traces
# aes2-ql3 elapsed time: 211.10276985168457 with 114 traces
# aes2-ql3 elapsed time: 207.0895972251892 with 130 traces
# aes2-ql3 elapsed time: 210.6625497341156 with 146 traces
# aes2-ql3 elapsed time: 215.1593337059021 with 162 traces
# aes2-ql3 elapsed time: 223.23983025550842 with 178 traces
# aes2-ql3 elapsed time: 230.21345782279968 with 194 traces
# aes2-ql3 elapsed time: 240.4984645843506 with 210 traces
# aes2-ql3 elapsed time: 249.94672536849976 with 226 traces
# aes2-ql3 elapsed time: 260.14381170272827 with 242 traces
# aes2-ql3 elapsed time: 272.6399509906769 with 258 traces
# aes2-ql3 elapsed time: 285.5906307697296 with 274 traces
# aes2-ql3 elapsed time: 295.57088351249695 with 290 traces
# aes2-ql3 elapsed time: 307.3969316482544 with 306 traces
# aes2-ql4 elapsed time: 280.29691314697266 with 114 traces
# aes2-ql4 elapsed time: 277.0191991329193 with 130 traces
# aes2-ql4 elapsed time: 280.92984104156494 with 146 traces
# aes2-ql4 elapsed time: 288.3605799674988 with 162 traces
# aes2-ql4 elapsed time: 297.8920066356659 with 178 traces
# aes2-ql4 elapsed time: 307.46907567977905 with 194 traces
# aes2-ql4 elapsed time: 319.83290815353394 with 210 traces
# aes2-ql4 elapsed time: 334.9429361820221 with 226 traces
# aes2-ql4 elapsed time: 348.4918112754822 with 242 traces
# aes2-ql4 elapsed time: 364.78632140159607 with 258 traces
# aes2-ql4 elapsed time: 380.5983986854553 with 274 traces
# aes2-ql4 elapsed time: 396.6848073005676 with 290 traces
# aes2-ql4 elapsed time: 412.7790722846985 with 306 traces
# aes2-cl2 elapsed time: 387.7007484436035 with 114 traces
# aes2-cl2 elapsed time: 381.4245676994324 with 130 traces
# aes2-cl2 elapsed time: 386.1526472568512 with 146 traces
# aes2-cl2 elapsed time: 396.35721158981323 with 162 traces
# aes2-cl2 elapsed time: 409.23515605926514 with 178 traces
# aes2-cl2 elapsed time: 422.7187349796295 with 194 traces
# aes2-cl2 elapsed time: 436.81358075141907 with 210 traces
# aes2-cl2 elapsed time: 453.6931862831116 with 226 traces
# aes2-cl2 elapsed time: 470.57132935523987 with 242 traces
# aes2-cl2 elapsed time: 490.7526378631592 with 258 traces
# aes2-cl2 elapsed time: 510.9798753261566 with 274 traces
# aes2-cl2 elapsed time: 531.1320381164551 with 290 traces
# aes2-cl2 elapsed time: 552.0145440101624 with 306 traces
# aes2-cl3 elapsed time: 459.06303453445435 with 114 traces
# aes2-cl3 elapsed time: 451.1157121658325 with 130 traces
# aes2-cl3 elapsed time: 458.215252161026 with 146 traces
# aes2-cl3 elapsed time: 468.9189176559448 with 162 traces
# aes2-cl3 elapsed time: 482.58494997024536 with 178 traces
# aes2-cl3 elapsed time: 501.21766114234924 with 194 traces
# aes2-cl3 elapsed time: 517.5306992530823 with 210 traces
# aes2-cl3 elapsed time: 538.6653575897217 with 226 traces
# aes2-cl3 elapsed time: 559.7463760375977 with 242 traces
# aes2-cl3 elapsed time: 583.4668281078339 with 258 traces
# aes2-cl3 elapsed time: 606.5393524169922 with 274 traces
# aes2-cl3 elapsed time: 629.5527305603027 with 290 traces
# aes2-cl3 elapsed time: 655.6227695941925 with 306 traces
# aes2-cl4 elapsed time: 547.6667892932892 with 114 traces
# aes2-cl4 elapsed time: 538.7054128646851 with 130 traces
# aes2-cl4 elapsed time: 545.6823585033417 with 146 traces
# aes2-cl4 elapsed time: 557.9427447319031 with 162 traces
# aes2-cl4 elapsed time: 575.7643027305603 with 178 traces
# aes2-cl4 elapsed time: 592.4037399291992 with 194 traces
# aes2-cl4 elapsed time: 617.60245013237 with 210 traces
# aes2-cl4 elapsed time: 641.076824426651 with 226 traces
# aes2-cl4 elapsed time: 666.1659469604492 with 242 traces
# aes2-cl4 elapsed time: 693.1522631645203 with 258 traces
# aes2-cl4 elapsed time: 721.8711318969727 with 274 traces
# aes2-cl4 elapsed time: 748.0055179595947 with 290 traces
# aes2-cl4 elapsed time: 781.506728887558 with 306 traces
# aes2-clear elapsed time: 5.510002613067627 with 114 traces
# aes2-clear elapsed time: 5.636198997497559 with 130 traces
# aes2-clear elapsed time: 5.952534914016724 with 146 traces
# aes2-clear elapsed time: 6.203113794326782 with 162 traces
# aes2-clear elapsed time: 6.562439918518066 with 178 traces
# aes2-clear elapsed time: 6.99556040763855 with 194 traces
# aes2-clear elapsed time: 7.366389513015747 with 210 traces
# aes2-clear elapsed time: 7.660674333572388 with 226 traces
# aes2-clear elapsed time: 8.08679485321045 with 242 traces
# aes2-clear elapsed time: 8.559169054031372 with 258 traces
# aes2-clear elapsed time: 8.855508804321289 with 274 traces
# aes2-clear elapsed time: 9.447039604187012 with 290 traces
# aes2-clear elapsed time: 9.818166494369507 with 306 traces
# aes2-isw2 elapsed time: 15.303198099136353 with 114 traces
# aes2-isw2 elapsed time: 15.444081544876099 with 130 traces
# aes2-isw2 elapsed time: 15.995335102081299 with 146 traces
# aes2-isw2 elapsed time: 16.623050451278687 with 162 traces
# aes2-isw2 elapsed time: 17.330716371536255 with 178 traces
# aes2-isw2 elapsed time: 18.22111463546753 with 194 traces
# aes2-isw2 elapsed time: 19.213433504104614 with 210 traces
# aes2-isw2 elapsed time: 20.12177538871765 with 226 traces
# aes2-isw2 elapsed time: 21.193077564239502 with 242 traces
# aes2-isw2 elapsed time: 22.377628564834595 with 258 traces
# aes2-isw2 elapsed time: 23.391473531723022 with 274 traces
# aes2-isw2 elapsed time: 24.427293062210083 with 290 traces
# aes2-isw2 elapsed time: 25.516074657440186 with 306 traces
# aes2-isw3 elapsed time: 29.388243198394775 with 114 traces
# aes2-isw3 elapsed time: 29.269273281097412 with 130 traces
# aes2-isw3 elapsed time: 30.103126287460327 with 146 traces
# aes2-isw3 elapsed time: 31.034419298171997 with 162 traces
# aes2-isw3 elapsed time: 32.46589684486389 with 178 traces
# aes2-isw3 elapsed time: 33.6596896648407 with 194 traces
# aes2-isw3 elapsed time: 35.36994552612305 with 210 traces
# aes2-isw3 elapsed time: 36.975207805633545 with 226 traces

# ----------------------------------------------------------

# /usr/bin/python3 /home/lalex/.pycharm_helpers/pycharm/_jb_unittest_runner.py --target attack_testing.TestMethods.test_lda_aes
# Testing started at 02:15 ...
# Launching unittests with arguments python -m unittest attack_testing.TestMethods.test_lda_aes in /mnt/h/Master/Thesis/Implementation
#
# aes2-clear elapsed time: 5.440603733062744 with 114 traces
# aes2-clear elapsed time: 5.589576244354248 with 130 traces
# aes2-clear elapsed time: 5.86006760597229 with 146 traces
# aes2-clear elapsed time: 6.128944635391235 with 162 traces
# aes2-clear elapsed time: 6.638039588928223 with 178 traces
# aes2-isw2 elapsed time: 15.312106370925903 with 114 traces
# aes2-isw2 elapsed time: 15.313214778900146 with 130 traces
# aes2-isw2 elapsed time: 15.720897674560547 with 146 traces
# aes2-isw2 elapsed time: 16.444363832473755 with 162 traces
# aes2-isw2 elapsed time: 17.17342782020569 with 178 traces
# aes2-isw3 elapsed time: 29.11679434776306 with 114 traces
# aes2-isw3 elapsed time: 29.107664823532104 with 130 traces
# aes2-isw3 elapsed time: 29.68756103515625 with 146 traces
# aes2-isw3 elapsed time: 30.728752851486206 with 162 traces
# aes2-isw3 elapsed time: 32.09496450424194 with 178 traces
# aes2-isw4 elapsed time: 47.20313596725464 with 114 traces
# aes2-isw4 elapsed time: 47.088515520095825 with 130 traces
# aes2-isw4 elapsed time: 48.01134371757507 with 146 traces
# aes2-isw4 elapsed time: 49.70813202857971 with 162 traces
# aes2-isw4 elapsed time: 51.68973970413208 with 178 traces
# aes2-minq elapsed time: 118.6519525051117 with 114 traces
# aes2-minq elapsed time: 117.54326820373535 with 130 traces
# aes2-minq elapsed time: 119.22465348243713 with 146 traces
# aes2-minq elapsed time: 122.14904522895813 with 162 traces
# aes2-minq elapsed time: 126.67842364311218 with 178 traces
# aes2-ql2 elapsed time: 155.82058835029602 with 114 traces
# aes2-ql2 elapsed time: 153.62791466712952 with 130 traces
# aes2-ql2 elapsed time: 155.9987211227417 with 146 traces
# aes2-ql2 elapsed time: 159.8354208469391 with 162 traces
# aes2-ql2 elapsed time: 165.56592178344727 with 178 traces
# aes2-ql3 elapsed time: 207.59663271903992 with 114 traces
# aes2-ql3 elapsed time: 206.0067207813263 with 130 traces
# aes2-ql3 elapsed time: 207.60635781288147 with 146 traces
# aes2-ql3 elapsed time: 212.86365342140198 with 162 traces
# aes2-ql3 elapsed time: 220.57341861724854 with 178 traces
# aes2-ql4 elapsed time: 277.0586121082306 with 114 traces
# aes2-ql4 elapsed time: 273.1708483695984 with 130 traces
# aes2-ql4 elapsed time: 277.6653802394867 with 146 traces
# aes2-ql4 elapsed time: 284.8244435787201 with 162 traces
# aes2-ql4 elapsed time: 295.172000169754 with 178 traces
# aes2-cl2 elapsed time: 382.41150736808777 with 114 traces
# aes2-cl2 elapsed time: 378.23337411880493 with 130 traces
# aes2-cl2 elapsed time: 382.8083791732788 with 146 traces
# aes2-cl2 elapsed time: 393.0264000892639 with 162 traces
# aes2-cl2 elapsed time: 403.2573926448822 with 178 traces
# aes2-cl3 elapsed time: 453.5750889778137 with 114 traces
# aes2-cl3 elapsed time: 447.6094694137573 with 130 traces
# aes2-cl3 elapsed time: 457.56841802597046 with 146 traces
# aes2-cl3 elapsed time: 462.6275517940521 with 162 traces
# aes2-cl3 elapsed time: 476.4398093223572 with 178 traces
# aes2-cl4 elapsed time: 540.9084677696228 with 114 traces
# aes2-cl4 elapsed time: 532.7154381275177 with 130 traces
# aes2-cl4 elapsed time: 539.3741252422333 with 146 traces
# aes2-cl4 elapsed time: 551.1416063308716 with 162 traces
# aes2-cl4 elapsed time: 568.976927280426 with 178 traces
# aes2-clear elapsed time: 5.399395942687988 with 114 traces
# aes2-clear elapsed time: 5.533383369445801 with 130 traces
# aes2-clear elapsed time: 5.793898105621338 with 146 traces
# aes2-clear elapsed time: 6.099315404891968 with 162 traces
# aes2-clear elapsed time: 6.400784492492676 with 178 traces
# aes2-isw2 elapsed time: 15.073419332504272 with 114 traces
# aes2-isw2 elapsed time: 15.194902420043945 with 130 traces
# aes2-isw2 elapsed time: 15.706335544586182 with 146 traces
# aes2-isw2 elapsed time: 16.35288119316101 with 162 traces
# aes2-isw2 elapsed time: 17.073833227157593 with 178 traces
# aes2-isw3 elapsed time: 29.085712909698486 with 114 traces
# aes2-isw3 elapsed time: 29.044951677322388 with 130 traces
# aes2-isw3 elapsed time: 29.58515238761902 with 146 traces
# aes2-isw3 elapsed time: 30.64351987838745 with 162 traces
# aes2-isw3 elapsed time: 31.9698588848114 with 178 traces
# aes2-isw4 elapsed time: 47.53949809074402 with 114 traces
# aes2-isw4 elapsed time: 47.33109712600708 with 130 traces
# aes2-isw4 elapsed time: 48.23528528213501 with 146 traces
# aes2-isw4 elapsed time: 49.664515256881714 with 162 traces
# aes2-isw4 elapsed time: 52.0170738697052 with 178 traces
# aes2-minq elapsed time: 118.55967283248901 with 114 traces
# aes2-minq elapsed time: 118.00641298294067 with 130 traces
# aes2-minq elapsed time: 119.16126227378845 with 146 traces
# aes2-minq elapsed time: 122.54500317573547 with 162 traces
# aes2-minq elapsed time: 126.7432632446289 with 178 traces
# aes2-ql2 elapsed time: 155.59618997573853 with 114 traces
# aes2-ql2 elapsed time: 153.823246717453 with 130 traces
# aes2-ql2 elapsed time: 156.41197657585144 with 146 traces
# aes2-ql2 elapsed time: 160.32181978225708 with 162 traces
# aes2-ql2 elapsed time: 165.67775440216064 with 178 traces
# aes2-ql3 elapsed time: 207.43609166145325 with 114 traces
# aes2-ql3 elapsed time: 205.70971536636353 with 130 traces
# aes2-ql3 elapsed time: 207.9787118434906 with 146 traces
# aes2-ql3 elapsed time: 213.15508890151978 with 162 traces
# aes2-ql3 elapsed time: 221.28459072113037 with 178 traces
# aes2-ql4 elapsed time: 275.65827465057373 with 114 traces
# aes2-ql4 elapsed time: 274.0285704135895 with 130 traces
# aes2-ql4 elapsed time: 278.4408299922943 with 146 traces
# aes2-ql4 elapsed time: 284.69360184669495 with 162 traces
# aes2-ql4 elapsed time: 294.73777174949646 with 178 traces
# aes2-cl2 elapsed time: 382.0649411678314 with 114 traces
# aes2-cl2 elapsed time: 376.9695768356323 with 130 traces
# aes2-cl2 elapsed time: 382.44805574417114 with 146 traces
# aes2-cl2 elapsed time: 391.27912616729736 with 162 traces
# aes2-cl2 elapsed time: 403.1166338920593 with 178 traces
# aes2-cl3 elapsed time: 452.53746032714844 with 114 traces
# aes2-cl3 elapsed time: 445.7825827598572 with 130 traces
# aes2-cl3 elapsed time: 455.49481177330017 with 146 traces
# aes2-cl3 elapsed time: 462.06910014152527 with 162 traces
# aes2-cl3 elapsed time: 477.19150614738464 with 178 traces
# aes2-cl4 elapsed time: 539.9586865901947 with 114 traces
# aes2-cl4 elapsed time: 533.4961614608765 with 130 traces
# aes2-cl4 elapsed time: 539.4677183628082 with 146 traces
# aes2-cl4 elapsed time: 551.9476993083954 with 162 traces
# aes2-cl4 elapsed time: 568.2315185070038 with 178 traces
# attack_testing.TestMethods.test_lda_aes: 22658.155 seconds
#
#
# Ran 1 test in 22658.173s
#
# OK
#
# Process finished with exit code 0

# /usr/bin/python3 /home/lalex/.pycharm_helpers/pycharm/_jb_unittest_runner.py --target attack_testing.TestMethods.test_lda_aes
# Testing started at 11:10 ...nr_of_runs = 2
# Launching unittests with arguments python -m unittest attack_testing.TestMethods.test_lda_aes in /mnt/h/Master/Thesis/Implementation
#
# aes2-isw2 elapsed time: 31.321855306625366 with 114 traces
# aes2-isw2 elapsed time: 31.76059627532959 with 115 traces
# aes2-isw2 elapsed time: 31.05227017402649 with 116 traces
# aes2-isw2 elapsed time: 31.668189764022827 with 117 traces
# aes2-isw2 elapsed time: 31.172528505325317 with 118 traces
# aes2-isw2 elapsed time: 31.603604793548584 with 119 traces
# aes2-isw2 elapsed time: 31.08590865135193 with 120 traces
# aes2-isw2 elapsed time: 31.86269760131836 with 121 traces
# aes2-isw2 elapsed time: 31.257648468017578 with 122 traces
# aes2-isw2 elapsed time: 31.78044843673706 with 123 traces
# aes2-isw2 elapsed time: 31.285975217819214 with 124 traces
# aes2-isw2 elapsed time: 31.872957468032837 with 125 traces
# aes2-isw2 elapsed time: 31.563244342803955 with 126 traces
# aes2-isw2 elapsed time: 31.798345804214478 with 127 traces
# aes2-isw2 elapsed time: 31.272671699523926 with 128 traces
# aes2-isw2 elapsed time: 31.703857898712158 with 129 traces
# aes2-isw2 elapsed time: 31.67380142211914 with 130 traces
# aes2-isw2 elapsed time: 32.11700487136841 with 131 traces
# aes2-isw2 elapsed time: 31.62382698059082 with 132 traces
# aes2-isw2 elapsed time: 32.070857524871826 with 133 traces
# aes2-isw2 elapsed time: 31.711243629455566 with 134 traces
# aes2-isw2 elapsed time: 32.14047884941101 with 135 traces
# aes2-isw2 elapsed time: 31.996427059173584 with 136 traces
# aes2-isw2 elapsed time: 32.310078620910645 with 137 traces
# aes2-isw2 elapsed time: 31.919031858444214 with 138 traces
# aes2-isw2 elapsed time: 32.61269807815552 with 139 traces
# aes2-isw2 elapsed time: 32.22621989250183 with 140 traces
# aes2-isw2 elapsed time: 32.62111020088196 with 141 traces
# aes2-isw2 elapsed time: 32.13924860954285 with 142 traces
# aes2-isw2 elapsed time: 32.64653301239014 with 143 traces
# aes2-isw2 elapsed time: 32.35359811782837 with 144 traces
# aes2-isw2 elapsed time: 33.19170331954956 with 145 traces
# aes2-isw2 elapsed time: 33.17460632324219 with 146 traces
# aes2-isw2 elapsed time: 33.20589518547058 with 147 traces
# aes2-isw2 elapsed time: 32.825392961502075 with 148 traces
# aes2-isw2 elapsed time: 33.27979612350464 with 149 traces
# aes2-isw2 elapsed time: 33.01585531234741 with 150 traces
# aes2-isw2 elapsed time: 33.542444705963135 with 151 traces
# aes2-isw2 elapsed time: 33.12322950363159 with 152 traces
# aes2-isw2 elapsed time: 33.85692763328552 with 153 traces
# aes2-isw2 elapsed time: 33.64441275596619 with 154 traces
# aes2-isw2 elapsed time: 33.7867636680603 with 155 traces
# aes2-isw2 elapsed time: 33.57568049430847 with 156 traces
# aes2-isw2 elapsed time: 33.79194688796997 with 157 traces
# aes2-isw2 elapsed time: 33.73282289505005 with 158 traces
# aes2-isw2 elapsed time: 33.94224190711975 with 159 traces
# aes2-isw2 elapsed time: 33.97358512878418 with 160 traces
# aes2-isw2 elapsed time: 34.26030731201172 with 161 traces
# aes2-isw2 elapsed time: 34.57201790809631 with 162 traces
# aes2-isw2 elapsed time: 34.8571412563324 with 163 traces
# aes2-isw2 elapsed time: 34.228737115859985 with 164 traces
# aes2-isw2 elapsed time: 34.66454195976257 with 165 traces
# aes2-isw2 elapsed time: 34.45488977432251 with 166 traces
# aes2-isw2 elapsed time: 35.010910987854004 with 167 traces
# aes2-isw2 elapsed time: 34.74202513694763 with 168 traces
# aes2-isw2 elapsed time: 34.946144819259644 with 169 traces
# aes2-isw2 elapsed time: 35.1293466091156 with 170 traces
# aes2-isw2 elapsed time: 35.312386989593506 with 171 traces
# aes2-isw2 elapsed time: 35.20147466659546 with 172 traces
# aes2-isw2 elapsed time: 35.738041400909424 with 173 traces
# aes2-isw2 elapsed time: 35.34731578826904 with 174 traces
# aes2-isw2 elapsed time: 35.88392114639282 with 175 traces
# aes2-isw2 elapsed time: 35.99100637435913 with 176 traces
# aes2-isw2 elapsed time: 35.82339024543762 with 177 traces
# aes2-isw2 elapsed time: 35.88321375846863 with 178 traces
# attack_testing.TestMethods.test_lda_aes: 2153.947 seconds
#
#
# Ran 1 test in 2153.958s
#
# OK
#
# Process finished with exit code 0

# /usr/bin/python3 /home/lalex/.pycharm_helpers/pycharm/_jb_unittest_runner.py --target attack_testing.TestMethods.test_lda_aes
# Testing started at 11:47 ...  nr_of_runs = 10
# Launching unittests with arguments python -m unittest attack_testing.TestMethods.test_lda_aes in /mnt/h/Master/Thesis/Implementation
#
# aes2-isw2 elapsed time: 151.1662003993988 with 114 traces
# aes2-isw2 elapsed time: 153.11829352378845 with 115 traces
# aes2-isw2 elapsed time: 149.38470673561096 with 116 traces
# aes2-isw2 elapsed time: 151.89494371414185 with 117 traces
# aes2-isw2 elapsed time: 149.06058073043823 with 118 traces
# aes2-isw2 elapsed time: 151.53233456611633 with 119 traces
# aes2-isw2 elapsed time: 149.07679152488708 with 120 traces
# aes2-isw2 elapsed time: 151.48894214630127 with 121 traces
# aes2-isw2 elapsed time: 149.9481976032257 with 122 traces
# aes2-isw2 elapsed time: 151.6413698196411 with 123 traces
# aes2-isw2 elapsed time: 149.68853068351746 with 124 traces
# aes2-isw2 elapsed time: 151.51526713371277 with 125 traces
# aes2-isw2 elapsed time: 149.8083381652832 with 126 traces
# aes2-isw2 elapsed time: 152.08639907836914 with 127 traces
# aes2-isw2 elapsed time: 149.3576889038086 with 128 traces
# aes2-isw2 elapsed time: 151.55494022369385 with 129 traces
# aes2-isw2 elapsed time: 151.4204740524292 with 130 traces
# aes2-isw2 elapsed time: 153.12977242469788 with 131 traces
# aes2-isw2 elapsed time: 150.68136715888977 with 132 traces
# aes2-isw2 elapsed time: 152.82630443572998 with 133 traces
# aes2-isw2 elapsed time: 151.0110604763031 with 134 traces
# aes2-isw2 elapsed time: 152.96717524528503 with 135 traces
# aes2-isw2 elapsed time: 151.57221221923828 with 136 traces
# aes2-isw2 elapsed time: 153.8116853237152 with 137 traces
# aes2-isw2 elapsed time: 152.7844934463501 with 138 traces
# aes2-isw2 elapsed time: 154.51919651031494 with 139 traces
# aes2-isw2 elapsed time: 153.5360128879547 with 140 traces
# aes2-isw2 elapsed time: 155.45614194869995 with 141 traces
# aes2-isw2 elapsed time: 153.85382199287415 with 142 traces
# aes2-isw2 elapsed time: 155.74161005020142 with 143 traces
# aes2-isw2 elapsed time: 154.20560240745544 with 144 traces
# aes2-isw2 elapsed time: 156.15001773834229 with 145 traces
# aes2-isw2 elapsed time: 156.83631920814514 with 146 traces
# attack_testing.TestMethods.test_lda_aes: 5022.832 seconds
#
#
# Ran 1 test in 5022.837s
#
# OK
#
# Process finished with exit code 0

# /usr/bin/python3 /home/lalex/.pycharm_helpers/pycharm/_jb_unittest_runner.py --target attack_testing.TestMethods.test_lda_aes
# Testing started at 13:56 ...  10 rounds
# Launching unittests with arguments python -m unittest attack_testing.TestMethods.test_lda_aes in /mnt/h/Master/Thesis/Implementation
#
# aes2-isw2 elapsed time: 152.15811777114868 with 114 traces
# aes2-isw2 elapsed time: 157.1763665676117 with 146 traces
# aes2-isw2 elapsed time: 170.6532952785492 with 178 traces
# aes2-isw3 elapsed time: 289.79916524887085 with 114 traces
# aes2-isw3 elapsed time: 298.6478519439697 with 146 traces
# aes2-isw3 elapsed time: 319.20194721221924 with 178 traces
# aes2-isw4 elapsed time: 472.81574988365173 with 114 traces
# aes2-isw4 elapsed time: 480.8398094177246 with 146 traces
# aes2-isw4 elapsed time: 517.5399718284607 with 178 traces
# attack_testing.TestMethods.test_lda_aes: 3224.332 seconds
# SubTest failure: Traceback (most recent call last):
#   File "/usr/lib/python3.10/unittest/case.py", line 59, in testPartExecutor
#     yield
#   File "/usr/lib/python3.10/unittest/case.py", line 498, in subTest
#     yield
#   File "/mnt/h/Master/Thesis/Implementation/attack_testing.py", line 181, in test_lda_aes
#     self.assertEqual(key, r)  # should succeed
#   File "/home/lalex/.pycharm_helpers/pycharm/teamcity/diff_tools.py", line 33, in _patched_equals
#     old(self, first, second, msg)
# AssertionError: '61626364656667684142434445464748' != ''
# - 61626364656667684142434445464748
# +
#
#
#
#
# Ran 1 test in 3224.346s
#
# FAILED (failures=3)
#
# SubTest failure: Traceback (most recent call last):
#   File "/usr/lib/python3.10/unittest/case.py", line 59, in testPartExecutor
#     yield
#   File "/usr/lib/python3.10/unittest/case.py", line 498, in subTest
#     yield
#   File "/mnt/h/Master/Thesis/Implementation/attack_testing.py", line 181, in test_lda_aes
#     self.assertEqual(key, r)  # should succeed
#   File "/home/lalex/.pycharm_helpers/pycharm/teamcity/diff_tools.py", line 33, in _patched_equals
#     old(self, first, second, msg)
# AssertionError: '61626364656667684142434445464748' != ''
# - 61626364656667684142434445464748
# +
#
#
#
# SubTest failure: Traceback (most recent call last):
#   File "/usr/lib/python3.10/unittest/case.py", line 59, in testPartExecutor
#     yield
#   File "/usr/lib/python3.10/unittest/case.py", line 498, in subTest
#     yield
#   File "/mnt/h/Master/Thesis/Implementation/attack_testing.py", line 181, in test_lda_aes
#     self.assertEqual(key, r)  # should succeed
#   File "/home/lalex/.pycharm_helpers/pycharm/teamcity/diff_tools.py", line 33, in _patched_equals
#     old(self, first, second, msg)
# AssertionError: '61626364656667684142434445464748' != ''
# - 61626364656667684142434445464748
# +
#
#
#
#
# One or more subtests failed
# Failed subtests list: (name=(PosixPath('traces/abcdefghABCDEFGH/aes2-minq'), 114), T=114), (name=(PosixPath('traces/abcdefghABCDEFGH/aes2-minq'), 146), T=146), (name=(PosixPath('traces/abcdefghABCDEFGH/aes2-minq'), 178), T=178)
#
# Process finished with exit code 1

# /usr/bin/python3 /home/lalex/.pycharm_helpers/pycharm/_jb_unittest_runner.py --target attack_testing.TestMethods.test_lda_aes
# Testing started at 14:51 ...  10 rounds
# Launching unittests with arguments python -m unittest attack_testing.TestMethods.test_lda_aes in /mnt/h/Master/Thesis/Implementation
#
# aes2-isw2 elapsed time: 154.2543625831604 with 114 traces
# aes2-isw2 elapsed time: 159.5877764225006 with 146 traces
# aes2-isw2 elapsed time: 173.32448744773865 with 178 traces
# aes2-isw3 elapsed time: 294.77472472190857 with 114 traces
# aes2-isw3 elapsed time: 301.4629063606262 with 146 traces
# aes2-isw3 elapsed time: 324.3542935848236 with 178 traces
# aes2-isw4 elapsed time: 477.828795671463 with 114 traces
# aes2-isw4 elapsed time: 487.29572105407715 with 146 traces
# aes2-isw4 elapsed time: 523.0008361339569 with 178 traces
# aes2-minq elapsed time: 1211.1801557540894 with 114 traces
# aes2-minq elapsed time: 1211.8934774398804 with 146 traces
#
#
# Ran 1 test in 6598.826s
#
# OK
# aes2-minq elapsed time: 1279.8623569011688 with 178 traces
# attack_testing.TestMethods.test_lda_aes: 6598.822 seconds
#
# Process finished with exit code 0

# /usr/bin/python3 /home/lalex/.pycharm_helpers/pycharm/_jb_unittest_runner.py --target attack_testing.TestMethods.test_lda_aes
# Testing started at 16:43 ...10 rounds interesting
# Launching unittests with arguments python -m unittest attack_testing.TestMethods.test_lda_aes in /mnt/h/Master/Thesis/Implementation
#
# aes2-isw2 elapsed time: 179.04027676582336 with 82 traces
# aes2-isw2 elapsed time: 152.65068101882935 with 114 traces
# aes2-isw3 elapsed time: 346.1883487701416 with 82 traces
# aes2-isw3 elapsed time: 291.05431485176086 with 114 traces
# aes2-isw4 elapsed time: 566.847414970398 with 82 traces
# aes2-isw4 elapsed time: 478.8140869140625 with 114 traces
# aes2-minq elapsed time: 1567.1374037265778 with 82 traces
#
# aes2-minq elapsed time: 1181.6137132644653 with 114 traces
# attack_testing.TestMethods.test_lda_aes: 4763.348 seconds
#
# Ran 1 test in 4763.350s
#
# OK
#
# Process finished with exit code 0