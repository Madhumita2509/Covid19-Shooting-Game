#import pygame
import pygame
import random
import math
from pygame import mixer
#initialize the pygame
pygame.init()
#create screen
screen=pygame.display.set_mode((800,600))
#background
background=pygame.image.load("background.jpg")

#title and icon
pygame.display.set_caption("COVID19")
icon=pygame.image.load("virus.png")
pygame.display.set_icon(icon)
#enemy
enemyImg=[]
enemyX=[]
enemyY=[]
enemyX_change=[]
enemyY_change=[]
num_of_enemies=6
for i in range(num_of_enemies):
 enemyImg.append(pygame.image.load("covid.png"))
 enemyX.append(random.randint(0,735))
 enemyY.append(random.randint(50,150))
 enemyX_change.append(0.2)
 enemyY_change.append(40)
#player
playerImg=pygame.image.load("patient.png")
playerX=370
playerY=520
playerX_change=0
#bullet
#ready means it wont appear on screen
bulletImg=pygame.image.load("spray.png")
bulletX=0
bulletY=520
bulletX_change=0
bulletY_change=1.8
bullet_state="ready"
#background music
mixer.music.load("background.wav")
mixer.music.play(-1)

#score
score_value=0
font=pygame.font.Font("freesansbold.ttf",32)
textX=10
textY=10
#game game_over_text
over_font=pygame.font.Font("freesansbold.ttf",80)
def game_over_text():
    over_text=over_font.render("GAME OVER",True,(255,0,0))
    screen.blit(over_text,(200,250))
def show_score(x,y):
    score=font.render("Score:"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def player(x,y):
 screen.blit(playerImg,(playerX,playerY))
def enemy(x,y,i):
 screen.blit(enemyImg[i],(enemyX[i],enemyY[i]))

def fire_bullet(x,y):
    global bullet_state
    bullet_state="fire"
    screen.blit(bulletImg,(x,y))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance=math.sqrt((math.pow(enemyX-bulletX,2))+(math.pow(enemyY-bulletY,2)))
    if distance<27:
        return True
    else:
        return False

#game loop
running=True
while running:
 screen.fill((0,0,0))

 #background
 screen.blit(background,(0,0))
 for event in pygame.event.get():
  if event.type==pygame.QUIT:
   running=false
  if event.type==pygame.KEYDOWN:
      if event.key==pygame.K_LEFT:
          playerX_change=-0.7
      if event.key==pygame.K_RIGHT:
          playerX_change=0.7
      if event.key==pygame.K_SPACE:
          if bullet_state is "ready":
              mixer.music.load("spray.wav")
              mixer.music.play()
              bulletX=playerX
              fire_bullet(bulletX,bulletY)

  if event.type==pygame.KEYUP:
      if event.key==pygame.K_LEFT or event.key==pygame.K_RIGHT:
          playerX_change=0

 playerX+=playerX_change
 if playerX<=0:
     playerX=0
 elif playerX>=736:
     playerX=736

 for i in range(num_of_enemies):
     #game over
     if enemyY[i]>400:
         for j in range(num_of_enemies):
             enemyY[j]=2000
         game_over_text()
         break
     enemyX[i]+=enemyX_change[i]
     if enemyX[i]<=0:
        enemyX_change[i]=0.5
        enemyY[i]+=enemyY_change[i]
     elif enemyX[i]>=736:
        enemyX_change[i]=-0.5
        enemyY[i]+=enemyY_change[i]

     #isCollision
     collision=isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
     if collision:
      mixer.music.load("laser.wav")
      mixer.music.play()
      bulletY=520
      bullet_state="ready"
      score_value+=1
      enemyX[i]=random.randint(0,735)
      enemyY[i]=random.randint(50,150)
     enemy(enemyX[i],enemyY[i],i)

 if bulletY<=0:
     bulletY=520
     bullet_state="ready"

 if bullet_state is "fire":
     fire_bullet(bulletX,bulletY)
     bulletY-=bulletY_change



 player(playerX,playerY)
 show_score(textX,textY)
 pygame.display.update()
