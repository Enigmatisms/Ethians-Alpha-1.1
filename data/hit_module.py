
import random


class Calc:
    def __init__(self):
        self.a = -1.84266 * (10 ** -6)
        self.b = 0.000706326
        self.c = 0.05583372942
        self.d = 0.836691169
        
    def basic_dmg(self, atk):
        res=self.a*(atk**3)+self.b*(atk**2)+self.c*atk+self.d+1
        return int(res)

    def show(self, tag=0):
        if tag:
            for i in range(1, 70):
                print(i, int(self.basic_dmg(i)/2))
        else:
            for i in range(1, 70):
                print(i, self.basic_dmg(i))

if __name__=='__main__':
    c=Calc()

                
