import os
#!/usr/bin/env python3
#-*-coding:utf-8-*-

import pygame, os, json
import time
from src.ezplot import *
__author__='SEeHz3'
__date__='2019.2.16'


pygame.init()
path=os.path.join('asset', 'fonts', 'verdana.ttf')
font=pygame.font.Font(path, 21)
font2=pygame.font.Font(path, 14)

class DIY:      #地图编辑器模块，开发者可以自己画地图，对应的level数据将被保存。
    def __init__(self):
        self.font, self.font2=font, font2
        MySprite.__init__(self)
        self.house=MySprite()
        self.house.load(os.path.join("asset", "floor2.png"),0,0,32,32,11)
        self.sur=MySprite()
        self.posx,self.posy=(32, 22)
        self.c1,self.c2=pygame.image.load(os.path.join("asset", "cursor.png")).convert_alpha(), pygame.image.load(os.path.join("asset", "cursor2.png")).convert_alpha()
        self.cursors_list=[self.c1, self.c2]
        self.cursors=self.c2           #cursor是地图编辑器里的光标，初始显示绿色光标，表示地砖编辑模式，红色表示环境物品（地图道具）编辑模式
        self.sur.load(os.path.join("asset", "surroundings.png"), 0, 0, 32, 32, 11)
        self.house_level=[[0 for i in range(42)] for j in range(64)]
        self.sur_level=[[-1 for i in range(42)] for j in range(64)]
        self.house_set=True        #按TAB可以切换环境设置以及房间地面设置，house_set为真时设置房间地面，反之设置环境
        self.house_char, self.sur_char=0,0
        self.blocked, self.saver_read, self.saver_del=False,False, False      #(如果为真，则不会对地图进行修改，按3键可以调整这个值)    #saver_read是否允许读取历史文件
        self.xat, self.yat=0,0      #与图像设置有关的位置，（id位置，比正式位置x，y各小1）
        self.pos=None       #显示的坐标值
        self.hq, self.id1, self.id2=None,None,None      #hq控制类，显示的两个参数        
        self.block_text=self.font.render('ID-setter blocking is on', True, (255, 0, 0))

    #中心绘制
    def center(self, surface):     #基准点是（16，9），表示把（x, y）点放置在屏幕中心
    #参数是self.house以及self.surrounding
    #这个方法会用在所有的图像绘制上。
    #这个方法才是绘制地图。
        for y in range(42):
            for x in range(64):
                value=self.getChar1(x, y)
                if value>=0:
                    self.house.X=(16-self.posx)*32+80+x*32
                    self.house.Y=(9-self.posy)*32+10+y*32
                    self.house.frame=value
                    self.house.last_frame=value
                    self.house.update(0)
                    self.house.draw(surface)
        for y in range(42):
            for x in range(64):
                value=self.getChar2(x, y)
                if value>=0:
                    self.sur.X=(16-self.posx)*32+80+x*32
                    self.sur.Y=(9-self.posy)*32+10+y*32
                    self.sur.frame=value
                    self.sur.last_frame=value
                    self.sur.update(0)
                    self.sur.draw(surface)
                else:
                    pass
        self.standat()
        

    def getChar1(self, x, y):       #house   id搜索
        return self.house_level[x][y]

    def setChar1(self, x, y, value):        #house    id设置
        if value!=-1:
            self.house_level[x][y]=value

    def getChar2(self, x, y):       #surrounding   id搜索
        return self.sur_level[x][y]

    def setChar2(self, x, y, value):        #surrounding   id设置
        self.sur_level[x][y]=value

    #========================================#
    '''位置信息以及键盘操作块
    键盘操作，开发者对应踩着的方块会变为需要的方块'''
    def key_up(self):
        if self.posy>1:
            self.posy-=1

    def key_down(self):
        if self.posy<42:
            self.posy+=1

    def key_left(self):
        if self.posx>1:
            self.posx-=1

    def key_right(self):
        if self.posx<64:
            self.posx+=1

    def key_tab(self):
        #按下tab可以使house_set进行开关操作，house_set为真：设置房间地面，反之为环境
        #光标变成另一个
        self.house_set= not self.house_set
        self.cursors=self.cursors_list[ self.house_set ]

    def key_1(self):        #选择框选择的id值-1
        #注意，sur_char=-1意思是为空
        if self.house_set:
            if self.house_char==0:
                self.house_char=32
            else:
                self.house_char-=1
        else:
            if self.sur_char==-1:
                self.sur_char=42
            else:
                self.sur_char-=1

    def key_2(self):        #选择框选择的id值+1
        #注意sur_char=-1是为空，也就是删除原有的物品
        if self.house_set:
            if self.house_char==32:
                self.house_char=0
            else:
                self.house_char+=1
        else:
            if self.sur_char==42:
                self.sur_char=-1
            else:
                self.sur_char+=1

    def key_3(self):        #跳过操作
        self.blocked= not self.blocked
        '''如果self.blocked为真，需要有一个提示，告诉开发者，地形改变已经被禁用了'''

    def key_4(self):        #迅速归0快捷键
        if self.house_set:
            self.house_char=0
        else:
            self.sur_char=-1

    def key_5(self):        #迅速取半操作快捷键
        if self.house_set:
            self.house_char=16
        else:
            self.sur_char=20

    def key_6(self):        #吸管快捷键，可以获取地面上相同砖块或物品的id
        if self.house_set:
            self.house_char=self.getChar1(self.xat, self.yat)
        else:
            self.sur_char=self.getChar2(self.xat, self.yat)

    def key_7(self):        #最为fancy的一个功能：测试地图，地图是要拿去用的，要尽早想一个办法把地图整合
        #到main, house_room, surroundings, npc模块里
        #待解决
        pass

    def key_8(self):        #读取以前的地图设置，编辑已经保存的地图
        #这对于地图修改非常必要
        try:
            with open(os.path.join('data', 'diy.json'), 'r') as read:
                tem=json.load(read)
        except FileNotFoundError:
                self.saver_read=False
        else:
            if len(tem)>0:
                self.saver_read=True
                index=input('The map index you want to overwrite: ')
                try:
                    index=int(index)
                except ValueError:
                    self.saver_read=False
                    print('Argument error or File-read error: Exit.')
                else:
                    if index<0 or index >len(tem): self.saver_read=False
                    if self.saver_read:         #index和索引不同，index是符合人类计数规则，从1开始计数的
                        self.house_level=tem[ index-1 ][ 0 ]
                        self.sur_level=tem[ index-1 ][ 1 ]
                        print('Map %s is loaded successfully.'%index)
                    else:
                        print('Argument error or File-read error: Exit.')
    
    def key_9(self):        #删除某些已经保存的地图
        try:
            with open(os.path.join('data', 'diy.json'), 'r') as read:
                tem=json.load(read)
        except FileNotFoundError:
                self.saver_del=False
        else:
            if len(tem)>0:
                print('You have %s map files in storage.\n'%(len(tem)))
                self.saver_del=True
                index=input('The map index you want to delete: ')
                try:
                    index=int(index)
                except ValueError:
                    self.saver_del=False
                    print('Argument error or File-read error: Exit.')
                else:
                    if index<=0 or index >len(tem):  self.saver_del=False
                    if self.saver_del:         #index和索引不同，index是符合人类计数规则，从1开始计数的
                        tem.remove(tem[index-1])
                        with open('data\diy.json', 'w') as setting:
                            json.dump(tem, setting)
                        print('Map %s is deleted successfully.'%index)
                    else:
                        print('Argument error or File-read error: Exit.')
            

    def key_0(self):
        #保存按钮：按下之后会输出self.house_level和self.sur_level
        def dump(file):
            try:
                with open(os.path.join('data', 'diy.json'), 'r') as read:
                    tem=json.load(read)
                    tem.append(file)
                with open(os.path.join('data', 'diy.json'), 'w') as fir:
                    json.dump(tem, fir)
            except FileNotFoundError:
                with open(os.path.join('data', 'diy.json'), 'w') as fir:
                    json.dump([], fir)
                    print('Catalog "diy.json" is created successfully!')
                with open(os.path.join('data', 'diy.json'), 'r') as read:
                    tem=json.load(read)
                    tem.append(file)
                with open(os.path.join('data', 'diy.json'), 'w') as fir:
                    json.dump(tem, fir)
            print('File saved successfully!')
        dump([self.house_level, self.sur_level])
        time.sleep(1)               #防止过度响应按键事件
            
    def standat(self):
        self.xat, self.yat=self.posx-1, self.posy-1
    '''========================================'''

    
    #设置值块
    def set_floor(self):        #设置环境信息
        if self.house_set and not self.blocked:
            self.setChar1(self.xat, self.yat, self.house_char)      #玩家踩在的区块id被改为设置值
        elif not self.house_set and not self.blocked:
            self.setChar2(self.xat, self.yat, self.sur_char)

    '''=================================================='''
    #=================文字和图像辅助模块====================#
    def text_set(self, surface):
        where=self.getChar1(self.xat, self.yat)
        where2=self.getChar2(self.xat, self.yat)
        text=self.font.render('Current ID:'+str((where, where2)), True, (0,0,0))
        surface.blit(text, (4, 560))
        
    @staticmethod
    def image_set(surface, target, x, y, frame):          #单个图像绘制
        #接收的参数surface为screen, target是一个MySprite类，x,y是位置，frame是图像帧数
        target.X=x
        target.Y=y
        target.frame=frame
        target.last_frame=frame
        target.update(0)
        target.draw(surface)
    '''=================================================='''
    #=================文字和图像辅助模块====================#
        

    def display(self, surface):
        #显示选择的id，包括house和sur，以及其他参数信息显示
        if self.blocked:
            surface.blit(self.block_text, (450, 610))       #ID-setter Blocking mode，开启以后，屏幕下方出现红字
        self.id1=self.font.render(str(self.house_char), True, (0,0,0))
        self.id2=self.font.render(str(self.sur_char), True, (0,0,0))
        self.pos=self.font.render('Position:'+str((self.posx, self.posy)), True, (0,0,0))
        self.image_set(surface, self.house, 25, 120, self.house_char)
        #显示当前使用的房屋地砖id以及样式
        surface.blit(self.id1, (28, 153))
        #=================================#
        self.sur.X=25
        self.sur.Y=190
        if self.sur_char>=0:
            self.sur.frame=self.sur_char
            self.sur.last_frame=self.sur_char
        else:
            self.sur.frame=43
            self.sur.last_frame=43
        self.sur.update(0)
        self.sur.draw(surface)          #显示当前使用的环境道具样式以及id
        surface.blit(self.id2, (28, 223))
        surface.blit(self.cursors, (560, 266))          #绘制光标
        surface.blit(self.pos, (4, 530))       #绘制坐标信息
        self.text_set(surface)
        pygame.display.update()

    def reset(self):    #退出时清除数据
        self.house_level = [[0 for i in range(42)] for j in range(64)]
        self.sur_level = [[-1 for i in range(42)] for j in range(64)]
        self.house_set=True        
        self.house_char, self.sur_char=0,0
        self.blocked, self.saver_read=False,False      
        self.posx,self.posy=(32, 22)
        self.cursors=self.c2
        self.pos=None
        time.sleep(0.8)
            
             
