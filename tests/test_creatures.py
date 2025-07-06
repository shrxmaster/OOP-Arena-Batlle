import pytest
from src.creatures import Creature, Warrior, Mage, Archer
import random

@pytest.fixture
def warrior():
    return Warrior("Conan")

@pytest.fixture
def mage():
    return Mage("Gandalf")

@pytest.fixture
def archer():
    return Archer("Legolas")

class TestCreatureBasics:
    def test_initialization(self, warrior):
        assert warrior.name == "Conan"
        assert warrior.health == 120
        assert warrior.is_alive is True
    
    def test_take_damage(self, warrior):
        damage_taken = warrior.take_damage(15)
        assert damage_taken == 5  
        assert warrior.health == 115
        
        damage_taken = warrior.take_damage(5)
        assert damage_taken == 1
        assert warrior.health == 114
        
        warrior.take_damage(200)
        assert warrior.health == 0
        assert warrior.is_alive is False

class TestWarrior:
    def test_attack(self, warrior, mage):
        initial_health = mage.health
        _, message = warrior.attack(mage)
        assert "strikes with sword" in message
        assert mage.health < initial_health
        assert warrior._rage == 15
    
    def test_special_ability_success(self, warrior):
        warrior._rage = 30
        special = warrior.special_ability()
        assert special is not None
        assert "RAGE SMASH" in special["message"]
        assert warrior._rage == 0
    
    def test_special_ability_fail(self, warrior):
        warrior._rage = 20
        assert warrior.special_ability() is None

class TestMage:
    def test_attack(self, mage, warrior):
        initial_health = warrior.health
        _, message = mage.attack(warrior)
        assert "casts a fireball" in message
        assert warrior.health < initial_health
        assert mage._mana == 100
    
    def test_special_ability_success(self, mage, warrior):
        mage._mana = 40
        special = mage.special_ability()
        assert special is not None
        assert "ICE SPIKE" in special["message"]
        assert mage._mana == 0
        assert special["ignore_defense"] is True
    
    def test_special_ability_fail(self, mage):
        mage._mana = 30
        assert mage.special_ability() is None

class TestArcher:
    def test_normal_attack(self, archer, mage, monkeypatch):
        monkeypatch.setattr(random, 'random', lambda: 0.3) 
        initial_health = mage.health
        damage, message = archer.attack(mage)
        assert "shoots an arrow" in message
        expected_damage = max(1, archer._attack_power - mage._defense)
        assert damage == expected_damage
        assert mage.health == initial_health - damage
    
    def test_critical_attack(self, archer, mage, monkeypatch):
        monkeypatch.setattr(random, 'random', lambda: 0.1)
        initial_health = mage.health
        damage, message = archer.attack(mage)
        assert "CRITICAL shot" in message
        expected_damage = max(1, archer._attack_power * 2 - mage._defense)
        assert damage == expected_damage
        assert mage.health == initial_health - damage
        monkeypatch.setattr(random, 'random', lambda: 0.3) 
        initial_health = mage.health
        
        original_defense = mage._defense
        mage._defense = 0
        
        damage, message = archer.attack(mage)
        
        mage._defense = original_defense
        
        assert "shoots an arrow" in message
        assert damage == archer._attack_power
