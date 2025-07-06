import pytest
from src.game import Game
from src.creatures import Warrior, Mage, Archer
from unittest.mock import patch, MagicMock

class TestGame:
    @patch("builtins.input", side_effect=["1", "TestPlayer"])
    def test_character_selection(self, mock_input):
        game = Game()
        game.select_creature()
        
        assert isinstance(game.player_creature, Warrior)
        assert game.player_creature.name == "TestPlayer"
    
    def test_computer_generation(self):
        game = Game()
        game.generate_computer_opponent()
        
        assert game.computer_creature is not None
        assert any(isinstance(game.computer_creature, cls) 
                  for cls in [Warrior, Mage, Archer])
    
    @patch("builtins.input", side_effect=["2", "Gandalf"])
    @patch("src.game.Game.generate_computer_opponent")
    @patch("src.game.Arena")
    def test_game_flow(self, mock_arena, mock_generate, mock_input):
        game = Game()
        game.start()
        
        # Verify character selection
        assert isinstance(game.player_creature, Mage)
        assert game.player_creature.name == "Gandalf"
        
        # Verify computer generation
        mock_generate.assert_called_once()
        
        # Verify battle start
        mock_arena.assert_called_once_with(
            game.player_creature,
            game.computer_creature
        )
        mock_arena.return_value.battle.assert_called_once()