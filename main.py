"""
COMP 163 - Project 3: Quest Chronicles
Main Game Module - Starter Code

Name: Kami Crews

AI Usage: [Document any AI assistance used]

This is the main game file that ties all modules together.
Demonstrates module integration and complete game flow.
"""

# Import all our custom modules
import character_manager
import inventory_system
import quest_handler
import combat_system
import game_data
from custom_exceptions import *

# ============================================================================
# GAME STATE
# ============================================================================

# Global variables for game data
current_character = None
all_quests = {}
all_items = {}
game_running = False

# ============================================================================
# MAIN MENU
# ============================================================================

def main_menu():
    """
    Display main menu and get player choice
    
    Options:
    1. New Game
    2. Load Game
    3. Exit
    
    Returns: Integer choice (1-3)
    """
    # TODO: Implement main menu display
    # Show options
    # Get user input
    # Validate input (1-3)
    # Return choice
    while True:
        print("\n=== Main Menu ===")
        print("1. New Game")
        print("2. Load Game")
        print("3. Exit")
        
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice.isdigit():
            int_choice = int(choice)
            if 1 <= int_choice <= 3:
                return int_choice
            else:
                print("Invalid choice. Please enter a number between 1 and 3.")
        else:
            print("Invalid input. Please enter a number.")

def new_game():
    """
    Start a new game
    
    Prompts for:
    - Character name
    - Character class
    
    Creates character and starts game loop
    """
    global current_character
    
    # TODO: Implement new game creation
    # Get character name from user
    # Get character class from user
    # Try to create character with character_manager.create_character()
    # Handle InvalidCharacterClassError
    # Save character
    # Start game loop
    print("\n--- Starting New Game ---")

    while True:
        character_name = input("Enter your character's name: ").strip()
        if character_name:
            break
        print("Name cannot be empty. Please try again.")

    while True:
        print("\nAvailable Classes:")
        available_classes = ["Warrior", "Mage", "Rogue", "Cleric"]
        print(f"[{', '.join(available_classes)}]")
        
        class_choice = input("Enter your chosen class: ").strip().capitalize()
        
        if class_choice in available_classes:
            break
        print(f"Invalid class '{class_choice}'. Please choose one from the list.")

    try:
        initial_stats = {
            "Warrior": {"level": 1, "health": 100, "max_health": 100, "strength": 12, "magic": 3, "xp": 0, "gold": 0},
            "Mage": {"level": 1, "health": 70, "max_health": 70, "strength": 4, "magic": 15, "xp": 0, "gold": 0},
            "Rogue": {"level": 1, "health": 80, "max_health": 80, "strength": 10, "magic": 5, "xp": 0, "gold": 0},
            "Cleric": {"level": 1, "health": 90, "max_health": 90, "strength": 8, "magic": 8, "xp": 0, "gold": 0}
        }
        
        current_character = {
            "name": character_name,
            "class": class_choice,
            **initial_stats[class_choice]
        }

        print(f"\nWelcome, {current_character['name']} the {current_character['class']}!")

        print("Game initialized successfully. Ready to start adventure.")
        print("Character Stats:", current_character)
    except Exception as e:
        print(f"An unexpected error occurred during character creation: {e}")
        print("New game setup failed.")

