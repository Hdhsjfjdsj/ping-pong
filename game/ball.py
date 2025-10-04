import pygame
import random

WHITE = (255, 255, 255)

class Ball:
    def __init__(self, x, y, size):
        self.screen_width = 800
        self.screen_height = 600
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x = 7 * random.choice((1, -1))
        self.speed_y = 7 * random.choice((1, -1))

    def draw(self, screen):
        pygame.draw.ellipse(screen, WHITE, self.rect)

    def move(self, player_paddle, ai_paddle):
        self.rect.x += self.speed_x
        
        if self.rect.colliderect(player_paddle.rect):
            self.speed_x *= -1
            self.rect.left = player_paddle.rect.right
            return 'paddle_hit'
        if self.rect.colliderect(ai_paddle.rect):
            self.speed_x *= -1
            self.rect.right = ai_paddle.rect.left
            return 'paddle_hit'

        self.rect.y += self.speed_y
        
        if self.rect.top <= 0 or self.rect.bottom >= self.screen_height:
            self.speed_y *= -1
            return 'wall_hit'

        if self.rect.left <= 0:
            self.reset()
            return 'ai_score'
        if self.rect.right >= self.screen_width:
            self.reset()
            return 'player_score'
            
        return None

    def reset(self):
        self.rect.center = (self.screen_width / 2, self.screen_height / 2)
        self.speed_y *= random.choice((1, -1))
        self.speed_x *= random.choice((1, -1))