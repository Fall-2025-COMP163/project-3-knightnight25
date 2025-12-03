"""
COMP 163 - Project 3: Quest Chronicles
Game Data Module - Starter Code

Name: Kami Crews

AI Usage: [Document any AI assistance used]

This module handles loading and validating game data from text files.
"""

import os
from custom_exceptions import (
    InvalidDataFormatError,
    MissingDataFileError,
    CorruptedDataError
)

# ============================================================================
# DATA LOADING FUNCTIONS
# ============================================================================

def load_quests(filename="data/quests.txt"):
    """
    Load quest data from file
    
    Expected format per quest (separated by blank lines):
    QUEST_ID: unique_quest_name
    TITLE: Quest Display Title
    DESCRIPTION: Quest description text
    REWARD_XP: 100
    REWARD_GOLD: 50
    REQUIRED_LEVEL: 1
    PREREQUISITE: previous_quest_id (or NONE)
    
    Returns: Dictionary of quests {quest_id: quest_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle:
    # - FileNotFoundError → raise MissingDataFileError
    # - Invalid format → raise InvalidDataFormatError
    # - Corrupted/unreadable data → raise CorruptedDataError
    import os
    all_quests = {}

    if not os.path.exists(filename):
        raise MissingDataFileError(f"Quest file not found at: {filename}")
        
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f]
            
    except Exception as e:
        raise CorruptedDataError(f"Error reading quest file: {e}")

    quest_data_lines = []
    current_quest = {}
    
    for line in lines:
        if not line: 
            if current_quest:
                quest_data_lines.append(current_quest)
                current_quest = {}
            continue
        
        if ':' in line:
            key, value = line.split(':', 1)
            current_quest[key.strip()] = value.strip()
        else:
            raise InvalidDataFormatError(f"Quest line format error: '{line}' is missing a colon separator.")

    if current_quest:
        quest_data_lines.append(current_quest)
        
    required_keys = [
        "quest_id", "title", "description", 
        "reward_xp", "reward_gold", "required_level", "prerequisite"
    ]
    
    for raw_quest in quest_data_lines:
        
        for key in required_keys:
            if key not in raw_quest:
                quest_id = raw_quest.get("quest_id", "Unknown Quest")
                raise InvalidDataFormatError(f"Quest '{quest_id}' is missing required field: {key}")

        quest_id = raw_quest["quest_id"]
        
        try:
            quest_details = {
                "id": quest_id,
                "title": raw_quest["title"],
                "description": raw_quest["description"],
                "reward_xp": int(raw_quest["reward_xp"]),
                "reward_gold": int(raw_quest["reward_gold"]),
                "required_level": int(raw_quest["required_level"]),
                "prerequisite": raw_quest["prerequisite"] if raw_quest["prerequisite"].upper() != 'NONE' else None
            }
        except ValueError:
            raise CorruptedDataError(f"Quest '{quest_id}' has non-numeric value for a reward or level field.")
        
        if quest_id in all_quests:
            raise InvalidDataFormatError(f"Duplicate quest_id found: {quest_id}")
            
        all_quests[quest_id] = quest_details

    return all_quests

def load_items(filename="data/items.txt"):
    """
    Load item data from file
    
    Expected format per item (separated by blank lines):
    ITEM_ID: unique_item_name
    NAME: Item Display Name
    TYPE: weapon|armor|consumable
    EFFECT: stat_name:value (e.g., strength:5 or health:20)
    COST: 100
    DESCRIPTION: Item description
    
    Returns: Dictionary of items {item_id: item_data_dict}
    Raises: MissingDataFileError, InvalidDataFormatError, CorruptedDataError
    """
    # TODO: Implement this function
    # Must handle same exceptions as load_quests
    import os
    all_items = {}
    
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Item data file not found at: {filename}")
        
    try:
        with open(filename, 'r') as f:
            lines = [line.strip() for line in f]
            
    except Exception as e:
        raise IOError(f"Error reading item file: {e}")

    item_data_lines = []
    current_item = {}
    
    for line in lines:
        if not line:
            if current_item:
                item_data_lines.append(current_item)
                current_item = {}
            continue
        
        if ':' in line:
            key, value = line.split(':', 1)
            current_item[key.strip().lower()] = value.strip() 
        else:
            item_id = current_item.get("item_id", "Unknown Item in preceding block")
            raise ValueError(f"Invalid data format near item '{item_id}'. Line missing colon separator: '{line}'")

    if current_item:
        item_data_lines.append(current_item)
        
    required_keys = [
        "item_id", "name", "type", "effect", "cost", "description"
    ]
    
    for raw_item in item_data_lines:
        
        for key in required_keys:
            if key not in raw_item:
                item_id = raw_item.get("item_id", "unknown item")
                raise ValueError(f"Item '{item_id}' is missing required field: {key}")

        item_id = raw_item["item_id"]
        
        effect_raw = raw_item["effect"]
        if ':' not in effect_raw:
            raise ValueError(f"Item '{item_id}' has an invalid effect format: '{effect_raw}'. Expected 'stat:value'.")
        
        effect_stat, effect_value_raw = effect_raw.split(':', 1)
        
        try:
            cost = int(raw_item["cost"])
            effect_value = int(effect_value_raw.strip())
            
        except ValueError as e:
            raise ValueError(f"Item '{item_id}' has non-numeric value for 'cost' or 'effect' value. Details: {e}")
        
        item_type = raw_item["type"].lower()
        valid_types = {"weapon", "armor", "consumable"}
        if item_type not in valid_types:
            raise ValueError(f"Item '{item_id}' has invalid type: '{item_type}'. Must be one of {', '.join(valid_types)}.")
            
        item_details = {
            "id": item_id,
            "name": raw_item["name"],
            "type": item_type,
            "effect": {
                "stat": effect_stat.strip(),
                "value": effect_value
            },
            "cost": cost,
            "description": raw_item["description"]
        }
        
        if item_id in all_items:
            raise ValueError(f"Duplicate item_id found: {item_id}")
            
        all_items[item_id] = item_details

    return all_items

def validate_quest_data(quest_dict):
    """
    Validate that quest dictionary has all required fields
    
    Required fields: quest_id, title, description, reward_xp, 
                    reward_gold, required_level, prerequisite
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields
    """
    # TODO: Implement validation
    # Check that all required keys exist
    # Check that numeric values are actually numbers
    required_keys = [
        "id", "title", "description", 
        "reward_xp", "reward_gold", "required_level", "prerequisite"
    ]
    
    for key in required_keys:
        if key not in quest_dict:
            quest_id = quest_dict.get("id", "unknown quest")
            raise ValueError(f"Quest '{quest_id}' is missing required field: {key}")

    # Validate numeric fields
    numeric_keys = ["reward_xp", "reward_gold", "required_level"]
    
    for key in numeric_keys:
        value = quest_dict[key]
        if not isinstance(value, int) or value < 0:
            quest_id = quest_dict.get("id", "unknown quest")
            raise ValueError(f"Quest '{quest_id}' field '{key}' must be a non-negative integer. Received: {value}")

    return True

def validate_item_data(item_dict):
    """
    Validate that item dictionary has all required fields
    
    Required fields: item_id, name, type, effect, cost, description
    Valid types: weapon, armor, consumable
    
    Returns: True if valid
    Raises: InvalidDataFormatError if missing required fields or invalid type
    """
    # TODO: Implement validation
    required_keys = [
        "id", "name", "type", "effect", "cost", "description"
    ]
    valid_types = {"weapon", "armor", "consumable"}
    
    for key in required_keys:
        if key not in item_dict:
            item_id = item_dict.get("id", "unknown item")
            raise ValueError(f"item '{item_id}' is missing required field: {key}")

    item_id = item_dict["id"]
    item_type = item_dict["type"].lower()
    
    if item_type not in valid_types:
        raise ValueError(f"item '{item_id}' has invalid type: '{item_type}'. must be one of {', '.join(valid_types)}")

    cost = item_dict["cost"]
    if not isinstance(cost, int) or cost < 0:
        raise ValueError(f"item '{item_id}' cost must be a non-negative integer. received: {cost}")

    effect = item_dict["effect"]
    if not isinstance(effect, dict) or "stat" not in effect or "value" not in effect:
        raise ValueError(f"item '{item_id}' effect field is malformed. expected {{'stat': str, 'value': int}}")
    
    effect_value = effect["value"]
    if not isinstance(effect_value, int):
        raise ValueError(f"item '{item_id}' effect value must be an integer. received: {effect_value}")

    return True

def create_default_data_files():
    """
    Create default data files if they don't exist
    This helps with initial setup and testing
    """
    # TODO: Implement this function
    # Create data/ directory if it doesn't exist
    # Create default quests.txt and items.txt files
    # Handle any file permission errors appropriately
    import os
    data_directory = "data"
    
    try:
        if not os.path.exists(data_directory):
            os.makedirs(data_directory)
            print(f"created directory: {data_directory}/")
    except OSError as e:
        print(f"error creating directory '{data_directory}/': {e}")
        return 

    default_quests_content = """\
    quest_id: tutorial_1
    title: first steps
    description: talk to the elder in the village square.
    reward_xp: 10
    reward_gold: 5
    required_level: 1
    prerequisite: none

    quest_id: beginner_slayer
    title: the rat problem
    description: kill 3 pesky forest rats.
    reward_xp: 50
    reward_gold: 20
    required_level: 1
    prerequisite: tutorial_1
    """

    default_items_content = """
    item_id: rusty_sword
    name: rusty sword
    type: weapon
    effect: strength:3
    cost: 10
    description: a weak, old sword. better than nothing.

    item_id: leather_armor
    name: leather vest
    type: armor
    effect: magic:1
    cost: 15
    description: basic protection against minor threats.

    item_id: health_potion
    name: health potion
    type: consumable
    effect: health:25
    cost: 50
    description: restores a small amount of health instantly.
    """

    files_to_create = {
        "quests.txt": default_quests_content,
        "items.txt": default_items_content
    }

    for filename, content in files_to_create.items():
        filepath = os.path.join(data_directory, filename)
        
        if not os.path.exists(filepath):
            try:
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"created default file: {filepath}")
            except IOError as e:
                print(f"error writing to file '{filepath}': {e}")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_quest_block(lines):
    """
    Parse a block of lines into a quest dictionary
    
    Args:
        lines: List of strings representing one quest
    
    Returns: Dictionary with quest data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    # Split each line on ": " to get key-value pairs
    # Convert numeric strings to integers
    # Handle parsing errors gracefully
    quest_data = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if ': ' not in line:
            raise ValueError(f"Invalid quest format. Line must contain ': ' separator: '{line}'")
        
        key, value = line.split(': ', 1)
        key = key.strip().lower()
        value = value.strip()
        
        if not key:
            raise ValueError(f"Invalid quest format. Key is missing on line: '{line}'")

        quest_data[key] = value

    quest_id = quest_data.get('quest_id', 'unknown quest')
 
    numeric_fields = {
        "reward_xp": int, 
        "reward_gold": int, 
        "required_level": int
    }
    
    for field, field_type in numeric_fields.items():
        if field not in quest_data:
            raise ValueError(f"Quest '{quest_id}' block is missing required field: {field}")
            
        try:
            numeric_value = field_type(quest_data[field])
            if numeric_value < 0:
                 raise ValueError(f"Value cannot be negative.")
            quest_data[field] = numeric_value
        except ValueError as e:
            raise ValueError(f"Quest '{quest_id}' field '{field}' has corrupted or non-numeric data: '{quest_data[field]}'. Details: {e}")

    prerequisite_key = 'prerequisite'
    if prerequisite_key in quest_data:
        prereq_value = quest_data[prerequisite_key].upper()
        if prereq_value == 'NONE' or not prereq_value:
            quest_data[prerequisite_key] = None
        else:
            quest_data[prerequisite_key] = quest_data[prerequisite_key] 
    else:
        raise ValueError(f"Quest '{quest_id}' block is missing required field: {prerequisite_key}")

    return quest_data

