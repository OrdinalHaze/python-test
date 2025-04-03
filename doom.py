#!/usr/bin/env python3
import os
import time
from argparse import ArgumentParser

import numpy as np
import pygame
import vizdoom as vzd
from vizdoom import Button


def create_environment(config_file_path="./basic.cfg", visible=True, screen_format=vzd.ScreenFormat.RGB24, 
                       screen_resolution=vzd.ScreenResolution.RES_640X480, mode=vzd.Mode.PLAYER):
    """Create and configure the ViZDoom environment."""
    print(f"Creating environment from: {config_file_path}")
    game = vzd.DoomGame()
    
    # Game configuration
    game.load_config(config_file_path)
    game.set_window_visible(visible)
    game.set_mode(mode)
    game.set_screen_format(screen_format)
    game.set_screen_resolution(screen_resolution)
    
    # Add available buttons
    game.add_available_button(Button.MOVE_LEFT)
    game.add_available_button(Button.MOVE_RIGHT)
    game.add_available_button(Button.MOVE_FORWARD)
    game.add_available_button(Button.MOVE_BACKWARD)
    game.add_available_button(Button.TURN_LEFT)
    game.add_available_button(Button.TURN_RIGHT)
    game.add_available_button(Button.ATTACK)
    game.add_available_button(Button.USE)
    
    # Add available game variables
    game.add_available_game_variable(vzd.GameVariable.AMMO2)
    game.add_available_game_variable(vzd.GameVariable.HEALTH)
    
    # Initialize the game
    game.init()
    print("Environment created.")
    return game


def human_player():
    """Run the game in human player mode using PyGame for input handling."""
    # Initialize pygame for input handling
    pygame.init()
    # Create a dummy window to capture keyboard events
    pygame.display.set_mode((100, 100), pygame.HIDDEN)
    
    # Find the scenarios path
    scenarios_path = vzd.scenarios_path
    print(f"Looking for config in: {scenarios_path}")
    
    # Default config file path
    config_path = os.path.join(scenarios_path, "basic.cfg")
    
    # Check if the configuration file exists
    if not os.path.exists(config_path):
        # Try local path
        config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "basic.cfg")
        print(f"Config not found in scenarios path, trying local path: {config_path}")
        
        if not os.path.exists(config_path):
            raise FileNotFoundError(
                f"Config file not found at {config_path}. "
                f"Please make sure the file exists or create it using the provided template."
            )
    
    # Create game environment
    game = create_environment(config_path, visible=True)
    
    running = True
    
    # Episodes loop
    for episode in range(1, 11):
        if not running:
            break
            
        print(f"\nEpisode #{episode}")
        
        # Initialize new episode
        game.new_episode()
        
        while not game.is_episode_finished() and running:
            # Process events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Get the game state
            state = game.get_state()
            
            if state is None:
                continue
                
            # Get game variables
            health = state.game_variables[1]
            ammo = state.game_variables[0]
            
            print(f"Health: {health}, Ammo: {ammo}")
            
            # Prepare action (default: no action)
            action = [0] * 8
            
            # Get pressed keys
            keys = pygame.key.get_pressed()
            
            # Map keyboard input to actions
            if keys[pygame.K_w]:  # Move forward
                action[2] = 1
            if keys[pygame.K_s]:  # Move backward
                action[3] = 1
            if keys[pygame.K_a]:  # Turn left
                action[4] = 1
            if keys[pygame.K_d]:  # Turn right
                action[5] = 1
            if keys[pygame.K_q]:  # Strafe left
                action[0] = 1
            if keys[pygame.K_e]:  # Strafe right
                action[1] = 1
            if keys[pygame.K_SPACE]:  # Fire
                action[6] = 1
            if keys[pygame.K_f]:  # Use
                action[7] = 1
            if keys[pygame.K_ESCAPE]:  # Exit
                running = False
                
            # Perform action and get reward
            reward = game.make_action(action)
            
            # Display info
            print(f"Reward: {reward}")
            
            # Sleep to avoid excessive CPU usage
            time.sleep(0.028)  # ~35 fps
        
        # Episode finished
        if running:
            print(f"Episode finished. Total reward: {game.get_total_reward()}")
            time.sleep(2)
    
    # Close the game and pygame
    game.close()
    pygame.quit()


def main():
    """Main function."""
    parser = ArgumentParser("ViZDoom Simple Example")
    parser.add_argument("--mode", default="player", choices=["player", "spectator"], 
                       help="Game mode - player or spectator")
    args = parser.parse_args()
    
    print(f"ViZDoom paths:")
    print(f"  Scenarios path: {vzd.scenarios_path}")
    
    try:
        # Run the game
        if args.mode == "player":
            human_player()
        else:
            # For spectator mode, we would add different logic here
            print("Spectator mode not implemented in this example")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()