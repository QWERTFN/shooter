#Создай собственный Шутер!

from pygame import *
from random import randint

def reset(self):
    window.blit(self.image, (self.rect.x, self.rect.y))
win_width = 700
win_height = 500
window = display.set_mode((win_width, win_height))
display.set_caption("Шутер")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
font.init()
font = font.SysFont('Arial', 70)
win = font.render('YOU WIN!', True, (255, 215, 0))
lose = font.render('YOU LOSE!', True, (180, 0, 0))

life = 3  


lost = 0
score = 0



class GameSprite(sprite.Sprite):
   #конструктор класса
   def __init__(self, player_image, player_x, player_y, size_x,size_y, player_speed):
       super().__init__()
       # каждый спрайт должен хранить свойство image - изображение
       self.image = transform.scale(image.load(player_image), (size_x, size_y))
       self.speed = player_speed
       # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
       self.rect = self.image.get_rect()
       self.rect.x = player_x
       self.rect.y = player_y

   def reset(self):
       window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
   def update(self):
       keys = key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 10:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < win_width - 80:
           self.rect.x += self.speed
   def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top,15,20,-15)
        bullets.add(bullet)


class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


           




class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost+=1
    




game = True
finish = False

player = Player('Rocket.png', 5, win_height - 100, 80, 100, 48)
monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png',randint(80, win_width -80), -40, 80, 50,randint(1,5))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(4):
    asteroid = Enemy('asteroid.png',randint(80, win_width -80), -40, 80, 50,randint(1,5))
    asteroids.add(asteroid)

bullets = sprite.Group()
while game:
   for e in event.get():
       if e.type == QUIT:
           game = False
       elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()




 
   if not finish:
        text = font.render('Пропущено: ' +str(lost),1,(255, 255, 255))
        window.blit(text,(10, 50))
        window.blit(background,(0, 0))
        schet = font.render('Счёт:' +str(score),1,(255,255,255))
        player.update()
        monsters.update()
        asteroids.update()
        bullets.update()
        player.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
        collibes = sprite.groupcollide(monsters, bullets, True, True)
        for c in collibes:
            monster = Enemy('ufo.png',randint(80, win_width -80), -40, 80, 50,randint(1,5))
            monsters.add(monster)
            score += 1

        if sprite.spritecollide(player, asteroids, False):
            sprite.spritecollide(player, asteroids, True)
            life = life -1
        if score == -100:
            finish = True
            window.blit(win,(100,90))
        if lost >= 3:
            finish = True
            window.blit(lose,(100,90))
        display.update()
   time.delay(50)

