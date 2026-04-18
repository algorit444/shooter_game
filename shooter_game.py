from pygame import *
from random import randint
# подгружаем отдельно функции для работы со шрифтом
font.init()
font1 = font.Font(None, 80)
win = font1.render('YOU WIN!', True, (255, 255, 255))
lose = font1.render('YOU LOSE!', True, (180, 0, 0))


font2 = font.SysFont("Arial", 30)


#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')


# нам нужны такие картинки:
img_back = "galaxy.jpg" # фон игры
 
img_bullet = "bullet.png" # пуля
img_hero = "rocket.png" # герой
img_enemy = "ufo.png" # враг
 
score = 0 # сбито кораблей
goal = 25 # столько кораблей нужно сбить для победы
lost = 0 # пропущено кораблей
max_lost = 10 # проиграли, если пропустили столько
hearts = 3
 
# класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
  # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)


        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed


        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
 
  # метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# класс главного игрока
class Player(GameSprite):
    # метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed
  # метод "выстрел" (используем место игрока, чтобы создать там пулю)
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)


# класс спрайта-врага  
class Enemy(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        global lost
        # исчезает, если дойдет до края экрана
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1
 
# класс спрайта-пули  
class Bullet(GameSprite):
    # движение врага
    def update(self):
        self.rect.y += self.speed
        # исчезает, если дойдет до края экрана
        if self.rect.y < 0:
            self.kill()
class SurfaceGame(GameSprite):
    def __init__(self, color1, color2, color3, x, y, sx, sy):
        sprite.Sprite.__init__(self)
        self.surface = Surface((sx,sy))
        self.surface.fill((color1,color2,color3))
        self.rect = self.surface.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        window.blit(self.surface, (self.rect.x, self.rect.y))


heartsg = sprite.Group()
for i in range(1,4):
    heartspr = SurfaceGame(255, 0, 0, 25*i-10, 85, 15, 15)
    heartsg.add(heartspr)

# Создаем окошко
win_width = 700
win_height = 500
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
 
# создаем спрайты
ship = Player(img_hero, 5, win_height - 100, 80, 100, 5)
 
# создание группы спрайтов-врагов
monsters = sprite.Group()
for i in range(1, 6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 2))
    monsters.add(monster)
 
asteroids = sprite.Group()
asteroids.add(Enemy("asteroid.png", randint(80, win_width - 80), -40, 80, 50, randint(1, 2)))

bullets = sprite.Group()
 
# переменная "игра закончилась": как только там True, в основном цикле перестают работать спрайты
finish = False
# Основной цикл игры:
run = True # флаг сбрасывается кнопкой закрытия окна
tickcollide = 180
timer = time.Clock()
tickreload = 0
bulletsamount = 5
while run:
    # событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        # событие нажатия на пробел - спрайт стреляет
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if bulletsamount!=0:
                    bulletsamount-=1
                    if bulletsamount==0:
                        tickreload=180
                    fire_sound.play()
                    ship.fire()
 
  # сама игра: действия спрайтов, проверка правил игры, перерисовка
    if not finish:
        # обновляем фон
        window.blit(background,(0,0))


        # пишем текст на экране
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))


        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))


        # производим движения спрайтов
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()

        for i in range(3):
            if not hearts-1 < i:
                heartsg.sprites()[i].update()


        # обновляем их в новом местоположении при каждой итерации цикла
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)
 
        # проверка столкновения пули и монстров (и монстр, и пуля при касании исчезают)
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            # этот цикл повторится столько раз, сколько монстров подбито
            score = score + 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            monsters.add(monster)


        # возможный проигрыш: пропустили слишком много или герой столкнулся с врагом
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            if tickcollide==0:
                hearts-=1
                tickcollide=180
                print(hearts)
        
        if lost >= max_lost or hearts<1:
            finish = True
            window.blit(lose, (200, 200))


        # проверка выигрыша: сколько очков набрали?
        if score >= goal:
            finish = True
            window.blit(win, (200, 200))

        if tickcollide!=0:
            tickcollide-=1
        if tickreload!=0:
            tickreload-=1
            if tickreload==0:
                bulletsamount=5
        display.update()
    # цикл срабатывает каждую 0.05 секунд
    timer.tick(60)
