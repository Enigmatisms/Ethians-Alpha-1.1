#!/usr/bin/env python3
#-*-coding:utf-8-*-

import os, pygame
from src.blittools import Infoimage


__author__='SEeHz3'
__date__='2019.2.16'

path=os.path.join('asset', 'fonts', 'verdana.ttf')

class Cursors:      #游戏内光标，主要有：
    """自主选择攻击对象的攻击光标
        手动控制的交互光标"""
    def __init__(self, surface, func_lst):
        #func_lst是po, dg.sur, npc
        pygame.init()
        self.screen=surface
        self.font=pygame.font.Font(path, 16)
        self.cursor_list=([pygame.image.load('asset\cursor3.png').convert_alpha(),
                           pygame.image.load('asset\cursor2.png').convert_alpha(),
                           pygame.image.load('asset\cursor.png').convert_alpha()])
        self.cursors=self.cursor_list[0]
        self.posx, self.posy=-1,-1
        self.xat, self.yat=(0,0)
        self.temx, self.temy=0, 0
        self.data, self.info, self.po=None,None,None
        self.pos_lst=[]
        self.func_lst=func_lst
        self.len_lst=len(self.func_lst)
        self.img=Infoimage(surface)
        self.gui, self.fem=None, None
        self.texts=None
        self.detail_judge=0         #等于1是是装备系统，等于2时是怪物系统
        self.attack_judge=False         #攻击标签，当使用弓箭或者法杖，书本时激活

    def draw_cursor(self):
        self.screen.blit(self.cursors, (560, 266))

    def cursor_pos(self, pos):       #自动设定cursor的位置，原则上应该在player处，若是攻击模式，则随机选择一个怪物
        #target参数就是接收了monster类或者ply中对应信息的，接收一个元组，只执行一次
        self.posx, self.posy=pos    
  
    def key_left(self, target):       #target是pl类，用于玩家图标的重绘
        if self.posx>1:
            self.posx-=1
            target.player_img.X+=32

    def store_playerpos(self, target):
        self.pos_lst=[]
        self.temx, self.temy=target.xat, target.yat
        for i in range(self.temx-1, self.temx+2):
            for j in range(self.temy-1, self.temy+2):
                self.pos_lst.append([i, j])
        self.pos_lst.remove([self.temx, self.temy])
            

    def key_right(self, target):       
        if self.posx<64:
            self.posx+=1
            target.player_img.X-=32

    def key_up(self, target):       
        if self.posy>1:
            self.posy-=1
            target.player_img.Y+=32

    def key_down(self, target):       
        if self.posy<42:
            self.posy+=1
            target.player_img.Y-=32

    def standat(self, func_list):       #检测光标的位置
        """func_list有严格顺序规定, 第一个检测位置的是mist类，如果不被黑雾覆盖
        就可以检测其他id信息：无黑雾但有阴影的可以检测equip, surround, house_room
        无阴影的可以检测：monster, npc, equip, surround, house_room"""
        self.xat, self.yat=self.posx-1, self.posy-1
        judge=self.getChar(func_list[0], self.xat, self.yat, 0)
        if judge:
            length=len(func_list)
            if judge!=2:
                for i in range(1, length):
                    where=self.getChar(func_list[ i ], self.xat, self.yat, i)
                    if where in func_list[ i ].detect:
                        self.data=func_list[ i ].detect[where]        #返回id数据对应的文字信息
                        break
                    else:
                        self.data=None
            else:
                for i in range(3, length):          #TBS, 还得改切片的位置，因为equip和monster都没写
                    where=self.getChar(func_list[ i ], self.xat, self.yat, i)
                    if where in func_list[ i ].detect:
                        self.data=func_list[ i ].detect[where]        #返回id数据对应的文字信息
                        break
                    else:
                        self.data=None
        else:
            self.data='Covered by Mist.'
        

    def interact(self, remote=False):            #这个是交互,remote参数默认为false,当true的时候可以远程交互（只限查看信息）
        #应该实现：近距离的开关宝箱，清除陷阱，开关门。
        #func_lst的参数是[dg.sur, npc]
        if not remote:
            print("Tryed")
            if [self.xat, self.yat] in self.pos_lst and not self.func_lst[0].getChar(self.xat, self.yat):
                """for i in range(1, self.len_lst):
                    where=self.func_lst[i].getChar(self.xat, self.yat)
                    if where in self.func_lst[i].inter_dict:
                        if i-1:
                            self.func_lst[i].inter_dict[ where ]()
                        else:
                            self.func_lst[i].interDict(self.xat, self.yat, where)         #索引和传参都是where
                    else: return False"""
                where = self.func_lst[1].getChar(self.xat, self.yat)
                if where in self.func_lst[1].inter_dict:
                    self.func_lst[1].interDict(self.xat, self.yat, where)  # 索引和传参都是where
                else:
                    return False
                where = self.func_lst[2].getChar(self.xat, self.yat)
                if where>0:
                    where=self.func_lst[2].getNPC(self.xat, self.yat)
                    self.func_lst[2].inter_dict[where]()
                else:
                    return False
            else: return False
        else: return False
        return True

    @staticmethod
    def getChar(target, x, y, tag):
        if tag==1:
            return target.getMobid(x, y)
        elif tag==2:
            if target.getChar(x, y)>=0:
                return target.getNPC(x, y)
            return -1
        return target.getChar(x, y)

    @staticmethod
    def setChar(target, x, y, value):
        target.level[x][y]=value

    def show_info(self, x, y):
        #把information展示在屏幕的(x,y)点处
        self.info=self.font.render(self.data, True, (0,0,0))
        self.screen.blit(self.info, (x, y))

    def center(self, surface, target):     #基准点是（16，9），表示把（x, y）点放置在屏幕中心
        for y in range(42):
            for x in range(64):
                value=target.getChar(x, y)
                if value>=0:
                    target.image.X=(16-self.posx)*32+80+x*32
                    target.image.Y=(9-self.posy)*32+10+y*32
                    target.image.frame=value
                    target.image.last_frame=value
                    target.image.update(0)
                    target.image.draw(surface)

    def cursor_info(self, x, y):
        if self.po.getChar(self.xat, self.yat):
            mob=self.po.getMob(self.xat, self.yat)
            self.img.blitMobInfo(mob, x, y)

    def item_info(self, x, y):
        if self.fem.getChar(self.xat, self.yat) != -1 and self.po.getChar(self.xat, self.yat):            #怪物优先级是最高的
            stuff=self.fem.pool[(self.xat, self.yat)]
            self.img.blitItemInfo(stuff, x, y)

    def detail(self):
        flag1=self.fem.getChar(self.xat, self.yat)
        flag2=self.po.getChar(self.xat, self.yat)
        if flag2:
            mob=self.po.getMob(self.xat, self.yat)
            self.img.getDetail(mob)
            self.detail_judge=2
        elif not flag2 and flag1 != -1:
            stuff=self.fem.pool[(self.xat, self.yat)]
            self.img.getDetail(stuff)
            self.detail_judge=1

    def drawDetail(self):
        length=len(self.img.texts)
        if self.detail_judge==1:            #绘制装备detail
            self.screen.blit(self.img.texts[0], (70, 60))
            self.screen.blit(self.img.texts[1], (218, 60))
            self.screen.blit(self.img.texts[2], (70, 208))
            for i in range(3, length-11-self.img.texts[-1]):
                self.screen.blit(self.img.texts[i], (70, 208+45*(i-2)))
            for i in range(length-11-self.img.texts[-1], length-6-self.img.texts[-1]):
                self.screen.blit(self.img.texts[i], (330, 270+40*(i-length+11+self.img.texts[-1])))
            for i in range(length-6-self.img.texts[-1], length-1-self.img.texts[-1]):
                self.screen.blit(self.img.texts[i], (750, 270+40*(i-length+6+self.img.texts[-1])))
            for i in range(length-1-self.img.texts[-1], length-1):
                self.screen.blit(self.img.texts[i], (580, 60+ 40 * (i - length + 1 + self.img.texts[-1])))
        elif self.detail_judge==2:          #绘制怪物detail
            self.screen.blit(self.img.texts[0], (70, 60))
            self.screen.blit(self.img.texts[1], (218, 60))
            for i in range(2, 5):
                self.screen.blit(self.img.texts[i], (218, 70+30*i))
            for i in range(5, 10):
                self.screen.blit(self.img.texts[i], (120, 260+45*(i-5)))
            self.screen.blit(self.img.texts[10], (860, 60))
            for i in range(11, length):
                self.screen.blit(self.img.texts[i], (520, 260 + 45 * (i - 11)))
    '''====================进攻部分======================'''

    def getNearBy(self):            #获得一个index
        return self.po.getNearBy()

