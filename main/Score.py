"""
Score,py

contains score class that handles scoring and multipliers, etc.
"""

from Colors import *

class Score(object):
    def __init__(self):
        self.score = 0
        self.multiplier = 1
        self.biggestMultiplier = 1
        self.scorePerHit = 1
        self.hits = 0
        self.curStreak = 0
        self.maxStreak = 0
        self.threshold = 20
        self.scoreX = 10
        self.scoreY = 50
        self.dy = 20
        self.scorePos = (self.scoreX, self.scoreY)
        self.misses = 0
        self.maxMult = 1024

    def update(self):
        self.updateHits()
        self.updateScore()
        self.updateStreak()
        self.updateMultiplier()

    def updateHits(self):
        self.hits += 1

    def updateScore(self):
        self.score += self.scorePerHit*self.multiplier

    def updateStreak(self):
        self.curStreak += 1
        if self.curStreak > self.maxStreak:
            self.maxStreak = self.curStreak

    def updateMultiplier(self):
        if self.curStreak % self.threshold == 0:
            if 2*self.multiplier <= self.maxMult:
                self.multiplier *= 2
        if self.multiplier > self.biggestMultiplier:
            self.biggestMultiplier = self.multiplier

    def breakStreak(self):
        self.curStreak = 0
        self.multiplier = 1
        self.updateMisses()

    def updateMisses(self):
        self.misses += 1

    def getTotalHitsAndMisses(self):
        return self.hits + self.misses

    def getPercentHit(self):
        return (self.hits/self.getTotalHitsAndMisses()) * 100

    def getPercentMissed(self):
        return (self.misses/self.getTotalHitsAndMisses()) * 100

    def draw(self, screen, font):
        scoreText = font.render("Score:", True, Colors.white)
        scoreNum = font.render(str(self.score), True, Colors.white)
        multText = font.render("Multiplier:", True, Colors.white)
        multNum = font.render("x%d"%self.multiplier, True, Colors.white)
        for i, text in enumerate([scoreText, scoreNum, multText, multNum]):
            screen.blit(text, (self.scoreX, self.scoreY+i*self.dy))
        
        
