#usr/bin/env python3
#-*-coding:utf-8-*-
import os, pygame, json
from ezplot import MySprite
from equipment.equip import Equip

path=os.path.join('asset', 'fonts', 'verdanab.ttf')
path2=os.path.join('asset', 'fonts', 'verdana.ttf')

class Note:
    def __init__(self, surface):
        self.screen=surface
        self.po=None
        self.font=pygame.font.Font(path, 17)
        self.font2=pygame.font.Font(path, 18)
        self.ptr=None
        self.cs=None

    def center_note(self, notes, target=None):           #target是某一个monster的target.X, target.Y
        if target:
            tuple1=(target.X, target.Y-5)
        else:           #如果没有target说明，target是默认的玩家
            if (self.cs.posx, self.cs.posy)==(-1, -1):
                tuple1=(550, 256)
            else:
                x_adjust=self.po.pl.posx-self.cs.posx
                y_adjust=self.po.pl.posy-self.cs.posy
                tuple1=(550+32*x_adjust, 256+32*y_adjust)
        int_note=notes
        if int_note>0:
            b_note=self.font.render(str(notes), True, (0, 255, 0))
        elif int_note<0 and not target:
            b_note=self.font.render(str(notes), True, (255, 0, 0))
        elif int_note<0 and target:
            b_note=self.font.render(str(notes), True, (255, 255, 255))
        if int_note:
            self.screen.blit(b_note, tuple1)
            pygame.display.update()

    def player_hit(self, hits=0, tag=1):            #tag是个辅助参数，以免绘制血量信息的时候错位
        if hits>0:
            h_note=self.font2.render('+'+str(hits), True, (0, 255, 0))
            self.ptr.de_diff()
        elif hits<0:
            h_note=self.font2.render(str(hits), True, (255, 0, 0))
            self.ptr.de_diff()
        if hits:
            if (self.cs.posx, self.cs.posy)==(-1, -1) or tag==1:
                tuple1=(558, 260)
            else:
                x_adjust=self.po.pl.posx-self.cs.posx
                y_adjust=self.po.pl.posy-self.cs.posy
                tuple1=(550+32*x_adjust, 256+32*y_adjust)
            self.screen.blit(h_note, tuple1)
            #pygame.display.update()

