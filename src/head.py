#-*-coding:utf-8-*-
"""主控系统类，用于统筹游戏内循环参数等设置"""

class HQ:
    def __init__(self):
        __slots__=('__loop_ctrl','__npc_state','__judge','state')
        self.__loop_ctrl=0

    def set_loop(self, value):
        if value<0 or value>12: raise ValueError('Valid value:1~12')
        self.__loop_ctrl=value

    def get_loop(self):
        return self.__loop_ctrl
    
