#!/usr/bin/env python3
#-*-coding:utf-8-*-

import json,pickle,time

class Saveit:
    def __init__(self):
        self.deathJudge=False
        self.eqf, self.inf, self.gui=None, None, None

    def saveGamer(self, gamer):         #存档
        if self.deathJudge:
            self.clrRecord()
        else:
            gamer.eqf, gamer.inf,  gamer.gui=None, None, None   #消除所有的surface
            with open(r'data\playerData.pkl', 'wb') as saver:
                pickle.dump(gamer, saver)
            gamer.eqf, gamer.inf, gamer.gui=self.eqf, self.inf, self.gui
            self.inf.prefabTell('saved')


    def loadGamer(self):                #读取存档
        try:
            with open(r'data\playerData.pkl', 'rb') as loader:
                stuff = pickle.load(loader)
        except FileNotFoundError:
            return None
        else:
            if stuff:
                self.inf.prefabTell('loaded')
                stuff.eqf, stuff.inf, stuff.gui = self.eqf, self.inf, self.gui
                return stuff
            else:
                return None

    def clrRecord(self):
        self.deathJudge=True
        with open(r'data\playerData.pkl', 'wb') as wri:
            pickle.dump(None, wri)

    @staticmethod
    def saveDeath(desc):          #保存死亡信息
        key=[time.asctime()]
        key.extend(desc)
        try:
            with open(r'data\death.json', 'r') as read:
                dct=json.load(read)
        except FileNotFoundError:
            with open(r'data\death.json', 'w') as first:
                json.dump([key], first)
        else:
            dct.append(key)
            with open(r'data\death.json', 'w') as wri:
                json.dump(dct, wri)

    @staticmethod
    def loadDeath():            #加载死亡信息
        try:
            with open(r'data\death.json', 'r') as read:
                dct = json.load(read)
                dct = dct[:len(dct) - 40:-1]        #反排列并且限定长度取值
        except FileNotFoundError:
            with open(r'data\death.json', 'w'):
                return None
        else:
            return dct

    @staticmethod
    def saveHero(desc):          #TBS
        key = [time.asctime()]
        key.extend(desc)
        try:
            with open(r'data\heroes.json', 'r') as read:
                dct = json.load(read)
        except FileNotFoundError:
            with open(r'data\heroes.json', 'w') as first:
                json.dump([key], first)
        else:
            dct.append(key)
            with open(r'data\heroes.json', 'w') as wri:
                json.dump(dct, wri)

    @staticmethod
    def loadHero():         #TBS
        try:
            with open(r'data\heroes.json', 'r') as read:
                dct = json.load(read)
                dct=dct[:len(dct)-34:-1]        #反排列并且限定长度取值
        except FileNotFoundError:
            with open(r'data\heroes.json', 'w'):
                return None
        else:
            return dct



