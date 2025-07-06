class Arena:
    def __init__(self, player, computer):
        self.player = player
        self.computer = computer
        self.turn_count = 0
    
    def execute_turn(self, attacker, defender):
        self.turn_count += 1
        
        # Обычная атака
        damage, attack_message = attacker.attack(defender)
        turn_log = [
            f"Turn {self.turn_count}: {attack_message}",
            f"  {defender.name} takes {damage} damage!"
        ]
        
        # Проверка спецспособности
        special = attacker.special_ability()
        if special:
            if "damage_multiplier" in special:
                damage = int(defender.take_damage(attacker._attack_power * special["damage_multiplier"]))
                turn_log.append(f"  {special['message']}")
                turn_log.append(f"  Additional {damage} damage!")
            elif "ignore_defense" in special:
                original_defense = defender._defense
                defender._defense = 0
                damage = attacker.attack(defender)[0]
                defender._defense = original_defense
                turn_log.append(f"  {special['message']}")
                turn_log.append(f"  Deals {damage} ignoring defense!")
        
        turn_log.append(f"  {defender}")
        return "\n".join(turn_log)
    
    def battle(self):
        log = ["Battle starts!", f"Player: {self.player}", f"Computer: {self.computer}"]
        
        while self.player.is_alive and self.computer.is_alive:
            log.append(self.execute_turn(self.player, self.computer))
            if not self.computer.is_alive:
                break
                
            log.append(self.execute_turn(self.computer, self.player))
        
        winner = self.player if self.player.is_alive else self.computer
        log.append(f"\n{winner.name} wins the battle!")
        return "\n\n".join(log)