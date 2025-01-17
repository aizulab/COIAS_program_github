#!/usr/bin/env python3
# -*- coding: UTF-8 -*
#Timestamp: 2022/08/05 21:00 sugiura
############################################################################################
# mpc3.txtのある行の15-80カラム目(つまり観測日, ra, dec, 等級, フィルター, 観測所まで)と
# all.txtのある行の15-80カラム目と完全に一致するような行を見つけ出し,
# mpc3.txtのその行の0-14カラム目(名前部分)とall.txtのその行の15カラム目以降(その他情報)を結合させ,
# newall.txtに書き出す.
# 要は, mpc3.txtに記載の天体のみの情報をall.txtから抽出してnewall.txtに書き出す.
# また, newall.txtのうち 天体名 画像番号 等級 等級誤差 Xpixel Ypixel のみをpredisp.txtに書き出す.
# 入力: mpc3.txt
# 　　  all.txt
# 出力: newall.txt
# 　　  predisp.txt
#
# その後, AstsearchR_between_COIAS_and_ReCOIASで
# predisp.txtの1, 2, 5, 6カラム目 (天体名 画像番号 Xpixel Ypixel)のみを取り出し, redisp.txtに書き出す.
############################################################################################
import traceback
import os
import numpy as np
import print_detailed_log

try:
    # detect list
    tmp1 = "all.txt"
    tmp2 = "mpc3.txt"
    tmp3 = "newall.txt"
    tmp4 = "predisp.txt"

    if os.stat("mpc3.txt").st_size == 0:
        empty = []
        np.savetxt(tmp3,empty,fmt="%s")
        np.savetxt(tmp4,empty,fmt="%s")

    else:
        data1 = open(tmp1, "r")
        data2 = open(tmp2, "r")
        data3 = open(tmp3, "w")
        data4 = open(tmp4, "w")
        lines = data1.readlines()
        lines2 = data2.readlines()

        list = []
        for i in range(len(lines)):
            # tmp = lines[i].strip()
            tmp1 = lines[i]
            # print(tmp[15:80])
            tmp1b = tmp1[15:80]
            for j in range(len(lines2)):
                tmp2 = lines2[j]
                # print(tmp2[15:80])
                tmp2b = tmp2[15:80]
                if tmp1b == tmp2b:
                    tmp3 = tmp2[0:15] + tmp1[15:124]
                    # print(tmp3,i,j)
                    list.append(tmp3)
        # delete daburi
        list2 = sorted(list, reverse=True)
        list3 = []
        list4 = []
        for i in range(len(list2) - 1):
            tmp4 = list2[i]
            stock1 = tmp4[15:80]
            tmp5 = list2[i + 1]
            stock2 = tmp5[15:80]
            if not stock1 == stock2:
                tmp6 = list2[i]
                tmp7 = list2[i][0:14] + list2[i][81:124]
                list3.append(tmp6)
                list4.append(tmp7)
        list3.append(list2[len(list2) - 1])
        list4.append(list2[len(list2) - 1][0:14] + list2[len(list2) - 1][81:124])
        for x in list3:
            tmp8 = x.strip('\n')
            data3.write(str(tmp8) + '\n')

        for x in list4:
            tmp9 = x.strip('\n')
            data4.write(str(tmp9) + '\n')

        data1.close()
        data2.close()
        data3.close()
        data4.close()

except FileNotFoundError:
    print("Some previous files are not found in redisp.py!",flush=True)
    print(traceback.format_exc(),flush=True)
    error = 1
    errorReason = 64

except Exception:
    print("Some errors occur in redisp.py!",flush=True)
    print(traceback.format_exc(),flush=True)
    error = 1
    errorReason = 65

else:
    error = 0
    errorReason = 64

finally:
    errorFile = open("error.txt","a")
    errorFile.write("{0:d} {1:d} 606 \n".format(error,errorReason))
    errorFile.close()

    if error==1:
        print_detailed_log.print_detailed_log(dict(globals()))
