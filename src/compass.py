import pygame

class Compass:
    def __init__(self, surface, func_list):
        self.screen=surface
        self.dg=func_list[0]
        self.npc=func_list[1]
        self.ms=func_list[2]
        self.pl=func_list[3]
        self.level=[[0 for i in range(42)] for j in range(64)]
        self.color={'mist':(0,0,0), 'bk':(255, 255, 255), 'wall1':(100, 100, 100),
                    'floor1':(190, 190, 190), 'box':(225, 185, 0), 'grass':(124, 252, 0),
                    'tree':(0,128, 0), 'swamp':(50, 205, 50), 'water':(30, 144, 255),
                    'lava':(255, 0, 0), 'stairs':(128, 0, 0), 'fence':(150, 150, 150), 'door':(128, 128, 0),
                    'clay1':(105, 50, 0), 'clay2':(130, 90, 50), 'deco1':(255, 99, 71),
                    'deco2':(110, 255, 195), 'trap':(0, 0, 255), 'npc':(186, 85, 211)}
        self.colorMap={0:'wall1',  # 灰色砖墙
            1:'floor1',  # 黑色地板
            2:'stairs', # 楼梯
            3:'grass',  # 草地
            4:'water',  # 水体
            5:'lava',  # 岩浆
            6: 'swamp',  # 沼泽
            7: 'tree',  # 树木
            8:'fence',  # 铁栅栏和gate
            9:'clay1',      #洞穴墙
            10:'clay2',     #洞穴地面
            64 :'door',       #不透明门
            65 :'box',       #箱子
            66 :'trap',       #陷阱
            67:'deco1',  #不可交互的装饰品
            68:'deco2'      #可交互物品
        }
        self.judge=0
        self.pic=pygame.image.load(r'asset/compass.png').convert_alpha()

    def getColor(self, x):
        if x<=99:
            return self.colorMap[x]
        elif x>99: return 'npc'
        else: return 'floor1'

    def getChar(self, x, y):
        return self.level[x][y]

    def setChar(self, x, y, val):
        self.level[x][y]=val

    def getMap(self):
        for x in range(0, 64):
            for y in range(0, 42):
                dgp = self.convertDg(self.dg.getChar(x, y))
                surp = self.convertSur(self.dg.sur.getChar(x, y))
                self.setChar(x, y, max(dgp, surp))
        for k in self.npc.npc_pos:
            self.setChar(*k, 100)

    @staticmethod
    def convertDg(x):
        if x in {0, 10, 15, 22}:
            return 0        #灰色砖墙
        elif x in {1, 2, 11, 12, 14, 23, 24, 25, 26}:
            return 1        #黑色地板
        elif x in {3, 4, 16, 17, 29, 30}:
            return 2        #楼梯
        elif x in {5, 6}:
            return 3        #草地
        elif x in {8, 9}:
            return 4        #水体
        elif x in {18, 19}:
            return 5        #岩浆
        elif x in {20, 21}:
            return 6        #沼泽
        elif x==7:
            return 7        #树木
        elif x==13:
            return 8        #铁栅栏和gate
        elif x in {27, 28}:     #褐色墙壁
            return 9
        elif x in {31, 32}:     #褐色地面
            return 10

    @staticmethod
    def convertSur(x):
        if x in {0, 1, 2, 12, 39}:
            return 64       #不透明门
        elif x in {3, 4}:
            return 8        #铁栅栏和gate
        elif x in range(5, 10):
            return 65       #箱子
        elif x in {10, 11, 13, 14, 15}:
            return 66       #陷阱
        elif x in {16, 17, 18, 24, 26, 29, 32, 34, 36, 42}:
            return 67       #不可交互的装饰品
        elif x in {22, 23, 25, 27, 28, 30, 31, 33, 34, 37, 38, 40, 41}:     #其他装饰
            return 68
        else: return -1

    def drawMist(self, x, y):
        for i in range(0, 64):
            for j in range(0, 42):
                judge=self.ms.getChar(i, j)
                if not judge:
                    pygame.draw.rect(self.screen, self.color['mist'], (x+4*i, 4*j+y, 4, 4), 0)

    def drawMap(self, x, y):
        for i in range(0, 64):
            for j in range(0, 42):
                judge=self.getChar(i, j)
                tag=self.getColor(judge)
                pygame.draw.rect(self.screen, self.color[tag], (x+4*i, y+4*j, 4, 4), 0)

    def drawCompass(self, x, y):
        if self.judge:
            self.getMap()
            self.screen.blit(self.pic, (x-9, y-9))
            self.drawMap(x, y)
            pygame.draw.rect(self.screen, self.color['bk'], (self.pl.xat*4+x, self.pl.yat*4+y, 4, 4), 0)
            self.drawMist(x, y)


    def openMap(self):
        self.judge=1-self.judge

