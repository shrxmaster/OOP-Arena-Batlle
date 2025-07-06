import random

class Creature:
    def __init__(self, name, health, attack_power, defense):
        self._name = name
        self._health = health
        self._max_health = health
        self._attack_power = attack_power
        self._defense = defense
    
    @property
    def name(self):
        return self._name
    
    @property
    def health(self):
        return self._health
    
    @property
    def is_alive(self):
        return self._health > 0
    
    def take_damage(self, damage):
        actual_damage = max(1, damage - self._defense)
        self._health = max(0, self._health - actual_damage)
        return actual_damage
    
    def attack(self, target):
        raise NotImplementedError("Subclasses must implement attack()")
    
    def special_ability(self):
        return None
    
    def __str__(self):
        return f"{self._name} (HP: {self._health}/{self._max_health})"

class Warrior(Creature):
    def __init__(self, name):
        super().__init__(
            name=name,
            health=120,
            attack_power=25,
            defense=10
        )
        self._rage = 0
    
    def attack(self, target):
        # Каждая атака увеличивает ярость
        self._rage = min(100, self._rage + 15)
        
        # Базовая атака
        damage = self._attack_power
        return target.take_damage(damage), f"{self.name} strikes with sword!"
    
    def special_ability(self):
        if self._rage >= 30:
            self._rage -= 30
            return {
                "damage_multiplier": 2.0,
                "message": f"{self.name} uses RAGE SMASH!"
            }
        return None

class Mage(Creature):
    def __init__(self, name):
        super().__init__(
            name=name,
            health=80,
            attack_power=30,
            defense=5
        )
        self._mana = 100
    
    def attack(self, target):
        # Восстановление маны
        self._mana = min(100, self._mana + 10)
        
        # Магическая атака
        damage = self._attack_power + random.randint(0, 5)
        return target.take_damage(damage), f"{self.name} casts a fireball!"
    
    def special_ability(self):
        if self._mana >= 40:
            self._mana -= 40
            return {
                "ignore_defense": True,
                "message": f"{self.name} casts ICE SPIKE! (ignores defense)"
            }
        return None

class Archer(Creature):
    def __init__(self, name):
        super().__init__(
            name=name,
            health=90,
            attack_power=22,
            defense=8
        )
    
    def attack(self, target):
        # Шанс критического удара 25%
        if random.random() < 0.25:
            damage = self._attack_power * 2
            return target.take_damage(damage), f"{self.name} lands a CRITICAL shot!"
        
        damage = self._attack_power
        return target.take_damage(damage), f"{self.name} shoots an arrow!"