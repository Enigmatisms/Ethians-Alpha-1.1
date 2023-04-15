#!/usr/bin/env python3
#-*-coding:utf-8-*-
#This is the main loop of Ethians

__author__='SEeHz3'
__date__='2019.2.16'

import sys, os, random, pygame
from pygame.locals import *
from src.house_room import *
from src.ply import *
from src.mist import *
from src.npcs import *
from src.ezgui_m import Ezgui
from src.head import *
from src.diymap import *
from src.cursors import *
from src.mobs import *
from src.blittools import *
from src.buttons import Button
from src.playerAttr import Pattr
from loop_module.loop10 import PlayerGui
from equipment.equip import *
from equipment.equipfunc import EquipFunction
from src.info import *
from src.compass import Compass
from src.selection2 import Selection
from src.save import Saveit
from src.quitM import Quitting
from loop_module.loop11 import Monument
from src.keysets import keySets
from loop_module.Startup import Face

pygame.init()
pygame.key.set_repeat(480,30)
hq=HQ()         #主控函数

#defaults
'''======================全局变量========================'''
black=(0, 0, 0)
white=(255, 255, 255)
gray=(128,128,128)
de_size=(1200, 650)
screen=pygame.display.set_mode(de_size, 0, 32)
pygame.display.set_caption('Ethians Alpha 1.0.0')
path=os.path.join('asset', 'fonts', 'verdana.ttf')
font=pygame.font.Font(path, 24)
back=pygame.image.load(r'asset/back.png').convert_alpha()      #这是图形遮盖框
map_back=pygame.image.load(r'asset/map_back.png').convert_alpha()      #地图编辑器特有图形覆盖框
framerate = pygame.time.Clock()         #游戏内时钟
ks=keySets(screen, hq.set_loop)          #按键设置模块
ks.loadPreference()         #载入用户按键偏好设置
fc=Face(screen)
'''======================全局变量========================'''


'''================各种类的实例创建以及参数传递==================='''
inf=Info(screen)
dg=Dungeon(screen)      #创建Dungeon实例, Dungeon是house_room模块中的类，用来绘制随机地图
npc=NPC(dg)
dg.npc=npc
pl=Player(dg)     #创建Player实例，用来检测玩家的地图位置以及和Dungeon的交互
ms=Mist(dg)
pl.ms=ms
dg.sur.getLoop=hq.get_loop           #更加复杂的嵌套
npc.hq=hq           #npc模块可以控制hq,比如和商人交谈会进入5模式，交易会进入3模式
#有关gui模块的初始化================================
'''======gui负责对话框========'''
gui=Ezgui(screen)
gui.text_init()
gui.setSmallRect(680, 580, 104, 3)
gui.hq=hq
npc.gui=gui
gui.setBigRect(100, 140, 54, 8)
gui.setBigRect(150, 140, 54, 8, 1)
#=================DIY类初始化====================
diy=DIY()
#=============================================
#===============Monster&Mob类初始化===============
po=Pool(screen, [dg, dg.sur, npc], pl, ms)
po.arg_funcs=[dg, dg.sur, npc, po]
pl.summon=po.summon     #召唤怪物方法地址传递
po.loopSetter=hq.set_loop
dg.po=po           #dg传入po实例
#=====================playerAttribute模块=====================
ptr=Pattr()
ptr.loopSetter=hq.set_loop
pl.ptr,dg.sur.ptr,po.ptr=ptr,ptr,ptr
ptr.hp_setter(1)              #设置生命值(必要的初始化设定)
ptr.maxhp_setter(1)           #设置生命值上限(必要的初始化设定)
#==================================================
#===============Cursor类初始化====================
cs=Cursors(screen,[po, dg.sur, npc])
cs.po=po
#=============================================
#===============loop10方法=================
pg=PlayerGui(screen, ptr)
def pg_update():
    pg.player_num=ptr.career_getter()           #实时传入当前玩家职业
    pg.getInfo()
    pg.str2Surface()
    pg.formFig()
    hq.set_loop(10)
