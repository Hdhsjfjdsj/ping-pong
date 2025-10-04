from game.game_engine import GameEngine

def main():
    """
    Initializes and runs the game engine.
    """
    engine = GameEngine()
    engine.game_loop()

if __name__ == '__main__':
    main()