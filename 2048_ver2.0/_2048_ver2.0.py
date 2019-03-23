import numpy as np
import numpy.matlib
import random as ra
from copy import deepcopy
from time import time

# 全局变量
_pos_ls = [
        (0, 0), (0, 1), (0, 2), (0, 3),
        (1, 0), (1, 1), (1, 2), (1, 3),
        (2, 0), (2, 1), (2, 2), (2, 3),
        (3, 0), (3, 1), (3, 2), (3, 3) 
        ]
_gen_ls = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]
_input_player = [0, 1, 2, 3]                # 上，下，左，右
_score = 0
_m0 = np.matlib.zeros((4,4))


class status:

    def __init__(self, status=''):
        global _m0
        if status == '':
            self.martix = _m0
            self.depth = 0
            self.generate_init()
            self.alive = True
        else:
            self.martix = status.martix.copy()             # 初始化矩阵
            self.depth = status.depth + 1                  # 记录深度
            self.islife = True

        # 生成函数 
    def generate(self, pos, n):
        self.martix[pos] = n

        # 开局初始化,仅在 d==0 时调用
    def generate_init(self):
        global _pos_ls
        global _gen_ls
        while True:
            pos0 = ra.choice(_pos_ls)
            pos1 = ra.choice(_pos_ls)
            if pos0 != pos1:
                break
        self.generate(pos0, ra.choice(_gen_ls))
        self.generate(pos1, ra.choice(_gen_ls))

        # 随机电脑输入，面板生成函数(有bug没修！)
    def input_enemy(self):
        global _pos_ls
        global _gen_ls
        pos_ls = deepcopy(_pos_ls)     
        for pos in pos_ls:
            if self.martix[pos]:
                del(pos)
        self.generate(ra.choice(pos_ls), ra.choice(_gen_ls))
    
    def input_enemy_pos(self, pos, gen):
        self.generate(pos, gen)
        return 0

        # 玩家输入，面板移动函数
    def input_player(self, dir):      # dir = the direction to move, which belongs to range(4).
        
        origin = self.martix.copy()

        for line in range(4):

            arr = np.array([])
            if dir in (2, 3):
                for i in np.nditer(self.martix[line, ...]):
                    if i != 0:
                        arr = np.append(arr, i)
            else:
                for i in np.nditer(self.martix[..., line]):
                    if i != 0:
                        arr = np.append(arr, i)

            if dir in (1, 3):
                arr = np.flipud(arr)
            for i in range(arr.size):
                try:
                    if arr[i] == arr[i+1]:
                        arr = np.delete(arr, i+1)
                        arr[i] *= 2
                except IndexError:
                    break
            while True:
                if len(arr) == 4:
                    break
                arr = np.append(arr, 0)
            if dir in (1, 3):
                arr = np.flipud(arr)

            if dir in (2, 3):
                self.martix[line, ...] = arr
            else:
                self.martix[..., line] = arr.T

                   
        if (self.martix == origin).all():               # 若该方向无法移动，返回-1
            return -1
        else:
            return 0


        

class node:
    def __init__(self, nod='', dep=None, arg=None, gen=None):
        if nod == '':
            self.status = status(nod)
            self.parent = -1
            self.firstchild = None
            self.lastchild = None
        else:
            self.status = status(nod.status)
            if dep == 0:
                self.status.input_player(arg)
            else:
                self.status.input_enemy_pos(arg, gen)
            self.parent = gameTree.index(nod)
            self.firstchild = None
            self.lastchild = None

    def genallchild(self):
        global _pos_ls
        ls = []

        if self.status.depth % 2 == 0:
            t = 0
            for dir in range(4):
                if self.status.input_player(dir) == 0:
                    t += 1
                    child = node(nod=self, dep=0, arg=dir)
                    ls.append(child)     
            if t == 0:
                self.status.alive = False
                self.firstchild = None
                self.lastchild = None
            else:
                self.firstchild = len(gameTree)
                self.lastchild = len(gameTree)+len(ls)-1
            return ls
        else:
            pos_ls = deepcopy(_pos_ls)
            for pos in pos_ls:
                if self.status.martix[pos] != 0:
                    pos_ls.remove(pos)
            for pos in pos_ls:
                child = node(nod=self, dep=1, arg=pos, gen=2)
                ls.append(child)

            '''
            for pos in pos_ls:
                child = node(nod=self, dep=1, arg=pos, gen=4)
                ls.append(child)
            '''

            self.firstchild = len(gameTree)
            self.lastchild = len(gameTree)+len(ls)-1
            return ls


n = node()
m = np.load('m_arr_95_98.npy')
print(m[0])
n.status.martix = m[0]
gameTree = [n]

# gameTree.append(node(n))
begin = time()
for n in gameTree:
    gameTree.extend(n.genallchild())
    if len(gameTree) % 5000 == 0:
        t = time()
        te = '已经生成了'+str(len(gameTree))+'个节点, 目前在第'+str(gameTree[-1].status.depth)+'层, 耗时'+str(t-begin)+'s'
        print(te)
    if gameTree[-1].status.depth == 8:
        break

a = '生成完成，共'+str(len(gameTree))+'个节点'
print(a)

arr = np.asarray(gameTree)
np.save('arr1.npy', arr)