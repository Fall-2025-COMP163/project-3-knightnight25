"""
COMP 163 - Project 3: Quest Chronicles
Combat System Module - Starter Code

Name: Kami Crews

AI Usage: [Document any AI assistance used]

Handles combat mechanics
"""

from custom_exceptions import (
    InvalidTargetError,
    CombatNotActiveError,
    CharacterDeadError,
    AbilityOnCooldownError
)

# ============================================================================
# ENEMY DEFINITIONS
# ============================================================================

def create_enemy(enemy_type):
    """
    Create an enemy based on type
    
    Example enemy types and stats:
    - goblin: health=50, strength=8, magic=2, xp_reward=25, gold_reward=10
    - orc: health=80, strength=12, magic=5, xp_reward=50, gold_reward=25
    - dragon: health=200, strength=25, magic=15, xp_reward=200, gold_reward=100
    
    Returns: Enemy dictionary
    Raises: InvalidTargetError if enemy_type not recognized
    """
    # TODO: Implement enemy creation
    # Return dictionary with: name, health, max_health, strength, magic, xp_reward, gold_reward
    enemy_templates = {
        "goblin": {
            "health": 50,
            "strength": 8,
            "magic": 2, 
            "xp_reward": 25,
            "gold_reward": 10
        },
        "orc": {
            "health": 80,
            "strength": 12,
            "magic": 5,
            "xp_reward": 50,
            "gold_reward": 25
        },
        "dragon": {
            "health": 200, 
            "strength": 25,
            "magic": 15,
            "xp_reward": 200,
            "gold_reward": 100
        }
    }

    enemy_type_lower = enemy_type.lower()
    if enemy_type_lower not in enemy_templates:
        raise InvalidTargetError(f"Enemy type '{enemy_type}' not recognized.")
    
    template = enemy_templates[enemy_type_lower]

    enemy = {
        "name": enemy_type.capitalize(),
        "health": template["health"],
        "max_health": template["health"],
        "strength": template["strength"],
        "magic": template["magic"],
        "xp_reward": template["xp_reward"],
        "gold_reward": template["gold_reward"]
    }

    return enemy 


def get_random_enemy_for_level(character_level):
    """
    Get an appropriate enemy for character's level
    
    Level 1-2: Goblins
    Level 3-5: Orcs
    Level 6+: Dragons
    
    Returns: Enemy dictionary
    """
    # TODO: Implement level-appropriate enemy selection
    # Use if/elif/else to select enemy type
    # Call create_enemy with appropriate type
    if character_level <= 2:
        enemy_type = "goblin"
    elif character_level <= 5:
        enemy_type = "orc"
    else:
        enemy_type = "dragon"

    return create_enemy(enemy_type)

# ============================================================================
# COMBAT SYSTEM
# ============================================================================

