from vizdoom import DoomGame, Mode, ScreenFormat, ScreenResolution
import random
import numpy as np
import time

# Initialize Doom Environment
def initialize_game():
    game = DoomGame()
    game.load_config("scenarios/deadly_corridor.cfg")  # Complex Doom scenario
    game.set_screen_resolution(ScreenResolution.RES_1024X768)
    game.set_screen_format(ScreenFormat.RGB24)
    game.set_render_hud(True)
    game.set_render_crosshair(True)
    game.set_render_weapon(True)
    game.set_render_decals(True)
    game.set_render_particles(True)
    game.set_mode(Mode.PLAYER)
    game.init()
    return game

# Define Actions for the Agent
actions = [
    [1, 0, 0, 0, 0, 0, 0],  # Move Left
    [0, 1, 0, 0, 0, 0, 0],  # Move Right
    [0, 0, 1, 0, 0, 0, 0],  # Move Forward
    [0, 0, 0, 1, 0, 0, 0],  # Move Backward
    [0, 0, 0, 0, 1, 0, 0],  # Shoot
    [0, 0, 0, 0, 0, 1, 0],  # Turn Left
    [0, 0, 0, 0, 0, 0, 1]   # Turn Right
]

def play_game():
    game = initialize_game()
    episodes = 10  # Number of games to play
    for episode in range(episodes):
        print(f"Episode {episode+1}")
        game.new_episode()
        while not game.is_episode_finished():
            state = game.get_state()
            game_variables = state.game_variables  # Health, Ammo, Score, etc.
            screen_buffer = state.screen_buffer  # Raw pixel data

            action = random.choice(actions)  # Random action for now
            reward = game.make_action(action)

            # Ensure we only access available variables
            health = game_variables[0] if len(game_variables) > 0 else "N/A"
            ammo = game_variables[1] if len(game_variables) > 1 else "N/A"
            score = game_variables[2] if len(game_variables) > 2 else "N/A"

            print(f"Action: {action}, Reward: {reward}, Health: {health}, Ammo: {ammo}, Score: {score}")
            time.sleep(0.02)  # Slow down to visualize
        
        print(f"Episode finished. Total reward: {game.get_total_reward()}\n")
    game.close()

if __name__ == "__main__":
    play_game()