"""
COMP 163 - Project 3: Quest Chronicles
Inventory System Module - Starter Code

Name: Kami Crews

AI Usage: [Document any AI assistance used]

This module handles inventory management, item usage, and equipment.
"""

from custom_exceptions import (
    InventoryFullError,
    ItemNotFoundError,
    InsufficientResourcesError,
    InvalidItemTypeError
)

# Maximum inventory size
MAX_INVENTORY_SIZE = 20

# ============================================================================
# INVENTORY MANAGEMENT
# ============================================================================

def add_item_to_inventory(character, item_id):
    """
    Add an item to character's inventory
    
    Args:
        character: Character dictionary
        item_id: Unique item identifier
    
    Returns: True if added successfully
    Raises: InventoryFullError if inventory is at max capacity
    """
    # TODO: Implement adding items
    # Check if inventory is full (>= MAX_INVENTORY_SIZE)
    # Add item_id to character['inventory'] list
    if 'inventory' not in character:
        character['inventory'] = []

    inventory = character['inventory']

    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"{character['name']}'s inventory is full. Max capacity: {MAX_INVENTORY_SIZE}")
    
    inventory.append(item_id)
    return True

def remove_item_from_inventory(character, item_id):
    """
    Remove an item from character's inventory
    
    Args:
        character: Character dictionary
        item_id: Item to remove
    
    Returns: True if removed successfully
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement item removal
    # Check if item exists in inventory
    # Remove item from list
    inventory = character.get('inventory', [])

    if item_id not in inventory:
        if 'inventory' not in character:
            raise ItemNotFoundError(f"Character {character.get('name', '')} has no inventory list.")
        else:
            raise ItemNotFoundError(f"Item '{item_id}' not found in {character.get('name', '')}'s inventory.")
        
    inventory.remove(item_id)
    character['inventory'] = inventory
    return True

def has_item(character, item_id):
    """
    Check if character has a specific item
    
    Returns: True if item in inventory, False otherwise
    """
    # TODO: Implement item check
    inventory = character.get('inventory', [])
    return item_id in inventory

def count_item(character, item_id):
    """
    Count how many of a specific item the character has
    
    Returns: Integer count of item
    """
    # TODO: Implement item counting
    # Use list.count() method
    inventory = character.get('inventory', [])
    item_count = inventory.count(item_id)
    return item_count

def get_inventory_space_remaining(character):
    """
    Calculate how many more items can fit in inventory
    
    Returns: Integer representing available slots
    """
    # TODO: Implement space calculation
    current_items = len(character.get('inventory', []))
    space_remaining = MAX_INVENTORY_SIZE - current_items
    return max(0, space_remaining)

def clear_inventory(character):
    """
    Remove all items from inventory
    
    Returns: List of removed items
    """
    # TODO: Implement inventory clearing
    # Save current inventory before clearing
    # Clear character's inventory list
    if 'inventory' not in character or not isinstance(character['inventory'], list):
        character['inventory'] = []
        return []
    
    removed_items = list(character['inventory'])
    character['inventory'].clear()
    return removed_items

# ============================================================================
# ITEM USAGE
# ============================================================================

def use_item(character, item_id, item_data):
    """
    Use a consumable item from inventory
    
    Args:
        character: Character dictionary
        item_id: Item to use
        item_data: Item information dictionary from game_data
    
    Item types and effects:
    - consumable: Apply effect and remove from inventory
    - weapon/armor: Cannot be "used", only equipped
    
    Returns: String describing what happened
    Raises: 
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'consumable'
    """
    # TODO: Implement item usage
    # Check if character has the item
    # Check if item type is 'consumable'
    # Parse effect (format: "stat_name:value" e.g., "health:20")
    # Apply effect to character
    # Remove item from inventory
    inventory = character.get('inventory', [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"Item '{item_id}' not found in {character.get('name', '')}'s inventory.")
    
    item = item_data.get(item_id, {})
    item_type = item.get('type')
    if item_type != 'consumable':
        raise InvalidItemTypeError(f"Item '{item_id}' is of type '{item_type}' and cannot be used.")
    
    effect_str = item.get('effect', "")

    if not effect_str:
        character['inventory'].remoce(item_id)
        return f"{character['name']} used the {item.get('name', item_id)}, but nothing happened."
    
    try:
        stat_name, value_str = effect_str.split(':')
        stat_name = stat_name.strip()
        value = int(value_str.strip())
    except ValueError:
        character['inventory'].remove(item_id)
        return f"Warning: Item '{item.get('name', item_id)}' has an invalid effect format: '{effect_str}'. It was consumed."
    
    original_value = character.get(stat_name, 0)

    if stat_name == 'health':
        max_health = character.get('max_health', original_value)
        new_health = min(original_value + value, max_health)
        heal_amount = new_health - original_value
        character['health'] = new_health
        result_message = f"{character['name']} healed for {heal_amount} health."
    elif stat_name == 'experience':
        character['experience'] = original_value + value
        result_message = f"{character['name']} gained {value} experience points."
    elif stat_name in character:
        character[stat_name] = original_value + value
        result_message = f"{character['name']}'s {stat_name} increased by {value}."
    else:
        result_message = f"{character['name']} used the {item.get('name', item_id)}, but the effect on {stat_name} could not be applied."

    character['inventory'].remove(item_id)
    return f"Used {item.get('name', item_id)}. {result_message}"

def equip_weapon(character, item_id, item_data):
    """
    Equip a weapon
    
    Args:
        character: Character dictionary
        item_id: Weapon to equip
        item_data: Item information dictionary
    
    Weapon effect format: "strength:5" (adds 5 to strength)
    
    If character already has weapon equipped:
    - Unequip current weapon (remove bonus)
    - Add old weapon back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'weapon'
    """
    # TODO: Implement weapon equipping
    # Check item exists and is type 'weapon'
    # Handle unequipping current weapon if exists
    # Parse effect and apply to character stats
    # Store equipped_weapon in character dictionary
    # Remove item from inventory
    if 'inventory' not in character:
        character['inventory'] = []

    if item_id not in character['inventory']:
        raise ItemNotFoundError(f"Item '{item_id}' not found in {character.get('name', '')}'s inventory.")
    
    weapon_item = item_data.get(item_id, {})
    weapon_name = weapon_item.get('name', item_id)

    item_type = weapon_item.get('type')
    if item_type != 'weapon':
        raise InvalidItemTypeError(f"Item '{weapon_name}' is of type '{item_type}' and cannot be equipped as a weapon.")
    
    new_weapon_effect_str = weapon_item.get('effect', "")
    equipped_weapon_id = character.get('equipped_weapon')
    
    return_message = ""

    if equipped_weapon_id:
        old_weapon_item = item_data.get(equipped_weapon_id, {})
        old_weapon_name = old_weapon_item.get('name', equipped_weapon_id)
        old_weapon_effect_str = old_weapon_item.get('effect', "")

        if old_weapon_effect_str:
            try:
                stat_name, value_str = old_weapon_effect_str.split(':')
                stat_name = stat_name.strip()
                value = int(value_str.strip()) * -1
            except ValueError:
                print(f"Warning: Old weapon effect format invalid: '{old_weapon_effect_str}'. Skipping stat change.")
                value = 0
            if value != 0 and stat_name in character:
                character[stat_name] = character[stat_name] + value
                if stat_name != 'health':
                    character[stat_name] = max(0, character[stat_name])
                elif value != 0:
                    print(f"Warning: Stat '{stat_name}' not found on character. Skipping stat change.")

        character['inventory'].remove(item_id)

        if new_weapon_effect_str:
            try:
                stat_name, value_str = new_weapon_effect_str.split(':')
                stat_name = stat_name.strip()
                value = int(value_str.strip()) * 1
            except ValueError:
                print(f"Warning: New weapon effect format invalid: '{new_weapon_effect_str}'. Skipping stat change.")
                value = 0

            if value != 0 and stat_name in character:
                character[stat_name] = character[stat_name] + value
                if stat_name != 'health':
                    character[stat_name] = max(0, character[stat_name])
                elif value != 0:
                    print(f"Warning: Stat '{stat_name}' not found on character. Skipping stat change.")

        character['equipped_weapon'] = item_id
        return_message += f"Equipped **{weapon_name}**."
        return return_message

def equip_armor(character, item_id, item_data):
    """
    Equip armor
    
    Args:
        character: Character dictionary
        item_id: Armor to equip
        item_data: Item information dictionary
    
    Armor effect format: "max_health:10" (adds 10 to max_health)
    
    If character already has armor equipped:
    - Unequip current armor (remove bonus)
    - Add old armor back to inventory
    
    Returns: String describing equipment change
    Raises:
        ItemNotFoundError if item not in inventory
        InvalidItemTypeError if item type is not 'armor'
    """
    # TODO: Implement armor equipping
    # Similar to equip_weapon but for armor
    if 'inventory' not in character:
        character['inventory'] = []

    if item_id not in character['inventory']:
        raise ValueError(f"ItemNotFoundError: Item '{item_id}' not found in {character.get('name', '')}'s inventory.")
    
    armor_item = item_data.get(item_id, {})
    armor_name = armor_item.get('name', item_id)

    item_type = armor_item.get('type')
    armor_slot = armor_item.get('slot')

    if item_type != 'armor':
        raise TypeError(f"InvalidItemTypeError: Item '{armor_name}' is of type '{item_type}' and cannot be equipped as armor.")
    
    if not armor_slot or armor_slot not in ['head', 'chest', 'legs', 'boots']:
        raise KeyError(f"Armor item '{armor_name}' is missing a valid 'slot' property.")
    
    slot_key = f"equipped_{armor_slot}"
    new_armor_effect_str = armor_item.get('effect', "")
    equipped_armor_id = character.get(slot_key)
    return_message = ""

    if equipped_armor_id:
        old_armor_item = item_data.get(equipped_armor_id, {})
        old_armor_name = old_armor_item.get('name', equipped_armor_id)
        old_armor_effect_str = old_armor_item.get('effect', "")

        if old_armor_effect_str:
            try:
                stat_name, value_str = old_armor_effect_str.split(':')
                stat_name = stat_name.strip()
                value = int(value_str.strip()) * -1
            except ValueError:
                print(f"Warning: Old armor effect format invalid: '{old_armor_effect_str}'. Skipping stat change.")
                value = 0
            
            if value != 0 and stat_name in character:
                character[stat_name] = character[stat_name] + value

                if stat_name not in ['health', 'max_health']:
                    character[stat_name] = max(0, character[stat_name])
                
                if stat_name == 'max_health' and value < 0:
                    if character.get('health', 0) > character['max_health']:
                        character['health'] = character['max_health']
            elif value != 0:
                print(f"Warning: Stat '{stat_name}' not found on character. Skipping stat change.")
            
        character['inventory'].append(equipped_armor_id)
        return_message += f"Unequipped {old_armor_name} ({armor_slot}) and return it to inventory."

    character['inventory'].remove(item_id)

    if new_armor_effect_str:
        try:
            stat_name, value_str = new_armor_effect_str.split(':')
            stat_name = stat_name.strip()
            value = int(value_str.strip()) * 1
        except ValueError:
            print(f"Warning: New armor effect format invalid: '{new_armor_effect_str}'. Skipping stat change.")
            value = 0
        
        if value != 0 and stat_name in character:
            character[stat_name] = character[stat_name] + value

            if stat_name not in ['health', 'max_health']:
                character[stat_name] = max(0, character[stat_name])
        elif value != 0:
            print(f"Warning: Stat '{stat_name}' not found on character. Skipping stat change.")

    character[slot_key] = item_id

    return_message += f"Equipped **{armor_name}** in the {armor_slot} slot."
    return return_message

def unequip_weapon(character):
    """
    Remove equipped weapon and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no weapon equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement weapon unequipping
    # Check if weapon is equipped
    # Remove stat bonuses
    # Add weapon back to inventory
    # Clear equipped_weapon from character
    equipped_weapon_id = character.get('equipped_weapon')

    if not equipped_weapon_id:
        return None
    
    inventory = character.get('inventory', [])
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"{character.get('name', 'Character')}'s invenotry is full. Cannot unequip weapon.")
    
    print(f"Warning: Stat bonuses for {equipped_weapon_id} were not removed from {character.get('name', 'character')}'s stats.")

    character['inventory'].append(equipped_weapon_id)

    del character['equipped_weapon']
    return equipped_weapon_id

