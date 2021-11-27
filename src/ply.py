#!/usr/bin/env python3
#-*-coding:utf-8-*-
import random, time
from src.ezplot import *

__author__='SEeHz3'
__date__='2019.2.19'


class Player:
    def __init__(self, func):
        self.enter, self.spike_hurt=True, False
        self.posx,self.posy=(32,22)
        self.player_img=MySprite()
        self.player_img.load(r'asset\me.png', 0, 0, 32, 32, 7)          #TBS:这个需要改动，专门的Player类将会引入，也就是说，load的图像与选择的职业有关,以后要改成可变参数
        self.player_img.first_frame, self.player_img.last_frame=0, 0        #TBS:设置图像，上一行注释提到的问题可以通过这个来解决
        self.ptr = None
        self.xat, self.yat=(0,0)
        self.where, self.where2=0, 0
        self.dg=func    #传入参数函数self.dg=func=dg=Dungeon实例
        self.ms=None    #传入Mist实例ms
        self.eq=None
        self.trig_list={13:self.trig_portal, 14:self.trig_summon, 15:self.trig_spikes}
        self.player_img.X=560
        self.player_img.Y=266
        self.inf, self.svt=None, None   #引入信息模块和文件读写模块
        self.mn=None    #loop11的monument类
        self.dgNoTp={1,2,5, 6, 7, 8, 9, 11,12,14,18,19, 23, 24, 25, 26, 31, 32}     #玩家可传送到达的地方
        self.surNoTp={0, 3, 10, 12, 16, 17, 18, 23, 25, 26, 30, 31, 33, 34, 37, 38, 40, 41, 42}     #玩家不可传送到达的地方
        
    def center(self, surface, target, tag=0):     #基准点是（16，9），表示把（x, y）点放置在屏幕中心
        #这个方法会用在所有的图像绘制上。
        #这个方法才是绘制地图。
        for y in range(0, 42):
            for x in range(0, 64):
                value=target.getChar(x, y)
                if value>=0:
                    target.image.X=(16-self.posx)*32+80+x*32
                    target.image.Y=(9-self.posy)*32+10+y*32
                    if tag: r=random.randint(0, 1)
                    else: r=0
                    target.image.frame=value+r
                    target.image.last_frame=value+r
                    target.image.update(0)
                    target.image.draw(surface)

    def draw_player(self, surface):     #画出玩家
        hold=self.ptr.career_getter()*2
        frame=random.randint(hold, hold+1)
        self.player_img.frame, self.player_img.last_frame=frame, frame
        self.player_img.update(0)
        self.player_img.draw(surface)

    def playerImgPos(self, cx, cy, tag=False):
        if tag:
            x_adjust=self.posx-cx
            y_adjust=self.posy-cy
            self.player_img.X, self.player_img.Y =(560+32*x_adjust, 266+32*y_adjust)

    def player_trap(self):      #玩家落入落入陷阱，落入陷阱后会到下一层。对应的关卡数+1，但是会落到下一层的随机处，关卡重置。
        self.dg.level_num+=1
        pygame.display.update()
        time.sleep(0.9)     #会卡0.9s
        self.dg.create_map()
        self.trap_reset_pos()
        hit=random.randint(1, 2)
        self.ptr.hp_adder(-hit)
        if not self.ptr.hp_getter():
            self.inf.deathCause('trap')
        self.inf.prefabTell('trap')
        self.ms.reset_mist()
        self.svt.saveGamer(self.ptr)  # 游戏保存
        pygame.display.update()

    '''================================================================================'''
    def trig_trap(self,position):       #position参数传入的是玩家所在的环境道具id信息，是self.where2在self.standat这个方法里定义了
        if position in self.trig_list:            
            self.trig_list[position]()
        else:
            self.spike_hurt=True

    def trig_spikes(self):          #TBS: 踩中了钉刺陷阱
        if self.spike_hurt:
            hit=random.randint(1, 2)
            self.inf.prefabTell('spike')
            self.ptr.hp_adder(-hit)
            if not self.ptr.hp_getter():
                self.inf.deathCause('spike')
            self.spike_hurt=False       #踩中陷阱之后，若是没有离开陷阱位置，就不会持续受伤害

    def trig_portal(self):
        self.dg.sur.setChar(self.posx-1, self.posy-1, -1)
        self.inf.prefabTell('tp')
        self.trap_reset_pos()           #踩到传送陷阱是被在本层内传送了
        self.ms.reset_mist()

    def trig_summon(self):      #TBS:   踩到召唤怪物陷阱就会召唤怪物
        self.dg.sur.setChar(self.posx-1 , self.posy-1, -1)
        self.inf.prefabTell('summon')
        self.dg.po.more_mob(radius=4)          #引用po类中的方法
    '''================================================================================'''

    def dgEvent(self):
        if self.where in {20, 21}:
            if not random.randint(0, 4):        #中毒
                self.ptr.setStat()
        elif self.where in {18, 19}:
            self.ptr.setStat(2, 4 - self.ptr.fireR)

    def nearByEvent(self):      #临近触发事件
        for point in self.getAttackRange():
            if self.dg.sur.getChar(*point)==9:          #暗门
                if random.randint(0,1):
                    self.dg.sur.setChar(*point, 39)
                    self.inf.prefabTell('new!')
            elif self.dg.sur.getChar(*point)==37:           #活死人
                if random.randint(0, 1):
                    self.dg.sur.setChar(*point, 36)
                    self.dg.po.more_mob(point, 0, 26, flag=True)
            elif self.dg.sur.getChar(*point)==5:            #钉刺箱子
                if not random.randint(0, 8):
                    self.dg.sur.setChar(*point, 7)

    #移动
    def move(self, x, y):
        if self.posx < 64 and self.posy < 64:
            func_list=[self.dg, self.dg.sur, self.dg.npc, self.dg.po]
            judge = 1
            for func in func_list:
                if func.getChar(self.posx-1+x, self.posy-1+y) in func.no_walk:
                    judge = 0
                    break
            if judge:
                self.posx += x
                self.posy += y
                f1 = func_list[1]
                judge1 = f1.getChar(self.posx - 1, self.posy - 1)
                self.trig_trap(judge1)
                self.inf.judge = True
            else:
                f1, f2, f3 = func_list[1], func_list[2], func_list[3]  # f1是surrounding类方法
                judge1 = f1.getChar(self.posx-1+x, self.posy-1+y)  # f2是NPC类方法
                judge2 = f2.getChar(self.posx-1+x, self.posy-1+y)
                judge3 = f3.getChar(self.posx-1+x, self.posy-1+y)
                if judge1 in {10, 11}:
                    self.player_trap()
                elif judge1 == 12:
                    if self.ptr.haveKey():  # 背包内有钥匙
                        self.ptr.useKey()  # 使用背包内的钥匙
                        f1.setChar(self.posx-1+x, self.posy-1+y, 1)
                        self.inf.prefabTell('door&-')
                    else:
                        self.inf.prefabTell('door&')
                elif judge1 in {25, 26, 31, 33, 37}:
                    self.dg.sur.interDict(self.posx-1+x, self.posy-1+y, judge1)
                elif judge1 in {40, 41}:
                    self.mn.inspect(judge1, self.posx-1+x, self.posy-1+y)
                else:
                    f1.modChar(self.posx-1+x, self.posy-1+y)
                if judge2>=0:
                    f2.npcSelect(f2.getNPC(self.posx - 1+x, self.posy - 1+y))  # 触发f2也就是NPC方法中的某些项，比如遇上商人等。
                if judge3:
                    f3.attacked(self.posx-1+x, self.posy-1+y)
                if not all([judge1 == -1, judge2 == -1]):
                    self.inf.prefabTell('block')

    def standat(self, target):      #检查站在什么位置,target是fem
        self.xat, self.yat=self.posx-1, self.posy-1
        self.where=self.dg.getChar(self.xat, self.yat)    #where是具体站位所在方块的数据值
        self.where2=self.dg.sur.getChar(self.xat, self.yat)
        where3=target.getChar(self.xat, self.yat)
        self.dgEvent()
        self.nearByEvent()
        self.inf.oneTime(self.where, self.where2, where3)

    def inter_map(self, func_list):
        self.xat, self.yat=self.posx-1, self.posy-1
        for i in range(3):
            where=func_list[ i ].getChar(self.xat, self.yat)
            if not i and where != -1:       #捡起装备
                self.eq.pickUp(self.xat, self.yat)        #站在了装备上
                break
            elif i==1 and where != -1:
                if where in {5, 6, 7}:      #不可以站在门上关门或是站在陷阱上清除陷阱
                    self.dg.sur.interDict(self.xat, self.yat, where)
                break
            elif i==2:
                if where in {3, 4, 16, 17, 29, 30}:
                    self.stairMove(where, func_list[2], func_list[3])
        
    def stairMove(self, where, func, func2):   #interfere with the map (地图操作，在楼梯处按下ENTER会上/下楼),这个函数是不进入循环的，语句每次只执行一次
        #func的传入参数是Dungeon的dg实例，func2的传入参数是Mist的ms实例，使只有成功上下楼才能更新迷雾。
        #where表示的是地图方格属性id，检测到上下楼梯的id时就可以按ENTER上下楼
        if where in {3, 16, 29}:
            if func.level_num>1:
                func.level_num-=1
                func2.reset_mist()
                func.create_map()
                self.posx, self.posy=func.d_x+1, func.d_y+1
                func2.reset_mist()
            else:       #进入地牢第0层（地牢之外，峡谷）
                func.level_num-=1
                func2.reset_mist()
                func.create_map()
                self.posx, self.posy=func.d_x+1, func.d_y+1
                func2.reset_mist()
        elif where in {4, 17, 30}:
            func.level_num+=1
            self.ptr.deepestSet(func.level_num)     #设置ptr最深层
            func2.reset_mist()
            func.create_map()
            self.posx, self.posy=func.u_x+1, func.u_y+1
            func2.reset_mist()
        self.svt.saveGamer(self.ptr)            #游戏保存


    def inter_sur(self):        #和环境交互的类方法（其实也就只有开箱子的作用了）
        self.xat, self.yat=self.posx-1, self.posy-1
        where=self.dg.sur.getChar(self.xat, self.yat)
        self.dg.sur.interDict(self.xat, self.yat, where)
                
    def reset_pos(self):
        self.posx, self.posy=(32, 22)
 
    def trap_reset_pos(self):       #踩到陷阱后，玩家位置的自动重设
        x, y=random.randint(5, 58), random.randint(5, 38)
        judge1=self.dg.getChar(x-1, y-1)
        judge2=self.dg.sur.getChar(x-1, y-1)
        judge3=self.dg.po.getChar(x-1, y-1)
        while not judge1 in self. dgNoTp or judge2 in self.surNoTp or judge3:
            x, y=random.randint(5, 58), random.randint(5, 38)
            judge1=self.dg.getChar(x-1, y-1)
            judge2=self.dg.sur.getChar(x-1, y-1)
            judge3 = self.dg.po.getChar(x - 1, y - 1)
        self.posx, self.posy=(x, y)

    def getActiveRange(self):
        lst=list()
        for x in range(self.posx-6, self.posx+5):
            for y in range(self.posy-6, self.posy+5):
                lst.append((x, y))
        for item in self.getAttackRange():
            lst.remove(item)
        return lst

    def getAttackRange(self):
        lst=list()
        for x in range(self.posx-2, self.posx+1):
            for y in range(self.posy-2, self.posy+1):
                lst.append((x, y))
        lst.remove((self.posx-1, self.posy-1))
        return lst

    def getShootRange(self):
        radius=self.ptr.LR
        return self.ms.getShootRange(self.posx-1, self.posy-1, radius)

    def returnScroll(self):         #给eqf库提供辅助
        if self.dg.level_num != 0:          #不在地表时，传送回地面
            self.dg.level_num=0
            self.ms.reset_mist()
            self.dg.create_map()
            self.posx, self.posy=self.dg.d_x+1, self.dg.d_y+1
            self.ms.reset_mist()
        else:           #在地表时，传送到最深一层
            if self.ptr.deepest_lvl != 0:
                self.dg.level_num=self.ptr.deepest_lvl
                self.ms.reset_mist()
                self.dg.create_map()
                self.posx, self.posy=self.dg.u_x+1, self.dg.u_y+1
                self.ms.reset_mist()
                self.inf.prefabTell('bkscroll')
        self.svt.saveGamer(self.ptr)  # 游戏保存

    def clearMist(self):            #给eqf提供辅助
        self.ms.mapClear()
        self.inf.prefabTell('map')

    def tpScroll(self):
        self.dg.sur.setChar(self.posx-1, self.posy-1, -1)
        self.trap_reset_pos()           
        self.ms.reset_mist()
        self.inf.prefabTell('tps')
