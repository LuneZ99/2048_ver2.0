from itertools import combinations_with_replacement
from time import time
import numpy as np
import numpy.matlib
import math

begin = time()

s_list = [0, 4, 16, 54, 128, 320, 768, 1792, 4096, 9216, 20480, 45056, 98304, 212992, 458752] 
            # 45056, 98304, 212992, 458752, 983040(65536)
s_list = [0, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 16384, 32768]
# g_list = combinations_with_replacement(s_list, 16)
m_arr_95_98 = np.empty([0, 4, 4], dtype = int)

arr = np.asarray(s_list, dtype = int)

l = 10000
i = 0
while True:
    m = np.random.choice(arr, 16)
    s = 0
    for i in m:
        if i != 0:
            s += (math.log2(i)-1)*i
    if 950000 <= s <= 983040:
        m_arr_95_98 = np.append(m_arr_95_98, m.reshape(1, 4, 4), axis=0)
        if len(m_arr_95_98) % 100 == 0:
            print('已生成', len(m_arr_95_98), '种状态，进度', len(m_arr_95_98)/l*100, '%, 耗时', time()-begin, 's')
        if len(m_arr_95_98) == 10000:
            break

np.save('m_arr_95_98.npy', m_arr_95_98)

print('操作完成，耗时', time()-begin, 's')