def unequip_armor(character):
    """
    Remove equipped armor and return it to inventory
    
    Returns: Item ID that was unequipped, or None if no armor equipped
    Raises: InventoryFullError if inventory is full
    """
    # TODO: Implement armor unequipping
    armor_slots = ['head', 'chest', 'legs', 'boots']
    unequipped_items = []

    inventory = character.get('inventory', [])
    equipped_count = 0

    for slot in armor_slots:
        if character.get(f'equipped_{slot}'):
            equipped_count += 1

    if len(inventory) + equipped_count > MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"{character.get('name', 'Character')}'s inventory is full. Cannot unequip {equipped_count} armor pieces.")
    
    for slot in armor_slots:
        slot_key = f'equipped_{slot}'
        equipped_armor_id = character.get(slot_key)

        if equipped_armor_id:
            print(f"Warning: Stat bonuses for {equipped_armor_id} ({slot}) were not removed from {character.get('name', 'character')}'s stats.")

            inventory.append(equipped_armor_id)
            unequipped_items.append(equipped_armor_id)

            del character[slot_key]
    
    character['inventory'] = inventory

    if not unequipped_items:
        return None
    else:
        return unequipped_items

# ============================================================================
# SHOP SYSTEM
# ============================================================================

def purchase_item(character, item_id, item_data):
    """
    Purchase an item from a shop
    
    Args:
        character: Character dictionary
        item_id: Item to purchase
        item_data: Item information with 'cost' field
    
    Returns: True if purchased successfully
    Raises:
        InsufficientResourcesError if not enough gold
        InventoryFullError if inventory is full
    """
    # TODO: Implement purchasing
    # Check if character has enough gold
    # Check if inventory has space
    # Subtract gold from character
    # Add item to inventory
    item = item_data.get(item_id)
    if not item:
        raise KeyError(f"Item ID '{item_id}' not found in item_data.")
    
    cost = item.get('cost')
    if cost is None:
        raise KeyError(f"Item '{item_id}' is missing the 'cost' field.")
    
    character_gold = character.get('gold', 0)

    if character_gold < cost:
        raise InsufficientResourcesError(f"Cannot purchase '{item.get('name', item_id)}'. Requires {cost} gold but {character.get('name', 'character')} only has {character_gold} gold.")
    
    inventory = character.get('inventory', [])
    if len(inventory) >= MAX_INVENTORY_SIZE:
        raise InventoryFullError(f"{character.get('name', 'character')}'s inventory is full. Max capacisty: {MAX_INVENTORY_SIZE}")
    
    character['gold'] = character_gold - cost

    inventory.append(item_id)
    character['inventory'] = inventory
    return True

