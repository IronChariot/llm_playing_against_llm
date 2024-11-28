import argparse
import sys
from config import Config
from game_manager import GameManager
from models import Model, OllamaModel, AnthropicModel, OpenAIModel
from games import CoinFlipGame
from system_prompt import SystemPrompt
from utilities import setup_logging

def parse_arguments():
    parser = argparse.ArgumentParser(description="LLM Game Playing System")
    parser.add_argument("game", help="Name of the game to play")
    parser.add_argument("--model1", default="llama31_q5", help="Name of the first model (default: llama31_q5)")
    parser.add_argument("--model2", default="llama31_q5", help="Name of the second model (default: llama31_q5)")
    parser.add_argument("--prompt1", default="default", help="Filename of the first system prompt (default: default)")
    parser.add_argument("--prompt2", default="default", help="Filename of the second system prompt (default: default)")
    parser.add_argument("--rounds", type=int, default=1, help="Number of rounds to play (default: 1)")
    return parser.parse_args()

def test_system_prompt(model: Model, logger):
    logger.info("Testing system prompt understanding...")
    response = model.test_system_prompt()
    logger.info(f"Model's understanding of the game rules:\n{response}")
    print(f"Model's understanding of the game rules:\n{response}")
    input("Press Enter to continue...")

def main():
    args = parse_arguments()
    
    # Setup logging
    main_logger, model1_logger, model2_logger = setup_logging(args.game, args.model1, args.model2)
    
    # Load configuration
    config = Config()
    
    # Load system prompts
    try:
        system_prompt1 = SystemPrompt.load_from_file(args.game, args.prompt1)
        system_prompt2 = SystemPrompt.load_from_file(args.game, args.prompt2)
    except FileNotFoundError as e:
        main_logger.error(f"System prompt file not found: {e}")
        sys.exit(1)
    
    # Initialize models
    try:
        if args.model1 in ["opus", "sonnet", "haiku"]:
            model1 = AnthropicModel(args.model1, system_prompt=system_prompt1, logger=model1_logger)
        elif args.model1 in ["gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-3.5"]:
            model1 = OpenAIModel(args.model1, system_prompt=system_prompt1, logger=model1_logger)
        else:
            model1 = OllamaModel(args.model1, system_prompt=system_prompt1, logger=model1_logger)
            
        if args.model2 in ["opus", "sonnet", "haiku"]:
            model2 = AnthropicModel(args.model2, system_prompt=system_prompt2, logger=model2_logger)
        elif args.model2 in ["gpt-4o", "gpt-4o-mini", "gpt-4", "gpt-3.5"]:
            model2 = OpenAIModel(args.model2, system_prompt=system_prompt2, logger=model2_logger) 
        else:
            model2 = OllamaModel(args.model2, system_prompt=system_prompt2, logger=model2_logger)
    except ValueError as e:
        main_logger.error(f"Error initializing models: {e}")
        sys.exit(1)
    
    # Test system prompts
    # test_system_prompt(model1, main_logger)
    # test_system_prompt(model2, main_logger)

    # Initialize game
    if args.game.lower() == "coinflip":
        game = CoinFlipGame("Player 1", "Player 2", model1, model2, args.rounds, logger=main_logger)
    else:
        main_logger.error(f"Unknown game: {args.game}")
        sys.exit(1)
    
    # Initialize game manager
    game_manager = GameManager(game)
    
    # Run the game
    game_manager.run_game()
    
    # Print results
    print(game.get_game_state())

if __name__ == "__main__":
    main()