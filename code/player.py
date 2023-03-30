import pygame
from support import import_folder
class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.import_character_assets()
        self.frame_index = 0
        self.animation_speed = 0.15
        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft = pos)
        #player movement
        self.direction = pygame.math.Vector2(0,0)
        self.speed = 8
        self.gravity = 0.8
        self.jump_speed = -20
        #player status
        self.status = 'idle'
        self.facing_right = True
        self.on_ground = False
        self.on_ceiling = False
        self.on_left = False
        self.on_right = False

    def import_character_assets(self):
        character_path = '../graphics/characters/warrior/'
        self.animations = {'idle':[],'run':[],'jump':[],'fall':[]}

        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
    def animate(self):
        animation = self.animations[self.status]
        #loop over frame index
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        image = animation[int(self.frame_index)]
        if self.facing_right:
            self.image = image
        else:
            flipped_image = pygame.transform.flip(image,True,False) #notatka: flip(powierzchnia,obrócenie względem osi x,obrócenie względem osi y)
            self.image = flipped_image
        #set the rect
        if self.on_ground and self.on_right:#dół prawo
            self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
        elif self.on_ground and self.on_left:#dół lewo
            self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
        elif self.on_ground:#dół
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)

        elif self.on_ceiling and self.on_right:#góra prawo
            self.rect = self.image.get_rect(topright = self.rect.topright)
        elif self.on_ceiling and self.on_left:#góra lewo
            self.rect = self.image.get_rect(topleft = self.rect.topleft)
        elif self.on_ceiling:#góra
            self.rect = self.image.get_rect(midtop = self.rect.midtop)

        else:#środek
            self.rect = self.image.get_rect(center = self.rect.center)

    def get_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]:
            self.direction.x = 1
            self.facing_right = True
        elif keys[pygame.K_a]:
            self.direction.x = -1
            self.facing_right = False
        else:
            self.direction.x = 0

        if keys[pygame.K_w] and self.on_ground:
            self.jump()
        if keys[pygame.K_SPACE] and self.on_ground:
            self.jump()

    def get_status(self):
        if self.direction.y < 0:
            self.status = 'jump'
        elif self.direction.y > 0: #można zmienić na 1(większe niż grwitacja) jeśli podczas stania w miejscu widać animacje spadania
            self.status = 'fall'
        else:
            if self.direction.x != 0:
                self.status = 'run'
            else:
                self.status = 'idle'
    def apply_gravity(self):
        self.direction.y += self.gravity
        self.rect.y += self.direction.y
    def jump(self):
        self.direction.y = self.jump_speed
    def update(self):
        self.get_input()
        self.get_status()
        self.animate()
