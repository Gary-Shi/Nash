import numpy as np
import os
import copy

def mul(a):

    b = 1
    for i in a:
        b *= i
    return b

class Game:

    
    def __init__(self, n_agent, n_action, cmd_string):

        self.n_agent = n_agent # agent的数目
        self.n_action = n_action # 每个agent的action的数目
        self.result = [] # 找到的nash均衡

        shape = copy.deepcopy(n_action)
        shape.append(n_agent)
        
        self.reward = np.empty(mul(shape))
        cmd_string ="java -jar gamut.jar "+ cmd_string +" -f Game.game"
        os.system(cmd_string)


        sum = mul(n_action)
        print(sum)
        with open('Game.game', 'r') as f:

            while 1:

                ss = f.readline()

                if(ss != "" and ss[0] == '['):

                    sum -= 1
                    ss = ss.replace(':','') 
                    ss = ss.replace('[','') 
                    ss = ss.replace(']','')
                    ss = ss.replace('	','')
                    ss = ss.split()
                    pos = 0
                    for i in range(n_agent):
                        pos *= n_action[i]
                        pos += int(ss[i]) - 1

                    pos *= n_agent

                    for i in range(n_agent):
                        self.reward[pos + i] = float(ss[n_agent + i])
                if sum == 0:break
            self.reward = self.reward.reshape(shape) # reward 最终的结构为: [a1][a2]...[an][k]表示n个人的动作分别为a1~an时第k个人的reward
            print(self.reward)

def temp(x):

    xx = abs(x[0] - x[1])
    return xx * 1000000 + x[0] + x[1];

def generate_pair(n_action):

    a = []
    for i in range(n_action[0]):
        for j in range(n_action[1]):
            a.append((i+1, j+1))
    a.sort(key = temp)
    return a

def count(x):

    cnt = 0
    while x:
        cnt += x & 1
        x >>= 1
    return cnt

def generate_set(n, m):

    b = []
    for i in range(1,n):
        if count(i) == m and (i | n) == n:b.append(i)
    return b

def generate_action(s):

    b = []
    i = 0
    while (1<<i) <= s:
        if (1<<i) & s:b.append(i)
        i += 1
    return b

def dominated(game, i, a, A):
    
    l_a = [generate_action(A[0]), generate_action(A[1])]
    for ap in l_a[i]:
        if ap != a:
            cnt = 0
            for aa in l_a[1-i]:
                if i == 0:
                    if game.reward[ap][aa][i] > game.reward[a][aa][i]:cnt += 1
                    else:break
                else:
                    if game.reward[aa][ap][i] > game.reward[aa][a][i]:cnt += 1
                    else:break

            if cnt == len(l_a[1-i]):return True
    return False

def LP(game, s1, s2):

    return False

def find_nash_equilibrium(game):

    if game.n_agent == 2:

        a = generate_pair(game.n_action)
        print(a)
        for t in a:
            A1 = (1<<game.n_action[0])-1
            S1 = generate_set(A1, t[0])
            for s in S1:
                A2 = 0
                for i in range(game.n_action[1]):
                    if not dominated(game, 1, i, (s, (1<<game.n_action[1]) - 1)):A2 += 1<<i
                flag = False
                for a_s in generate_action(s):
                    if dominated(game, 0, a_s, (s, A2)):
                        flag = True
                        break
                if flag:continue
                S2 = generate_set(A2, t[1])
                for s2 in S2:
                    flag = False
                    for a_s in generate_action(s):
                        if dominated(game, 0, a_s, (s, s2)):
                            flag = True
                            break
                    if flag:continue
                    if LP(game, s, s2):return True


def main():

    game = Game(2, [2,3], "-g RandomGame -players 2 -normalize -min_payoff 0 -max_payoff 1 -f BoS.game -actions 2 3")
    if find_nash_equilibrium(game):
        print('success!', game.result)
    else:
        print('failed!')


main()