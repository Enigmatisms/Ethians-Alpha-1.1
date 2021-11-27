#-*-coding:utf-8-*-

import random

class Level0:
    def __init__(self):
        self.level=[[0 for i in range(42)] for j in range(64)]

    def getChar(self, x, y):
        return self.level[x][y]

    def setChar(self, x, y, val):
        self.level[x][y]=val
    
    def __getVinc(self, x, y, radius=1):
        lst = list()
        for i in range(x - radius, x + radius + 1):
            for j in range(y - radius, y + radius + 1):
                lst.append((i, j))
        if radius > 1:
            for i in self.__getVinc(x, y, radius - 1):
                lst.remove(i)
        return lst

    def __countWall(self, x, y, radius=1, counted_id={0}):
        lst = self.__getVinc(x, y, radius)
        count = 0
        for i in lst:
            if self.getChar(*i) in counted_id:
                count += 1
        return count

    def wallsGen(self):
        for x in range(4, 60):
            for y in range(4, 38):
                if self.getChar(x, y)==0:
                    if self.__countWall(x, y) < 4:
                        self.setChar(x, y, 5)
                else:
                    if self.__countWall(x, y) >= 5:
                        self.setChar(x, y, 0)

    def lakeGen(self, times):
        x=random.randint(8, 34)
        y=random.randint(8, 25)
        length=random.randint(12, 18)
        width=random.randint(8, 13)
        for i in range(x, x+length):
            for j in range(y, y+width):
                self.setChar(i, j, random.choice([5, 8]))
        for t in range(times):                          #处理次数
            for i in range(x, x+length):
                for j in range(y, y+width):
                    if self.getChar(i, j) in {8, 9}:
                        if self.__countWall(i, j, counted_id={8, 9}) < 4:
                            self.setChar(i, j, 5)
                    else:
                        if self.__countWall(i, j, counted_id={8, 9}) >= 5:
                            self.setChar(i, j, random.choice([8, 9]))

    def randomRoad(self):         #传入门的位置
        x, y=1, 1
        endx, endy=1, 1
        while self.getChar(endx, endy) or self.getChar(x, y)==0 or (x, y)==(endx, endy):
            x, y=random.randint(5, 59), random.randint(5, 37)
            endx, endy=random.randint(5, 59), random.randint(5, 37)
        self._roadGen(x, y, endx, endy)

    def _roadGen(self, startx, starty, endx, endy):
        posx, posy=startx, starty
        xstep, ystep=abs(endx-startx), abs(endy-starty)
        xdir=1 if startx-endx<0 else -1
        ydir=1 if starty-endy<0 else -1
        while xstep and ystep:
            dirJudge=random.choice([0, 1])
            if dirJudge:
                if self.getChar(posx+xdir, posy) !=0:
                    self.setChar(posx+xdir, posy, 26)
                    posx+=xdir
                    xstep-=1
                elif self.getChar(posx, posy+ydir) !=0:
                    self.setChar(posx, posy+ydir, 26)
                    posy+=ydir
                    ystep-=1
                else: return
            else:
                if self.getChar(posx, posy+ydir) !=0:
                    self.setChar(posx, posy+ydir, 26)
                    posy+=ydir
                    ystep-=1
                elif self.getChar(posx+xdir, posy) !=0:
                    self.setChar(posx+xdir, posy, 26)
                    posx+=xdir
                    xstep-=1
                else: return
        while xstep:
            if self.getChar(posx+xdir, posy) !=0:
                self.setChar(posx+xdir, posy, 26)
                posx+=xdir
                xstep-=1
            else: break
        while ystep:
            if self.getChar(posx, posy+ydir) !=0:
                self.setChar(posx, posy+ydir, 26)
                posy+=ydir
                ystep-=1
            else: break

    def setUpMap(self, times=4):
        for x in range(4, 60):
            for y in range(4, 38):
                self.setChar(x, y, random.choices([0, 5], [0.24, 0.76])[0])
        self.mapGen(times)
        self.lakeGen(2)
        self.randomRoad()
        self.modMap()
        return self.level

    def modMap(self):           #环境多样化
        for i in range(64):
            for j in range(42):
                flag=self.getChar(i, j)
                if flag==0:
                    if random.choices([0, 1], [0.95, 0.05])[0]:
                        self.setChar(i, j, 10)
                elif flag==5:
                    setted=random.choices([0, 7, 6], [0.7, 0.18, 0.12])[0]
                    if setted:
                        self.setChar(i, j, setted)

    def mapGen(self, time=3):
        for i in range(time):
            self.wallsGen()

            
                    
