#!/usr/bin/env python3
#-*-coding:utf-8-*-

import os, json, pygame
from collections import deque
from src.ezplot import MySprite

__author__='SEeHZ3'
__date__='2019/2/19'

path=os.path.join('asset', 'fonts', 'verdana.ttf')

with open(os.path.join('data', 'prefabs.json'), 'r') as r:
    DCT = json.load(r)

class Info:
    def __init__(self, surface):
        self.font=pygame.font.Font(path, 20)
        self.font2=pygame.font.Font(path, 56)
        self.screen=surface
        self.textList=deque([],maxlen=32)
        self.drawList=deque([],maxlen=4)        #双向队列
        self.judge=True
        self.textMod=0  #此参数在每次绘制时起作用，从deque中取出部分，以免浪费
        self.stat_death={1:'Before you die, you were poisoned heavily.', 2:'Your corpse is still being burnt.',
                         3:'Dark sorceries, the spells of chaos result in your death.', 4:'Your blood has been drained up...',
                         5:'The hit shattered your armor, as well as your bones.', 6:'Your corpse will be well preserved in ice.',
                         7:'You despaired, for before you die, your body repelled life-saving potion.'}
        self.epitaph={0:'Sword bent, shield broken, blood shed with corpse blackened...',
                      1:'Where is my ultimated end? O I found it shattered in my hand...',
                      2:'I shall return to whence I came and visit those by whom I made...'}
        self.truimph={0:'Swing his blade, ride by the lake, love shall be craved, glory never fades.',
                      1:'Utimated end is reached by this man, who grasps fate with his own hand.',
                      2:'For him, the grand meeting is postponed for the faith he had shown...'}
        self.careerPic=MySprite()
        self.careerPic.load(os.path.join("asset", "win.png"), 0, 0, 600, 200, 1)
        self.careerPic.X, self.careerPic.Y=0, 410
        self.deadpic=pygame.image.load(os.path.join("asset", "epitaph.png")).convert_alpha()
        self.winpic=pygame.image.load(os.path.join("asset", "winBk.png")).convert_alpha()
        self.winList=list()
        self.epiList=list()
        self.surface = pygame.Surface((1200, 650))
        self.surface.fill((0,0,0))
        self.death="You bled to death, hopelessly.."
        self.draw_judge=True       #保证死亡信息的绘制是一个一次性过程

    def reset(self):
        self.textList.clear()
        self.drawList.clear()
        self.epiList.clear()
        self.textMod = 0


    #预设信息生成
    def prefabTell(self, key:str, front='', back=''):
        text=(''.join((str(front), ' ', DCT[key], str(back) ) )).strip()
        if text[-1] not in ['.', '!', "?"]:
            text+='.'
        self.textList.append(text)
        self.textMod+=1     #表示了textList改变了几位
    #[pl, sur, po, pg, bt, nt, img, fem, eqf, eqf.ect, gui, slt]
    #多重不连续参数
    def moreArg(self, key:str, args):
            if key=='hit':          #
                text=f"{args[0]} is hit with {args[1]} HP."
            elif key=='mhit':           #
                text=f"{args[0]} hits you with {args[1]} HP."
            elif key=="kill":           #
                text=f"You have slayed {args[0]}. Exp + {args[1]}."
            elif key=="servantK":       #怪物击杀
                text = f"{args[0]} has slayed {args[1]}."
            elif key=="servantA":       #怪物攻击
                text= f"{args[0]} hits {args[1]} with {args[2]} HP."
            else :      #"reach"
                text=f"Now you are inside of a {args[0]}. Level: {args[1]}. Game saved."
            self.textList.append(text)
            self.textMod += 1  # 表示了textList改变了几位

    #物品计量
    @staticmethod
    def measure(count:int, tag:str, name:str):
        if tag in {"Leg", "Feet"}:
            if count==1:
                mes = "a pair of"
            else:
                mes="%d pairs of"%count
        elif tag=="Potion":
            if name != "Mushrooms":
                if count==1:
                    mes="a bottle of"
                else:
                    mes="%d bottles of"%count
            else:
                if count==1:
                    mes="a bunch of"
                else:
                    mes="%d bunches of"%count
        else:
            if count == 1:
                mes="one"
            else:
                mes="%d"%count
        return mes+' '+name

    def oneTime(self, where1, where2, where3):
        if self.judge:
            self.judge=False
            if where1 in {3, 16}: self.prefabTell('stair+')
            elif where1 in {4, 17}: self.prefabTell('stair-')
            if where2 == 1: self.prefabTell('atdoor')
            elif where2== 2: self.prefabTell('atdoorx')
            elif where2== 4: self.prefabTell('atgate')
            elif where2 == 5: self.prefabTell('box')
            elif where2 == 6: self.prefabTell('boxg')
            elif where2 in {8, 9}: self.prefabTell('box0')
            if where3 != -1: self.prefabTell('stand')

    #准备要打印的信息
    def getSurface(self):
        length=len(self.textList)
        self.textMod = min(length, self.textMod)
        if self.textMod:
            for i in range(length-self.textMod, length - 1):
                tem=self.font.render(self.textList[i], True, (0,0,0))
                self.drawList.append([tem, self.textList[i], False])
            self.font.set_bold(True)
            self.drawList.append([self.font.render(self.textList[-1], True, (0,0,0)), self.textList[-1], True])
            self.font.set_bold(False)
            self.textMod=0

    #打印信息
    def drawText(self, x, y):
        length=len(self.drawList)
        for i in range(length - 1):
            if self.drawList[i][2]:
                image = self.font.render(self.drawList[i][1], True, (0,0,0))
                self.drawList[i][0] = image
                self.drawList[i][2] = False
            self.screen.blit(self.drawList[i][0], (x, y-26*(length-i-1)))
        if self.drawList:
            self.screen.blit(self.drawList[-1][0], (x, y))

    def deathCause(self, tag, name='the Curse of Enigma'):
        if tag=='poison': self.death='The toxic substances in your body cost your life.'
        elif tag=='trap': self.death='You fell down and hit too hard on the ground...'
        elif tag=='burn': self.death='Why the weather seems hotter? Maybe you are lit...'
        elif tag=='spike': self.death='Watch out, your blood is all over the spikes...'
        elif tag=='boxspike': self.death='Greed is never a virtue, which sometimes takes your life.'
        elif tag=='break': self.death='It is extremely painful when your bones are shattered.'
        else: self.death='You have been slayed by %s.'%name

    def deathInfo(self, text):          #死亡信息转换为surface
        IMG=[]
        t=self.font2.render(text[0], True, (255, 255, 255))
        IMG.append(t)
        for i in text[1:]:
            IMG.append(self.font.render(i, True, (255, 255, 255)))
        IMG.append(self.font.render(self.death, True, (255, 255, 255)))        #真正的死因
        self.epiList=IMG

    def winInfo(self, text):          #胜利转换为surface
        IMG=[]
        t=self.font2.render(text[0], True, (255, 255, 255))
        IMG.append(t)
        for i in text[1:-1]:
            IMG.append(self.font.render(i, True, (255, 255, 255)))
        IMG.append(text[-1])
        self.winList=IMG

    def drawDeathInfo(self, x, y):          #绘制死亡信息
        self.screen.blit(self.deadpic, (0,0))
        length=len(self.epiList)
        self.screen.blit(self.epiList[0], (845, 35))
        for i in range(1, length):
            self.screen.blit(self.epiList[i], (x, y+32*(i-1)))

    def drawWinInfo(self, x, y):
        self.screen.blit(self.winpic, (0,0))
        length=len(self.winList)
        self.screen.blit(self.winList[0], (x-8, 95))
        for i in range(1, length-1):
            self.screen.blit(self.winList[i], (x, y + 36 *i))
        self.careerPic.frame, self.careerPic.last_frame=self.winList[-1], self.winList[-1]
        self.careerPic.update(0)
        self.careerPic.draw(self.screen)

    def draw(self, win=False):         #loop9隐去复杂度
        if self.draw_judge:
            i = 255
            while i > 0:
                i -= 1
                if win: self.drawWinInfo(60, 150)
                else: self.drawDeathInfo(485, 130)
                self.surface.set_alpha(i)
                self.screen.blit(self.surface, (0, 0))
                pygame.display.update()
            if win:
                self.drawWinInfo(60, 150)
            else:
                self.drawDeathInfo(485, 130)
            pygame.display.update()
        self.draw_judge = False


