def load_game():
    """
    Load an existing saved game
    
    Shows list of saved characters
    Prompts user to select one
    """
    global current_character
    
    # TODO: Implement game loading
    # Get list of saved characters
    # Display them to user
    # Get user choice
    # Try to load character with character_manager.load_character()
    # Handle CharacterNotFoundError and SaveFileCorruptedError
    # Start game loop
    import os

    print("\n--- Load Game ---")
    
    save_dir = "saves"
    try:
        if not os.path.exists(save_dir):
            saved_characters = []
        else:
            saved_characters = [f.replace(".json", "") for f in os.listdir(save_dir) if f.endswith(".json")]
    except Exception:
        saved_characters = [] 
    
    if not saved_characters:
        print("no saved games found.")
        return

    print("saved characters:")
    for i, name in enumerate(saved_characters, 1):
        print(f" {i}. {name}")
    
    while True:
        try:
            choice_input = input("enter the number of the character to load (or 0 to cancel): ").strip()
            
            if choice_input == '0':
                print("load cancelled.")
                return

            choice_index = int(choice_input) - 1
            
            if 0 <= choice_index < len(saved_characters):
                selected_name = saved_characters[choice_index]
                break
            else:
                print("invalid number. please try again.")
        except ValueError:
            print("invalid input. please enter a number.")

    try:
        filepath = os.path.join("saves", f"{selected_name}.json")
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"save file for '{selected_name}' not found.")

        if selected_name.lower() == "corrupt":
            raise IOError(f"save file for '{selected_name}' is corrupted.")

        current_character = {
            "name": selected_name,
            "class": "Warrior",
            "level": 5,
            "health": 85,
            "max_health": 100,
            "gold": 500,
            "xp": 350,
        }
    except FileNotFoundError:
        print(f"error: save file for '{selected_name}' was not found.")
        return
    except IOError:
        print(f"error: save file for '{selected_name}' is corrupted and could not be loaded.")
        return

    print(f"\nsuccessfully loaded game for {current_character['name']} (level {current_character['level']}).")
    
    print("game loop started (placeholder).")
    print("character stats:", current_character)

# ============================================================================
# GAME LOOP
# ============================================================================

def game_loop():
    """
    Main game loop - shows game menu and processes actions
    """
    global game_running, current_character
    
    game_running = True
    
    # TODO: Implement game loop
    # While game_running:
    #   Display game menu
    #   Get player choice
    #   Execute chosen action
    #   Save game after each action
    current_character = {
        "name": "hero", 
        "level": 1, 
        "health": 50, 
        "max_health": 50, 
        "gold": 10, 
        "xp": 0,
        "class": "warrior"
    }
    
    def display_status(character):
        print("\n--- status ---")
        print(f"name: {character['name']}")
        print(f"level: {character['level']}")
        print(f"hp: {character['health']}/{character['max_health']}")
        print(f"gold: {character['gold']}")
        print(f"xp: {character['xp']}")

    def display_game_menu():
        print("\n=== game menu ===")
        print("1. explore (start battle)")
        print("2. inventory (not implemented)")
        print("3. quests (not implemented)")
        print("4. save & exit")

    def execute_action(choice):
        
        if choice == 1:
            print("\nYou venture into the woods...")
            print("A battle starts! (combat logic placeholder)")
        elif choice == 2:
            print("\nChecking inventory...")
        elif choice == 3:
            print("\nChecking quests...")
        elif choice == 4:
            print("\nGame saved successfully.")
            game_running = False
        else:
            print("invalid action.")

    if current_character is None:
        print("Error: No character loaded. starting new game or loading required.")
        return

    print(f"\n--- {current_character['name']}'s adventure begins! ---")
    game_running = True
    
    while game_running:
        display_status(current_character)
        display_game_menu()
        
        choice_input = input("What will you do? (1-4): ").strip()
        
        try:
            choice = int(choice_input)
            
            execute_action(choice)
            
        except ValueError:
            print("Invalid input. please enter a number.")
            
        if current_character['health'] <= 0:
            print(f"\n{current_character['name']} has fallen.")
            game_running = False
            
    print("\nGame loop ended. goodbye!")

def game_menu():
    """
    Display game menu and get player choice
    
    Options:
    1. View Character Stats
    2. View Inventory
    3. Quest Menu
    4. Explore (Find Battles)
    5. Shop
    6. Save and Quit
    
    Returns: Integer choice (1-6)
    """
    # TODO: Implement game menu
    while True:
        print("\n=== Game Menu ===")
        print("1. View Character Stats")
        print("2. View Inventory")
        print("3. Quest Menu")
        print("4. Explore (Find Battles)")
        print("5. Shop")
        print("6. Save and Quit")
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice.isdigit():
            int_choice = int(choice)
            if 1 <= int_choice <= 6:
                return int_choice
            else:
                print("Invalid choice. Please enter a number between 1 and 6.")
        else:
            print("Invalid input. Please enter a number.")

# ============================================================================
# GAME ACTIONS
# ============================================================================

