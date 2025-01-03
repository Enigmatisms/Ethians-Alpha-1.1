#-*-coding:utf-8-*-

import random
import numpy as np
from pygame.locals import *

class Primtree:
    def __init__(self):
        self.rectList=[]
        self.level=np.zeros((64, 42), dtype = int)
        self.surLevel=np.full((64, 42), -1, dtype = int)
        self.cover=0
        self.floorList={}           #生成最小生成树时使用
        self.floorSet=set()         #生成复杂地形使用
        self.wallList=[]
        self.doorWall=[]
        self.barList=[]
        self.isGateSet=False        #是否设置了铁栅栏门

    def setChar(self, x, y, val):
        self.level[x, y]=val

    def getChar(self, x, y):
        return self.level[x, y]

    def setChar2(self, x, y, val):
        self.surLevel[x, y] = val

    def getChar2(self, x, y):
        return self.surLevel[x, y]

    def initMap(self):
        self.cover=0
        self.floorList.clear()
        self.wallList.clear()
        self.rectList.clear()
        self.level=np.zeros((64, 42), dtype = int)
        self.surLevel=np.full((64, 42), -1, dtype = int)
        self.level[5:60:2, 5:38:2] = 12

    def placeRoom(self, thres=800):
        num=-1
        while self.cover<thres:
            width = random.randint(6, 14)
            height = random.randint(5, 12) + width // 5
            posx = random.randint(5, 60 - width)
            posy = random.randint(5, 38 - height)
            tem = Rect(posx+1, posy+1, width-1, height-1)
            count = 0
            while self.collideList(tem):
                width = random.randint(6, 14)
                height = random.randint(5, 12) + width // 5
                posx = random.randint(5, 60 - width)
                posy = random.randint(5, 38 - height)
                tem = Rect(posx+1, posy+1, width-1, height-1)
                count += 1
                if count > 255:  # 死循环保护
                    break
            
            self.level[posx:posx + width, posy:posy + height - 1] = 1
            self.level[posy + 1:posy + height - 1, posx:posx + width - 1] = 1
            self.level[posx + 1:posx + width - 1, posy + 1:posy + height - 1] = num

            num-=1
            self.rectList.append(tem)
            self.cover+=width*height

    #初始化prim值
    def setWalls(self):
        count=12
        for i in range(5, 60,):
            for j in range(5, 38):
                flag=self.getChar(i, j)
                if flag==0:
                    self.wallList.append((i,j))
                elif flag==12:
                    self.floorList[count]=[(i,j)]
                    self.setChar(i, j, count)
                    count+=1
                elif flag==1:
                    self.doorWall.append((i, j))

    #随机破墙
    def breakWall(self):
        while self.wallList:
            point=random.choice(self.wallList)
            self.wallList.remove(point)         #以免重复破墙
            judge=self.wallJudge(*point)
            if judge==1: pos1, pos2=self.getChar(point[0], point[1] - 1),  self.getChar(point[0], point[1] + 1)         #南北向
            elif judge==2: pos1, pos2 = self.getChar(point[0]-1, point[1]), self.getChar(point[0]+1, point[1])          #东西向
            else: continue
            if 1 in {pos1, pos2}:
                continue
            if pos1 != pos2:
                maxi, mini = max(pos1, pos2), min(pos1, pos2)
                self.setChar(*point, mini)          # 破墙操作
                self.floorList[mini].append(point)
                while self.floorList[maxi]:
                    pt = self.floorList[maxi].pop()         #大值点列剪切点到小值点列
                    self.setChar(*pt, mini)         #更新为较小值
                    self.floorList[mini].append(pt)         #点列添加
        for i in range(5, 60):         #随机prim可能因为房间的假如无法保证地图中只有一个最小生成树
            for j in range(5, 38):
                k=self.getChar(i, j)
                if k>12: self.setChar(i, j, -255)

    def createMap(self):
        """生成地图的过程：
        1.随机放置房间，房间的总面积大于预设值:800
        2.构建随机prim环境,进行随机prim操作, 并且清除随机prim的非最小生成树
        3.寻找可以放置门的地方，放置门并改变地板位
        4.清除迷宫死角，让地图看起来更干净
        5.清除结束阶段，进一步寻找pointSpread导致的坏点，并且记录墙点，地面点
        6.生成内部环境和复杂的地图道具
        7.清除房间墙点"""
        self.placeRoom()
        self.setWalls()
        self.breakWall()
        self.setDoorWay()
        # 把所有值不是12的点设为12
        self.removeEnd(15)  # 填补空缺
        self.setPool(10)
        self.randomBox()
        self.surroundingGen()
        self.doubleChk()
        return [self.level, self.surLevel]

    # 减少死胡同n次
    def removeEnd(self, n):
        for k in range(n-1):
            for i in range(5, 60):
                for j in range(5, 38):
                    if self.getChar(i, j) >= 12:
                        judge = self.isEnd(i, j)
                        if judge: self.setChar(i, j, 0)
        for i in range(5, 60):          #最后的一次遍历用以增加复杂地形，检查非地板元素，保存墙点和地面
            for j in range(5, 38):
                if self.getChar(i, j) == 1:
                    self.extraDoor(i, j)
                elif self.getChar(i, j) in range(-254, 0):
                    self.setChar(i, j, 12)
                    self.floorSet.add((i, j))
                elif self.getChar(i, j)==-255:      #清除Bug区
                    self.setChar(i, j, 0)
                elif self.getChar(i, j)==12:
                    self.floorSet.add((i, j))
                    judge = self.isEnd(i, j)
                    if judge: self.setChar2(i, j, random.choice([16, 17, 18, 31, 42]))          #死胡同设置环境道具


    """===================更复杂的地形=================="""
    #设置小水池
    def setPool(self, radius:int):
        x=random.randint(5, 60)
        y=random.randint(5, 38)
        while self.getChar(x, y) != 12:
            x = random.randint(5, 60)
            y = random.randint(5, 38)
        self.pointSpread(x, y, 12, 8, radius)

    #设置铁牢
    def setBars(self, barList, length:int):
        if len(barList) >= length:  # 栅栏需要有一定长度，否则不美观
            for point in barList:
                self.barList.append(point)
                self.setChar(*point, 13)
            return True
        return False

    """===============有关门放置位置墙点的判断==============="""
    def setDoorWay(self):
        while self.doorWall:
            point=self.selectDoorWall()
            self.breakDoorWay(*point)

    #随机选择一个可以放置门的位置
    def selectDoorWall(self):
        point=random.choice(self.doorWall)
        self.doorWall.remove(point)
        return point

    def doorJudge(self, x, y):
        if not self.getChar(x, y-1) in range(13):
            return 1        #南墙
        elif not self.getChar(x, y+1) in range(13):
            return 2        #北墙
        elif not self.getChar(x-1, y) in range(13):
            return 3        #东墙
        elif not self.getChar(x+1, y) in range(13) :
            return 4        #西墙
        else:
            return 0        #无效墙

    #删除应该创建门的墙
    def breakDoorWay(self, x, y):
        judge=self.doorJudge(x, y)
        k1, k2=0, 0     #两个系数
        if judge==1: k2=1
        elif judge==2: k2=-1
        elif judge==3: k1=1
        elif judge==4: k1=-1
        else: return
        flag1 = self.getChar(x - k1, y - k2)
        maxi, mini=0, 0
        for i in range(1, 4):
            flag2 = self.getChar(x + k1 * i, y + k2 * i)
            if flag2 < 0 or flag2>11:
                maxi, mini = max(flag1, flag2), min(flag1, flag2)
                if maxi==mini: return
                count = 0
                while count < i:
                    self.setChar(x + k1 * count, y + count * k2, maxi)
                    count += 1
                break
        if 0 in {maxi, mini}: return
        self.pointSpread(x, y, mini, maxi)
        self.setChar(x, y, 12)        #门通道设置
        self.setChar2(x, y, 0)         #开门位置设置

    # 不完美的迷宫构建:放置更多的门
    def extraDoor(self, x, y):
        if self.getChar(x - 1, y) not in {0, 1} and self.getChar(x + 1, y) not in {0, 1}:  # 东西分割墙
            for i in range(-2, 3):
                if not self.getChar(x, y + i) in {0, 1, 10}: return
        elif self.getChar(x, y - 1) not in {0, 1} and self.getChar(x, y + 1) not in {0, 1}:  # 南北分割墙
            if random.choices([0, 1], [0.9, 0.1])[0]:
                self.setBars(self.findWall(x, y), 3)
                return
            for i in range(-2, 3):
                if not self.getChar(x + i, y) in {0, 1,10}: return
        else:
            return
        if random.choices([0, 1], [0.95, 0.05])[0]:
            self.setChar(x, y, 12)
            self.setChar2(x, y, 0)

    #生成地图环境
    def doubleChk(self):
        for x in range(64):
            for y in range(42):
                if self.getChar(x, y)==1:
                    self.setChar(x, y, random.choices([0, 10, 15], [0.90, 0.08, 0.02])[0])
                elif self.getChar(x, y)<0:
                    self.setChar(x, y, random.choices([0, 10, 15], [0.90, 0.08, 0.02])[0])
                elif self.getChar(x, y)==0:
                    val=random.choices([0, 10, 15], [0.92, 0.07, 0.01])[0]
                    if val:
                        self.setChar(x, y, val)
                elif self.getChar(x, y)==12:
                    val = random.choices([0, 2, 11, 14], [0.84, 0.04, 0.06, 0.06])[0]
                    if val:
                        self.setChar(x, y, val)
        self.floorSet.clear()                               #最后清除地面集合中的所有元素

    def surroundingGen(self):
        furnitureNum=random.randint(5, 8)
        furniture=random.sample(self.floorSet, furnitureNum)
        for point in furniture:
            chairPos=self.unOccupied(*point)
            if chairPos:
                self.setChar2(*point, random.choice([22, 27, 35]))                              #设置中心家具
                self.setChar2(*chairPos, random.choices([29, 28], [0.1, 0.9])[0])           #有可能是破椅子
        self.floorSet=self.floorSet-set(furniture)      #差集操作
        bucketNum=random.randint(6, 8)
        bucket=random.sample(self.floorSet, bucketNum)
        for point in bucket:
            if self.getChar2(*point)==-1:
                self.setChar2(*point, random.choices([31, 32], [0.9, 0.1])[0])                  #可能是破桶
        self.floorSet=self.floorSet-set(bucket)
        coffinNum=random.randint(0, 2)
        coffin=random.sample(self.floorSet, coffinNum)
        for point in coffin:
            if self.getChar2(*point)==-1:
                self.setChar2(*point, 37)
        self.floorSet=self.floorSet-set(coffin)
        if len(self.barList)>2:
            gateNum = random.randint(1, 2)
            gatePos = random.sample(self.barList, gateNum)
            for point in gatePos:  # 设置铁栅栏门
                self.setChar(*point, 12)
                self.setChar2(*point, 3)
            self.barList.clear()

    def randomBox(self):
        boxNum=random.randint(8, 11)
        lst=random.sample(self.floorSet, boxNum)
        self.floorSet=self.floorSet-set(lst)        #差集操作
        for point in lst:
            self.setChar2(*point, 5)

    def unOccupied(self, x, y):                 #判断地图的某个点以及四周是否有未被占用的地方
        if self.getChar2(x, y)==-1:
            pointList=[(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            random.shuffle(pointList)
            for point in pointList:
                if self.getChar(*point)==12 and self.getChar2(*point)==-1:
                    return point
        return None

    #寻找一面隔墙
    def findWall(self, x, y):
        barList=[]     #铁栅栏墙壁
        def nsWall(i, j):       #南北分隔墙
            return True if all([self.getChar(i, j - 1) not in {0, 1}, self.getChar(i, j + 1) not in {0, 1},
                        self.getChar(i, j)==1, self.getChar2(i, j) != 11]) else False
        if nsWall(x, y):
            temx=x
            barList.append((x, y))
            temx-=1
            while nsWall(temx-1, y) and nsWall(temx, y):
                barList.append((temx, y))
                temx-=1
            temx=x+1
            while nsWall(temx+1, y) and nsWall(temx, y):
                barList.append((temx,y))
                temx+=1
        return barList


    #在（x, y）点附近寻找值为jVal的点，将其设置为setVal
    def pointSpread(self, x, y, jVal:int, setVal:int, depth:int=-1):
        if depth == 0:
            self.setChar(x, y, setVal)
            return
        else:
            self.setChar(x, y, setVal)
            posList = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
            for point in posList:
                if self.getChar(*point) == jVal:
                    self.pointSpread(*point, jVal, setVal, depth-1)
    """================================================="""

    #是死胡同吗
    def isEnd(self, x, y):
        posList = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]
        count=0
        for i in posList:
            if self.getChar(*i) >1: count += 1
            if count >= 2: return False
        return True

    @staticmethod
    def wallJudge(x, y):
        if x%2 and y%2==0: return 1            #南北隔墙
        elif x%2==0 and y%2: return 2            #东西隔墙
        else: return 0          #无用的墙

    def collideList(self, rect):
        for i in self.rectList:
            if rect.colliderect(i): return True
        return False











