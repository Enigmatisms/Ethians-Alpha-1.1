#-*-coding:utf-8-*-
import time, sys, json, pygame
sys.path.append('..')
from src.ezplot import MySprite

pygame.init()
screen=pygame.display.set_mode((128,128), 0, 32)
pygame.display.set_caption('Weapon Creater')

class EquipSetter:
    def __init__(self, surface):
        self.img=MySprite()
        self.img.load('process.png', 0, 0, 128, 128, 16)
        self.screen=surface
        self.text=None
        self.pic=None
        self.storage=[]
        self.id=None
        self.energy=0
        self.main_loop=0
        

    def inputInfo(self):        #输入装备信息
        self.id=int(input('Please input the ID: '))        #ID
        with open('equipment.json', 'r') as read:
                stuff=json.load(read)
                while str(self.id) in stuff:
                    print('==================================')
                    self.id=int(input('Please re-input the ID: '))
        print('==================================')
        self.drawPic()
        self.text=int(input('Input    label    infomation: '))          #附魔标签
        self.storage.append(int(self.text))
        print('==================================')
        pygame.display.update()
        self.drawPic()
        self.text=input('Input: Attack, Defence, Magic, Speed: ')       #四项基本属性
        print('==================================')
        pygame.display.update()
        judge=self.converter(self.text)
        while not judge:
            self.text=input('Input: Attack, Defence, Magic, Speed: ')
            print('==================================')
            pygame.display.update()
            judge=self.converter(self.text)
        self.drawPic()
        self.text=input('Input: Weight, Price, item_Level, Item_generating_Level: ')       #输入物品重量，价格，物品等级
        print('==================================')
        pygame.display.update()
        judge=self.converter(self.text)
        while not judge:
            self.text=input('Input: Weight, Price, item_Level, Item_generating_Level: ')
            print('==================================')
            pygame.display.update()
            judge=self.converter(self.text)
            
        self.text=input('Name your weapon: ')       #物品名称
        self.storage.append(self.text)
        print('==================================')
        pygame.display.update()
        while self.text.strip() == '' or len(self.text)>25:
            self.text=input('Input Error, reinput name: ')
            print('==================================')
            pygame.display.update()
            
        self.text=input('Describe your weapon: ')           #物品描述
        print('==================================')
        pygame.display.update()
        if not len(self.text.strip()):
            self.storage.append(None)
        else:
            self.storage.append(self.text)
            
        print("Tag: Left, Right, Dual, Head, Armor, Leg, Necklace, Arrow, Ring, Feet, Wand, Book, Cape, Amulet, Task, Potion, Gem, Others.")
        self.text=input("Tag for this item:")           #物品标签
        if not len(self.text.strip()):
            self.storage.append('Others')
        else:
            self.storage.append(self.text)
        print('==================================')
        self.energy=input('Energy Points:')
        try:
            self.energy=int(self.energy)
        except TypeError:
            self.energy=0
        else:
            pass
        print('==================================')
        print('\t\tGeneral attributes are set up')
        print('==================================')
        pygame.display.update()

    def enchantInfo(self):          #enchant类的附加属性输入
        self.text=input('Any prefix?: ')            #前缀属性
        print('==================================')
        pygame.display.update()
        judge=self.converter(self.text, 2)
        if self.text:
            while not judge:
                self.text=input('Wrong prefix number, reinput: ')
                pygame.display.update()
                print('==================================')
                judge=self.converter(self.text, 1)
            self.storage.append(judge)
        else:
            self.storage.append([])             #如果开始时没有附加性前缀，则自动设置为-1
        self.text=input('Enchant level: ')          #附魔等级
        print('==================================')
        pygame.display.update()
        try:
            int(self.text)
        except TypeError:
            self.text=input('Reinput enchant level: ')
            print('==================================')
            pygame.display.update()
        self.storage.append(int(self.text))
        self.text=input('Any special Attribute?: ')         #特殊属性
        print('==================================')
        pygame.display.update()
        judge=self.converter(self.text, 1)
        if self.text:
            while not judge:
                self.text=input('Wrong attribute number, reinput: ')
                print('==================================')
                pygame.display.update()
                judge=self.converter(self.text, 1)
            self.storage.append(judge)
        else:
            self.storage.append([])             #如果开始时没有附加属性，则ID自动设为-1
        time.sleep(0.5)
        print('==================================')
        print('\t\tEnchant attributes are set up')
        print('==================================')
        pygame.display.update()

    def diagnostic(self):           #检查输入是否有误
        print(len(self.storage))
        print(self.storage)
        print('\n============DIAGNOSTICS=============\n')
        print('根据self.storage的数据，新装备属性如下：')
        print('装备名称：%s， 装备ID：%d'%(self.storage[9],self.id))
        print('装备是否可附魔：%s'%self.getEnchant(self.storage[0]))
        print('七项基本属性：')
        print('\t攻击：%d'%self.storage[1])
        print('\t防御：%d'%self.storage[2])
        print('\t魔法：%d'%self.storage[3])
        print('\t速度：%d'%self.storage[4])
        print('\t重量：%d'%self.storage[5])
        print('\t买入价格：%d'%self.storage[6])
        print('\t等级：%d'%self.storage[7])
        print('\t自然生成概率等级：%d'%self.storage[8])
        print('描述：%s'%self.storage[10])
        print('物品标签: %s'%self.storage[11])
        print('能量点数: %d'%self.energy)
        if not self.storage[0]:
            print('前缀属性：')
            for i in self.storage[12]:
                print('---'+str(i))
            print('当前附魔等级：%d'%self.storage[13])
            print('其他属性：')
            print(len(self.storage), self.storage)
            for i in self.storage[14]:
                print('---'+str(i))
        pygame.display.update()

    @staticmethod
    def getEnchant(num):          #用于诊断系统生成字符串
        if num:
            return "No"
        else:
            return "Yes"

    @staticmethod
    def storeJudge():       #是否储存？如果否，则重新输入，如果是则直接保存
        try:
            num=int(input("Store?( 1 for/ 0 against) "))
        except TypeError:
            print('==================================')
            print("Input Error!")
            print('==================================')
            return False
        else:
            print('==================================')
            print("Storing...")
            print('==================================')
            if num:
                return True
            else:
                return False
        finally:
            pygame.display.update()

    def store(self):        #json保存模式
        try:
            with open('equipment.json', 'r') as read:
                stuff=json.load(read)
        except FileNotFoundError:
            with open('equipment.json', 'w') as wri:
                json.dump({}, wri)
            with open('equipment.json', 'r') as read:
                stuff=json.load(read)
        finally:
            stuff[self.id]=self.storage
            self.reset()
            stuff=dict(sorted(stuff.items(), key=lambda x:int(x[0])))
            with open('equipment.json', 'w') as wri:
                json.dump(stuff, wri)
            print('==================================')
            print("Equipment Stored.")
            print('==================================')
            pygame.display.update()

                
    def reset(self):        #重置所有项目（执行新的数据输入）
        self.text=None
        self.pic=None
        self.storage=[]
        self.id=None
        

    def converter(self, string, tag=0):         #将连续输入的字符串分开
        #比如atk, defc, magic, speed四项属性输入时是由括号分割的字符串，用方法分开
        if not len(string) and tag: return True
        tem=string.split(',')
        tem_list=[]
        for s in tem:
            try:
                i=int(s.strip())
            except TypeError:
                print('Error! Input includes illegal chars.')
                return False
            else:
                tem_list.append(i)
        if tag==1:
            return tem_list
        elif tag==2:
            self.storage.append(tem_list)
        else:
            self.storage+=tem_list
            return True

    @staticmethod
    def proceedJudge():     #是否执行下一次循环的判定方式
        try:
            num=int(input("Create New Equipment?( 1 for/ 0 against) "))
        except TypeError:
            print('==================================')
            print("Input Error!")
            print('==================================')
            return False
        else:
            print('==================================')
            print("Processing...")
            print('==================================')
            if num:
                return True
            else:
                return False
        finally:
            pygame.display.update()

    def main(self):     #主要执行功能的函数
        while self.main_loop==0:
            self.inputInfo()
            if not self.storage[0]:
                self.enchantInfo()
            self.diagnostic()                       #以下是预设项：
            self.storage.append(0)          #表示的是是否装备标签
            self.storage.append(self.energy)          #表示装备能量的标签
            self.storage.append(1)          #数量标签
            self.storage.append(0)          #物品功能标签
            self.storage.append(0)          #远程武器标签
            if self.storeJudge():
                self.store()
            else:
                self.reset()
                continue
            if self.proceedJudge():
                continue
            else:
                self.main_loop=1
                break

        if self.main_loop:          #main_loop为1时退出
            print('==================================')
            print("Shutting Down Internal Server...")
            print('==================================')
            pygame.display.update()
            time.sleep(1)
            pygame.quit()
            sys.exit()
            
    def drawPic(self):
        self.pic=self.img.getImage(self.id)
        self.screen.fill((255,255,255))
        self.screen.blit(self.pic, (0,0))
        pygame.display.update()

#TBS：能够查找并且修改已经设定的武器的功能.
                

if __name__=='__main__':
    print('==================================')
    print("\tThis is Equipment Creator Module")
    print('==================================\n')
    es=EquipSetter(screen)
    es.main()

            
        
                
