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
                    #print(ss)
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


def find_nash_equilibrium(game):

    if game.n_agent == 2:

        pass

    else:

        pass


def main():

    game = Game(2, [2,3], "-g RandomGame -players 2 -normalize -min_payoff 0 -max_payoff 150 -f BoS.game -actions 2 3")
    if find_nash_equilibrium(game):
        print('success!')
    else:
        print('failed!')


main()