class Infoimage:
    def __init__(self, surface):            #绘制怪物信息概览的小玩意
        self.screen=surface
        self.mob_rect=pygame.image.load(r'asset\mob_back.png').convert()
        self.hp_rect=None
        self.hp_slot=MySprite()
        self.hp_slot.load(r'asset\hp_slot.png', 0, 0, 72, 500, 3)
        self.exp_slot=pygame.image.load(r'asset\exp_slot.png').convert_alpha()
        self.item=MySprite()
        self.item.load(r'asset\process1.png', 0, 0, 32, 32, 16)
        self.item_detail=MySprite()
        self.item_detail.load(r'equipment\process.png', 0, 0, 128, 128, 16)
        self.mob_detail=MySprite()
        self.mob_detail.load(r'asset\mob_demo.png', 0, 0, 128, 128, 10)
        self.stats=MySprite()        #状态显示
        self.stats.load(r'asset\stat.png', 0, 0, 48, 48, 6)
        self.ptr=None
        self.po, self.inf=None, None
        self.origin_hp=0
        self.o_exp=0
        self.image, self.text, self.text2=None, None, None
        self.font=pygame.font.Font(path, 16)
        self.font2=pygame.font.Font(path, 18)
        self.font3=pygame.font.Font(path2, 17)
        self.bigf=pygame.font.Font(path2, 24)
        self.text, self.text2, self.text3=None, None, None
        self.texts=[]
        self.mobIntel = {0: "This monster won't flee from a combat",
                         1: "A coward monster which will flee if badly hurt",
                         2: "Neutral, but will conterattack if hurt",
                         3: "The monster will teleport itself when dying.",
                         4: "This monster knows how to heal itself",
                         5: "Notorious summon sorcery or division ability it has",
                         6: "This monster is a sorcery master",
                         7: "It will summon and it can put spells on you",
                         8: "Long range shots are their favorite",
                         9:"This is a domintator, pray for yourself"}
        self.mobDebuff = {0:"The monster is poisoned", 1:"The monster is frightened", 2:"The monster is cursed",
                          3:"The monster is frozen"}
        self.mobAttri={1:"The monster is toxic", 2:"The monster can make you burn", 3:"The monster knows sorcery of chaos",
                       4:"The monster drains your blood", 5:"The monster can break your shield", 6:"The monster freezes your move",
                       7:"The monster shall make you bleed"}
        

    def getMobInfo(self, mob):          #通过传入的mob参数获取信息
        hp, ohp = mob.hp, mob.origin_hp
        atk, defc, magic, speed = mob.attack, mob.defence, mob.magic, mob.speed
        name=mob.name
        self.image = mob.image
        text="       HP:%2d/%2d"%(hp, ohp)
        text2="%2d|%2d|%2d|%2d"%(atk, defc, magic, speed)
        if mob.servant: color = (0, 100, 0)
        else: color=(0,0,0)
        self.text=self.font.render(text, True, color)
        self.text2=self.font.render(text2, True, color)
        self.text3=self.font.render(name, True, color)
        

    def blitMobInfo(self, mob, x, y):           #屏幕左方渲染信息框
        self.getMobInfo(mob)
        self.screen.blit(self.mob_rect, (x, y))
        self.screen.blit(self.text, (x+10, y+36))
        self.screen.blit(self.text2, (x+38, y+60))
        self.screen.blit(self.text3, (x+50, y+13))
        self.screen.blit(self.image, (x+8, y+12))

    '''=================显示玩家信息=================='''
    def playerInfoSetup(self, x, y):
        self.origin_hp=self.ptr.maxhp_getter()
        self.hp_slot.X, self.hp_slot.Y = x, y

    def getPlayerHp(self, x, y):
        hp=self.ptr.hp_getter()
        self.origin_hp=self.ptr.maxhp_getter()
        rate=hp/self.origin_hp
        height = int(420*rate)
        y_pos=420-height
        if rate>0:
            self.hp_rect=pygame.draw.rect(self.screen, (255, 0, 0), (x, y+y_pos, 56, height), 0)
        text="HP:%2d/%2d"%(hp, self.origin_hp)
        b_text=self.font.render(text, True, (0, 0, 0))
        self.screen.blit(b_text, (x-25, y+450))
        return height

    def drawPlayerStat(self):
        j = 0
        self.stats.Y = 24
        for i in self.ptr.getStat().keys():
            if self.ptr.getStat()[ i ]:
                self.stats.X=90+50*j
                ID=i-2 if i>4 else i-1
                self.stats.frame=ID
                self.stats.last_frame=ID
                self.stats.update(0)
                self.stats.draw(self.screen)
                j+=1


    def blitPlayerExp(self, x, y):
        exp=self.ptr.exp_getter()
        self.o_exp=self.ptr.need_getter()
        level=self.ptr.lv_getter()
        rate=exp/self.o_exp
        height = int(480*rate)
        y_pos=425-height
        if rate>0:
            self.hp_rect=pygame.draw.rect(self.screen, (106, 90, 205), (x+10, y+y_pos, 14, height), 0)
        text="Exp:%2d/%2d"%(exp, self.o_exp )
        text2="Lv.%d"%level
        b_text1=self.font.render(text, True, (0, 0, 0))
        b_text2=self.font.render(text2, True, (0, 0, 0))
        self.screen.blit(b_text1, (x, y+450))
        self.screen.blit(b_text2, (x, y+475))
        self.screen.blit(self.exp_slot, (x, y-70))

    def blitPlayerInfo(self, x1, y1, x2, y2):
        len_slot=self.getPlayerHp(x1, y1)
        if len_slot>210:
            self.hp_slot.frame=0
            self.hp_slot.last_frame=0
        elif len_slot<=210 and len_slot>75:
            self.hp_slot.frame=1
            self.hp_slot.last_frame=1
        else:
            self.inf.prefabTell('dying')
            self.hp_slot.frame=2
            self.hp_slot.last_frame=2
        self.hp_slot.update(0)
        self.hp_slot.draw(self.screen)
        self.blitPlayerExp(x2, y2)

    '''=======================显示装备信息=========================='''
    def getItemInfo(self, stuff):
        text=stuff.name
        if len(text)>=19:
            text=text[:12]+'...'
        self.text=self.font.render(text, True, (0,0,0))
        atk, defc, mgc, spd=stuff.atk, stuff.defc, stuff.magic, stuff.speed
        text='%2d|%2d|%2d|%2d'%(atk, defc, mgc, spd)
        self.text2=self.font.render(text, True, (0,0,0))
        text=str(stuff.price)+' g'
        self.text3=self.font.render(text, True, (0,0,0))
        self.image=self.item.getImage(stuff.ID)
        
    def blitItemInfo(self, stuff, x, y):
        self.getItemInfo(stuff)
        self.screen.blit(self.mob_rect, (x, y))
        self.screen.blit(self.text, (x+50, y+13))
        self.screen.blit(self.text2, (x+45, y+36))
        self.screen.blit(self.text3, (x+48, y+60))
        self.screen.blit(self.image, (x+10, y+14))

    '''==================细节显示=================='''
    def getDetail(self, item):
        self.texts=[]
        if isinstance(item, Equip):
            ID=item.ID
            img=self.item_detail.getImage(ID)
            self.texts.append(img)
            t=item.name
            if item.label==0:
                if item.enchant_lvl==6: text=self.bigf.render(t, True, (148,0,211))        #relic需要紫色的名字
                else: text=self.bigf.render(t, True, (0,0,0))
            else: text=self.bigf.render(t, True, (0,0,0))
            self.texts.append(text)
            t=item.describe
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            t='Attack: '+str(item.atk)
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            t='Defence: '+str(item.defc)
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            t='Magic: '+str(item.magic)
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            t='Speed: '+str(item.speed)
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            t='Weight: '+str(item.weight)+'   Price: '+str(item.price)+' g'
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            lvl=item.lvl
            if lvl != -1:
                t='Level: '+str(lvl)
            else:
                t='Level: NaN'
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            t='Generating Level: '+str(item.gnrt_lvl)
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            if item.energy:
                t='Energy: '+str(item.energy)+'    Number of amount: '+str(item.count)
            else:
                t='Item has no Energy /Number of amount: '+str(item.count)
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            for i in item.form_desc[:-1-item.form_desc[-1]]:      #准备普通装备描述
                text=self.font3.render(i, True, (0,0,0))
                self.texts.append(text)
            for i in item.form_desc[-item.form_desc[-1] - 1:-1]:  # 准备lv6装备的攻击属性描述
                text = self.font2.render(i, True, (148, 0, 211))
                self.texts.append(text)
            self.texts.append(item.form_desc[-1])
        else:
            ID=item.ID
            img=self.mob_detail.getImage(ID)
            self.texts.append(img)
            t=item.name
            text=self.bigf.render(t, True, (0,0,0))
            self.texts.append(text)
            with open(r'data\mob_desc.json', 'r') as read:
                desc=json.load(read)[str(ID)]
            for i in desc:
                text=self.font3.render(i, True, (0,0,0))
                self.texts.append(text)
            t='HP: %2d/%2d'%(item.hp, item.origin_hp)
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            t='Attack: '+str(item.attack)
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            t='Defence: '+str(item.defence)
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            t='Magic: '+str(item.magic)
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            t='Speed: '+str(item.speed)
            text=self.font3.render(t, True, (0,0,0))
            self.texts.append(text)
            self.texts+=self.mobDetail(item)

    def mobDetail(self, mob):
        extra=[]
        if mob.servant:
            t = "Friendly"
            text = self.bigf.render(t, True, (0, 100, 0))
        else:
            t="Hostile"
            text = self.bigf.render(t, True, (100, 0, 0))
        extra.append(text)
        text = self.font3.render(self.mobIntel[mob.intelligent], True, (0, 0, 0))       #获取怪物能力信息
        extra.append(text)
        for k in mob.status.keys():
            if mob.status[k]:
                text = self.font3.render(self.mobDebuff[k], True, (0, 0, 100))      #怪物当前状态
                extra.append(text)
        for k in mob.tags:
             text = self.font3.render(self.mobAttri[k], True, (160, 0, 0))         #怪物攻击特性
             extra.append(text)
        return extra


        
    
            
            
