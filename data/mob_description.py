import json

dct={}


dct[0]=["The green, smelly, jelly like foul creature can crawl slowly to you,",
        "Get you absorbed in its mud-made body and digest you,",
        "It is indeed slow, but it doesn\t' belie the truth that it is dangerous."]
dct[2]=["There is more water inside their body compared with green slime,",
        "They are not smelly, nor are they lovely, by no means are they friendly,",
        "Lighter are they, they can move silently towards you and get you killed."]
dct[4]=["It is commonly believed that these creatures are made of magma,",
        "Normally, they dwell on the volcanos and they are rarely seen,",
        "Definitely, Lich King and its zealots have corrupted their minds."]
dct[6]=["Watch out, peacemaker! Watch out for the moving sand!",
        "It is not quicksand that I warn you of, it is another foul creature,",
        "Yellow like sand, thick like a Ooze, smelly as a green slime..."]
dct[8]=["The underground environment has changed them completely...",
        "Their eyes decayed, while other senses were enhanced...",
        "They are the mutants of the normal huge rat, yes, Lich King's work."]
dct[10]=["Ah, those are huge rats, normally they are harmless and afraid of you,",
         "Do not tease them, however, they can be agitated to be aggressive.",
         "Leave them alone, as they just want to live in the wild peacefully."]
dct[12]=["Squeaking, creaking, these are the skeletons being not at peace,",
         "Wandering, seeking, they are jealous of life, because they are dead.",
         "Killing, slaughtering, all they want is to make you a member of them."]
dct[14]=["Bolisian's Caravan rested in an obsolete castle, when it was at dusk,",
         "But NONE of the members woke up ever again, with blood drained,",
         "What a coincidence that human blood is vampire bats' favorite."]
dct[16]=["Most notorious race of creature, they are born in reek,",
         "Killing, chopping, biting, buring! No one can be their friend.",
         "Yet they can be slaves of the Lich King, good heaven!"]
dct[18]=["Eight eyes, glistening in the dark, venomteeth, grinding in silence,",
         "They seldom make cobweb, for they are fast and strong enough,",
         "Just one sting, dead are small creatures, dizzy will men be."]
dct[20]=["Floating, giant, tyrant eyeball stares, glares at you..., it is said... ",
         "to have dropped out of the skull of King Loccoso when he was beheaded,",
         "Full of malice, filled with hatred, brimmed with sorrow, immersed in vengeance."]
dct[22]=["Ah, necromancers are never mild creatures who wander in the daylight,",
         "Obsessed by corpses, these mortal men were dragged into the abyss...",
         "Servants as they are, they serve the Lich King with their drained blood."]
dct[24]=["Beneath the hood there is no flesh, inside the coat nothing hides,",
         "Chaos, the very sorcery that they like, in which lies magic and might,",
         "Never do they flee or overwhelmed by fright, for their dark faith is like fire."]
dct[26]=["Poor souls, should be tortured before in peace they truly rest,",
         "Summoned, to kill for the Lich King and necromancers, who aroused...",
         "their envy for those living creatures, longing to make everything dead."]
dct[28]=["Toxic! Shame! True fighters use no poison in a combat!",
         "Hypocrite! Foe! Seduced by false creed and serve the evil masters!",
         "Martyr! Sacrifice! Your evil cause shall never be vindicated and belied."]
dct[30]=["Oh they are the foulest creatures people know through their lives,",
         "It might be that those creatures stink people to death, those ditch dwellers...",
         "Be aware, stink as they do, they are mighty with fast healing skills..."]
dct[32]=["They aren't normal goblins... If must ask ask, I would say they are...",
         "Villains, mobs in inside of the Goblin Clan. They are born in the dark...",
         "Underground in the cave and dungeon and have feasts on people's heart."]
dct[34]=["Sly. These are the fastest squads of the Goblin Clan with bow in hand.",
         "They are usually small, called the dwarves of goblins yet move fast as no one can.",
         "Watch out in the dungeon, the arrow has mercy in this malicious land."]
dct[36]=["Wizardry is vital to all of the Clans on the Continent, yet notorious are some.",
         "Shamans of goblin are the hands of Goblin Clan, preaching evil dogma...",
         "Providing cure to all the foul creatures, belying themselves as salvation..."]
dct[38]=["You see eyeballs glow like fire. You see hollowed body with no flesh.",
         "You see a Wraith lingering in the shadow. Things they stood for turned to ash.",
         "They were once fighters against those devils. Yet their stories are full of misery."]
dct[40]=["The origination of Vampire: A sorcerer was obessed with Draining sorcery,",
         "He studied vampire bats and dwelled in the Vampire Book for years. Gradually,",
         "The sorcery consumed him, changed his appearance, made him a vampire."]
dct[42]=["Mutant wolves, cultivated by goblins, called Worgs are not only for riding.",
         "Unlike horses, they can be powerful weapons with fierce teeth and jaw,",
         "Extremely fast and mighty yet vulnerable to wizardry, they are still formidable."]
dct[44]=["Leader of Goblins, with golden crown and red silk cloak with golden lace.",
         "He commands the Goblin Clan and Worgs, only answer to the call of Lich King.",
         "Almost he is a master of all kind of things... melee and wizardry and necromancy..."]
dct[46]=["Pandora the Box carries all the malice and horror down to the midgard.",
         "Knowing that people are greedy for treasure and scramble for wealth...",
         "It hides its all the havoc inside of its body which resembles treasure box."]
dct[48]=["Armor rack is put spells on, which is vivified and brought to life.",
         "This kind of sorcery is the favorite of the Lich King, though corrupted as usual...",
         "The glaring light inside of the helmet blazes like flames, hits you off guard."]

print(dct)
with open('mob_desc.json', 'w') as w:
    json.dump(dct, w)

with open('mob_desc.json', 'r') as r:
    ddd=json.load(r)
for key in ddd.keys():
    print(type(key))



