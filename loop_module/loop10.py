import os
#!/usr/bin/env python3
#-*-coding:utf-8-*-

import pygame, time, sys, json
sys.path.append('..')
from src.ezplot import MySprite

class PlayerGui:
    def __init__(self, surface, ptr):
        self.screen=surface
        self.font1=pygame.font.Font(os.path.join("asset", "fonts", "verdana.ttf"), 20)
        self.font2=pygame.font.Font(os.path.join("asset", "fonts", "verdana.ttf"), 15)
        self.mob=MySprite()
        self.mob.load(os.path.join("asset", "mobs.png"), 0, 0, 32, 32, 10)
        self.mob_name={}
        """============按钮有关属性============="""
        self.btn=MySprite()
        self.btn.load(os.path.join("asset", "buttons_2.png"), 0, 0, 96, 50, 1)
        self.btn.X, self.btn.Y=1000, 80
        self.button_word=[self.font1.render('Kills', True, (0,0,0)), self.font1.render('Back', True, (0,0,0))]
        self.rect=pygame.Rect((1000, 80, 96, 50))
        #====================================
        self.header=self.font1.render("Statistics for monsters killed", True, (0,0,0))
        self.player=MySprite()
        self.player.load(os.path.join("asset", "player.png"), 0, 0, 104, 104, 3)
        self.item=MySprite()
        self.item.load(os.path.join("asset", "items.png"), 0, 0, 64, 64, 6)
        self.bg_slot=[]
        self.equips=MySprite()
        self.equips.load(os.path.join("asset", "process.png"), 0, 0, 64, 64, 16)
        d=pygame.image.load(os.path.join("asset", "warrior.png")).convert()
        self.bg_slot.append(d)
        d=pygame.image.load(os.path.join("asset", "ranger.png")).convert()
        self.bg_slot.append(d)
        d=pygame.image.load(os.path.join("asset", "wizard.png")).convert()
        self.bg_slot.append(d)
        self.ptr=ptr
        self.player_num=self.ptr.career_getter()
        with open(os.path.join("data", "eng_person_des.txt")) as read:
           total=json.load(read)
        with open(os.path.join("data", "mob_dir.json")) as read:
            dct=json.load(read)
            for v in dct.values():
                self.mob_name[v[7]]=v[8]
        self.dscp=[]
        for i in range(5):
            d=self.font2.render(total[self.player_num*5+i], True, (0,0,0))
            self.dscp.append(d)
        self.infos=[]
        self.texts=[]
        self.mode=0     #绘制界面模式标值（0是玩家信息，1是统计信息）
        self.killDict={}            #杀死怪物统计
        self.str_dict={'Left':(708, 320), 'Right':(456, 320), 'Head':(540, 236), 'Armoos.path.join(":(540, 320), ")Leg':(540, 404), 'Necklace':(456, 236),
                        'Ring':(456, 404), 'Feet':(624, 404), 'Wand':(708, 404), 'Cape':(624, 320), 'Amulet':(624, 236), 'Dual':0, 'Book':(708, 236)}

    def getInfo(self):      #获取信息
        self.infos=[]
        self.infos.append(self.ptr.hp_getter())
        self.infos.append(self.ptr.maxhp_getter())
        self.infos.append(self.ptr.atk_getter())
        self.infos.append(self.ptr.def_getter())
        self.infos.append(self.ptr.magic_getter())
        self.infos.append(self.ptr.speed_getter())
        self.infos.append(self.ptr.lv_getter())
        self.infos.append(self.ptr.exp_getter())
        self.infos.append(self.ptr.need_getter())
        self.infos.append(self.ptr.score_getter())
        self.infos.append(self.ptr.weight_getter())
        self.infos.append(self.ptr.brate_getter())
        self.infos.append(self.ptr.career_str_getter())
        self.infos.append(self.ptr.career_getter())
        self.infos.append(self.ptr.carring_getter())
        self.infos.append(self.ptr.LR)
        self.infos.append(self.ptr.poisonR)
        self.infos.append(self.ptr.fireR)
        self.infos.append(self.ptr.iceR)
        self.infos.append(self.ptr.magicR)


    def formFig(self):      #产生玩家信息
        self.texts=[]
        d=self.font2.render("HP:%2d/%2d"%(self.infos[0], self.infos[1]), True, (0,0,0))
        self.texts.append(d)
        d=self.font2.render("Attack: %d"%self.infos[2], True, (0,0,0))
        self.texts.append(d)
        d=self.font2.render("Defence: %d"%self.infos[3], True, (0,0,0))
        self.texts.append(d)
        d=self.font2.render("Magic: %d"%self.infos[4], True, (0,0,0))
        self.texts.append(d)
        d=self.font2.render("Speed: %d"%self.infos[5], True, (0,0,0))
        self.texts.append(d)
        d=self.font2.render("Exp: %d/%d"%(self.infos[7], self.infos[8]), True, (0,0,0))
        self.texts.append(d)
        d=self.font2.render("Level: %d"%self.infos[6], True, (0,0,0))
        self.texts.append(d)
        d=self.font2.render("Score: %d"%self.infos[9], True, (0,0,0))
        self.texts.append(d)
        d=self.font2.render("Weight taken: %d/%d"%(self.infos[14], self.infos[10]), True, (0,0,0))
        self.texts.append(d)
        d=self.font2.render("Blocking rate: %d%%"%self.infos[11], True, (0,0,0))
        self.texts.append(d)
        d = self.font2.render("Luminous Range: %d (Block)" % self.infos[15], True, (0, 0, 0))
        self.texts.append(d)
        d = self.font2.render("Poison Resistance: %d/4" % self.infos[16], True, (0, 0, 0))
        self.texts.append(d)
        d = self.font2.render("Fire Resistance: %d/4" % self.infos[17], True, (0, 0, 0))
        self.texts.append(d)
        d = self.font2.render("Frost Resistance: %d/4" % self.infos[18], True, (0, 0, 0))
        self.texts.append(d)
        d = self.font2.render("Wizardry Resistance: %d/4" % self.infos[19], True, (0, 0, 0))
        self.texts.append(d)
        d = self.font1.render("%s" % self.infos[12], True, (0, 0, 0))
        self.texts.append(d)
        d=self.getMoney()
        self.texts.append(d) 

    def blitFig(self, x, y, gap):           #绘制玩家信息
        l=len(self.texts)
        for i in range(l-7):
            self.screen.blit(self.texts[ i ], (x, y+(i-1)*gap))
        self.player.frame, self.player.last_frame=self.player_num, self.player_num
        self.player.X, self.player.Y=40, 40
        for i in range(l-7, l-2):
            self.screen.blit(self.texts[i], (x+140, y -15+(i - l+7) * gap))
        self.screen.blit(self.texts[l - 2], (160, 50))
        for i in range(5):
            self.screen.blit(self.dscp[i], (250, 50+23*i))
        self.player.update(0)
        self.player.draw(self.screen)
        '''========玩家装备一览============='''
        #衣服
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame=540, 320, 0, 0
        self.item.update(0)
        self.item.draw(self.screen)
        #头盔582
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame=540, 236, 1, 1
        self.item.update(0)
        self.item.draw(self.screen)
        #右手武器
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame=456, 320, 2, 2
        self.item.update(0)
        self.item.draw(self.screen)
        #左手武器
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame=708, 320, 3, 3
        self.item.update(0)
        self.item.draw(self.screen)
        #披风
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame=624, 320, 4, 4
        self.item.update(0)
        self.item.draw(self.screen)
        #鞋子
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame=624, 404, 5, 5
        self.item.update(0)
        self.item.draw(self.screen)
        #裤子
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame=540, 404, 6, 6
        self.item.update(0)
        self.item.draw(self.screen)
        #项链486
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame=456, 236, 7, 7
        self.item.update(0)
        self.item.draw(self.screen)
        #戒指
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame=456, 404, 8, 8
        self.item.update(0)
        self.item.draw(self.screen)
        #法杖
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame=708, 404, 9, 9
        self.item.update(0)
        self.item.draw(self.screen)
        #护身符678
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame=624, 236, 10, 10
        self.item.update(0)
        self.item.draw(self.screen)
        #书籍
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame = 708, 236, 11, 11
        self.item.update(0)
        self.item.draw(self.screen)
        self.drawPlyItem()
        self.item.X, self.item.Y, self.item.frame, self.item.last_frame=460, 485, 12, 12
        self.item.update(0)
        self.item.draw(self.screen)
        self.drawPlyItem()
        self.screen.blit(self.texts[l-1], (540, 503))

    def getMoney(self):
        for i in self.ptr.getBag():
            if i.ID==46:
                return self.font1.render(str(i.count), True, (0,0,0))
        return self.font1.render('0', True, (0,0,0))


    def drawPlyItem(self):
        stuff=self.ptr.getEquipped()
        for k, v in stuff.items():
            if v and v != 1 and k in self.str_dict and k != 'Dual':
                tup=self.toID(k)        #将'Left'等位置标签转化为参数
                ID=v.ID
                self.drawItem(tup, ID)           #绘制对应装备
            elif k=='Dual' and k in self.str_dict and v != 1 and v:
                tup1=self.toID('Left')
                tup2=self.toID('Right')
                ID=v.ID
                self.drawItem(tup1, ID)
                self.drawItem(tup2, ID)

    def oneButtonPrep(self):
        posx, posy=pygame.mouse.get_pos()
        if self.rect.collidepoint(posx, posy):
            self.btn.frame, self.btn.last_frame=1, 1
            self.btn.update(0)
        else:
            self.btn.frame, self.btn.last_frame = 0, 0
            self.btn.update(0)

    def oneButtonJudge(self):
        posx, posy = pygame.mouse.get_pos()
        if self.rect.collidepoint(posx, posy):
            self.btn.frame, self.btn.last_frame = 2, 2
            self.btn.update(0)
            self.btn.draw(self.screen)
            pygame.display.update()
            time.sleep(0.2)
            self.modeChange()

    def drawButton(self):
        self.btn.draw(self.screen)
        self.screen.blit(self.button_word[self.mode], (1025, 92))

    def modeChange(self):       #模式变更
        self.mode=1-self.mode

    def _listMob(self):          #信息准备函数1
        tem=dict()
        for k, v in self.ptr.kill_dict.items():
            if v:
                tem[k]=v
        return tem

    def str2Surface(self):     #信息准备函数2
        dct=self._listMob()
        self.killDict.clear()
        for k, v in dct.items():
            string="%s X %d"%(self.mob_name[k], v)
            text=self.font2.render(string, True, (0,0,0))
            self.killDict[k]=text

    def drawKillDict(self):
        self.screen.blit(self.header, (50, 45))
        count=0
        for k, v in self.killDict.items():
            if count>11:
                self.mob.X, self.mob.Y=340, 95+40*(count-12)
                self.screen.blit(v, (380, 97+40*(count-12)))
            else:
                self.mob.X, self.mob.Y=60, 95+40*count
                self.screen.blit(v, (100, 97 + 40 * count))
            self.mob.frame, self.mob.last_frame=k, k
            self.mob.update(0)
            self.mob.draw(self.screen)
            count+=1


    def toID(self, string):
        return self.str_dict[string]

    def drawItem(self, tup, ID):
        self.equips.X, self.equips.Y=tup
        self.equips.frame, self.equips.last_frame=ID, ID
        self.equips.update(0)
        self.equips.draw(self.screen)

    
        

        
        
        
        
        
        
        
        
            
        
        

