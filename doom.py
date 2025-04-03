from vizdoom import DoomGame, Mode, ScreenFormat, ScreenResolution
import random
import numpy as np
import time

# Initialize Doom Environment
def initialize_game():
    game = DoomGame()
    game.load_config("scenarios/basic.cfg")  # Load a predefined Doom scenario
    game.set_screen_resolution(ScreenResolution.RES_640X480)
    game.set_screen_format(ScreenFormat.GRAY8)
    game.set_render_hud(False)
    game.set_render_crosshair(False)
    game.set_render_weapon(True)
    game.set_render_decals(False)
    game.set_render_particles(False)
    game.set_mode(Mode.PLAYER)
    game.init()
    return game

# Define Actions for the Agent
actions = [
    [1, 0, 0],  # Move Left
    [0, 1, 0],  # Move Right
    [0, 0, 1]   # Shoot
]

def play_game():
    game = initialize_game()
    episodes = 10  # Number of games to play
    for episode in range(episodes):
        print(f"Episode {episode+1}")
        game.new_episode()
        while not game.is_episode_finished():
            state = game.get_state()
            game_variables = state.game_variables  # Health, Ammo, etc.
            screen_buffer = state.screen_buffer  # Raw pixel data
            
            action = random.choice(actions)  # Random action for now
            reward = game.make_action(action)
            
            print(f"Action: {action}, Reward: {reward}")
            time.sleep(0.02)  # Slow down to visualize
        
        print(f"Episode finished. Total reward: {game.get_total_reward()}\n")
    game.close()

if __name__ == "__main__":
    play_game()