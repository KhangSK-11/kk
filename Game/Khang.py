import pygame
from random import randint, uniform

class Spaceship(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load('spaceship.png').convert_alpha()
        self.rect = self.image.get_rect(topleft=(370, 480))
        self.Ship_direct = pygame.math.Vector2(0, 0)
        self.spd = 500
        self.can_shoot = True
        self.bullet_shoot_time = 0
        self.cooldown_duration = 100

    def bullet_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.bullet_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def giuvitri(self):
        # Giữ cho phi thuyền di chuyển trong một khoảng không bị out ra khung hình
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= 736:
            self.rect.right = 736
        if self.rect.top <= 50:
            self.rect.top = 50
        if self.rect.bottom >= 536:
            self.rect.bottom = 536

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.Ship_direct.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.Ship_direct.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.Ship_direct = self.Ship_direct.normalize() if self.Ship_direct else self.Ship_direct
        self.rect.center += self.Ship_direct * self.spd * dt
        if keys[pygame.K_SPACE] and self.can_shoot:
            Bullet(self.rect.midtop, (all_sprites, Bullet_sprites))  # Tạo đạn
            self.can_shoot = False
            self.bullet_shoot_time = pygame.time.get_ticks()
            Lasersound.play()
        self.bullet_timer()
        self.giuvitri()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.original_surf = pygame.image.load('bullet.png').convert_alpha()
        self.image = self.original_surf
        self.rect = self.image.get_rect(midbottom=pos)
        self.spd = 400

    def update(self, dt):
        self.rect.y -= self.spd * dt  # Di chuyển laser lên trên
        if self.rect.bottom < 0:  # Xóa laser khi ra khỏi màn hình
            self.kill()


class Trash(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.originall_surf = surf
        self.image = self.originall_surf
        self.rect = self.image.get_rect(center=pos)
        self.spd = 300 + score // 5
        self.start_time = pygame.time.get_ticks()
        self.life_time = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.rotation = 0
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, dt):
        self.rect.center += self.direction * self.spd * dt
        if pygame.time.get_ticks() - self.start_time >= self.life_time:
            self.kill()
        self.rotation += 40 * dt
        self.image = pygame.transform.rotozoom(self.originall_surf, self.rotation, 1.5)
        self.rect = self.image.get_rect(center=self.rect.center)


class Hieu_ung_no(pygame.sprite.Sprite):
    def __init__(self, frame, pos, groups):
        super().__init__(groups)
        self.frame = frame
        self.current_frame = 0
        self.image = self.frame[self.current_frame]
        self.rect = self.image.get_rect(center=pos)

    def update(self, dt):
        self.current_frame += 20 * dt
        if self.current_frame < len(self.frame):
            self.image = self.frame[int(self.current_frame)]
        else:
            self.kill()


def vacham():
    global game_over, score
    # Va chạm giữa spaceship và trash
    Tainan = pygame.sprite.spritecollide(spaceship, Trash_sprites, True, pygame.sprite.collide_mask)
    if Tainan:  # Nếu va chạm, kết thúc trò chơi
            game_over = True
            explosionSound.play()

    # Va chạm giữa bullet và trash
    for bullet in Bullet_sprites:
        rac_va_cham = pygame.sprite.spritecollide(bullet, Trash_sprites, True)
        if rac_va_cham:
            bullet.kill()
            Hieu_ung_no(No_frame, bullet.rect.midtop, all_sprites)
            explosionSound.play()
            score += 1


def Score():
    Text_sur = font.render(f"SCORE: {score}", True, "White")
    Text_s = Text_sur.get_rect(topleft=(10, 10))
    screen.blit(Text_sur, Text_s)


def reset_game():
    global score, game_over, spaceship
    # Reset các đối tượng và biến
    all_sprites.empty()
    Trash_sprites.empty()
    Bullet_sprites.empty()

    # Khởi tạo lại các đối tượng
    spaceship = Spaceship(all_sprites)  # Tạo đối tượng spaceship mới
    score = 0
    game_over = False


# Khởi tạo game
pygame.init()

Screen_Width = 800
Screen_Height = 600
screen = pygame.display.set_mode((Screen_Width, Screen_Height))
background = pygame.image.load('background.png').convert_alpha()
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)
explosionSound = pygame.mixer.Sound("explosion.wav")
Lasersound = pygame.mixer.Sound("laser.wav")

# Tiêu đề và biểu tượng game
pygame.display.set_caption("Xử lý rác không gian")
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

score = 0
game_over = False
font = pygame.font.Font("04B_30__.TTF", 25)

# Game over text
over_font = pygame.font.Font('Freesansbold.ttf', 64)
over = over_font.render('GAME OVER', True, (255, 255, 255))

# Chơi lại
replay = pygame.font.Font('Freesansbold.ttf', 32)
lai = replay.render('If you want to play again press space bar', True, (255, 255, 255))

rac = pygame.image.load('rac.png')
apple = pygame.image.load('apple.png')
fishbone = pygame.image.load('fishbone.png')
No_frame = [pygame.image.load(f"{i}.png").convert_alpha() for i in range(21)]

all_sprites = pygame.sprite.Group()
spaceship = Spaceship(all_sprites)
Trash_sprites = pygame.sprite.Group()
Bullet_sprites = pygame.sprite.Group()

# Custom events -> Meteor event
Trash_event = pygame.event.custom_type()
pygame.time.set_timer(Trash_event, 2000-score)
Trash_type = [rac, apple, fishbone]
running = True

while running:
    screen.blit(background, (0, 0))
    dt = clock.tick(60) / 1000
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == Trash_event and not game_over:  # Tạo rác mỗi khi sự kiện Trash_event được kích hoạt
          num_trash = max(1,score // 5)  # Mỗi 5 điểm sẽ thả ra thêm 1 rác
          for _ in range(num_trash): 
            trash = Trash_type[randint(0, len(Trash_type) - 1)]
            x, y = randint(50, Screen_Width - 50), randint(-200, -100)
            Trash(trash, (x, y), (all_sprites, Trash_sprites))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_over:  # Chơi lại khi nhấn SPACE
                reset_game()

    if not game_over:
        all_sprites.update(dt)
        vacham()
        Score()

    # Hiển thị màn hình game over nếu trò chơi kết thúc
    if game_over:
        screen.blit(over, (Screen_Width // 2 - over.get_width() // 2, Screen_Height // 4))
        screen.blit(lai, (Screen_Width // 2 - lai.get_width() // 2, Screen_Height // 2))

    all_sprites.draw(screen)
    pygame.display.update()
