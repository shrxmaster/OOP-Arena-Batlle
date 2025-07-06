import pytest
from src.arena import Arena
from src.creatures import Warrior, Mage

@pytest.fixture
def player():
    return Warrior("Player")

@pytest.fixture
def computer():
    return Mage("Computer")

@pytest.fixture
def arena(player, computer):
    return Arena(player, computer)

class TestArena:
    def test_initialization(self, arena, player, computer):
        assert arena.player == player
        assert arena.computer == computer
        assert arena.turn_count == 0
    
    def test_execute_turn(self, arena, player, computer):
        log = arena.execute_turn(player, computer)
        assert "strikes with sword" in log
        assert computer.health < 80
        assert arena.turn_count == 1
        
        log = arena.execute_turn(computer, player)
        assert "casts a fireball" in log
        assert player.health < 120
    
    def test_battle_flow(self, arena, player, computer):
        # Force quick battle by reducing health
        player._health = 10
        computer._health = 5
        
        battle_log = arena.battle()
        assert "Player wins" in battle_log or "Computer wins" in battle_log
        assert not (player.is_alive and computer.is_alive)
    
    def test_warrior_special_in_battle(self, arena, player, computer, monkeypatch):
        # Setup rage for special
        player._rage = 30
        
        log = arena.execute_turn(player, computer)
        assert "RAGE SMASH" in log
        assert "Additional" in log
    
    def test_mage_special_in_battle(self, arena, player, computer, monkeypatch):
        # Setup mana for special
        computer._mana = 40
        
        # Skip player turn
        arena.execute_turn(player, computer)
        
        log = arena.execute_turn(computer, player)
        assert "ICE SPIKE" in log
        assert "ignoring defense" in log