#-*-coding:utf-8-*-

from src.ezplot import MySprite

#定向除雾系统
class Mist:
    def __init__(self, func):    #r是照亮半径，func函数是pl，func2参数是dg
        MySprite.__init__(self)
        self.image=MySprite()
        self.image.load(r'asset/mist.png', 0, 0, 32, 32, 3)
        self.dg=func
        self.level=[[0 for i in range(42)] for j in range(64)]     #0代表未勘探（黑色浓雾，不透明），1代表正在勘探（全透明），2代表勘探过但是不在勘探（半透明，不显示生物（这怎么写？））
        self.open_set, self.close_set = [], []
        self.dgMist={0, 10, 15, 22, 27, 28}
        self.surMist={0, 12, 25, 26, 38, 39}
        self.lst=set()
        self.mult=[
                [1,  0,  0, -1, -1,  0,  0,  1],
                [0,  1, -1,  0,  0, -1,  1,  0],
                [0,  1,  1,  0,  0, -1, -1,  0],
                [1,  0,  0,  1, -1,  0,  0, -1]
            ]       #矩阵变换

    def mapClear(self):         #优化方法的尝试
        for y in range(21):
            for x in range(64):
                if self.getChar(x, y) != 1:
                    self.setChar(x, y, 2)
                    self.setChar(x, 41-y, 2)

    '''画迷雾的功能丢给pl的center方法去做试试'''

    def getChar(self, x, y):        #获取一个地图方块的id
        if all([x >= 0, x < 64, y >= 0, y < 42]):
            return self.level[x][y]
        return -1

    def setChar(self, x, y, val=1):         #无val参数则是clearMist
        self.level[x][y]=val

    def isOpaque(self, x, y, tag=False):        #是否是不透明方块？
        return self.dg.getChar(x, y) in self.dgMist or self.dg.sur.getChar(x, y) in self.surMist or (tag and self.dg.po.getChar(x, y) >=0)

    def isNoMist(self, x, y):       #是否无雾？
        return self.getChar(x, y)==1

    def __castLight(self, cx, cy, row, start, end, radius, xx, xy, yx, yy, ID, tag=False):
        if start<end: return
        radius2=radius*radius       #半径的平方
        for j in range(row, radius+1):
            dx, dy=-j-1, -j
            blocked=False
            while dx<=0:
                dx+=1           #横行遍历
                X, Y = cx + dx * xx + dy * xy, cy + dx * yx + dy * yy   #做矩阵变化，8个直角三角形区都要处理
                l_slope, r_slope = (dx - 0.5) / (dy + 0.5), (dx + 0.5) / (dy - 0.5)
                if start < r_slope:
                    continue
                elif end > l_slope:
                    break
                else:
                    # 除去某个方块的雾
                    if dx * dx + dy * dy < radius2:
                        if tag: self.lst.add((X, Y))
                        else: self.setChar(X, Y)
                    if blocked:
                        # 遇到成排的障碍物：跳过
                        if self.isOpaque(X, Y, tag):
                            new_start = r_slope
                            continue
                        else:
                            blocked = False
                            start = new_start
                    else:
                        if self.isOpaque(X, Y, tag) and j<radius:
                            blocked = True
                            self.__castLight(cx, cy, j + 1, start, l_slope,
                                             radius, xx, xy, yx, yy, ID+1, tag)
                            new_start = r_slope
            if blocked:         #最后一块方块不透明：后面不用扫描了
                 break

    def set_fog(self, x, y, r):      #这个是放在doFov前的一个函数，把所有的1变成2，加上半透明的雾
        for i in range(x-r, x+r+1):
            for j in range(y-r, y+r+1):
                if self.getChar(i, j)==1:
                    self.setChar(i, j, 2)

    def doFov(self, x, y, radius):      #主接口程序
        self.set_fog(x, y, radius+1)
        self.setChar(x, y, 1)
        for octant in range(8):
            self.__castLight(x, y, 1, 1.0, 0.0, radius, self.mult[0][octant], self.mult[1][octant],
                             self.mult[2][octant], self.mult[3][octant], 0)

    def getShootRange(self, x, y, radius):
        self.lst.clear()
        for octant in range(8):
            self.__castLight(x, y, 1, 1.0, 0.0, radius, self.mult[0][octant], self.mult[1][octant],
                             self.mult[2][octant], self.mult[3][octant], 0, tag=True)
        return self.lst

    def reset_mist(self):
        self.level=[[0 for i in range(42)] for j in range(64)]
        