#===============Button类初始化=====================
cps=Compass(screen, [dg, npc, ms, pl])
bt=Button(screen)
bt.dg, bt.pl, bt.cs, bt.hq , bt.inf= dg, pl, cs, hq, inf

def openMap():
    cps.openMap()
    if cps.judge: inf.prefabTell('sm')
    else: inf.prefabTell('dsm')

def partial(func, para):
    def f():
        func(*para)
    return f

bt.work_lst[1], bt.work_lst[4], bt.work_lst[5]=openMap, partial(pl.move, (-1, -1)), partial(pl.move, (1, -1))
bt.work_lst[6], bt.work_lst[7]=partial(pl.move, (-1, 1)), partial(pl.move, (1, 1))
bt.work_lst[8]=pg_update
bt.ptr=ptr
#==================伤害显示note, Infoimage模块=====================
nt=Note(screen)
nt.ptr, nt.po=ptr, po
nt.cs=cs
img=Infoimage(screen)
img.ptr=ptr
img.playerInfoSetup(1100, 70)
#==================装备系统=======================
fem=FloorEquipManage(screen)
fem.ptr, fem.dg, fem.npc, fem.sur, fem.gui=ptr, dg, npc, dg.sur, gui
pl.eq, fem.pl=fem, pl        #给pl传入实例
dg.fem=fem
po.fem, dg.sur.pl = fem, pl
po.itemDrop=fem.mobItemDrop
dg.sur.itemDrop=fem.boxItemDrop
#==================装备功能系统=======================
eqf=EquipFunction()
eqf.ptr, eqf.ect.ptr, eqf.eq, ptr.eqf, dg.sur.eqf=ptr, ptr, Equip(), eqf, eqf         #dg.sur也需要，比如金币箱子直接加钱
eqf.eq.getInfo()
gui.ptr, gui.eqf, gui.fem=ptr, eqf, fem
gui.owner_init()
eqf.gui, eqf.pl=gui, pl        #eqf中有好几个函数需要能够直接触发loop3
eqf.funcsForGUI()
ptr.gui=gui        #ptr需要gui中的几个参数
bt.work_lst[3]=gui.openBag
cs.gui, cs.fem=gui, fem         #光标系统传入类参数
'''====================================================='''
#====================游戏保存模块===================
svt=Saveit()
svt.gui, svt.eqf=gui, eqf     #需要传递给gamer
for i in [dg, pl, po, dg.sur, ptr, eqf, img, svt, fem, fem.ect, eqf.ect, gui.owner, fem]:     #设置信息显示模块
    i.inf=inf
slt=Selection(screen)
slt.hq, slt.ptr=hq, ptr
pl.svt, slt.svt=svt, svt            #游戏保存模块载入
def creatorLoaderFunc(num):     #游戏创造者界面（供给给Select类使用）
    ms.reset_mist()
    dg.load_level(num)
    po.reset()
    fem.reset()
    if num: npc.infoNPC()
    else: dg.sur.modSur(*mn.mapChange())
    pl.posx, pl.posy = (33, 38)
slt.creatorLoaderFunc=creatorLoaderFunc
#================其他GUI：退出模块================
qt=Quitting(screen)
qt.hq, qt.svt, qt.ptr, qt.slt=hq, svt, ptr, slt
#===============纪念碑Monument(loop11)===============
mn=Monument(screen)
mn.svt, mn.hq=svt, hq
pl.mn=mn

def readRecord():      #全局函数：读取存档后，ptr内部方法更新和地图重建
    ptr.eqf, ptr.gui=eqf, gui
    for k in [pl, dg.sur, po, pg, bt, nt, img, fem, eqf, eqf.ect, gui, slt, qt, gui.owner]:
        k.ptr=ptr
    ptr.loopSetter = hq.set_loop
    #dg.create_map(ptr.nowLvl)

def resetRecord():
    ptr.reset()
    inf.reset()

