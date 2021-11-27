# Ethians-Alpha-1.1

---

## I. Intros

My own Rougelike game during the first year of university. This project is currently suspended until 2021.11.27, the latest  minor revisions and organization are added.

A Rougelike game, in the hope of implement some of my own ideas. About the origin version of this project, search `Dweller`.

`asset`文件夹中部分图片来源与`Dweller`这个游戏，包括所有monster, 部分items, 其余都是个人使用PS进行的创作：

* 2019年一月开始断断续续写这个项目，知道2019年8月29日写完
* 在上完数据结构与算法后，对这个项目进行了一些优化，但是很有限，这个项目的代码结构太乱，类间的调用关系不清晰，可维护性很差，所以我称之为“练手项目”
* 对于这个游戏，以后有时间可能进行重构（甚至重写），里面太多的实现在我现在看来都是垃圾。
* 个人不想再使用Pygame做这个项目，Pygame没有很好的交互系统，只能自己写交互，有点难受。如果需要重构，预计使用C#实现，可以省去GUI、动画、交互以及并行程序的开发

---

## II. Attributes

### 2.1 随机生成的地图

- 地牢随机生成，并且附带地图编辑器，可以自定义地图。
- 陷阱，宝箱，怪物，地形丰富
- FOV shadow casting 迷雾算法，小地图显示

![](README/1.png)

### 2.2 装备\背包系统

- 装备等级与词缀加成
- 附魔升级以及随机名字 + 随机属性
- 装备掉落系统
- 人物属性、抗性系统，游戏信息记录
- 三个职业：狂战士，游侠，巫师
- 人物等级系统，商店交易系统，可与NPC进行对话

![](README/3.png)

![](README/2.png)

### 2.3 主菜单与彩蛋

- 游戏编写者的彩蛋世界，内有编写者的家人
- 英灵殿：记录死亡信息，记录通关信息
- 支持游戏保存
- 支持进行键盘设置

![](README/5.png)

![](README/4.png)

---

## III. Play

​		应该只依赖于Pygame库（Pygame 1.9.6），Windows / Ubuntu均可

```
python ./main.py
```