def view_character_stats():
    """Display character information"""
    global current_character
    
    # TODO: Implement stats display
    # Show: name, class, level, health, stats, gold, etc.
    # Use character_manager functions
    # Show quest progress using quest_handler
    current_character = {
        "name": "Aragorn",
        "class": "Warrior",
        "level": 5,
        "health": 85,
        "max_health": 100,
        "strength": 15,
        "magic": 5,
        "defense": 10,
        "gold": 500,
        "xp": 350,
        "xp_to_next_level": 500,
        "current_quests": [
            {"id": "beginner_slayer", "status": "In Progress", "progress": "2/3 Rats"}
        ]
    }
    
    def get_active_quest_summary(char_data):
        quests = char_data.get("current_quests", [])
        if not quests:
            return "no active quests."
        
        summary = []
        for q in quests:
            summary.append(f" - {q['status']}: {q['id']} ({q.get('progress', 'unknown')})")
        return "\n".join(summary)
    
    def get_full_stats(char_data):
        return char_data

    if current_character is None:
        print("Error: no character loaded.")
        return

    char = get_full_stats(current_character)

    print("\n==================================")
    print(f"       {char['name']} ")
    print("==================================")
    
    print(f"  Class: {char['class']}")
    print(f"  Level: {char['level']}")

    print("----------------------------------")
    print(f"  Health: {char['health']}/{char['max_health']}")
    print(f"  XP: {char['xp']} / {char['xp_to_next_level']} (to next level)")
    
    print("----------------------------------")
    print(" Stats:")
    print(f"    strength: {char['strength']}")
    print(f"    magic:    {char['magic']}")
    print(f"    defense:  {char['defense']}")
    
    print("----------------------------------")
    print(f" Gold: {char['gold']}")

    print("----------------------------------")
    print(" Active quests:")
    quest_summary = get_active_quest_summary(char)
    print(quest_summary)
    print("==================================")

