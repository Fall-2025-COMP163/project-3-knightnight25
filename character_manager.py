"""
COMP 163 - Project 3: Quest Chronicles
Character Manager Module - Starter Code

Name: Kami Crews

AI Usage: [Document any AI assistance used]

This module handles character creation, loading, and saving.
"""

import os
from custom_exceptions import (
    InvalidCharacterClassError,
    CharacterNotFoundError,
    SaveFileCorruptedError,
    InvalidSaveDataError,
    CharacterDeadError
)

# ============================================================================
# CHARACTER MANAGEMENT FUNCTIONS
# ============================================================================

def create_character(name, character_class):
    """
    Create a new character with stats based on class
    
    Valid classes: Warrior, Mage, Rogue, Cleric
    
    Returns: Dictionary with character data including:
            - name, class, level, health, max_health, strength, magic
            - experience, gold, inventory, active_quests, completed_quests
    
    Raises: InvalidCharacterClassError if class is not valid
    """
    # TODO: Implement character creation
    # Validate character_class first
    # Example base stats:
    # Warrior: health=120, strength=15, magic=5
    # Mage: health=80, strength=8, magic=20
    # Rogue: health=90, strength=12, magic=10
    # Cleric: health=100, strength=10, magic=15
    
    # All characters start with:
    # - level=1, experience=0, gold=100
    # - inventory=[], active_quests=[], completed_quests=[]
    
    # Raise InvalidCharacterClassError if class not in valid list
    valid_classes = {
        "Warrior": {"health": 100, "strength": 15, "magic": 5},
        "Mage": {"health": 70, "strength": 8, "magic": 20},
        "Rogue": {"health": 80, "strength": 12, "magic": 10},
        "Cleric": {"health": 90, "strength": 10, "magic": 15}
    }
    
    if character_class not in valid_classes:
        raise InvalidCharacterClassError(f"Invalid character class: {character_class}")
    
    base_stats = valid_classes[character_class]

    character_data = {
        "name": name,
        "class": character_class,
        "health": base_stats["health"],
        "max_health": base_stats["health"],
        "strength": base_stats["strength"],
        "magic": base_stats["magic"],
        "level": 1,
        "experience": 0,
        "gold": 100,
        "inventory": [],
        "active_quests": [],
        "completed_quests": []
    }

    return character_data

def save_character(character, save_directory="data/save_games"):
    """
    Save character to file
    
    Filename format: {character_name}_save.txt
    
    File format:
    NAME: character_name
    CLASS: class_name
    LEVEL: 1
    HEALTH: 120
    MAX_HEALTH: 120
    STRENGTH: 15
    MAGIC: 5
    EXPERIENCE: 0
    GOLD: 100
    INVENTORY: item1,item2,item3
    ACTIVE_QUESTS: quest1,quest2
    COMPLETED_QUESTS: quest1,quest2
    
    Returns: True if successful
    Raises: PermissionError, IOError (let them propagate or handle)
    """
    # TODO: Implement save functionality
    # Create save_directory if it doesn't exist
    # Handle any file I/O errors appropriately
    # Lists should be saved as comma-separated values
    import os

    os.makedirs(save_directory, exist_ok=True)
    character_name = character["name"]
    filename = f"{character_name}_save.txt"
    full_path = os.path.join(save_directory, filename)

    save_data = [
        "name", "class", "level", "health", "max_health",
        "strength", "magic", "experience", "gold"
    ]

    comma_data = [
        "inventory", "active_quests", "completed_quests"
    ]

    try:
        with open(full_path, 'w') as f:
            for data in save_data:
                f.write(f"{data.upper()}: {character[data]}\n")

            for data in comma_data:
                all_data = ",".join(map(str, character[data]))
                f.write(f"{data.upper()}: {all_data}\n")
        return True
    except IOError as e:
        raise IOError(f"Error writing save file to {full_path}: {e}")
    except PermissionError as e:
        raise PermissionError(f"Permission denied for writing to {full_path}: {e}")