def loop1_key():            #loop1按键时会做的事情
    """==============主要绘制操作:Center==============="""
    screen.fill((28,28,28))
    pl.center(screen,dg)        #以玩家为中心绘制地图，玩家移动后更新位置
    pl.center(screen,dg.sur)
    npc.center(screen,pl.posx, pl.posy)       #绘制帧可变
    pl.standat(fem)          #检测玩家的站位
    """================================"""
    ms.doFov(pl.xat, pl.yat, ptr.LR)           #除雾以及雾的绘制
    fem.center(pl.posx, pl.posy)
    pl.center(screen, ms)
    po.updateMob(0)             #怪物类
    po.center(pl.posx, pl.posy)
    screen.blit(back,(0,0))     #绘制alpha通道挡板
    ptr.statEffect()
    ptr.lv_autoAdder()
    img.drawPlayerStat()
    img.blitPlayerInfo(1108, 105, 20, 105)           #绘制玩家信息：血量和经验
    pl.draw_player(screen)
    nt.player_hit(ptr.diff_getter(), hq.get_loop())
    """===============玩家死亡=============="""
    if ptr.hp_getter()<=0:
        hq.set_loop(9)
    cps.drawCompass(791, 30)
    inf.getSurface()
    inf.drawText(380, 615)

def loop8_cursor():         #cs中使用
    """=================主要绘制操作: Center================"""
    screen.fill((28,28,28))
    cs.standat([ms, po, npc, dg.sur, dg])
    cs.center(screen,dg)        #以玩家为中心绘制地图，玩家移动后更新位置
    cs.center(screen,dg.sur)
    npc.center(screen, cs.posx, cs.posy)
    fem.center(cs.posx, cs.posy)     #装备的绘制
    cs.center(screen, ms)
    po.updateMob(0)             #怪物类
    po.center(cs.posx, cs.posy)
    ptr.statEffect()
    ptr.lv_autoAdder()
    pl.playerImgPos(cs.posx, cs.posy, cs.attack_judge)
    pl.draw_player(screen)
    nt.player_hit(ptr.diff_getter(), hq.get_loop())  # 绘制玩家血量改变
    if ms.getChar(cs.xat, cs.yat):
        cs.cursor_info(100, 330)
        cs.item_info(100, 330)
    screen.blit(back,(0,0))     #绘制alpha通道挡板
    img.drawPlayerStat()
    img.blitPlayerInfo(1108, 105, 20, 105)           #绘制玩家信息：血量和经验值
    cs.draw_cursor()
    bt.draw_button()
    cs.show_info(160,544)
    '''=======生命值为0========='''
    if ptr.hp_getter()<=0:
        hq.set_loop(9)
    inf.getSurface()
    inf.drawText(380, 615)

def loop8_quit():
    pl.player_img.X, pl.player_img.Y=560, 266       #退出光标模式时，屏幕中心回到player
    pl.xat, pl.yat=cs.temx, cs.temy
    cs.attack_judge=False
    hq.set_loop(1)
    #ptr.inUse=None          #正在使用的远程武器快速访问标签设置为空
    time.sleep(0.2)
    cs.posx, cs.posy = -1, -1

group=pygame.sprite.Group()