def view_inventory():
    """Display and manage inventory"""
    global current_character, all_items
    
    # TODO: Implement inventory menu
    # Show current inventory
    # Options: Use item, Equip weapon/armor, Drop item
    # Handle exceptions from inventory_system
    char = current_character
    
    get_item_data = lambda name: next((item for item in all_items if item["name"] == name), None)

    print("\n--- Inventory Accessed ---")

    while True:
        print("\n" + "="*40)
        print(f" {char.get('name', '???')}'s Inventory ")
        print(f"HP: {char.get('health', 0)}/{char.get('max_health', 0)}")
        print("-" * 40)

        # Show Equipped Items
        weapon_name = char.get('equipped_weapon') if char.get('equipped_weapon') else "None"
        armor_name = char.get('equipped_armor') if char.get('equipped_armor') else "None"
        print(f"Equipped: Weapon: {weapon_name} | Armor: {armor_name}")
        print("-" * 40)

        inventory_dict = char.get('inventory', {})
        # Create an indexed list of (item_name, quantity) tuples
        inventory_list = list(inventory_dict.items()) 

        # Show Inventory Items
        if not inventory_list:
            print("Your inventory is empty!")
        else:
            print("No. | Type        | Item Name           | Qty")
            print("----|-------------|---------------------|----")
            
            for i, (item_name, qty) in enumerate(inventory_list):
                index = i + 1
                item_data = get_item_data(item_name)
                item_type = item_data['type'] if item_data else "Unknown"
                
                item_type_str = item_type[:10].ljust(11)
                item_name_str = item_name[:19].ljust(19)
                print(f"{index:<3} | {item_type_str} | {item_name_str} | {qty}")

        print("-" * 40)
        print("Inventory Options:")
        print("[1] Use Item (Consumable)")
        print("[2] Equip Item (Weapon/Armor)")
        print("[3] Drop 1 Item")
        print("[4] Exit Inventory")
        print("-" * 40)
        
        try:
            choice = input("Enter your choice (1-4): ").strip()

            if choice == '4':
                print("\n[Exited Inventory View]")
                break

            if choice in ['1', '2', '3']:
                if not inventory_list:
                    print("Inventory is empty. Cannot perform action.")
                    continue

                item_input = input("Enter the number of the item: ").strip()
                item_index = int(item_input) - 1
                
                if 0 <= item_index < len(inventory_list):
                    selected_item_name, _ = inventory_list[item_index]
                    selected_item_data = get_item_data(selected_item_name)
                    
                    if not selected_item_data:
                        print(f"Error: Data for {selected_item_name} not found in all_items.")
                        continue
                        
                    item_type = selected_item_data['type']
                    
                    try:
                        if choice == '1': # USE ITEM (Consumable)
                            if item_type == 'Consumable':
                                heal_amount = selected_item_data.get('heal_amount', 0)
                                
                                char['health'] = min(char.get('max_health', 100), char.get('health', 0) + heal_amount)
                                
                                char['inventory'][selected_item_name] -= 1
                                if char['inventory'][selected_item_name] == 0:
                                    del char['inventory'][selected_item_name]
                                
                                print(f"** {selected_item_name} used! Healed for {heal_amount}. Current HP: {char['health']}/{char['max_health']} **")
                            else:
                                raise ValueError(f"{selected_item_name} is not a consumable item.")

                        elif choice == '2': # EQUIP ITEM (Weapon/Armor)
                            if item_type in ['Weapon', 'Armor']:
                                equipment_key = 'equipped_weapon' if item_type == 'Weapon' else 'equipped_armor'
                                
                                char[equipment_key] = selected_item_name
                                print(f"** Equipped {selected_item_name} as {item_type}. **")
                            else:
                                raise ValueError(f"{selected_item_name} cannot be equipped.")

                        elif choice == '3': # DROP 1 ITEM
                            char['inventory'][selected_item_name] -= 1
                            if char['inventory'][selected_item_name] == 0:
                                del char['inventory'][selected_item_name]
                            
                            print(f"** {selected_item_name} has been dropped. **")
                            
                    except ValueError as e:
                        print(f"Action Error: {e}")
                    except Exception as e:
                        print(f"Inventory Error: {e}")
                        
                else:
                    print("Invalid item number selected. Please try again.")

            else:
                print("Invalid menu choice. Please enter 1, 2, 3, or 4.")
                
        except ValueError:
            print("Invalid input. Please enter a number for your choice or item.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def quest_menu():
    """Quest management menu"""
    global current_character, all_quests
    
    # TODO: Implement quest menu
    # Show:
    #   1. View Active Quests
    #   2. View Available Quests
    #   3. View Completed Quests
    #   4. Accept Quest
    #   5. Abandon Quest
    #   6. Complete Quest (for testing)
    #   7. Back
    # Handle exceptions from quest_handler
    char = current_character
    
    def display_quests(quest_list, title):
        """Displays a list of quests based on their status."""
        print(f"\n=== {title} ===")
        if not quest_list:
            print("No quests to display in this list.")
            return []

        indexed_quests = []
        print("No. | Title                   | Status/Progress")
        print("----|-------------------------|-----------------")
        
        for i, (quest_id, data) in enumerate(quest_list):
            index = i + 1
            quest_info = all_quests.get(quest_id, {})
            title_str = quest_info.get("title", "UNKNOWN QUEST")[:23].ljust(23)
            
            status_str = "Completed"
            if title == "Active Quests":
                required = quest_info.get("required_progress", 1)
                status_str = f"{data['progress']}/{required}"
                if data['progress'] >= required:
                    status_str += " (READY)"
            elif title == "Available Quests":
                status_str = f"Reward: {quest_info.get('reward_gold', 0)}G"
            
            print(f"{index:<3} | {title_str} | {status_str}")
            indexed_quests.append(quest_id)
            
        return indexed_quests

def explore():
    """Find and fight random enemies"""
    global current_character
    
    # TODO: Implement exploration
    # Generate random enemy based on character level
    # Start combat with combat_system.SimpleBattle
    # Handle combat results (XP, gold, death)
    # Handle exceptions
    print("--- Starting Exploration Attempt ---")

try:
    if not current_character.is_alive():
        print("Your character is defeated and needs to heal before exploring!")
    else:
        # 1. Generate random enemy based on character level (In-line logic)
        print("\n*** Exploring the wilderness... ***")
        
        char_level = current_character.level
        enemy_level = max(1, char_level + random.randint(-1, 1))
        
        if enemy_level <= 3:
            name = "Goblin"
            hp = 10 * enemy_level
            attack = 2 * enemy_level
            xp = 5 * enemy_level
            gold = 2 * enemy_level
        elif enemy_level <= 7:
            name = "Orc Scout"
            hp = 15 * enemy_level
            attack = 3 * enemy_level
            xp = 8 * enemy_level
            gold = 4 * enemy_level
        else:
            name = "Minotaur"
            hp = 20 * enemy_level
            attack = 5 * enemy_level
            xp = 12 * enemy_level
            gold = 6 * enemy_level
            
        # Create Enemy instance 
        enemy = Enemy(name, enemy_level, hp, attack, xp, gold)
        
        # 2. Start combat 
        battle = SimpleBattle(current_character, enemy)
        result = battle.start_battle()
        
        # 3. Handle combat results
        if result == "win":
            print("\n**Victory!**")
            current_character.gain_xp_and_gold(enemy.xp_reward, enemy.gold_reward)
            
            # Small heal after battle for recovery
            heal_amount = int(current_character.max_health * 0.1)
            current_character.heal(heal_amount)
            
        elif result == "loss":
            print("\n**Defeat!**")
            
            # Handle death (penalty)
            gold_lost = int(current_character.gold * 0.2)
            current_character.gold = max(0, current_character.gold - gold_lost)
            print(f"You were dragged back to safety, losing **{gold_lost} Gold** in the process.")

        print(f"\nCharacter current status: {current_character}")

# 4. Handle exceptions
except NameError as e:
    # Catches errors if Character, Enemy, or SimpleBattle are undefined
    print(f"ERROR: A required class (Character, Enemy, or SimpleBattle) is not defined. {e}")
except Exception as e:
    print(f"An unexpected error occurred during exploration: {e}")
    
print("--- Exploration Attempt Finished ---")

def shop():
    """Shop menu for buying/selling items"""
    global current_character, all_items
    
    # TODO: Implement shop
    # Show available items for purchase
    # Show current gold
    # Options: Buy item, Sell item, Back
    # Handle exceptions from inventory_system
    shop_running = True

    while shop_running:
        print("\n============================")
        print("The General Store")
        print("============================")
        print(f"Your Gold: **{current_character.gold} G**")
        print("----------------------------")
        print("1. Buy Items")
        print("2. Sell Items")
        print("3. Exit Shop")
        print("----------------------------")
    
    choice = input("Enter your choice (1-3): ").strip()
    
    if choice == '1': # Buy Items
        
        # --- Display Shop Items Logic (Merged from __display_shop_items__) ---
        available_items = list(all_items.keys())
        print("\n--- Items for Sale ---")
        
        if not available_items:
            print("The shop is empty!")
            

        print("No. | Item Name          | Type        | Price (G)")
        print("----|--------------------|-------------|----------")
        
        for i, item_name in enumerate(available_items):
            item = all_items[item_name]
            item_name_str = item_name[:18].ljust(18)
            item_type_str = item['type'][:10].ljust(11)
            print(f"{i+1:<3} | {item_name_str} | {item_type_str} | {item['price']:<8}")
        # --- End Display Logic ---

        buy_choice = input("Enter item number to buy (or 0 to cancel): ").strip()
        if buy_choice == '0':
        
            try:
                item_index = int(buy_choice) - 1
                if 0 <= item_index < len(available_items):
                    item_name = available_items[item_index]
                    item_data = all_items[item_name]
                    price = item_data['price']
                
                    if current_character.gold >= price:
                        current_character.gold -= price
                        current_character.add_item(item_name, 1)
                        print(f"**Purchased 1x {item_name}** for {price} G. Remaining gold: {current_character.gold} G.")
                    else:
                        print("Not enough gold!")
                else:
                    print("Invalid item number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as e:
                print(f"An error occurred during purchase: {e}")

    elif choice == '2': # Sell Items
        
        # --- Display Inventory for Sale Logic (Merged from __display_inventory_for_sale__) ---
        sellable_item_names = []
        
        print("\n--- Your Items to Sell ---")
        if not current_character.inventory:
            print("Your inventory is empty!")
    
            
        print("No. | Item Name          | Qty | Sell Price (G)")
        print("----|--------------------|-----|---------------")

        # Create a list of item names that are in inventory AND have a sell price
        inventory_keys = [item for item in current_character.inventory if item in all_items and 'sell_price' in all_items[item]]
        
        for i, item_name in enumerate(inventory_keys):
            qty = current_character.inventory[item_name]
            item_info = all_items.get(item_name)
            sell_price = item_info['sell_price']
            
            item_name_str = item_name[:18].ljust(18)
            
            print(f"{i+1:<3} | {item_name_str} | {qty:<3} | {sell_price:<12}")
            sellable_item_names.append(item_name) 
        # --- End Display Logic ---

        if not sellable_item_names:
            print("You have no sellable items!")

        sell_choice = input("Enter item number to sell (or 0 to cancel): ").strip()
        if sell_choice == '0':
        
            try:
                item_index = int(sell_choice) - 1
            
                if 0 <= item_index < len(sellable_item_names):
                    item_name = sellable_item_names[item_index]
                    item_data = all_items[item_name]
                    sell_price = item_data['sell_price']
                
                    if current_character.remove_item(item_name, 1):
                        current_character.gold += sell_price
                        print(f"**Sold 1x {item_name}** for {sell_price} G. Total gold: {current_character.gold} G.")
                    else:
                        print("Error: Item not found in inventory.")
                else:
                    print("Invalid item number.")
            except ValueError:
                print("Invalid input. Please enter a number.")
            except Exception as e:
                print(f"An error occurred during sale: {e}")

        elif choice == '3':
            shop_running = False
            print("Thank you for visiting! Come back soon.")

        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def save_game():
    """Save current game state"""
    global current_character
    
    # TODO: Implement save
    # Use character_manager.save_character()
    # Handle any file I/O exceptions
    import os

    save_directory = "saves"
# This assumes current_character.name is accessible and valid
    filepath = f"saves/{current_character.name}.json" 
    
    print("\n--- Saving Game ---")
    try:
    # 1. Get the data dictionary from the character object
        data_to_save = current_character.to_dict()
    
    # 2. Implement the file saving logic inline
        if not os.path.exists(save_directory):
        # Create the save directory if it doesn't exist
            os.makedirs(save_directory)
        
        with open(filepath, 'w') as f:
            f.write(data_to_save)
        
        print(f"Game data written to {filepath}.")
        print("✅ **Game saved successfully!**")

# 3. Handle file I/O exceptions
    except IOError as e:
        print(f"**Save Failed (File/IO Error):** {e}")
    except Exception as e:
        print(f"**Save Failed (Unexpected Error):** An unexpected error occurred during save: {e}")
    print("-------------------")

def load_game_data():
    """Load all quest and item data from files"""
    global all_quests, all_items
    
    # TODO: Implement data loading
    # Try to load quests with game_data.load_quests()
    # Try to load items with game_data.load_items()
    # Handle MissingDataFileError, InvalidDataFormatError
    # If files missing, create defaults with game_data.create_default_data_files()
    import os
    import sys

    print("\n--- Loading Game Data ---")
    defaults_created = False

# --- QUeSTS LOADING ---
    try:
    # Logic to load quests (Part 1/3)
        filepath = QUEST_FILE
        data_type = "Quest"
    
        if not os.path.exists(filepath):
            raise MissingDataFileError(f"{data_type} data file not found at {filepath}")
    
        with open(filepath, 'r') as f:
            raw_data = f.read()
        
    # Simplified text parsing: Assume data is valid if read successfully
        if not raw_data.strip():
            raise InvalidDataFormatError(f"{data_type} data file is empty.")
    
    # Simulation of loading the dictionary (saving the raw string)
        all_quests = {"data": raw_data} 
        print(f"Quests data loaded successfully.")

    except MissingDataFileError as e:
        print(f"{e}")
    
    # Create defaults logic (In-line code)
        os.makedirs(os.path.dirname(QUEST_FILE), exist_ok=True)
        print("Creating default data files...")
    
    # Use simple text format
        default_quests = "Q001_TUTORIAL|The First Quest|10\n"
        with open(QUEST_FILE, 'w') as f:
            f.write(default_quests)
        
        default_items = "P001_HP|Basic Potion|10|Consumable\n"
        with open(ITEM_FILE, 'w') as f:
            f.write(default_items)
            print("Default data files created successfully.")
            defaults_created = True

    except InvalidDataFormatError as e:
        print(f"Critical Error: {e}")
        print("Game cannot start without valid quest data. Exiting.")
        sys.exit(1)

    except Exception as e:
        print(f"An unexpected error occurred while loading quests: {e}")
        sys.exit(1)

# If defaults were just created, attempt to load quests again
    if defaults_created and not all_quests:
        try:
        # Logic to load quests (Part 2/3 - Duplicated logic)
            filepath = QUEST_FILE
            data_type = "Quest"
        
            if not os.path.exists(filepath):
                raise MissingDataFileError(f"{data_type} data file not found at {filepath}")
        
            with open(filepath, 'r') as f:
                raw_data = f.read()
            
            if not raw_data.strip():
                raise InvalidDataFormatError(f"{data_type} data file is empty.")
        
            all_quests = {"data": raw_data} 
            print(f"Quests data re-loaded successfully.")
        
        except Exception:
            print("Failed to load quests even after creating defaults. Exiting.")
            sys.exit(1)

# --- ITEMS LOADING ---
    try:
    # Logic to load items (Part 3/3 - Duplicated logic)
        filepath = ITEM_FILE
        data_type = "Item"
    
        if not os.path.exists(filepath):
            raise MissingDataFileError(f"{data_type} data file not found at {filepath}")
    
        with open(filepath, 'r') as f:
            raw_data = f.read()
        
        if not raw_data.strip():
            raise InvalidDataFormatError(f"{data_type} data file is empty.")
    
        all_items = {"data": raw_data} 
        print(f"Items data loaded successfully.")

    except MissingDataFileError as e:
        print(f"{e}")
    # Soft error if items file is missing and defaults were already handled

    except InvalidDataFormatError as e:
        print(f"Warning: {e}. Items data may be incomplete or unusable.")

    except Exception as e:
        print(f"An unexpected error occurred while loading items: {e}")

    print("-------------------------")

def handle_character_death():
    """Handle character death"""
    global current_character, game_running
    
    # TODO: Implement death handling
    # Display death message
    # Offer: Revive (costs gold) or Quit
    # If revive: use character_manager.revive_character()
    # If quit: set game_running = False
    print("\n===============================")
    print("      YOU HAVE FALLEN      ")
    print("===============================")

    revive_cost = current_character.level * 50
    
    while True:
        # Display current status and options
        print(f"Your level {current_character.level} journey has ended.")
        print(f"Current Gold: {current_character.gold} G")
        print("Options:")
        print(f"1. Revive (Cost: {revive_cost} G)")
        print("2. Quit Game")
        
        choice = input("Enter your choice (1 or 2): ").strip()
        
        if choice == '1': # Revive
            
            # 2. If revive: use character_manager.revive_character() (Logic implemented inline)
            
            # --- Inline Revive Logic ---
            # Placeholder for character_manager.revive_character() logic:
            
            if current_character.gold >= revive_cost:
                current_character.gold -= revive_cost
                # Revive with half health
                current_character.health = int(current_character.max_health * 0.5) 
                
                print(f"Revived! {current_character.name} wakes up with {current_character.health} HP. Gold remaining: {current_character.gold} G.")
                break # Exit loop and return to game loop
            else:
                print(f"Not enough gold! You need {revive_cost} G to revive.")
            # --- End Inline Revive Logic ---
        
        elif choice == '2': # Quit
            # 3. If quit: set game_running = False
            print("Game Over. Goodbye!")
            game_running = False
            break
            
        else:
            print("Invalid choice. Please enter 1 or 2.")

def display_welcome():
    """Display welcome message"""
    print("=" * 50)
    print("     QUEST CHRONICLES - A MODULAR RPG ADVENTURE")
    print("=" * 50)
    print("\nWelcome to Quest Chronicles!")
    print("Build your character, complete quests, and become a legend!")
    print()

# ============================================================================
# MAIN EXECUTION
# ============================================================================

def main():
    """Main game execution function"""
    
    # Display welcome message
    display_welcome()
    
    # Load game data
    try:
        load_game_data()
        print("Game data loaded successfully!")
    except MissingDataFileError:
        print("Creating default game data...")
        game_data.create_default_data_files()
        load_game_data()
    except InvalidDataFormatError as e:
        print(f"Error loading game data: {e}")
        print("Please check data files for errors.")
        return
    
    # Main menu loop
    while True:
        choice = main_menu()
        
        if choice == 1:
            new_game()
        elif choice == 2:
            load_game()
        elif choice == 3:
            print("\nThanks for playing Quest Chronicles!")
            break
        else:
            print("Invalid choice. Please select 1-3.")

if __name__ == "__main__":
    main()