def parse_item_block(lines):
    """
    Parse a block of lines into an item dictionary
    
    Args:
        lines: List of strings representing one item
    
    Returns: Dictionary with item data
    Raises: InvalidDataFormatError if parsing fails
    """
    # TODO: Implement parsing logic
    item_data = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue

        if ': ' not in line:
            raise ValueError(f"invalid item format. line must contain ': ' separator: '{line}'")
        
        key, value = line.split(': ', 1)
        key = key.strip().lower() 
        value = value.strip()
        
        if not key:
            raise ValueError(f"invalid item format. key is missing on line: '{line}'")

        item_data[key] = value

    item_id = item_data.get('item_id', 'unknown item')
    
    required_keys = ["item_id", "name", "type", "effect", "cost", "description"]
    for key in required_keys:
        if key not in item_data:
            raise ValueError(f"item '{item_id}' block is missing required field: {key}")

    try:
        cost = int(item_data["cost"])
        if cost < 0:
            raise ValueError("cost cannot be negative.")
        item_data["cost"] = cost
    except ValueError as e:
        raise ValueError(f"item '{item_id}' field 'cost' has corrupted or non-numeric data: '{item_data['cost']}'. details: {e}")

    effect_raw = item_data["effect"]
    if ':' not in effect_raw:
        raise ValueError(f"item '{item_id}' has an invalid effect format: '{effect_raw}'. expected 'stat:value'.")
    
    effect_stat, effect_value_raw = effect_raw.split(':', 1)
    
    try:
        effect_value = int(effect_value_raw.strip())
    except ValueError as e:
        raise ValueError(f"item '{item_id}' effect value is non-numeric: '{effect_value_raw}'. details: {e}")
 
    item_data["effect"] = {
        "stat": effect_stat.strip().lower(),
        "value": effect_value
    }

    item_type = item_data["type"].lower()
    valid_types = {"weapon", "armor", "consumable"}
    if item_type not in valid_types:
        raise ValueError(f"item '{item_id}' has invalid type: '{item_type}'. must be one of {', '.join(valid_types)}.")
    
    item_data["type"] = item_type
    
    return item_data

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== GAME DATA MODULE TEST ===")
    
    # Test creating default files
    create_default_data_files()
    
    # Test loading quests
    try:
        quests = load_quests()
        print(f"Loaded {len(quests)} quests")
    except MissingDataFileError:
        print("Quest file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid quest format: {e}")
    
    # Test loading items
    try:
        items = load_items()
        print(f"Loaded {len(items)} items")
    except MissingDataFileError:
        print("Item file not found")
    except InvalidDataFormatError as e:
        print(f"Invalid item format: {e}")