def load_character(character_name, save_directory="data/save_games"):
    """
    Load character from save file
    
    Args:
        character_name: Name of character to load
        save_directory: Directory containing save files
    
    Returns: Character dictionary
    Raises: 
        CharacterNotFoundError if save file doesn't exist
        SaveFileCorruptedError if file exists but can't be read
        InvalidSaveDataError if data format is wrong
    """
    # TODO: Implement load functionality
    # Check if file exists → CharacterNotFoundError
    # Try to read file → SaveFileCorruptedError
    # Validate data format → InvalidSaveDataError
    # Parse comma-separated lists back into Python lists
    filename = f"{character_name}_save.txt"
    full_path = os.path.join(save_directory, filename)

    if not os.path.exists(full_path):
        raise CharacterNotFoundError(f"No save file found for character: {character_name}")
    
    raw_data = {}

    try:
        with open(full_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue

                parts = line.split(': ', 1)
                if len(parts) == 2:
                    key = parts[0].strip().lower()
                    value = parts[1].strip()
                    raw_data[key] = value
    except IOError as e:
        raise SaveFileCorruptedError(f"File reading error for {full_path}: {e}")
    
    required_data = {
        "name": str, "class": str,
        "level": int, "health": int, "max_health": int,
        "strength": int, "magic": int, "experience": int, "gold": int
    }

    comma_list = ["inventory", "active_quests", "completed_quests"]

    character_data = {}

    try:
        for key, type_func in required_data.items():
            if key not in raw_data:
                raise InvalidCharacterClassError(f"Missing required key: {key.upper()}")
            
            if type_func is str:
                character_data[key] = raw_data[key]
            else:
                character_data[key] = type_func(raw_data[key])
            
        for key in comma_list:
            if key not in raw_data:
                character_data[key] = []
            else:
                list_str = raw_data[key]
                if not list_str:
                    character_data[key] = []
                else:
                    character_data[key] = [item.strip() for item in list_str.split(",")]
    except (ValueError, KeyError, TypeError) as e:
        raise InvalidSaveDataError(f"Data format error in {character_name}'s save file: {e}")
    
    if character_data.get("name") != character_name:
        raise InvalidSaveDataError(f"Name mismatch: File is for '{character_data.get('name')}', but requested '{character_name}'")
    
    return character_data

def list_saved_characters(save_directory="data/save_games"):
    """
    Get list of all saved character names
    
    Returns: List of character names (without _save.txt extension)
    """
    # TODO: Implement this function
    # Return empty list if directory doesn't exist
    # Extract character names from filenames
    import os 

    if not os.path.isdir(save_directory):
        return []
    
    saved_characters = []

    for filename in os.listdir(save_directory):
        if filename.endswith("_save.txt"):
            char_name = filename[:-len("_save.txt")]
            saved_characters.append(char_name)

    return saved_characters

def delete_character(character_name, save_directory="data/save_games"):
    """
    Delete a character's save file
    
    Returns: True if deleted successfully
    Raises: CharacterNotFoundError if character doesn't exist
    """
    # TODO: Implement character deletion
    # Verify file exists before attempting deletion
    filename = f"{character_name}_save.txt"
    filepath = os.path.join(save_directory, filename)

    if not os.path.exists(filepath):
        raise CharacterNotFoundError(f"Character save file not found for: {character_name}")
    
    os.remove(filepath)

    return True

# ============================================================================
# CHARACTER OPERATIONS
# ============================================================================

def gain_experience(character, xp_amount):
    """
    Add experience to character and handle level ups
    
    Level up formula: level_up_xp = current_level * 100
    Example when leveling up:
    - Increase level by 1
    - Increase max_health by 10
    - Increase strength by 2
    - Increase magic by 2
    - Restore health to max_health
    
    Raises: CharacterDeadError if character health is 0
    """
    # TODO: Implement experience gain and leveling
    # Check if character is dead first
    # Add experience
    # Check for level up (can level up multiple times)
    # Update stats on level up
    if character['health'] <= 0:
        raise CharacterDeadError(f"{character['name']} is dead and cannot gain experience.")
    
    character['experience'] += xp_amount

    while True:
        required_xp = character['level'] * 100

        if character['experience'] >= required_xp:
            character['level'] +=1
            character['max_health'] += 10
            character['strength'] += 2
            character['magic'] += 2
            character['health'] = character['max_health']
            character['experience'] -= required_xp
            print(f"{character['name']} levled up to Level {character['level']}!")
        else:
            break

def add_gold(character, amount):
    """
    Add gold to character's inventory
    
    Args:
        character: Character dictionary
        amount: Amount of gold to add (can be negative for spending)
    
    Returns: New gold total
    Raises: ValueError if result would be negative
    """
    # TODO: Implement gold management
    # Check that result won't be negative
    # Update character's gold
    new_gold = character.get('gold', 0) + amount

    if new_gold < 0:
        raise ValueError(f"{character['name']} cannot spend {abs(amount)} gold; current gold is {character.get('gold', 0)}, resulting in a negative total.")
    
    character['gold'] = new_gold
    return character['gold']

def heal_character(character, amount):
    """
    Heal character by specified amount
    
    Health cannot exceed max_health
    
    Returns: Actual amount healed
    """
    # TODO: Implement healing
    # Calculate actual healing (don't exceed max_health)
    # Update character health
    current_health = character.get('health', 0)
    max_health = character.get('max_health', 0)

    missing_health = max_health - current_health

    actual_heal_amount = min(amount, missing_health)

    character['health'] += actual_heal_amount

    return actual_heal_amount

def is_character_dead(character):
    """
    Check if character's health is 0 or below
    
    Returns: True if dead, False if alive
    """
    # TODO: Implement death check
    if character.get('health', 0) <= 0:
        return True
    else:
        return False

def revive_character(character):
    """
    Revive a dead character with 50% health
    
    Returns: True if revived
    """
    # TODO: Implement revival
    # Restore health to half of max_health
    if character.get('health', 0) <= 0 and 'max_health' in character:
        max_health = character['max_health']

        revival_health = max_health // 2

        character['health'] = max(1, revival_health)

        print(f"{character['name']} has been revived with {character['health']} health.")
        return True
    elif character.get('health', 0) > 0:
        print(f"{character['name']} is already alive.")
        return False
    else:
        print(f"Cannot revive {character['name']}: 'max_health' not defined or health is invalid.")
        return False

# ============================================================================
# VALIDATION
# ============================================================================

def validate_character_data(character):
    """
    Validate that character dictionary has all required fields
    
    Required fields: name, class, level, health, max_health, 
                    strength, magic, experience, gold, inventory,
                    active_quests, completed_quests
    
    Returns: True if valid
    Raises: InvalidSaveDataError if missing fields or invalid types
    """
    # TODO: Implement validation
    # Check all required keys exist
    # Check that numeric values are numbers
    # Check that lists are actually lists
    required_fields = {
        'name': str,
        'class': str,
        'level': int,
        'health': int,
        'max_health': int,
        'strength': int,
        'magic': int,
        'experience': int,
        'gold': int,
        'inventory': list,
        'active_quests': list
    }

    for field, expected_type in required_fields.items():
        if field not in character:
            raise InvalidSaveDataError(f"Missing required field: '{field}'")
        
        value = character[field]

        if expected_type == int:
            if not isinstance(value, (int, float)):
                raise InvalidSaveDataError(f"Field '{field}' must be an integer (or float), found type {type(value).__name__}")
            elif not isinstance(value, expected_type):
                raise InvalidSaveDataError(f"Field '{field}' must be of type {expected_type.__name__}, found type {type(value).__name__}")
            
    if character['level'] < 1:
        raise InvalidSaveDataError("Character 'level' must be at least 1")
    if character['max_health'] <= 0:
        raise InvalidSaveDataError("Character 'max_health' must be greater than 0")
    if character['health'] > character['max_health'] or character['health'] < 0:
        raise InvalidSaveDataError("Character 'health' must be between 0 and 'max_health'")

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== CHARACTER MANAGER TEST ===")
    
    # Test character creation
    try:
         char = create_character("TestHero", "Warrior")
         print(f"Created: {char['name']} the {char['class']}")
         print(f"Stats: HP={char['health']}, STR={char['strength']}, MAG={char['magic']}")
    except InvalidCharacterClassError as e:
         print(f"Invalid class: {e}")
    
    # Test saving
    try:
         save_character(char)
         print("Character saved successfully")
    except Exception as e:
         print(f"Save error: {e}")
    
    # Test loading
    try:
         loaded = load_character("TestHero")
         print(f"Loaded: {loaded['name']}")
    except CharacterNotFoundError:
         print("Character not found")
    except SaveFileCorruptedError:
         print("Save file corrupted")

