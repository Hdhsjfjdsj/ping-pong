import pygame

WHITE = (255, 255, 255)

class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

    def move(self, direction, screen_height):
        self.rect.y += self.speed * direction
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

    def ai_move(self, ball, screen_height):
        if self.rect.centery < ball.rect.centery:
            self.rect.y += self.speed
        if self.rect.centery > ball.rect.centery:
            self.rect.y -= self.speed
        
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height