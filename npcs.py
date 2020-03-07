#!/usr/bin/env python3
#-*-coding:utf-8-*-

from ezgui_m import *

class NPC:      #NPC环境
    def __init__(self, func):      #传入参数为dg
        self.image=MySprite()
        self.dg=func
        self.image.load(r'asset\npcs.png', 0, 0, 32, 32, 8)
        #self.level=[[-1 for i in range(42)] for j in range(64)]
        self.no_stand={0, 4, 7, 8, 9, 10, 30}
        #self.no_walk={2*i for i in range(10)}
        self.no_walk={1}
        self.gui=None
        self.hq=None        #npc可以调整hq中的某些值
        self.npc_pos={}
        self.inter_dict=({0:self.priest, 2:self.merchant, 4:self.soldier})
        self.detect=({0:'Priest Moack', 2:'Merchant Derlian',
                      4:'Mercenary of the Merchant Dan', 6:'Mother Highness', 8:'Father Highness',
                      10:'Grandfather Highness', 12:'Grandmother Highness', 14:'Sister Highness',
                      16:'Lord King Enigma I', 18:'Friend of Enigma'})
        self.judge1=None
        
    def grt_npc(self):      #generate NPC,c初始的NPC只有三种：商人，牧师和士兵
        #先生成商人以及他的护卫
        tem_x, tem_y=self.dg.d_x, self.dg.d_y
        x, y=(random.randint(tem_x-4, tem_x+4),random.randint(tem_y-4, tem_y+4))
        judge1, judge2=self.dg.getChar(x, y), self.dg.getChar(x+1, y)
        flag=0
        while judge1 in self.no_stand or judge2 in self.no_stand:       #不可站在石头，楼梯，树，水上
            if flag==5:
                x, y=(random.randint(10, 48),random.randint(10, 28))
            else:
                x, y=(random.randint(tem_x-4, tem_x+4),random.randint(tem_y-4, tem_y+4))
                flag+=1
            judge1, judge2=self.dg.getChar(x, y), self.dg.getChar(x+1, y)
        self.npc_pos[(x, y)]=2
        self.npc_pos[(x+1, y)]=4
        x, y=(random.randint(tem_x-4, tem_x+4),random.randint(tem_y-4, tem_y+4))
        judge3, judge4=self.dg.getChar(x, y), self.getChar(x, y)
        flag=0
        while judge3 in self.no_stand or judge4 != -1:
            if flag==4:
                x, y=(random.randint(10, 48),random.randint(10, 28))
            else:
                x, y=(random.randint(tem_x-4, tem_x+4),random.randint(tem_y-4, tem_y+4))
                flag+=1
            judge3, judge4=self.dg.getChar(x, y), self.getChar(x, y)
        self.npc_pos[(x, y)]=0

    def infoNPC(self):      #只在限定地图内生成的NPC
        for i in range(5):
            self.npc_pos[(17+i, 12)]=6+2*i
        for i in range(2):
            self.npc_pos[(31+i, 14)] = 16+2*i

    def merchant(self):     #遇上了商人
        self.gui.form_words(1)
        self.gui.insertFuncs(None, 1)
        #给对应gui传入按钮对应的函数
        self.gui.setFuncs(self.gui.merchant_buy, 0, self.gui.func_list2)
        self.gui.setFuncs(self.gui.merchant_sell, 1, self.gui.func_list2)
        self.gui.setFuncs(self.gui.chatLines, 2, self.gui.func_list2)
        self.gui.current_npc=1
        self.gui.form_text()
        self.hq.set_loop(5)
        
    def soldier(self):      #和商人护卫交谈
        #此处只有一段信息
        #剧情对话框出现：可以由一个值，当其为True时，就显示这个输入框。不需要更改while信息
        self.gui.form_words(3)
        self.gui.insertFuncs(None, 1)
        #给对应gui传入按钮对应的函数
        self.gui.setFuncs(self.gui.soldier_hire, 0, self.gui.func_list2)
        self.gui.setFuncs(self.gui.chatLines, 1, self.gui.func_list2)
        self.gui.setFuncs(self.gui.quitSetter, 2, self.gui.func_list2)
        self.gui.current_npc=3
        self.gui.form_text()
        self.hq.set_loop(5)

    def priest(self):       #遇上了牧师
        #牧师可以提供治疗，会出售药剂和一些魔法物品。
        self.gui.form_words(2)
        self.gui.insertFuncs(None, 1)
        #给对应gui传入按钮对应的函数
        self.gui.setFuncs(self.gui.priest_buy, 0, self.gui.func_list2)
        self.gui.setFuncs(self.gui.priest_task, 1, self.gui.func_list2)
        self.gui.setFuncs(self.gui.chatLines, 2, self.gui.func_list2)
        self.gui.current_npc=2
        self.gui.form_text()
        self.hq.set_loop(5)

    def npcSelect(self, ID):
        if ID == -1: pass
        elif ID==0: self.priest()
        elif ID==2: self.merchant()
        elif ID==4: self.soldier()
        else:
            self.gui.form_words(11) if ID == 16 else self.gui.form_words(12)
            self.gui.insertFuncs(None, 1)
            # 给对应gui传入按钮对应的函数
            if ID == 16:
                self.gui.setFuncs(self.gui.chatLines, 0, self.gui.func_list2)
            self.gui.setFuncs(self.gui.quitSetter, 2, self.gui.func_list2)
            self.gui.current_npc = int(ID/2)+1
            self.gui.form_text()
            self.hq.set_loop(5)

    def noWalk(self, x, y):
        bejudge=self.getChar(x, y)
        return True if bejudge!=-1 else False

    def getChar(self, x, y):
        #上次改动了此处，并没有完全修改其他与getChar相关的函数
        #其他函数的判断还可能停留在
        #return True if(x, y) in self.npc_pos else False这个地方，已知此处会使
        #cursors中 interact函数某处被提供错误的值
        #已经修改cursor类，但是此处未修改
        return 1 if (x, y) in self.npc_pos else -1

    def getNPC(self, x, y):
        return self.npc_pos[(x, y)]

    def reset(self):
        #self.level=[[-1 for i in range(42)] for j in range(64)]
        self.npc_pos.clear()
        self.gui.m_judge, self.gui.p_judge=False, False         #gui中执行的任务更多

    def center(self, screen, cx, cy):
        for k in self.npc_pos.keys():
            x, y=k
            value=self.npc_pos[k]
            self.image.X = (16 - cx) * 32 + 80 + x * 32
            self.image.Y = (9 - cy) * 32 + 10 + y * 32
            rand=random.randint(0, 1)
            self.image.frame = value+rand
            self.image.last_frame = value+rand
            self.image.update(0)
            self.image.draw(screen)