while True:
    framerate.tick(30)
    ticks = pygame.time.get_ticks()

    while hq.get_loop() == 0:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        fc.draw()
        if fc.step>=3:
            hq.set_loop(4)
        pygame.display.update()


    if hq.get_loop()==1:
        loop1_key()
        pygame.display.update()

    while hq.get_loop()==1:
        #设置多循环：不同循环做的事情不一样：
        '''循环标签：共有1，2，3，4，5，6, 7种
        1>>>游戏主循环，渲染游戏界面，进行游戏操作
        2>>>单栏GUI界面循环，用于附属菜单：用户选项和设置
        3>>>双栏GUI界面循环，用于渲染游戏内GUI，比如商人的购买界面或是玩家本身的装备栏
        4>>>选择界面（主菜单，技能点，职业选择）
        5>>>特殊GUI界面循环，NPC互动时是否要分出单独一层渲染？还在思考
        6>>>退出游戏（主菜单，继续，退出游戏三个小按钮）界面
        7>>>开发者选项：自定义地图
        8>>>游戏玩家指针界面循环，在游戏主循环按下C后激活
        9>>>死亡界面
        10>>>玩家个人信息展示
        11>>>英雄纪念碑或是英雄缅怀碑绘制
        '''
    
        for event in pygame.event.get():
            if event.type==QUIT:
                qt.quitGame()
            elif event.type==KEYDOWN:
                if event.key==ks.keyPads['esc']:
                    cps.judge=False
                    qt.loopNum=1
                    hq.set_loop(6)
                elif event.key==K_SPACE:    #开发者选项：SPACE键以重新绘制地图
                    dg.create_map()
                    pl.reset_pos()
                    ms.reset_mist()
                elif event.key==ks.keyPads['up']:
                    #pl.key_up([dg, dg.sur, npc, po])
                    pl.move(0, -1)
                elif event.key==ks.keyPads['down']:
                    #pl.key_down([dg, dg.sur, npc, po])
                    pl.move(0, 1)
                elif event.key==ks.keyPads['lf']:
                    #pl.key_left([dg, dg.sur, npc, po])
                    pl.move(-1, 0)
                elif event.key==ks.keyPads['rt']:
                    #pl.key_right([dg, dg.sur, npc, po])
                    pl.move(1, 0)
                elif event.key==ks.keyPads['topl']:
                    #pl.top_left([dg, dg.sur, npc, po])
                    pl.move(-1, -1)
                elif event.key==ks.keyPads['topr']:
                    #pl.top_right([dg, dg.sur, npc, po])
                    pl.move(1, -1)
                elif event.key==ks.keyPads['btl']:
                    #pl.bottom_left([dg, dg.sur, npc, po])
                    pl.move(-1, 1)
                elif event.key==ks.keyPads['btr']:
                    #pl.bottom_right([dg, dg.sur, npc, po])
                    pl.move(1, 1)
                elif event.key==ks.keyPads['etr']:           #捡起装备，打开箱子等交互操作全部在ply的inter_map或inter_sur方法中
                    pl.inter_map([fem, dg.sur, dg, ms])      #enter是交互按键
                elif event.key==ks.keyPads['save']:
                    svt.saveGamer(ptr)
                    #pl.inter_sur()
                elif event.key==K_t:        #开发者按键：t以测试地图
                    ms.reset_mist()
                    dg.load_level()
                    pl.posx,pl.posy=(32,22)
                elif event.key==ks.keyPads['cursor']:
                    cs.cursor_pos((pl.posx, pl.posy))
                    inf.prefabTell('cursor')
                    hq.set_loop(8)
                elif event.key==K_y:
                    hq.set_loop(7)
                loop1_key()
            elif event.type==MOUSEBUTTONDOWN:
                bt.mouse_judge()
                if bt.outside_judge:
                    bt.outside_judge=False
                    loop1_key()
            bt.mouse_prep()
            bt.draw_button()
            pygame.display.update()

    if hq.get_loop()==2:
        ks.init()
        ks.drawSurface()

    while hq.get_loop()==2:     #键盘设置
        framerate.tick(80)
        ticks = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if not ks.listen:
                    if event.key == K_ESCAPE:
                        hq.set_loop(4)
                    elif event.key == K_UP:
                        ks.previous()
                    elif event.key == K_DOWN:
                        ks.nextOne()
                    elif event.key == K_LEFT:
                        ks.goLeft()
                    elif event.key == K_RIGHT:
                        ks.goRight()
                    elif event.key == K_RETURN:
                        ks.enterKey()
                else:
                    ks.putKey(event.key)
                    ks.listen = False
                    ks.updateKey()
                ks.drawSurface()
        ks.drawInds(ticks)
        pygame.display.update()

    while hq.get_loop()==3:     #NPC交易界面循环
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                qt.quitGame()
            elif event.type==KEYDOWN:
                if event.key==ks.keyPads['esc']:
                    gui.quitSetter()
                    pl.player_img.X, pl.player_img.Y=560, 266
            elif event.type==MOUSEBUTTONDOWN:
                if not gui.detail_judge:   #在细节显示栏里不允许点击大按键（没画出来但是存在）
                    gui.mouseBigJudge(gui.func_tag)
                gui.mouseSmallJudge()
            if gui.quit:
                gui.reset(0)
                gui.quit = 0
                hq.set_loop(1)
            else:
                screen.blit(gui.shop_gui, (0, 0))
                gui.mouseBigPrep()
                gui.mouseSmallPrep()
                gui.drawSmallButton(gui.current_npc, gui.detail_judge)
                gui.drawButtonWords(gui.current_npc, gui.detail_judge)
                if gui.detail_judge:
                    gui.drawDetail(70, 60, 45)
                else:
                    gui.drawShopHeader()
                    if gui.img_num > 2:
                        gui.drawBigButton(400, 80, 54, 8, 8, gui.item_list)
                    else:
                        gui.drawBigButton(100, 140, 54, 16, 8, gui.item_list)
                    gui.drawPic()
                    gui.drawInfo()
                    gui.pageDisplay(880, 520)
                pygame.display.update()

    if hq.get_loop()==4:        #loop4前准备
        slt.modeSetup()
        slt.drawSelect()
        pygame.display.update()

    while hq.get_loop()==4:     #选择模式
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                qt.quitGame()
            elif event.type==KEYDOWN:
                if event.key==ks.keyPads['esc']:
                    qt.loopNum = 4
                    hq.set_loop(6)
            elif event.type==MOUSEBUTTONDOWN:
                slt.mouseJudge()
            slt.mousePrep()
            slt.drawSelect()
            if slt.record and slt.mode != 2:          #如果存在存档, 并且不是在选择职业
                if isinstance(slt.record, Pattr):
                    ptr=slt.record
                    slt.record=None
                    readRecord()
                    hq.set_loop(1)
                else:
                    hq.set_loop(4)   #重新设置loop
                    continue
            if hq.get_loop()==1:
                if slt.mode != 1:       #只要不是加技能点，不管是重生还是加载，都要重设位置
                    if not any([slt.creator, slt.monu]):
                        dg.create_map(ptr.nowLvl)
                        pl.trap_reset_pos()         #在重生或是加载存档后，位置需要寻找
                        slt.creator, slt.monu=False, False
                    if slt.mode==2:         #进行职业选择之后，需要重置大量内容
                        inf.reset()
                        ms.reset_mist()
                pl.player_img.X, pl.player_img.Y = 560, 266
            pygame.display.update()

            

    while hq.get_loop()==5:
        '''注意，每个NPC的三个小按钮的功能都可能不一样，比如：
        >>>商人小按钮分别是：买，卖以及交谈，而gui.func_list2中的不同方法函数
        是由npc模块中的gui.setFuncs设置的'''
        for event in pygame.event.get():
            if event.type==QUIT:
                qt.quitGame()
            elif event.type==KEYDOWN:
                gui.quit=1
                pl.player_img.X, pl.player_img.Y=560, 266
            elif event.type==MOUSEBUTTONDOWN:
                gui.mouseSmallJudge()
        if gui.quit:            #此处的判断是：如果按下了键盘就直接退出循环，否则会出现卡一步的效果
            gui.quit=0
            gui.reset(0)
            hq.set_loop(1)
        else:
            screen.blit(back, (0,0))
            img.blitPlayerInfo(1108, 105, 20, 105)           #绘制玩家信息：血量和经验值
            gui.talkGui()
            gui.mouseSmallPrep()
            gui.drawSmallButton()
            gui.drawButtonWords()
            bt.draw_button()
            pygame.display.update()

    while hq.get_loop()==6:
        for event in pygame.event.get():
            if event.type==QUIT:
                qt.quitGame()
            elif event.type==KEYDOWN:
                if event.key==ks.keyPads['esc']:
                    qt.resume()
            elif event.type==MOUSEBUTTONDOWN:
                qt.mouseJudge()
            if hq.get_loop() != 6:
                break
            qt.mousePrep()
            qt.drawButton(150, 30)
            pygame.display.update()
        
                
    while hq.get_loop()==7:
        '''
        7>>>开发者选项：自定义地图
        '''
    
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    diy.reset()
                    hq.set_loop(1)
                elif event.key==K_UP:
                    diy.key_up()
                elif event.key==K_DOWN:
                    diy.key_down()
                elif event.key==K_LEFT:
                    diy.key_left()
                elif event.key==K_RIGHT:
                    diy.key_right()
                elif event.key==K_1:
                    diy.key_1()
                elif event.key==K_2:
                    diy.key_2()
                elif event.key==K_3:
                    diy.key_3()
                elif event.key==K_4:
                    diy.key_4()
                elif event.key==K_5:
                    diy.key_5()
                elif event.key==K_6:
                    diy.key_6()
                elif event.key==K_7:
                    diy.key_7()
                elif event.key==K_8:
                    diy.key_8()
                elif event.key==K_9:
                    diy.key_9()
                elif event.key==K_0:
                    diy.key_0()
                elif event.key==K_TAB:
                    diy.key_tab()

            #screen.fill(gray)
            screen.fill(gray)
            diy.set_floor()
            diy.center(screen)        #以玩家为中心绘制地图，玩家移动后更新位置
            screen.blit(map_back,(0,0))     #绘制alpha通道挡板
            diy.display(screen)
            #???
            pygame.display.update()

    while hq.get_loop()==8:
        for event in pygame.event.get():
            if event.type==QUIT:
                qt.quitGame()
            elif event.type==KEYDOWN:
                if event.key==ks.keyPads['esc']:     #按ESC退出cursor模式
                    if cs.detail_judge:
                        cs.detail_judge=0
                    else:
                        loop8_quit()
                        break
                elif event.key==ks.keyPads['up']:
                    cs.key_up(pl)
                elif event.key==ks.keyPads['down']:
                    cs.key_down(pl)
                elif event.key==ks.keyPads['lf']:
                    cs.key_left(pl)
                elif event.key==ks.keyPads['rt']:
                    cs.key_right(pl)
                elif event.key==ks.keyPads['etr']:       #在光标模式下，只有用户按下ENTER，进行了有意义的操作：
                    #比如解除陷阱，开门关门，相应的怪物才能有动作。
                    if cs.attack_judge:
                        loop8_cursor()
                        if hq.get_loop()==4: break  #升级模式直接退出
                        tuple1=cs.xat, cs.yat
                        judge=True
                        if po.getChar(*tuple1) and tuple1 in pl.getShootRange():      #检测到怪物在攻击范围内
                            if ptr.inUseAmmo():         #判断装备是否还有能量或数量
                                judge = po.distantAttacked(*tuple1, ptr.inUseTag(), ptr.inUseID())
                                if not judge:            #杀死怪物后要立即更新怪物pool，下次就不会选择死亡怪物进行攻击
                                    po.updateMob(0)
                                ptr.useInUse()          #使用武器消耗能量或数量,在点击按钮是会设置inUse
                            else:               #没有能量或数量的武器会引发退出
                                ptr.inUse=False
                                loop8_quit()
                                break
                        elif tuple1==(pl.xat, pl.yat):      #治疗法杖或卷轴
                            if ptr.inUse:
                                if ptr.inUseID() in {52, 195}:       #判断是否是治疗法杖？如果是则可以对自己使用
                                    judge = po.distantAttacked(*tuple1, ptr.inUseTag(), ptr.inUseID())
                                    ptr.useInUse()
                        elif po.getChar(*tuple1) and tuple1 not in pl.getShootRange():
                            inf.prefabTell('targetx')
                        else:       #直接退出
                            if ptr.inUse:
                                if ptr.inUseID() in {196, 197} and ptr.inUseAmmo():          #比如地图法杖或是骷髅法杖
                                    judge = po.distantAttacked(*tuple1, ptr.inUseTag(), ptr.inUseID())
                                    ptr.useInUse()
                        if cs.getNearBy():  # 杀死一个怪物之后，如果周围还有怪物则自动锁定，没有就退出攻击模式
                            cs.cursor_pos(cs.getNearBy())
                        else:
                            loop8_quit()
                            break
                    else:
                        cs.detail()
                        if not cs.detail_judge:
                            judge=cs.interact()        #开锁功能
                            eqf.locked=False
                            if not judge:
                                loop8_quit()
                                break
            '''============主绘制程序=============='''
            if cs.detail_judge:
                screen.blit(gui.shop_gui, (0,0))
                cs.drawDetail()
            else:
                screen.fill((28,28,28))
                cs.standat([ms, po, npc, dg.sur, dg])
                cs.store_playerpos(pl)
                cs.center(screen,dg)        #以玩家为中心绘制地图，玩家移动后更新位置
                cs.center(screen,dg.sur)
                npc.center(screen,cs.posx, cs.posy)
                fem.center(cs.posx, cs.posy)     #装备的绘制
                cs.center(screen, ms)
                po.center(cs.posx, cs.posy)
                pl.playerImgPos(cs.posx, cs.posy, cs.attack_judge)
                pl.draw_player(screen)
                if ms.getChar(cs.xat, cs.yat):
                    cs.cursor_info(100, 330)
                    cs.item_info(100, 330)
                screen.blit(back,(0,0))     #绘制alpha通道挡板
                img.drawPlayerStat()
                img.blitPlayerInfo(1108, 105, 20, 105)
                cs.draw_cursor()
                bt.draw_button()
                cs.show_info(160,544)
                inf.drawText(380, 615)
            pygame.display.update()

    if hq.get_loop()==9:                    #TBS：还需要添加saveDeath之类的语句
        svt.clrRecord()          #清空存档
        inf.draw_judge=True
        inf.deathInfo(ptr.death())
        svt.saveDeath(ptr.death(0))

    while hq.get_loop() == 9:         #game over, 死亡画面渲染，并且有选项：是否重新创建玩家：
        inf.draw()
        for event in pygame.event.get():
            if event.type==QUIT:
                svt.clrRecord()
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if event.key==ks.keyPads['esc']:     #死亡之后，需要重新选择职业，所以要回到大厅
                    slt.careerSet=False
                    slt.gameStart=False
                    resetRecord()
                    hq.set_loop(4)


    while hq.get_loop() == 10:
        for event in pygame.event.get():
            if event.type==QUIT:
                qt.quitGame()
            elif event.type==MOUSEBUTTONDOWN:
                pg.oneButtonJudge()
            elif event.type==KEYDOWN:
                if event.key==ks.keyPads['esc']:
                    pg.mode=0
                    hq.set_loop(1)
                    break
            pg.oneButtonPrep()
            screen.blit(pg.bg_slot[pg.player_num], (0, 0))
            if pg.mode:
                pg.drawKillDict()
            else:pg.blitFig(70, 200, 40)
            pg.drawButton()
            pygame.display.update()

    while hq.get_loop()==11:
        for event in pygame.event.get():
            if event.type == QUIT:      #不用保存游戏
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN: mn.quitSetter()
            elif event.type == MOUSEBUTTONDOWN: mn.quitSetter()
            mn.drawStone()
            pygame.display.update()

    if hq.get_loop()==12:
        svt.clrRecord()
        inf.draw_judge = True
        inf.winInfo(ptr.winSentence())
        svt.saveHero(ptr.death(0, True))        #信息准备

    while hq.get_loop()==12:        #游戏胜利界面
        inf.draw(True)
        for event in pygame.event.get():
            if event.type == QUIT:
                svt.clrRecord()
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == ks.keyPads['esc']:  # 死亡之后，需要重新选择职业，所以要回到大厅
                    slt.careerSet = False
                    slt.gameStart = False
                    resetRecord()
                    po.kingDead=False
                    hq.set_loop(4)
