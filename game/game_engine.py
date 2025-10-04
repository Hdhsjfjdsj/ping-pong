import pygame
import sys
from .paddle import Paddle
from .ball import Ball

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
DEFAULT_WINNING_SCORE = 5

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game States
PLAYING = 0
GAME_OVER = 1

class GameEngine:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Real-Time Ping Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
        self._load_sounds()
        self._reset_game(score_to_win=DEFAULT_WINNING_SCORE)

    def _reset_game(self, score_to_win):
        """Resets the game to its initial state with a specific winning score."""
        self.winning_score = score_to_win
        PADDLE_WIDTH, PADDLE_HEIGHT, BALL_SIZE = 10, 100, 15
        PADDLE_SPEED, AI_PADDLE_SPEED = 7, 6

        self.player_paddle = Paddle(20, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)
        self.ai_paddle = Paddle(SCREEN_WIDTH - 20 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT, AI_PADDLE_SPEED)
        self.ball = Ball(SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE)
        
        self.player_score = 0
        self.ai_score = 0
        self.game_state = PLAYING
        self.winner_text = ""

    def game_loop(self):
        """The main loop of the game."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                self._handle_input(event)

            if self.game_state == PLAYING:
                self._update_game_state()
            
            self._draw()
            pygame.display.flip()
            self.clock.tick(60)

    def _handle_input(self, event):
        """Handles user input for paddle movement and game over screen."""
        if self.game_state == GAME_OVER and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                self._reset_game(score_to_win=3)
            elif event.key == pygame.K_5:
                self._reset_game(score_to_win=5)
            elif event.key == pygame.K_7:
                self._reset_game(score_to_win=7)
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    def _update_game_state(self):
        """Updates the positions and scores of game objects."""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.player_paddle.move(-1, SCREEN_HEIGHT)
        if keys[pygame.K_s]:
            self.player_paddle.move(1, SCREEN_HEIGHT)

        collision_event = self.ball.move(self.player_paddle, self.ai_paddle)
        self._handle_collision_events(collision_event)

        self.ai_paddle.ai_move(self.ball, SCREEN_HEIGHT)
        
        if self.player_score >= self.winning_score:
            self.winner_text = "Player Wins!"
            self.game_state = GAME_OVER
        elif self.ai_score >= self.winning_score:
            self.winner_text = "AI Wins!"
            self.game_state = GAME_OVER

    def _draw(self):
        """Draws all game objects based on the current game state."""
        self.screen.fill(BLACK)
        if self.game_state == PLAYING:
            self._draw_playing()
        elif self.game_state == GAME_OVER:
            self._draw_game_over()

    def _draw_playing(self):
        pygame.draw.aaline(self.screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))
        self.player_paddle.draw(self.screen)
        self.ai_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        player_text = self.font.render(str(self.player_score), True, WHITE)
        self.screen.blit(player_text, (SCREEN_WIDTH // 4, 20))

        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        self.screen.blit(ai_text, (SCREEN_WIDTH * 3 // 4 - ai_text.get_width(), 20))

    def _draw_game_over(self):
        winner_surf = self.font.render(self.winner_text, True, WHITE)
        winner_rect = winner_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
        self.screen.blit(winner_surf, winner_rect)

        replay_surf = self.small_font.render("Play Again? Select a mode:", True, WHITE)
        replay_rect = replay_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(replay_surf, replay_rect)

        options = ["Press '3' - Best of 3", "Press '5' - Best of 5", "Press '7' - Best of 7", "Press 'Q' - Quit"]
        for i, text in enumerate(options):
            surf = self.small_font.render(text, True, WHITE)
            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50 + i * 40))
            self.screen.blit(surf, rect)

    def _load_sounds(self):
        try:
            self.paddle_hit_sound = pygame.mixer.Sound('assets/paddle_hit.wav')
            self.wall_bounce_sound = pygame.mixer.Sound('assets/wall_bounce.wav')
            self.score_sound = pygame.mixer.Sound('assets/score.wav')
        except pygame.error:
            class DummySound:
                def play(self): pass
            self.paddle_hit_sound = self.wall_bounce_sound = self.score_sound = DummySound()

    def _handle_collision_events(self, event):
        if event == 'paddle_hit':
            self.paddle_hit_sound.play()
        elif event == 'wall_hit':
            self.wall_bounce_sound.play()
        elif event == 'player_score':
            self.score_sound.play()
            self.player_score += 1
        elif event == 'ai_score':
            self.score_sound.play()
            self.ai_score += 1