#!/usr/bin/env python3
#-*-coding:utf-8-*-

import time, random, pygame, json, os
from ezplot import MySprite
from pygame.locals import *
from equipment.owner import Owner
from equipment.equip import Equip

class Ezgui:
    def __init__(self, surface):
        self.screen=surface
        self.item=MySprite()
        self.item.load(r'asset\column.png', 0, 0, 400, 46, 1)
        self.button=MySprite()
        self.button.load(r'asset\buttons_2.png', 0, 0, 96, 50, 1)
        self.header=MySprite()
        self.header.load(r'asset\header.png', 42, 36, 320, 106, 1)
        self.talk_gui=pygame.image.load(r'asset\conversation.png').convert_alpha()
        self.shop_gui=pygame.image.load(r'asset\shop.png').convert()
        self.words=([' Buy         Sell          Chat', ' Buy         Task       Chat', 'Hire        Chat         Quit',
                     ' <<<         >>>        Quit', 'Take         Inquire       Quit', 'Buy One    Buy All      Back',
                     'Equip      Dump1    DumpAll     Back', 'Strip       Dump1    DumpAll     Back', '  Sell1       SellAll       Back',
                     'Use        Dump1    DumpAll     Back', 'Chat', ' '])
        self.stuff=MySprite()
        self.stuff.load(r'asset\process1.png', 0, 0, 32, 32, 16)
        self.detail=MySprite()
        self.detail.load(r'equipment\process.png', 0, 0, 128, 128, 16)
        self.item_list=[]
        self.button_list=[]         #小按钮的rect列表
        self.btcover_list=[]        #按键的图案帧数信息表
        self.rect_list, self.word=[], None
        self.func_list1, self.func_list2=[],[]
        self.text_list, self.text=[], []        #与npc对话时:text_list是pygame 文字图像实例集合，text是实际显示的实例
        self.quit=False
        with open(r'data\npc_talks.txt', 'r') as read:
            self.texts=json.load(read)
        with open(r'data\chat_talks.txt', 'r') as read:
            self.chats=json.load(read)
        path=os.path.join('asset', 'fonts', 'verdana.ttf')
        self.font=pygame.font.Font(path, 21)
        self.font2=pygame.font.Font(path, 17)
        self.font3=pygame.font.Font(path, 14)
        self.current_npc=1          #这个参数，在每次遇到一个npc的时候会设置
        self.img_num=0            #这个参数，在对应不同的npc参数下对应的意义不同
        self.hq, self.ptr, self.eqf, self.fem=None, None, None, None
        self.count=0            #对话进行步数
        #和装备系统有关
        self.owner=Owner()
        self.m_bag, self.p_bag, self.bag_now=[], [], []         #bag_now变量，当每次选择一个交易对象后会设置（比如和商人交易就是m_bag为bag_now）
        self.m_judge, self.p_judge=False, False         #商店物品刷新标签，为True时不刷新，上下楼可以刷新标签为Fasle
        self.page, self.page_now, self.pageText = 0, 0, None
        self.det=[]         #容纳所有pygame.surface形式的单个装备细节（detail）信息，用于getDetail以及drawDetail
        self.detail_judge=False     #detail_judge的作用是，当detail_judge被激活，在loop3中会开启另一个模式, 通过bigMouseJudge修改
        #这个模式只有三个小按钮，没有header图片，显示特定装备细节
        self.flag=0         #记录点击的是哪一个大栏目
        self.sell_judge=False           #当self.sell_judge为True时，与商人等交互，小按钮功能会改变
        self.func_tag=0         #控制mouseBigJudge的外部赋值参数
        self.bigFunc=None       #mouseBigJudge使用的func，一般由外部赋值，比如eqf
        self.equip_funcs=None
        self.info_slot, self.img_slot, self.pos_slot=None, None, None

    def owner_init(self):
        self.owner.ptr, self.owner.eqf, self.owner.eq = self.ptr, self.eqf, Equip()
        self.owner.gui=self

    '''===================非gui绘制的其他方法函数或npc函数========================'''
    def passby(self):           #什么也不做函数
        pass

    def merchant_buy(self):         #买入：打开的是商人装备栏
        if not self.m_judge:
            self.m_bag=self.owner.createBag(1)
            self.m_judge=True
        self.img_num=0
        self.hq.set_loop(3)
        self.reset()
        self.getPage(self.m_bag)
        self.pageDisplayPrep()
        self.page_now, self.bag_now=0, self.m_bag
        self.prepImg(self.m_bag, self.page_now)
        self.setButtonFuncs(-1)         #包括了按键功能（翻页）和按键信息设置

    def merchant_sell(self):
        if not self.m_judge:
            self.m_bag=self.owner.createBag(1)
            self.m_judge=True
        self.img_num=0
        self.hq.set_loop(3)
        self.reset()
        self.getPage(self.ptr.getBag())
        self.pageDisplayPrep()
        self.page_now, self.bag_now=0, self.ptr.getBag()
        self.prepImg(self.ptr.getBag(), self.page_now)
        self.setButtonFuncs(-1)         #包括了按键功能（翻页）和按键信息设置
        self.sell_judge=True            #激活self.sell_judge
    
    def priest_buy(self):            #牧师的治疗药剂购买
        if not self.p_judge:
            self.p_bag=self.owner.createBag(2)
            self.p_judge=True
        self.img_num=1
        self.hq.set_loop(3)
        self.reset()
        self.getPage(self.p_bag)
        self.pageDisplayPrep()
        self.page_now, self.bag_now=0, self.p_bag
        self.prepImg(self.p_bag, self.page_now)
        self.setButtonFuncs(-1)         #包括了按键功能（翻页）和按键信息设置
        

    def priest_task(self):            #牧师的任务
        self.img_num=3
        self.hq.set_loop(3)
        self.reset(2)
        self.getPage([])
        self.pageDisplayPrep()
        self.page_now, self.bag_now=0, []
        self.prepImg([], self.page_now)
        self.setButtonFuncs(-1)         #包括了按键功能（翻页）和按键信息设置

    def soldier_hire(self):
        self.hq.set_loop(3)
        self.img_num=4
        self.reset(2)
        self.getPage([])
        self.pageDisplayPrep()
        self.page_now, self.bag_now=0, []
        self.prepImg([], self.page_now)
        self.setButtonFuncs(-1)         #包括了按键功能（翻页）和按键信息设置

    def openBag(self):
        self.current_npc=0
        self.img_num=2
        self.hq.set_loop(3)
        self.reset()
        self.setButtonFuncs(-1)
        self.getPage(self.ptr.getBag())
        self.pageDisplayPrep()
        self.page_now, self.bag_now=0, self.ptr.getBag()
        self.prepImg(self.ptr.getBag(), self.page_now)

    def chatLines(self):
        if self.count>9:
            self.count=0
            self.quit=1
        else:
            if self.current_npc==9: line=self.chats[self.count+30]
            else: line=self.chats[self.count+10*(self.current_npc-1)]
            self.text=self.font2.render(line, True, (0,0,0))
            self.count+=1

    def quitSetter(self):
        if self.detail_judge:
            self.detail_judge=False
            #从detail界面退出时，原按键的功能函数会被清除（owner.gui.reset()）
            self.reset()
            self.setButtonFuncs(-1)         #-1是退出reset专用tag
        else:
            self.bigFunc=[]
            self.quit=1
            self.sell_judge=False
            self.func_tag=0
        
    '''==========================================================='''
    def setBigRect(self, x, y, gap, n, col=0):    #在位置（x,y）处创建n个y坐标间隔为gap的Item Rect
        for i in range(n):
            r=Rect(x+500*col, y+gap*(i-col), 400, 46)
            self.rect_list.append(r)
        self.item_list=[0 for i in range(len(self.rect_list))]
        self.insertFuncs(None, 0)

    def setSmallRect(self, x, y, gap, n):
        for i in range(n):
            r=Rect(x+gap*i, y, 96, 56)
            self.button_list.append(r)
        self.btcover_list=[0 for i in range(n)]
        self.insertFuncs(None, 1)

    def drawBigButton(self, x, y, gap, n, col, val_lst):     #val_lst接受每个栏目或者按钮的帧数信息
        #col参数表示：一列存在col个item,当一列结束后自动绘制另一列。
        self.drawShopHeader()
        for i in range(col):
            self.item.X, self.item.Y=x, y+gap*i
            self.item.frame, self.item.last_frame=val_lst[ i ], val_lst[ i ]
            self.item.update(0)
            self.item.draw(self.screen)
        for i in range(col, n):         #另一列.
            self.item.X, self.item.Y=x+550, y+gap*(i-col-1)
            self.item.frame, self.item.last_frame=val_lst[ i ], val_lst[ i ]
            self.item.update(0)
            self.item.draw(self.screen)

    def drawSmallButton(self, tag=4, tag2=False):
        if not tag:         #传入的tag参数，在loop3中为self.current_npc
            if tag2:        #tag2是detail_judge
                self.smallButtonSeq(620, 550, 108, 4, self.btcover_list)
            else:
                self.smallButtonSeq(680, 550, 108, 3, self.btcover_list)
        elif tag == 4:          #loop5中使用
            self.smallButtonSeq(680, 580, 104, 3, self.btcover_list)
        else:
            self.smallButtonSeq(680, 550, 108, 3, self.btcover_list)

    def smallButtonSeq(self, x, y, gap, n, val_lst):
        for i in range(n):
            self.button.X, self.button.Y=x+gap*i, y
            self.button.frame, self.button.last_frame=val_lst[ i ], val_lst[ i ]
            self.button.update(0)
            self.button.draw(self.screen)

    def mouseBigJudge(self, tag=0):        #横栏的mouse_judge
        #tag不等于0的情况暂时有两种：1.由eqf控制的enchant, deEnchant   2.可能有的宝石镶嵌
        if tag:     #tag标签不为0时，按键引起的函数触发通过func_list
            x, y=pygame.mouse.get_pos()
            flag=len(self.rect_list)
            for i in range(flag):
                if self.rect_list[ i ].collidepoint((x, y)):
                    posx, posy=self.rect_list[ i ].topleft
                    self.item.X, self.item.Y=posx, posy
                    self.item.frame, self.item.last_frame=2, 2
                    self.item.update(0)
                    self.item.draw(self.screen)
                    pygame.display.update()
                    time.sleep(0.2)
                    self.item.frame, self.item.last_frame=0, 0
                    if self.func_tag == 1:          #tag=1是由eqf的enchant 和deEnchant函数确定的
                        item=self.bag_now[i+self.page_now*16]
                        self.bigFunc(item)
                        self.quitSetter()       #附魔或退魔完毕自动退出
                        self.quitSetter()
                    break
        else:       #tag标签为0时，按键触发函数通过 函数传递i参数
            x, y=pygame.mouse.get_pos()
            flag=len(self.rect_list)
            for i in range(flag):
                if self.rect_list[ i ].collidepoint((x, y)):
                    posx, posy=self.rect_list[ i ].topleft
                    self.item.X, self.item.Y=posx, posy
                    self.item.frame, self.item.last_frame=2, 2
                    self.item.update(0)
                    self.item.draw(self.screen)
                    pygame.display.update()
                    time.sleep(0.2)
                    self.item.frame, self.item.last_frame=0, 0
                    self.getDetail(i, self.bag_now, self.page_now)
                    break
                    

    def mouseBigPrep(self):
        x, y=pygame.mouse.get_pos()
        flag=len(self.rect_list)
        for i in range(flag):
            if self.rect_list[ i ].collidepoint((x, y)):
                self.item_list[ i ]=1
            else:
                self.item_list[ i ]=0

    def mouseSmallJudge(self):        #按钮mouse_judge
        x, y=pygame.mouse.get_pos()
        flag=len(self.button_list)
        for i in range(flag):
            if self.button_list[ i ].collidepoint((x, y)):
                posx, posy=self.button_list[ i ].topleft
                self.button.X, self.button.Y=posx, posy
                self.button.frame, self.button.last_frame=2, 2
                self.button.update(0)
                self.button.draw(self.screen)
                pygame.display.update()
                time.sleep(0.2)
                self.button.frame, self.button.last_frame=0, 0
                self.func_list2[ i ]()         #这个地方要对应执行函数列表的项目，点到什么功能的键执行什么功能
                break

    def mouseSmallPrep(self):
        x, y=pygame.mouse.get_pos()
        flag=len(self.button_list)
        for i in range(flag):
            if self.button_list[ i ].collidepoint((x, y)):
                self.btcover_list[ i ]=1
            else:
                self.btcover_list[ i ]=0

    def insertFuncs(self, func_lst=None, flag=0):       #flag=0，对应的是每一个横栏函数传入，flag=1则是按钮函数的传入
            if func_lst:
                if flag:
                    self.func_list2=func_lst
                else:
                    self.func_list1=func_lst
            else:
                if flag:
                    num=len(self.button_list)
                    self.func_list2=[self.passby for i in range(num)]
                else:
                    num=len(self.rect_list)
                    self.func_list1=[self.passby for i in range(num)]

    @staticmethod
    def setFuncs(func, pos, func_list):          #self.func_list的pos索引位置设置函数为func
        if pos>=len(func_list):
            pass
        else:
           func_list[ pos ]=func

    '''==============LOOP3方法============='''
    def talkGui(self):
        self.screen.blit(self.talk_gui, (160, 537))
        self.screen.blit(self.text, (200, 550))

    def text_init(self):
        flag=len(self.texts)
        for i in range(flag):
            g=self.font.render(self.texts[ i ], True, (0,0,0))
            self.text_list.append(g)

    '''===========================用于npc的函数=============================='''
    def form_text(self):       #npc参数限定了生成具体哪一个NPC的text,1是商人，2是牧师，3是士兵
        #form_text方法是在npc方法中调用的
        text_num=random.randint(5*self.current_npc-5, 5*self.current_npc-1)
        self.text=self.text_list[text_num]

    '''================================================================'''
    def drawButtonWords(self, tag=4, tag2=False):
        if not tag:         #传入的tag参数，在loop3中为self.current_npc
            if tag2:        #tag2是detail_judge
                self.screen.blit(self.word, (636, 560))
            else:
                self.screen.blit(self.word, (684, 560))
        elif tag == 4:          #loop5中使用
            self.screen.blit(self.word, (696, 590))
        else:
            self.screen.blit(self.word, (684, 560))

    def drawShopHeader(self):               #商店背景图的左上角图标
        self.header.frame, self.header.last_frame=self.img_num, self.img_num
        self.header.update(0)
        self.header.draw(self.screen)

    def form_words(self, npc):              #生成按键上的信息
        self.word=self.font.render(self.words[npc-1], True, (0,0,0))

    def reset(self, n=1):         #这是在loop5>>>loop3切换时，按键功能和位置需要发生变化
        #参数n的作用：loop5和loop3使用的button位置不一样，如果进入了loop3退出没有将按钮改回loop5模式则再进入loop5时按键会变奇怪
        if n==1:           #这是调整至loop3交易界面模式
            self.button_list=[]
            self.setSmallRect(680, 550, 108, 3)
        elif n==2:          #单栏reset()
            self.button_list=[]
            self.setSmallRect(680, 550, 108, 3)
            self.rect_list=[]
            self.setBigRect(400, 80, 54, 8)
        elif n==0:           #退出时使用
            self.count=0
            self.button_list=[]
            self.setSmallRect(680, 580, 104, 3)
            self.rect_list=[]
            self.setBigRect(100, 140, 54, 8)
            self.setBigRect(150, 140, 54, 8, 1)
        elif n==-1:         #需要定义其他形式的小按键（比如多于或少于3个时）
            self.button_list=[]

    def printItem(self, npc):           #显示商人和牧师都卖些什么
        if npc==1:
            return self.m_bag
        else:
            return self.p_bag
        
    '''==============装备信息显示================'''
    def getPage(self, bag):         #总共页数显示
        self.page=int(len(bag)/16.5)+1

    def itemInfo(self, bag, page):      #装备信息转换为pygame.surface的准备
        tem=[]
        lst=self.eqf.getBagInfo(bag, page)
        for i in lst:
            if i[-1]=='1':
                text=self.font3.render(i[:-1], True, (180,0,0))
            else:
                text = self.font3.render(i, True, (0, 0, 0))
            tem.append(text)

        return tem

    def prepImg(self, bag, page):           #一个页面的装备信息准备主函数
        self.info_slot=self.itemInfo(bag, page)
        self.img_slot=self.eqf.getImgInfo(bag, page)
        self.pos_slot=self.eqf.getPosInfo(bag, page)

    def drawPic(self):          #绘制函数
        length=len(self.img_slot)
        for i in range(length):
            self.stuff.frame, self.stuff.last_frame=self.img_slot[i], self.img_slot[i]
            self.stuff.X, self.stuff.Y=self.pos_slot[ i ][ 0 ], self.pos_slot[ i ][ 2 ]
            self.stuff.update(0)
            self.stuff.draw(self.screen)

    def drawInfo(self):
        length=len(self.img_slot)
        for i in range(length):
            self.screen.blit(self.info_slot[ i ], (self.pos_slot[ i ][ 1 ], self.pos_slot[ i ][ 2 ]))

    def pgUp(self):     #向前翻页
        if self.page_now:
            self.page_now-=1
            #向前翻页需要刷新三个slot以及page_now
            self.prepImg(self.bag_now, self.page_now)
            self.pageDisplayPrep()

    def pgDn(self):         #向后翻页
        if self.page_now<self.page-1:
            self.page_now+=1
            self.prepImg(self.bag_now, self.page_now)
            self.pageDisplayPrep()

    def pageDisplayPrep(self):          #显示当前页数的准备
        text='Page:'+str(self.page_now+1)+'/'+str(self.page)
        self.pageText=self.font2.render(text, True, (0,0,0))

    def pageDisplay(self, x, y):        #绘制页数信息
        self.screen.blit(self.pageText, (x, y))

    def resetItem(self):
        self.info_slot=[]
        self.img_slot=[]
        self.pos_slot=[]
        self.page, self.page_now=0, 0
        self.pageText=None

    '''==================装备详细信息==================='''

    def getDetail(self, flag, bag, page=0):     #在一个槽中显示装备的所有信息）
        #TBS:暂时不写有关prefix和attributes的有关内容
        texts=[]
        if flag+page*16>=len(bag):
            return
        else:
            ID=bag[flag+page*16].ID
            img=self.detail.getImage(ID)
            texts.append(img)
            t=bag[flag+page*16].name
            if bag[flag+page*16].label==0:
                if bag[flag+page*16].enchant_lvl==6: text=self.font.render(t, True, (148,0,211))        #relic需要紫色的名字
                else: text=self.font.render(t, True, (0,0,0))
            else: text=self.font.render(t, True, (0,0,0))
            texts.append(text)
            t=bag[flag+page*16].describe
            text=self.font2.render(t, True, (0,0,0))
            texts.append(text)
            t='Attack: '+str(bag[flag+page*16].atk)
            text=self.font2.render(t, True, (0,0,0))
            texts.append(text)
            t='Defence: '+str(bag[flag+page*16].defc)
            text=self.font2.render(t, True, (0,0,0))
            texts.append(text)
            t='Magic: '+str(bag[flag+page*16].magic)
            text=self.font2.render(t, True, (0,0,0))
            texts.append(text)
            t='Speed: '+str(bag[flag+page*16].speed)
            text=self.font2.render(t, True, (0,0,0))
            texts.append(text)
            t='Weight: '+str(bag[flag+page*16].weight)+'   Price: '+str(bag[flag+page*16].price)+' g'
            text=self.font2.render(t, True, (0,0,0))
            texts.append(text)
            lvl=bag[flag+page*16].lvl
            if lvl != -1:
                t='Level: '+str(lvl)
            else:
                t='Level: NaN'
            text=self.font2.render(t, True, (0,0,0))
            texts.append(text)
            t='Generating Level: '+str(bag[flag+page*16].gnrt_lvl)
            text=self.font2.render(t, True, (0,0,0))
            texts.append(text)
            if bag[flag+page*16].energy:
                t='Energy: '+str(bag[flag+page*16].energy)+'    Number of amount: '+str(bag[flag+page*16].count)
            else:
                t='Item has no Energy /Number of amount: '+str(bag[flag+page*16].count)
            text=self.font2.render(t, True, (0,0,0))
            texts.append(text)
            if bag[flag+page*16].equipped==1:
                text=self.font.render('Equipped', True, (200, 0, 0))
            else:
                text=self.font.render('Not Equipped', True, (0, 0, 0))
            texts.append(text)
            for i in bag[flag+page*16].form_desc[:-1-bag[flag+page*16].form_desc[-1]]:      #准备普通装备描述
                text=self.font2.render(i, True, (0,0,0))
                texts.append(text)
            for i in bag[flag+page*16].form_desc[-bag[flag+page*16].form_desc[-1]-1:-1]:        #准备lv6装备的攻击属性描述
                text = self.font2.render(i, True, (148, 0, 211))
                texts.append(text)
            texts.append(bag[flag+page*16].form_desc[-1])
            self.det=texts              #直接设置给一个实例变量
            #重新定义小按键的功能
            if self.current_npc==0:
                self.reset(-1)
                self.setSmallRect(620, 550, 108, 4)         #在打开自己背包时
                self.setButtonFuncs(self.current_npc, bag[flag+page*16].equipped)           #进入detail模式时自动调整小按钮的功能
            else:
                self.reset()
                self.setButtonFuncs(self.current_npc, bag[flag+page*16].equipped)           #进入detail模式时自动调整小按钮的功能
            self.detail_judge=True
            self.flag=flag
 
    def drawDetail(self, x, y, gap):
        length = len(self.det)
        self.screen.blit(self.det[0], (x, y))
        self.screen.blit(self.det[1], (x + 148, y))
        self.screen.blit(self.det[2], (x, y + 148))
        for i in range(3, length - 12 - self.det[-1]):
            self.screen.blit(self.det[i], (x, y + 148 + gap * (i - 2)))
        self.screen.blit(self.det[length - 12 - self.det[-1]], (x + 150, y + 60))
        for i in range(length - 11 - self.det[-1], length - 6 - self.det[-1]):
            self.screen.blit(self.det[i], (x + 330, y + 180 + 40 * (i - (length - 1 - self.det[-1]) + 11)))
        for i in range(length - 6 - self.det[-1], length - 1 - self.det[-1]):
            self.screen.blit(self.det[i], (x + 750, y + 180 + 40 * (i - (length - 1 - self.det[-1]) + 6)))
        for i in range(length - 1 - self.det[-1], length - 1):
            self.screen.blit(self.det[i], (x + 580, y + 3 + 40 * (i - (length - 1 - self.det[-1]))))

    def setButtonFuncs(self, npc, tag=0):         #tag用于：同一个current_npc值可能有两个不同的按键方式（比如自身装备的装备和取下）
        if npc==0:
            if tag:         #对应装备已经装备，则按钮是取下
                if tag==1:
                    self.setFuncs(self.ptr.deEquipTest, 0, self.func_list2)
                    self.form_words(8)
                elif tag>1:
                    self.setFuncs(self.expense(tag), 0, self.func_list2)        #对应的物品功能, expense是一个函数
                    self.form_words(10)
            else:
                self.setFuncs(self.ptr.equipTest, 0, self.func_list2)
                self.form_words(7)
            self.setFuncs(self.fem.throwAway1, 1, self.func_list2)
            self.setFuncs(self.fem.throwAwayAll, 2, self.func_list2)
            self.setFuncs(self.quitSetter, 3, self.func_list2)
        elif npc==-1:
            self.setFuncs(self.pgUp, 0, self.func_list2)
            self.setFuncs(self.pgDn, 1, self.func_list2)
            self.setFuncs(self.quitSetter, 2, self.func_list2)
            self.form_words(4)
        else:
            if self.sell_judge:
                self.setFuncs(self.owner.sellOne, 0, self.func_list2)
                self.setFuncs(self.owner.sellAll, 1, self.func_list2)
                self.setFuncs(self.quitSetter, 2, self.func_list2)
                self.form_words(9)
            else:
                self.setFuncs(self.owner.buyOne, 0, self.func_list2)
                self.setFuncs(self.owner.buyAll, 1, self.func_list2)
                self.setFuncs(self.quitSetter, 2, self.func_list2)
                self.form_words(6)

    def expense(self, tag):         #针对消耗品写的函数
        #除了物品数量自减1（只能一个一个使用），还包含别的函数，返回一个函数作为返回值
        def func():     #def 只定义不执行，所以self.equip_funcs[tag](不执行)
            self.bag_now[self.flag+self.page_now*16].count-=1
            if self.bag_now[self.flag+self.page_now*16].count==0:
                del self.bag_now[self.flag+self.page_now*16]
            #先数量自减，再执行其他函数（免得执行其他函数的时候self.flag和self.bag_now发生变化）
            self.equip_funcs[tag]()
        return func