def sell_item(character, item_id, item_data):
    """
    Sell an item for half its purchase cost
    
    Args:
        character: Character dictionary
        item_id: Item to sell
        item_data: Item information with 'cost' field
    
    Returns: Amount of gold received
    Raises: ItemNotFoundError if item not in inventory
    """
    # TODO: Implement selling
    # Check if character has item
    # Calculate sell price (cost // 2)
    # Remove item from inventory
    # Add gold to character
    inventory = character.get('inventory', [])
    if item_id not in inventory:
        raise ItemNotFoundError(f"ItemNotFoundError: Item '{item_id}' not found in {character.get('name', '')}'s inventory.")
    
    item = item_data.get(item_id)
    if not item:
        raise KeyError(f"Item ID '{item_id}' not found in item_data.")
    
    cost = item.get('cost')
    if cost is None:
        raise KeyError(f"Item '{item_id}' is missing the 'cost' field.")
    
    equipped_keys = ['equipped_weapon', 'equipped_head', 'equipped_chest', 'equipped_legs', 'equipped_boots']
    for key in equipped_keys:
        if character.get(key) == item_id:
            raise ValueError(f"Item '{item_id}' is currently equipped as a'{key.replace('equipped_', '')}' and must be unequipped before selling.")
        
    sell_price = cost // 2

    inventory.remove(item_id)
    character['inventory'] = inventory

    character['gold'] = character.get('gold', 0) + sell_price
    return sell_price
    

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def parse_item_effect(effect_string):
    """
    Parse item effect string into stat name and value
    
    Args:
        effect_string: String in format "stat_name:value"
    
    Returns: Tuple of (stat_name, value)
    Example: "health:20" → ("health", 20)
    """
    # TODO: Implement effect parsing
    # Split on ":"
    # Convert value to integer
    if not effect_string:
        raise ValueError("Effect string cannot be empty.")
    
    parts = effect_string.split(':')

    if len(parts) != 2:
        raise ValueError(f"Effect string must be in 'stat_name:value' format. Found: '{effect_string}'")
    
    stat_name = parts[0].strip()
    value_str = parts[1].strip()

    if not stat_name:
        raise ValueError("Stat name cannot be empty.")
    
    try:
        value = int(value_str)
    except ValueError:
        raise ValueError(f"Value '{value_str}' in effect string must be an integer.")
    
    return (stat_name, value)

