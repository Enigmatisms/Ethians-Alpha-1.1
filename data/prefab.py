import json

dct=dict()
#环境
dct['stair+']="Now you see a dark stair leading upwards."       #
dct['stair-']=dct['stair+'].replace('up', 'down')           #
dct['out']="Mendax canyon, the fresh air fills in your lungs."          #
dct['block']="You can not reach the blocked place."         #???
dct['trap']="You accidentally walked into a trap and fell down."        #
dct['spike']="You are stung by the spikes trap."            #
dct['summon']="There are foul creatures summoned by you."           #
dct['tp']="Once again you are lost in the dungeon."             #
dct['box']="Now beneath you is a treasure box."         #
dct['box-']="You open up the box, and it is empty."             #
dct['box0']="Now beneath you is an empty treasure box."         #
dct['boxg']="Now beneath you is a box of gold coins."           #
dct['door+']="You opened the closed door."              #
dct['door-']="You closed the open door."                #
dct['doorx']="With a terrible noise, the door became scraps."   #
dct['door#']="You unlock the door with a key."              #
dct['door!']="You have no keys to open this lock."              #
dct['atdoor']="You are standing in the door."               #
dct['atdoorx']="You are standing in the broken door."               #
dct['gate+']="You raise the gate."              #
dct['gate-']="You shut down the gate."              #
dct['atgate']="You are standing in the gate."           #
dct['trap-']="You eliminate the trap. Exp +5"              #
dct['boxtrap']="You have triggered a spike trap."           #
dct['bless']="Blessed by Lord Enigma I, you feel energetic."
dct['bless-']="You are out of health to make a pray to the Lord."
dct['door&']="The door is locked, you need a key."
dct['&door']="You locked up the door with a lock."
dct['door&-']="You opened the locked door with a key."
#自身debug
dct['poison']="You have been poisoned by "      #
dct['fire']="There are flames upon your body."          #
dct['blind']="The dungeon looks dimmer to you."         #
dct['frozen']="The coldness is like daggers scraping your bones."           #
dct['break']="Your armor is shattered by "          #
dct['bleed']="You throw at the potion you drink for the dark magic."           #
dct['dying']="You have bled too much. Find some cure or you will die."
#对怪物的攻击
dct['mfire']="You set fire on "     #
dct['mpoison']="You put poison on "         #
dct['mdrain']="You have drain some blood from "         #
dct['mcharm']="is charmed by you."          #
dct['mfrozen']="is frozen by ice sorcery."          #
dct['mbreak']="You break the armor of "         """!!!!!!!!!!!!!!!!"""          #!!!!!!!!!!!
dct['mcurse']="is cursed by you."           #
dct['mfright']="is scared away by you."         #
dct['mback']="You knock back the attack of "
dct['mdizzy']="feels dizzy right now."              #
dct['mchao']="You put chaotic spells on "       #
dct['targetx']="The target is blocked, you can not aim at it."
#工具
dct['tps']="You have used the sorcery of teleportation."        #TBS???
dct['map']="Darkness is blinding you no more."          #
dct['summonWand']="You summoned yourself some friendly monsters."       #
dct['bkscroll']="You return to the deepest the level you ever reached."         #
dct['no']="Nothing seems to happen."            #???
dct['enchant']="Beams of light flow inside the scroll..."           #
dct['decay']="The gleaming lights seem to fade..."              #
dct['lvl6x']="Maximum Level: 6 reached."
dct['lvl0x']="Minimum Level: 0 reached."
dct['lvl6-']="Level 6 item shall not decay."
dct['cure']="You cure yourself with potion. HP +"               #
dct['poison-']="You freed yourself from the grasp of poison."           #
dct['atk+']="You swing the weapon with more might even. Attack +"       #
dct['atk-']="The weapon in hand seems heavier to you. Attack -"         #
dct['defc+']="You hardened your skin and armor. Defence +"          #
dct['defc-']="You are more vulnerable to attack. Defence -"         #
dct['mgc+']="Your faith has been tested and strengthened. Magic +"          #
dct['mgc-']="Your spiritual power begins to shake. Magic -"         #
dct['spd+']="You feel that your have silk steps. Speed +"           #
dct['spd-']="It seems there was lump of steel in your boots. Speed -"           #
dct['cureWandm']="is cured by you."             #
dct['cureWand']="Your wounds start to heal and you cure yourself."          #
dct['knowledge']="You have used the Scroll of Knowledge."
#怪物交互
dct['stare']="is staring at you."
dct['mcure']="cures itself."            #
dct['mtp']="is frightened and teleported itself."       #
dct['wake']="is woken up by you."
dct['drain']="Your blood has been drained."            #
dct['dodge']="You have dodged the attack from "
dct['miss']="misses hitting you when attacking."
dct['missmob']="Your attack misses hitting "            #
dct['swap']="You switch the position with "         #
dct['shaman']="Shaman's healing bell is ringing..."
dct['slime']="divides itself into two..."
dct['msummon']="Devils are summoned by "
#与物品交互:TBS
dct['stand']="Now you are standing on some item..."         #
dct['pickup']="You pick up "            #
dct['ovrw']="Outweighted! Need more space in the bag."      #
dct['throw']="You throw away "          #
dct['throwx']="You can\'t drop multiple weighed items at once."             #
dct['occupied']="There is already something on the floor."
dct['eq']="You equip yourself with "            #
dct['deq']="You take down "             #
dct['berserker']="Berserker can not use "
dct['archer']="Archer can not use "
dct['sorcerer']="Sorcerer can not use "
dct['potionx']="No potion in take in 20 steps for potion sickness."
#模式信息触发：
dct['cursor']="You open up infomation cursor, select a target."         #
dct['attack']="You are using attacking mode, select a target."          #
dct['sm']="Satellite map activated."
dct['dsm']="Satellite map de-activated."
dct['wand0']="You have no wand equipped."
dct['b0']="You have no book or long range weapon equipped."
dct['a0']="You have no arrow left or equipped."
dct['saved']="The game record is saved."
dct['loaded']="The game record is retrieved."
dct['$x']="You don't have that much money."
dct['heavy']="You can not take that many things with you."
dct['new!']="You found something new around you!"




print(dct)
with open('prefabs.json', 'w') as w:
    json.dump(dct, w)

with open('prefabs.json', 'r') as r:
    ddd=json.load(r)



