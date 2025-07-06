from .creatures import Warrior, Mage, Archer
from .arena import Arena
import random

class Game:
    CREATURE_TYPES = {
        "1": ("Warrior", Warrior),
        "2": ("Mage", Mage),
        "3": ("Archer", Archer)
    }
    
    def __init__(self):
        self.player_creature = None
        self.computer_creature = None
    
    def select_creature(self):
        print("Select your creature:")
        for key, (name, _) in self.CREATURE_TYPES.items():
            print(f"{key}. {name}")
        
        while True:
            choice = input("Enter choice (1-3): ")
            if choice in self.CREATURE_TYPES:
                name = input("Give your creature a name: ")
                cls = self.CREATURE_TYPES[choice][1]
                self.player_creature = cls(name)
                break
            print("Invalid choice!")
    
    def generate_computer_opponent(self):
        creature_type = random.choice(list(self.CREATURE_TYPES.values()))
        name = f"Computer_{creature_type[0]}"
        self.computer_creature = creature_type[1](name)
    
    def start(self):
        print("=== BATTLE ARENA ===")
        self.select_creature()
        self.generate_computer_opponent()
        
        arena = Arena(self.player_creature, self.computer_creature)
        print("\nStarting battle...")
        battle_log = arena.battle()
        
        print("\n" + "="*40)
        print(battle_log)
        print("="*40)