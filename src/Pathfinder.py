#!/usr/bin/env python3
#-*-coding:utf-8-*-
#Pathfinder
import sys
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x, self.y=x, y
        self.cost=sys.maxsize
        self.parent=None

    def reset(self):
        self.cost=sys.maxsize
        self.parent=None

class Astar:
    def __init__(self, func_lst=None):
        self.__found=False
        self.open_set=[]
        self.close_set=[]
        self.d2=np.sqrt(2)
        self.start=Point(0, 0)
        self.goal=Point(0, 0)
        self.func_lst=[func_lst]
        self.func_lst2=[]
        self.step=0
        self.path=[]
    #==================代价计算方法======================
    def heuristic(self, node):        #代价启发函数(到终点)
        dy=abs(node.y-self.goal.y)
        dx=abs(node.x-self.goal.x)
        return (dy+dx)+(self.d2-2)*min(dy, dx)

    def g(self, node):        #g(n)函数，到起点的代价函数
        dy=abs(node.y-self.start.y)
        dx=abs(node.x-self.start.x)
        return (dy+dx)+(self.d2-1)*min(dy, dx)+self.extra_cost(node)

    def extra_cost(self, node):
        #TBS: 有一些地图块有额外的cost,比如钉板陷阱，如果有别的
        #略微有一些远的路径，怪物不会选择去踩陷阱让自己减血
        length=len(self.func_lst2)
        x, y=(node.x, node.y)
        cost=0
        for i in range(length):
            cost=self.func_lst2[i].getCost(x, y)
            if cost: return cost
        if not cost:
            return 0
        
    def totalCost(self, node):      #总代价函数
        return self.g(node)+2*self.heuristic(node)
    #==================点的判断方法======================
    def isValidPoint(self, x, y):           #判断该点是不是可用点，比如必须在边界内
        length=len(self.func_lst)
        if (x, y) == (self.start.x, self.start.y):
            return True
        else:
            for i in range(length):
                if self.func_lst[ i ].noWalk(x, y):
                    return False
            if x<0 or y<0 or x>=64 or y>=42:
                return False
            else:
                return True
    
    def isInCloseSet(self, p):      #在闭集内
        return self.isInPointList(p, self.close_set)

    def isInOpenSet(self, p):       #在开集内
        return self.isInPointList(p, self.open_set)

    def isEnd(self, p):         #是终点，开始返回路径
        if (p.x, p.y) == (self.goal.x, self.goal.y):
            return True
        else:
            return False

    def isStart(self, p):       #是起点，路径返回结束
        if (p.x, p.y) == (self.start.x, self.start.y):
            return True
        else:
            return False

    @staticmethod
    def isInPointList(p, point_list):      #辅助方法：用在前几个函数内
        for point in point_list:
            if (p.x, p.y) == (point.x, point.y):
                return True
        return False
    #=========================核心逻辑=======================
    '''=========================Core========================'''
    def selectPointInOpen(self):                #从open_set中寻找路径成本最小的节点
        if self.open_set:
            index = 0
            length=len(self.open_set)
            min_cost=sys.maxsize
            for i in range(length):
                cost=self.open_set[ i ].cost
                if cost<min_cost:
                    min_cost=cost
                    index=i
            return self.open_set[ index ]
        else:
            return None

    def processPoint(self, x, y, parent):       #不能进行迭代，迭代会栈溢出
        if self.isValidPoint(x, y):     #当说可用点的时候，就说明这个点可以被processed
            p=Point(x, y)
            p.parent=parent         #设置该点的父点是parent
            if self.isEnd(p):       #终点开始trace_back，把父点加入self.path内
                self.path.append(self.goal)
                self.trace_back(parent)
            else:
                if not self.isInCloseSet(p):        #不在close_set内
                    if self.isInOpenSet(p):          #在open_set的才会进行其周围的处理
                        pass
                    else:           #不在open_set内的就是将其加入open_set, 然后上面都不做，等待path_find循环进行最优选
                        p.cost=self.totalCost(p)
                        self.open_set.append(p)

    def pathfind(self, tuple1, tuple2):
        self.setStartGoal(tuple1, tuple2)
        self.processPoint(self.start.x, self.start.y, self.start)
        while not self.__found:         #当路径搜索没有结束时，持续搜索路径
            optimal=self.selectPointInOpen()        #每次都从open_set中选取一个optimal点
            if optimal:
                x, y, p = optimal.x, optimal.y, optimal       #将optimal点从open_set中删除，并处理其附近的点
                self.open2close(optimal)            #open_set中optimal点转到close_set中
                self.doAround(x, y, p)          #在optimal点周围搜索
                self.step+=1
                if self.step>24:
                    self.reset()
                    break
            else:
                break
        if self.__found:
            temx, temy=self.path[-2].x, self.path[-2].y
            self.reset()
            return temx, temy
        else:
            self.reset()
            return tuple1

    def mapJudge(self, tuple1, tuple2):
        self.setStartGoal(tuple1, tuple2)
        self.processPoint(self.start.x, self.start.y, self.start)
        while not self.__found:  # 当路径搜索没有结束时，持续搜索路径
            optimal = self.selectPointInOpen()  # 每次都从open_set中选取一个optimal点
            if optimal:
                x, y, p = optimal.x, optimal.y, optimal  # 将optimal点从open_set中删除，并处理其附近的点
                self.open2close(optimal)  # open_set中optimal点转到close_set中
                self.doAround(x, y, p)  # 在optimal点周围搜索
            else:
                break
        if self.__found:
            self.reset()
            return True
        else:
            self.reset()
            return False

    def trace_back(self, par):      #迭代法返回路径
        if not self.isStart(par):           #路径返回时是追踪parent点，如果找到了起点，则搜索结束
            self.path.append(par)
            self.trace_back(par.parent)
        else:
            self.path.append(par)
            self.__found=True

    def doAround(self, x, y, par):          #点(x, y)周围的点的操作
        self.processPoint(x-1, y-1, par)
        self.processPoint(x-1, y, par)
        self.processPoint(x-1, y+1, par)
        self.processPoint(x, y-1, par)
        self.processPoint(x, y+1, par)
        self.processPoint(x+1, y-1, par)
        self.processPoint(x+1, y, par)
        self.processPoint(x+1, y+1, par)

    #=========================其他方法=======================
    '''=========================Others========================'''
    def open2close(self, p):            #将open_set中的元素加入close_set
        for point in self.open_set:
            if (p.x, p.y) == (point.x, point.y):
                self.open_set.remove(point)
                self.close_set.append(p)
                break
    
    def setStartGoal(self, tuple1, tuple2):       #tuple1  tuple2分别是起点和终点
        self.start.x, self.start.y=tuple1
        self.goal.x, self.goal.y=tuple2
        self.start.reset()
        self.goal.reset()

    def reset(self):
        self.__found=False
        self.path.clear()
        self.open_set.clear()
        self.close_set.clear()
        self.step=0

if __name__=='__main__':
    print('The PathFinder Module is based on A* (Modified Algorithm), with average 10 times of\n'+\
          'path searching times (maximum step 32) down to 0.02s.\n'+'More information: Seek in Algorithm/Pathfinder.py or Astar Modified.py')