def apply_stat_effect(character, stat_name, value):
    """
    Apply a stat modification to character
    
    Valid stats: health, max_health, strength, magic
    
    Note: health cannot exceed max_health
    """
    # TODO: Implement stat application
    # Add value to character[stat_name]
    # If stat is health, ensure it doesn't exceed max_health
    valid_stats = ['health', 'max_health', 'strength', 'magic']
    if stat_name not in valid_stats:
        print(f"Warning: Invalid stat name '{stat_name}' for character {character.get('name', 'unknown')}. Skipping application.")
        return
    
    if stat_name not in character:
        if stat_name == 'health' or stat_name == 'max_health':
            character[stat_name] = 0
        else:
            character[stat_name] = 0

    character[stat_name] += value

    if stat_name in ['max_health', 'strength', 'magic']:
        character[stat_name] = max(0, character[stat_name])

    if stat_name == 'health':
        max_health = character.get('max_health', character['health'])

        if character['health'] > max_health:
            character['health'] = max_health

        character['health'] = max(0, character['health'])

    if stat_name == 'max_health' and 'health' in character:
        if character['health'] > character['max_health']:
            character['health'] = character['max_health']

def display_inventory(character, item_data_dict):
    """
    Display character's inventory in formatted way
    
    Args:
        character: Character dictionary
        item_data_dict: Dictionary of all item data
    
    Shows item names, types, and quantities
    """
    # TODO: Implement inventory display
    # Count items (some may appear multiple times)
    # Display with item names from item_data_dict
    inventory = character.get('inventory', [])
    char_name = character.get('name', 'The Character')

    if not inventory:
        print(f"Inventory for {char_name} is empty.")
        return
    
    item_counts = {}
    for item_id in inventory:
        item_counts[item_id] = item_counts.get(item_id, 0) + 1
    
    print(f"\n--- {char_name}'s Inventory ({len(inventory)}/{MAX_INVENTORY_SIZE}) ---")
    print(f"Gold: {character.get('gold', 0)}")
    print("-" * 35)

    equipped = {}
    equipped_keys = ['equipped_weapon', 'equipped_head', 'equipped_chest', 'equipped_legs', 'equipped_boots']
    for key in equipped_keys:
        item_id = character.get(key)
        if item_id:
            slot_name = key.replace('equipped_', '').capitalize()
            equipped[item_id] = slot_name

    sorted_item_ids = sorted(item_counts.keys(), key=lambda x: item_data_dict.get(x, {}).get('name', x))

    for item_id in sorted_item_ids:
        count = item_counts[item_id]
        item_data = item_data_dict.get(item_id, {})

        name = item_data.get('name', item_id)
        item_type = item_data.get('type', 'Unknown')

        equipped_status = ""
        if item_id in equipped:
            equipped_status = f" [EQ - {equipped[item_id]}]"

        if count > 1:
            print(f"| {name:<20} x{count:<2} ({item_type}){equipped_status}")
        else:
            print(f"| {name:<20}    ({item_type}){equipped_status}")
        
        print("-" * 35)

# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== INVENTORY SYSTEM TEST ===")
    
    # Test adding items
    test_char = {'inventory': [], 'gold': 100, 'health': 80, 'max_health': 80}
    # 
    try:
        add_item_to_inventory(test_char, "health_potion")
        print(f"Inventory: {test_char['inventory']}")
    except InventoryFullError:
         print("Inventory is full!")
    
    # Test using items
    test_item = {
        'item_id': 'health_potion',
        'type': 'consumable',
        'effect': 'health:20'
    }
    # 
    try:
        result = use_item(test_char, "health_potion", test_item)
        print(result)
    except ItemNotFoundError:
        print("Item not found")

