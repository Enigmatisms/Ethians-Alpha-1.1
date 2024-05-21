import os
#!/usr/bin/env python3
#-*-coding:utf-8-*-

import random, pygame, time

__author__='SEeHz3'
__date__='2019.8.28'
__note__="Alpha 1.0 complete time: Aug.28.2019"

class Face:
    def __init__(self, screen):
        path=random.choice([0, 1])
        if path: self.bk1 = pygame.image.load(os.path.join("asset", "ethians1.jpg")).convert()
        else: self.bk1=pygame.image.load(os.path.join("asset", "ethians2.jpg")).convert()
        self.author=pygame.image.load(os.path.join("asset", "author.png")).convert()
        self.screen=screen
        self.surface = pygame.Surface((1200, 650))
        self.surface.fill((0, 0, 0))
        self.step=0
        self.count=0
        self._mult=1
        self.alpha=255

    def draw(self):
        self.surface.set_alpha(self.alpha)
        if self.alpha==255:
            self._mult=self._mult*(-1)
            self.step+=1
        elif self.alpha==0:
            self._mult = self._mult * (-1)
            time.sleep(1)
        if self.step==1:
            self.screen.blit(self.author, (0, 0))
        elif self.step==2:
            self.screen.blit(self.bk1, (0, 0))
        self.screen.blit(self.surface, (0, 0))
        self.alpha+=self._mult

