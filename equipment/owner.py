#!/usr/bin/env python3
#-*-coding:utf-8-*-

import sys, random, copy
sys.path.append("..")
#from ezplot import MySprite

class Owner:        #商店系统主控函数
    def __init__(self):
        self.ptr, self.eqf, self.eq=None, None, None
        self.gui=None
        #商人
        self.dct1_must={2:5, 6:3, 8:4, 14:3, 118:2, 119:20, 121:5}
        self.dct1_high={53:1, 57:1, 58:1, 64:1, 66:1, 80:1, 83:1, 86:1, 87:1, 90:1,
           91:1, 96:1, 101:1, 103:1, 156:1}            #高概率生成
        self.dct1_mid={21:1, 22:1, 24:1, 25:1, 26:1, 27:1, 28:1, 29:1, 48:1,
          49:1, 50:1, 51:1, 52:1, 55:1, 56:1, 59:1, 60:1, 61:1, 62:1, 65:1, 70:1,
          76:1, 77:1, 81:1, 82:1, 84:1, 85:1, 88:1, 92:1, 97:1, 102:1, 104:1,
          117:1, 135:1, 157:1, 158:1, 190:1, }         #中等概率生成的物品ID字典
        self.dct1_low={7:1, 9:1, 10:1, 11:1, 23:1, 30:1, 31:1, 54:1, 63:1, 67:1, 68:1, 69:1,
          89:1, 93:1, 94:1, 98:1, 99:1, 112:1, 159:1, 162:1, 164:1, 188:1,
          192:1, 193:1, 194:1, 195:1, 196:1}        #低概率生成
        self.dct1_rare={95:1, 100:1, 113:1, 114:1, 115:1, 128:1, 133:1, 150:1, 163:1,
           165:1, 166:1, 189:1, 191:1, 197:1}       #稀有物品
        self.dct1_sss={18:1, 19:1, 20:1, 75:1, 78:1, 79:1, 105:1, 106:1, 107:1, 129:1,
          142:1, 143:1, 152:1, 153:1, 154:1, 155:1, 161:1, 170:1, 186:1, }      #极稀有
        #牧师
        self.abs_dct2={}     #必定生成的物品ID字典
        self.near_abs2={}            #几乎必定生成
        self.high_chance2={}         #高概率生成的物品ID字典
        self.low_chance2={}          #低概率生成物品ID字典
        self.inf=None

    def generateItem(self, ID, count=1):
        item=self.eqf.returnItem(ID, count)
        if not item.label and item.tag != 'Wand':
            if item.name_set:
                item.name_set=False
            tem=[-1, 0, 1, 2, 3, 4, 5]
            weight=[0.1, 0.55, 0.18, 0.08, 0.05, 0.03, 0.01]
            item.lvl=item.enchant_lvl=random.choices(tem, weight)[0]
            self.eqf.ect.enchant(item)
            if item.lvl==0:
                item.enchant_lvl=1
        elif item.tag=='Wand':      #法杖的生成
            item.name=item.basic_name
            item.lvl=item.enchant_lvl=1
        return item

    def createBag(self, npc=1):
        bag=[]
        if npc==1:
            for k, v in self.dct1_must.items():
                item=self.generateItem(k, v)
                bag.append(item)
            for k, v in self.dct1_high.items():
                judge=random.choice([0, 0, 0, 1])
                if judge:
                    item=self.generateItem(k, v)
                    bag.append(item)
            for k, v in self.dct1_mid.items():
                num1=random.choice([5, 6])
                choice_lst=[0]*num1+[1]
                judge=random.choice(choice_lst)
                if judge:
                    item=self.generateItem(k, v)
                    bag.append(item)
            for k, v in self.dct1_low.items():
                judge=random.choices([0, 1], [0.9, 0.01])[0]
                if judge:
                    item=self.generateItem(k, v)
                    bag.append(item)
            for k,v in self.dct1_rare.items():
                judge=random.choices([0, 1], [0.97, 0.03])[0]
                if judge:
                    item=self.generateItem(k, v)
                    bag.append(item)
            for k,v in self.dct1_sss.items():
                judge=random.choices([0, 1], [0.999, 0.001])[0]
                if judge:
                    item=self.generateItem(k, v)
                    bag.append(item)
        elif npc==2:
            for k, v in self.abs_dct2.items():
                item=self.generateItem(k, v)
                bag.append(item)
            for k, v in self.near_abs2.items():
                judge=random.choices([0, 0, 1])[0]
                if judge:
                    item=self.generateItem(k, v)
                    bag.append(item)
            for k, v in self.high_chance2.items():
                num1=random.choices([4, 5])[0]
                choice_lst=[0]*num1+[1]
                judge=random.choices(choice_lst)[0]
                if judge:
                    item=self.generateItem(k, v)
                    bag.append(item)
            for k, v in self.low_chance2.items():
                judge=random.choices([0, 1], [0.92, 0.08])
                if judge:
                    item=self.generateItem(k, v)
                    bag.append(item)
        return bag            
        

    def sellOne(self):          #出售一件
        bag=self.ptr.getBag()
        num=self.gui.page_now*16+self.gui.flag
        price=int(bag[num].price/2)
        if price==0:
            price=1
        self.eqf.create(46, price)
        self.ptr.deEquip(bag[num])
        stuff=copy.copy(bag[num])
        stuff.count=1       #复制需要卖出的物品然后返回(单个出售)
        self.ptr.carring_adder(-stuff.weight)       #减去物品重量
        self.ptr.getBag()[num].count-=1
        if self.ptr.getBag()[num].count==0:
            self.ptr.getBag().remove(bag[num])
        if self.gui.current_npc==1:
            for i in self.gui.m_bag:
                if stuff.name==i.name:
                    i.count+=1
                    break
            else:
                self.gui.m_bag.append(stuff)
        else:
            for i in self.gui.p_bag:
                if stuff.name==i.name:
                    i.count+=1
                    break
            else:
                self.gui.p_bag.append(stuff)
        self.gui.reset()
        self.gui.quitSetter()
        self.gui.quitSetter()

    def sellAll(self):          #出售全部
        bag=self.ptr.getBag()
        num=self.gui.page_now*16+self.gui.flag
        price=int(bag[num].price/2)
        if price==0:
            price=1
        self.ptr.deEquip(bag[num])
        stuff=copy.copy(bag[num])
        self.eqf.create(46, price*bag[num].count)
        self.ptr.carring_adder(-stuff.weight*stuff.count)       #减去物品重量
        bag[num].count-=stuff.count
        if bag[num].count==0:
            self.ptr.getBag().remove(bag[num])
        if self.gui.current_npc==1:
            for i in self.gui.m_bag:
                if stuff.name==i.name:
                    i.count+=stuff.count
                    break
            else:
                self.gui.m_bag.append(stuff)
        else:
            for i in self.gui.p_bag:
                if stuff.name==i.name:
                    i.count+=stuff.count
                    break
            else:
                self.gui.p_bag.append(stuff)
        self.gui.reset()
        self.gui.quitSetter()
        self.gui.quitSetter()

    
        
    def buyOne(self):       #玩家买入一件商品
        judge=self.gui.current_npc
        bag=self.gui.printItem(judge)
        num=self.gui.page_now*16+self.gui.flag
        price=bag[num].price
        money=self.ptr.getMoney()
        if money-price<0:
            self.inf.prefabTell('$x')       #没钱警告
            num=-1
        else:
            self.eqf.create(46,-price)
            if self.ptr.carring_getter()+bag[num].weight<=self.ptr.weight_getter():
                stuff=copy.copy(bag[num])
                stuff.count=1
                self.ptr.putInBag(stuff)#self.eqf.create(bag[num].ID) if bag[num].label else self.eqf.create(bag[num].ID, prefix=bag[num].prefix)
                self.ptr.carring_adder(bag[num].weight)
            else:
                self.inf.prefabTell('heavy')        #超重警告
                self.gui.reset()
                self.gui.quitSetter()
                return
        if num>=0:
            if bag[num].count>=1:
                bag[num].count-=1
            if bag[num].count==0:
                del bag[num]
        self.gui.reset()
        self.gui.quitSetter()
        self.gui.quitSetter()
        

    def buyAll(self):
        judge=self.gui.current_npc
        bag=self.gui.printItem(judge)
        num=self.gui.page_now*16+self.gui.flag
        price=bag[num].price
        money=self.ptr.getMoney()
        if money-price*bag[num].count<0:
            self.inf.prefabTell('$x')
            num=-1
        else:
            self.eqf.create(46,-price*bag[num].count)
            if self.ptr.carring_getter()+bag[num].weight*bag[num].count<=self.ptr.weight_getter():
                #检测是否超重
                stuff = copy.copy(bag[num])
                self.ptr.putInBag(stuff)
                self.ptr.carring_adder(bag[num].weight*bag[num].count)
            else:
                self.inf.prefabTell('heavy')
                self.gui.reset()
                self.gui.quitSetter()
                return
        if num>=0:
            del bag[num]
        self.gui.reset()
        self.gui.quitSetter()
        self.gui.quitSetter()
        #无论交易是否成功，都会导致退出到loop1

        

        
            
