#!/usr/bin/env python3
#-*-coding:utf-8-*-

import time
from ezplot import *

class Button:
    def __init__(self, surface):
        def passby():
            return 0
        self.screen=surface
        self.image=MySprite()
        self.image.load(r'asset\buttons.png', 0, 0, 48, 48, 6)
        self.button_lst=[]
        for i in range(11):
            self.button_lst.append(pygame.Rect(140+i*80, 450, 48, 48))
        self.transp_lst=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]        #是否透明
        self.work_lst=[passby, None, self.cs_func, passby, None, None, None, None, None, self.useWand, self.useBow]
        self.dg, self.pl, self.cs, self.hq, self.inf = None, None, None, None, None
        self.ptr=None
        self.outside_judge=False            #鼠标点击的时候，只有对角线移动能够引起全局更新

    def draw_button(self):
        for i in range(11):
            self.one_update(i)

    def one_update(self, i):
        self.image.X, self.image.Y=140+i*80, 450
        self.image.frame, self.image.last_frame=3*i+self.transp_lst[ i ], 3*i+self.transp_lst[ i ]
        self.image.update(0)
        self.image.draw(self.screen)
            
    def mouse_prep(self):
        x, y=pygame.mouse.get_pos()
        for i in range(11):
            if self.button_lst[ i ].collidepoint(x, y):
                self.transp_lst[ i ]=1
            else:
                self.transp_lst[ i ]=0

    def mouse_judge(self):
        x, y=pygame.mouse.get_pos()
        for i in range(11):
            if self.button_lst[ i ].collidepoint(x, y):
                self.transp_lst[ i ]=2
                self.one_update(i)
                self.work_lst[ i ]()
                pygame.display.update()
                if i>=8:
                    time.sleep(0.3)
                elif i>=4:
                    time.sleep(0.1)
                else:
                    time.sleep(0.2)
                self.outside_judge = True
            else:
                self.transp_lst[ i ]=0

    def cs_func(self):
        self.cs.cursor_pos((self.pl.posx, self.pl.posy))
        self.inf.prefabTell('cursor')
        self.hq.set_loop(8)

    def useWand(self):          #TBS
        wand=self.ptr.getEquipped()['Wand']
        if wand:
            self.inf.prefabTell('attack')
            self.cs.attack_judge=True
            self.ptr.useItem(wand)
            if self.cs.getNearBy():         #攻击时附近检测到怪物
                self.cs.cursor_pos(self.cs.getNearBy())
            else:           #未检测到怪物则以自己为中心
                self.cs.cursor_pos((self.pl.posx, self.pl.posy))
            self.hq.set_loop(8)
        else:
            self.inf.prefabTell('wand0')

    def useBow(self):
        if self.ptr.career_getter()==2:     #法师进入这个判断
            stuff = self.ptr.getEquipped()['Book']
            if stuff:
                self.inf.prefabTell('attack')
                self.cs.attack_judge = True
                self.ptr.useItem(stuff)
                if self.cs.getNearBy():
                    self.cs.cursor_pos(self.cs.getNearBy())
                else:
                    self.cs.cursor_pos((self.pl.posx, self.pl.posy))
                self.hq.set_loop(8)
            else:
                self.inf.prefabTell('b0')
        else:       #弓箭手（游侠进入这个判断）
            stuff = self.ptr.getEquipped()['Left']
            if stuff==1: stuff=self.ptr.getEquipped()['Dual']
            flag=False
            if stuff:
                if stuff.longRange: flag=True
            if flag:
                arw = self.ptr.getEquipped()['Arrow']
                if arw:
                    self.inf.prefabTell('attack')
                    self.cs.attack_judge = True
                    self.ptr.useItem(arw)
                    if self.cs.getNearBy(): self.cs.cursor_pos(self.cs.getNearBy())
                    else: self.cs.cursor_pos((self.pl.posx, self.pl.posy))
                    self.hq.set_loop(8)
                else:
                    self.inf.prefabTell('a0')
            else:
                self.inf.prefabTell('b0')
                
        