class SimpleBattle:
    """
    Simple turn-based combat system
    
    Manages combat between character and enemy
    """
    
    def __init__(self, character, enemy):
        """Initialize battle with character and enemy"""
        # TODO: Implement initialization
        # Store character and enemy
        # Set combat_active flag
        # Initialize turn counter
        self.character = character
        self.enemy = enemy

        self.combat_active = True

        self.turn_count = 0
    
    def start_battle(self):
        """
        Start the combat loop
        
        Returns: Dictionary with battle results:
                {'winner': 'player'|'enemy', 'xp_gained': int, 'gold_gained': int}
        
        Raises: CharacterDeadError if character is already dead
        """
        # TODO: Implement battle loop
        # Check character isn't dead
        # Loop until someone dies
        # Award XP and gold if player wins
        char = self.character
        enemy = self.enemy

        if char.get('health', 0) <= 0:
            raise ValueError(f"CharacterDeadError: {char.get('name', 'The Player')} is already dead and cannot start a battle.")
        
        display_battle_log(f"\n A wild {enemy['name']} appears! Battle Start!")

        self.combat_active = True
        self.turn_count = 0

        while self.combat_active:
            self.turn_count += 1
            print(f"\n=== Turn {self.turn_count} ===")

            player_damage = max(1, char.get('strength', 1) - enemy.get('magic', 0))

            enemy['health'] -= player_damage
            display_battle_log(f"{char['name']} attacks {enemy['name']} for {player_damage} damage. {enemy['name']} HP: {max(0, enemy['health'])}/{enemy['max_health']}")

            if enemy.get('health', 0) <= 0:
                self.combat_active = False
                break

            enemy_damage = max(1, enemy.get('strength', 1) - char.get('magic', 0))

            char['health'] -= enemy_damage
            display_battle_log(f"{enemy['name']} attacks {char['name']} for {enemy_damage} damage. {char['name']} HP: {max(0, char['health'])}/{char['max_health']}")

            if char.get('health', 0) <= 0: 
                winner = 'enemy'
                xp_gained = 0
                gold_gained = 0
                self.combat_active = False

            if not self.combat_active:
                if enemy.get('health', 0) <= 0:
                    winner = 'player'
                    xp_gained = enemy.get('xp_reward', 0)
                    gold_gained = enemy.get('gold_reward', 0)
                    
                    if xp_gained > 0:
                        char['experience'] = char.get('experience', 0) + xp_gained

                        while True:
                            current_level = char.get('level', 1)
                            required_xp = current_level * 100
                
                            if char['experience'] >= required_xp:
                                char['level'] = char.get('level', 1) + 1
                                char['max_health'] = char.get('max_health', 0) + 10
                                char['strength'] = char.get('strength', 0) + 2
                                char['magic'] = char.get('magic', 0) + 2
                                char['health'] = char['max_health']
                                char['experience'] -= required_xp
                                print(f"{char['name']} leveled up to Level {char['level']}!")
                            else:
                                break

                    if gold_gained > 0:
                        char['gold'] = char.get('gold', 0) + gold_gained
            
                    display_battle_log(f"\n Victory! {char['name']} defeated {enemy['name']}.")
                    display_battle_log(f"Gained {xp_gained} XP and {gold_gained} Gold.")
            else:
                winner = 'enemy'
                xp_gained = 0
                gold_gained = 0
                display_battle_log(f"\n Defeat! {char['name']} was slain by {enemy['name']}.")

            return {
                'winner': winner,
                'xp_gained': xp_gained,
                'gold_gained': gold_gained
            }
    
    def player_turn(self):
        """
        Handle player's turn
        
        Displays options:
        1. Basic Attack
        2. Special Ability (if available)
        3. Try to Run
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement player turn
        # Check combat is active
        # Display options
        # Get player choice
        # Execute chosen action
        if not self.combat_active:
            raise ValueError("CombatNotActiveError: Cannot execute player turn when combat is not active.")
        
        char = self.character
        enemy = self.enemy

        print(f"\nYour turn, {char['name']} (HP: {char['health']}/{char['max_health']})")
        print(f"Enemy {enemy['name']} (HP: {enemy['health']}/{enemy['max_health']})")

        print("Choose your action: ")
        print("1, Basic Attack (Strength-based damage)")
        print("2. Special Ability (Magic-based damage/effect - currently unavailiable in this simplifies example)")
        print(f"3. Try to run (50% chance to escape)")

        choice = input("Enter number: ")
        if choice == '1':
            player_damage = max(1, char.get('strength', 1) - enemy.get('magic', 0))
            enemy['health'] -= player_damage 
            print(f"{char['name']} use Basic Attack on {enemy['name']} for {player_damage} damage.")
            return 'attack'
        elif choice == '2':
            print("Special Ability used (Effect not implemented in this version).")
            return 'ability'
        elif choice == '3':
            print("You failed to escape the battle!")
            return 'run_failed'
        else:
            print("Invalid choice. Skipping turn.")
            return 'skipped'

    
    def enemy_turn(self):
        """
        Handle enemy's turn - simple AI
        
        Enemy always attacks
        
        Raises: CombatNotActiveError if called outside of battle
        """
        # TODO: Implement enemy turn
        # Check combat is active
        # Calculate damage
        # Apply to character
        if not self.combat_active:
            raise ValueError("CombatNotActiveError: Cannot execute enemy turn when combat is not active.")
        
        char = self.character
        enemy = self.enemy

        enemy_damage = max(1, enemy.get('strength', 1) - char.get('magic', 0))
        char['health'] -= enemy_damage
    
        print(f"The {enemy['name']} attacks {char['name']} for {enemy_damage} damage.")
        return 'attack'
    
    def calculate_damage(self, attacker, defender):
        """
        Calculate damage from attack
        
        Damage formula: attacker['strength'] - (defender['strength'] // 4)
        Minimum damage: 1
        
        Returns: Integer damage amount
        """
        # TODO: Implement damage calculation
        attacker_strength = attacker.get('strength', 0)

        defender_strength = defender.get('strength', 0)
        defensive_reduction = defender_strength // 4

        raw_damage = attacker_strength - defensive_reduction
        final_damage = max(1, raw_damage)
    
        return final_damage
    
    def apply_damage(self, target, damage):
        """
        Apply damage to a character or enemy
        
        Reduces health, prevents negative health
        """
        # TODO: Implement damage application
        current_health = target.get('health', 0)
    
        new_health = current_health - damage

        target['health'] = max(0, new_health)
    
        return target['health']
    
    def check_battle_end(self):
        """
        Check if battle is over
        
        Returns: 'player' if enemy dead, 'enemy' if character dead, None if ongoing
        """
        # TODO: Implement battle end check
        if self.enemy.get('health', 0) <= 0:
            return 'player'

        if self.character.get('health', 0) <= 0:
            return 'enemy'
        
        return None
    
    def attempt_escape(self):
        """
        Try to escape from battle
        
        50% success chance
        
        Returns: True if escaped, False if failed
        """
        # TODO: Implement escape attempt
        # Use random number or simple calculation
        # If successful, set combat_active to False
        import random
        if random.random() < 0.5:
            self.combat_active = False
            print(f"{self.character.get('name', 'The Character')} successfully escaped the battle!")
            return True
        else:
            print(f"{self.character.get('name', 'The Character')} failed to escape!")
            return False

# ============================================================================
# SPECIAL ABILITIES
# ============================================================================

def use_special_ability(character, enemy):
    """
    Use character's class-specific special ability
    
    Example abilities by class:
    - Warrior: Power Strike (2x strength damage)
    - Mage: Fireball (2x magic damage)
    - Rogue: Critical Strike (3x strength damage, 50% chance)
    - Cleric: Heal (restore 30 health)
    
    Returns: String describing what happened
    Raises: AbilityOnCooldownError if ability was used recently
    """
    # TODO: Implement special abilities
    # Check character class
    # Execute appropriate ability
    # Track cooldowns (optional advanced feature)
    import random
    char_class = character.get('class', 'Warrior').lower()
    char_name = character.get('name', 'The Character')
    
    if character.get('ability_cooldown', False):
        raise ValueError("AbilityOnCooldownError: Special ability is currently on cooldown.")
    
    character['ability_cooldown'] = True

    if char_class == 'warrior':
        
        base_damage = character.get('strength', 1)
        damage = base_damage * 2
        
        enemy['health'] -= damage
        enemy['health'] = max(0, enemy['health'])
        
        return f"{char_name} used **Power Strike** on {enemy.get('name', 'enemy')} for {damage} damage."

    elif char_class == 'mage':
        
        base_damage = character.get('magic', 1)
        damage = base_damage * 2
        
        enemy['health'] -= damage
        enemy['health'] = max(0, enemy['health'])
        
        return f"{char_name} used **Fireball** on {enemy.get('name', 'enemy')} for {damage} magic damage."
        
    elif char_class == 'rogue':
        
        base_damage = character.get('strength', 1)
        
        if random.random() < 0.5:
            damage = base_damage * 3
            message = "critical hit"
        else:
            damage = base_damage * 1
            message = "missed critical"
            
        enemy['health'] -= damage
        enemy['health'] = max(0, enemy['health'])
        
        return f"{char_name} used **Critical Strike**, resulting in a {message} for {damage} damage."
        
    elif char_class == 'cleric':
        
        heal_amount = 30
        max_health = character.get('max_health', character.get('health', 0))
        
        actual_heal_amount = min(heal_amount, max_health - character.get('health', 0))
        
        character['health'] += actual_heal_amount
        
        return f"{char_name} used **Heal**, restoring {actual_heal_amount} health."

    else:
        return f"{char_name}'s class ({char_class}) does not have a defined special ability."

def warrior_power_strike(character, enemy):
    """Warrior special ability"""
    # TODO: Implement power strike
    # Double strength damage
    Damage_multiplier = 2
    
    base_strength = character.get('strength', 1)
    
    damage = base_strength * Damage_multiplier
    
    enemy['health'] -= damage
    
    enemy['health'] = max(0, enemy['health'])
    
    return f"{character.get('name', 'Warrior')} used Power Strike on {enemy.get('name', 'enemy')} for {damage} damage."

def mage_fireball(character, enemy):
    """Mage special ability"""
    # TODO: Implement fireball
    # Double magic damage
    Damage_multiplier = 2
    
    base_magic = character.get('magic', 1)
    
    damage = base_magic * Damage_multiplier
   
    enemy['health'] -= damage
    
    enemy['health'] = max(0, enemy['health'])
    
    return f"{character.get('name', 'Mage')} launched a Fireball at {enemy.get('name', 'enemy')} for {damage} magic damage."

def rogue_critical_strike(character, enemy):
    """Rogue special ability"""
    # TODO: Implement critical strike
    # 50% chance for triple damage
    import random
    
    Base_damage_multiplier = 1
    Critical_multiplier = 3
    Critical_chance = 0.5
    
    base_strength = character.get('strength', 1)
    
    if random.random() < Critical_chance:
        damage = base_strength * Critical_multiplier
        message = f"{character.get('name', 'Rogue')} used Critical Strike, landing a **critical hit** on {enemy.get('name', 'enemy')} for {damage} damage."
    else:
        damage = base_strength * Base_damage_multiplier
        message = f"{character.get('name', 'Rogue')} used Critical Strike, but it was a regular attack on {enemy.get('name', 'enemy')} for {damage} damage."
        
    enemy['health'] -= damage
    enemy['health'] = max(0, enemy['health'])
    
    return message

def cleric_heal(character):
    """Cleric special ability"""
    # TODO: Implement healing
    # Restore 30 HP (not exceeding max_health)
    Heal_amount = 30
    
    current_health = character.get('health', 0)
    max_health = character.get('max_health', current_health)
    
    missing_health = max_health - current_health
    
    actual_heal_amount = min(Heal_amount, missing_health)
    
    character['health'] += actual_heal_amount
    
    return f"{character.get('name', 'Cleric')} used Heal, restoring {actual_heal_amount} health."

# ============================================================================
# COMBAT UTILITIES
# ============================================================================

def can_character_fight(character):
    """
    Check if character is in condition to fight
    
    Returns: True if health > 0 and not in battle
    """
    # TODO: Implement fight check
    is_alive = character.get('health', 0) > 0
    
    is_not_in_battle = not character.get('in_battle', False)
    
    return is_alive and is_not_in_battle

def get_victory_rewards(enemy):
    """
    Calculate rewards for defeating enemy
    
    Returns: Dictionary with 'xp' and 'gold'
    """
    # TODO: Implement reward calculation
    xp_reward = enemy.get('xp_reward', 0)
    gold_reward = enemy.get('gold_reward', 0)
    
    return {
        'xp': xp_reward,
        'gold': gold_reward
    }

def display_combat_stats(character, enemy):
    """
    Display current combat status
    
    Shows both character and enemy health/stats
    """
    # TODO: Implement status display
    print(f"\n{character['name']}: HP={character['health']}/{character['max_health']} Level: {character['level']}")
    print(f"{enemy['name']}: HP={enemy['health']}/{enemy['max_health']} Level: {character['level']}")
    

def display_battle_log(message):
    """
    Display a formatted battle message
    """
    # TODO: Implement battle log display
    print(f"Battle Log: {message}")
    

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== COMBAT SYSTEM TEST ===")
    
    # Test enemy creation
    try:
        goblin = create_enemy("goblin")
        print(f"Created {goblin['name']}")
    except InvalidTargetError as e:
        print(f"Invalid enemy: {e}")
    
    # Test battle
    test_char = {
        'name': 'Hero',
        'class': 'Warrior',
        'health': 120,
        'max_health': 120,
        'strength': 15,
        'magic': 5
    }
    #
    battle = SimpleBattle(test_char, goblin)
    try:
        result = battle.start_battle()
        print(f"Battle result: {result}")
    except CharacterDeadError:
        print("Character is dead!")

