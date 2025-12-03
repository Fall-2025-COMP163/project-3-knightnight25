"""
COMP 163 - Project 3: Quest Chronicles
Quest Handler Module - Starter Code

Name: Kami Crews

AI Usage: [Document any AI assistance used]

This module handles quest management, dependencies, and completion.
"""

from custom_exceptions import (
    QuestNotFoundError,
    QuestRequirementsNotMetError,
    QuestAlreadyCompletedError,
    QuestNotActiveError,
    InsufficientLevelError
)

# ============================================================================
# QUEST MANAGEMENT
# ============================================================================

def accept_quest(character, quest_id, quest_data_dict):
    """
    Accept a new quest
    
    Args:
        character: Character dictionary
        quest_id: Quest to accept
        quest_data_dict: Dictionary of all quest data
    
    Requirements to accept quest:
    - Character level >= quest required_level
    - Prerequisite quest completed (if any)
    - Quest not already completed
    - Quest not already active
    
    Returns: True if quest accepted
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        InsufficientLevelError if character level too low
        QuestRequirementsNotMetError if prerequisite not completed
        QuestAlreadyCompletedError if quest already done
    """
    # TODO: Implement quest acceptance
    # Check quest exists
    # Check level requirement
    # Check prerequisite (if not "NONE")
    # Check not already completed
    # Check not already active
    # Add to character['active_quests']
    quest = quest_data_dict.get(quest_id)
    if not quest:
        raise QuestNotFoundError(f"Quest ID '{quest_id}' not found in quest data.")
    
    required_level = quest.get('required_level', 1)
    prereq_quest = quest.get('prerequisite', "NONE")

    character_level = character.get('level', 1)
    active_quests = character.get('active_quests', [])
    completed_quests = character.get('completed_quests', [])

    if quest_id in completed_quests:
        raise QuestAlreadyCompletedError(f"Quest '{quest.get('name', quest_id)}' is already completed.")
    
    if quest_id in active_quests:
        raise InsufficientLevelError(f"Character level {character_level} is too low. Required level: {required_level}.")
    
    if prereq_quest != "NONE":
        if prereq_quest not in completed_quests:
            prereq_name = quest_data_dict.get(prereq_quest, {}).get('name', prereq_quest)
            raise QuestRequirementsNotMetError(f"Prerequisite quest '{prereq_name}' must be completed first.")
        
    active_quests.append(quest_id)
    character['active_quests'] = active_quests

    return True 

def complete_quest(character, quest_id, quest_data_dict):
    """
    Complete an active quest and grant rewards
    
    Args:
        character: Character dictionary
        quest_id: Quest to complete
        quest_data_dict: Dictionary of all quest data
    
    Rewards:
    - Experience points (reward_xp)
    - Gold (reward_gold)
    
    Returns: Dictionary with reward information
    Raises:
        QuestNotFoundError if quest_id not in quest_data_dict
        QuestNotActiveError if quest not in active_quests
    """
    # TODO: Implement quest completion
    # Check quest exists
    # Check quest is active
    # Remove from active_quests
    # Add to completed_quests
    # Grant rewards (use character_manager.gain_experience and add_gold)
    # Return reward summary
    quest = quest_data_dict.get(quest_id)
    if not quest:
        raise QuestNotFoundError(f"Quest ID '{quest_id}' not found in quest data.")
    
    active_quests = character.get('active_quests', [])
    completed_quests = character.get('completed_quests', [])

    if quest_id not in active_quests:
        raise QuestNotActiveError(f"Quest '{quest.get('name', quest_id)}' is not currently active.")
    
    reward_xp = quest.get('reward_xp', 0)
    reward_gold = quest.get('reward_gold', 0)

    active_quests.remove(quest_id)
    character['active_quests'] = active_quests

    completed_quests.append(quest_id)
    character['completed_quests'] = completed_quests

    if reward_xp > 0:
        character['experience'] = character.get('experience', 0) + reward_xp

        while True:
            current_level = character.get('level', 1)
            required_xp = current_level * 100
            
            if character['experience'] >= required_xp:
                character['level'] += 1
                character['max_health'] += 10
                character['strength'] += 2
                character['magic'] += 2
                character['health'] = character['max_health']
                character['experience'] -= required_xp
                print(f"{character['name']} leveled up to level {character['level']}!")
            else:
                break
    
    if reward_gold > 0:
        character['gold'] = character.get('gold', 0) + reward_gold

    return {
        "quest_id": quest_id,
        "name": quest.get('name', quest_id),
        "reward_xp": reward_xp,
        "reward_gold": reward_gold
    }

def abandon_quest(character, quest_id):
    """
    Remove a quest from active quests without completing it
    
    Returns: True if abandoned
    Raises: QuestNotActiveError if quest not active
    """
    # TODO: Implement quest abandonment
    active_quests = character.get('active_quests', [])

    if quest_id not in active_quests:
        raise QuestNotActiveError(f"Quest ID '{quest_id}' is not currently active an cannot be abandoned.")
    
    active_quests.remove(quest_id)
    character['active_quests'] = active_quests

    return True

def get_active_quests(character, quest_data_dict):
    """
    Get full data for all active quests
    
    Returns: List of quest dictionaries for active quests
    """
    # TODO: Implement active quest retrieval
    # Look up each quest_id in character['active_quests']
    # Return list of full quest data dictionaries
    active_quest_ids = character.get('active_quests', [])
    active_quests_data = []

    for quest_id in active_quest_ids:
        quest_data = quest_data_dict.get(quest_id)

        if quest_data:
            active_quests_data.append(quest_data)
    
    return active_quests_data

def get_completed_quests(character, quest_data_dict):
    """
    Get full data for all completed quests
    
    Returns: List of quest dictionaries for completed quests
    """
    # TODO: Implement completed quest retrieval
    completed_quest_ids = character.get('completed_quests', [])
    completed_quests_data = []

    for quest_id in completed_quest_ids:
        quest_data = quest_data_dict.get(quest_id)

        if quest_data:
            completed_quests_data.append(quest_data)

    return completed_quests_data

def get_available_quests(character, quest_data_dict):
    """
    Get quests that character can currently accept
    
    Available = meets level req + prerequisite done + not completed + not active
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement available quest search
    # Filter all quests by requirements
    available_quests = []

    character_level = character.get('level', 1)
    active_quests = character.get('active_quests', [])
    completed_quests = character.get('completes_quests', [])

    for quest_id, quest_data in quest_data_dict.items():
        if quest_id in completed_quests:
            continue
        
        if quest_id in active_quests:
            continue

        required_level = quest_data.get('required_level', 1)
        if character_level < required_level:
            continue

        prereq_quest = quest_data.get('prerequisite', "NONE")

        if prereq_quest != "NONE":
            if prereq_quest not in completed_quests:
                continue

    return available_quests

# ============================================================================
# QUEST TRACKING
# ============================================================================

def is_quest_completed(character, quest_id):
    """
    Check if a specific quest has been completed
    
    Returns: True if completed, False otherwise
    """
    # TODO: Implement completion check
    completed_quests = character.get('completed_quests', [])
    return quest_id in completed_quests

def is_quest_active(character, quest_id):
    """
    Check if a specific quest is currently active
    
    Returns: True if active, False otherwise
    """
    # TODO: Implement active check
    active_quests = character.get('active_quests', [])
    return quest_id in active_quests

def can_accept_quest(character, quest_id, quest_data_dict):
    """
    Check if character meets all requirements to accept quest
    
    Returns: True if can accept, False otherwise
    Does NOT raise exceptions - just returns boolean
    """
    # TODO: Implement requirement checking
    # Check all requirements without raising exceptions
    quest = quest_data_dict.get(quest_id)
    if not quest:
        return False
    
    required_level = quest.get('required_level', 1)
    prereq_quest = quest.get('prerequisite', "NONE")

    character_level = character.get('level', 1)
    active_quests = character.get('active_quests', [])
    completed_quests = character.get('completed_quests', [])

    if quest_id in completed_quests:
        return False
    
    if quest_id in active_quests:
        return False
    
    if character_level < required_level:
        return False
    
    if prereq_quest != "NONE":
        if prereq_quest not in completed_quests:
            return False
    
    return True

def get_quest_prerequisite_chain(quest_id, quest_data_dict):
    """
    Get the full chain of prerequisites for a quest
    
    Returns: List of quest IDs in order [earliest_prereq, ..., quest_id]
    Example: If Quest C requires Quest B, which requires Quest A:
             Returns ["quest_a", "quest_b", "quest_c"]
    
    Raises: QuestNotFoundError if quest doesn't exist
    """
    # TODO: Implement prerequisite chain tracing
    # Follow prerequisite links backwards
    # Build list in reverse order
    chain = []
    current_id = quest_id

    if current_id not in quest_data_dict:
        raise KeyError(f"QuestNotFoundError: Starting Quest ID '{quest_id}' not found in quest data.")
    
    while current_id and current_id != "NONE":
        chain.append(current_id)

        quest = quest_data_dict.get(current_id)

        if not quest:
            break

        prereq_id = quest.get('prerequisite', "NONE")

        if prereq_id in chain:
            print(f"Warning: Circular dependency detected in quest chain: {prereq_id} is a prerequisite for a quest in its own chain. Stopping chain tracing.")
            break 

        current_id = prereq_id 
    
    chain.reverse()

    return chain

# ============================================================================
# QUEST STATISTICS
# ============================================================================

def get_quest_completion_percentage(character, quest_data_dict):
    """
    Calculate what percentage of all quests have been completed
    
    Returns: Float between 0 and 100
    """
    # TODO: Implement percentage calculation
    # total_quests = len(quest_data_dict)
    # completed_quests = len(character['completed_quests'])
    # percentage = (completed / total) * 100
    total_quests = len(quest_data_dict)

    if total_quests == 0:
        return 0.0
    
    completed_quests = len(character.get('completed_quests', []))

    percentage = (completed_quests / total_quests) * 100

def get_total_quest_rewards_earned(character, quest_data_dict):
    """
    Calculate total XP and gold earned from completed quests
    
    Returns: Dictionary with 'total_xp' and 'total_gold'
    """
    # TODO: Implement reward calculation
    # Sum up reward_xp and reward_gold for all completed quests
    total_xp = 0
    total_gold = 0

    completed_quest_ids = character.get('completed_quests', [])

    for quest_id in completed_quest_ids:
        quest_data = quest_data_dict.get(quest_id)

        if quest_data:
            reward_xp = quest_data.get('reward_xp', 0)
            total_xp += reward_xp

            reward_gold = quest_data.get('reward_gold', 0)
            total_gold += reward_gold 

    return {
        'total_xp': total_xp,
        'total_gold': total_gold 
    }

def get_quests_by_level(quest_data_dict, min_level, max_level):
    """
    Get all quests within a level range
    
    Returns: List of quest dictionaries
    """
    # TODO: Implement level filtering
    filtered_quests = []

    for quest_id, quest_data in quest_data_dict.items():
        quest_level = quest_data.get('required_level', 1)

        if min_level <= quest_level <= max_level:
            filtered_quests.append(quest_data)

    return filtered_quests

# ============================================================================
# DISPLAY FUNCTIONS
# ============================================================================

def display_quest_info(quest_data):
    """
    Display formatted quest information
    
    Shows: Title, Description, Rewards, Requirements
    """
    # TODO: Implement quest display
    print(f"\n=== {quest_data['title']} ===")
    print(f"Description: {quest_data['description']}")
    # ... etc
    print(f"=== Rewards ===")
    print(f"Experience: {quest_data['experience']} XP")
    print(f"Gold: {quest_data['gold']} G")
    print(f"=== Requirements ===")
    print(f"Minimum Level: {quest_data['required_level']}")
    print(f"Prerequisite Quest ID: {quest_data['prerequisite']}")

def display_quest_list(quest_list):
    """
    Display a list of quests in summary format
    
    Shows: Title, Required Level, Rewards
    """
    # TODO: Implement quest list display
    print(f"\n=== Quest List Summary ===")
    print(f"Title: {quest_list['title']} | Requirement Level: {quest_list['required_level']} | Rewards: {quest_list['reward_xp']} XP and {quest_list['reward_gold']} G")

def display_character_quest_progress(character, quest_data_dict):
    """
    Display character's quest statistics and progress
    
    Shows:
    - Active quests count
    - Completed quests count
    - Completion percentage
    - Total rewards earned
    """
    # TODO: Implement progress display
    print(f"\n=== {character['name']}'s Quest Progress ===")
    print(f"Active Quests: {quest_data_dict['active_quests']}")
    print(f"Completed Quests: {quest_data_dict['completed_quests']}")
    print(f"Completion Percentage: {quest_data_dict['completion_percentage']:.2f} %")
    print(f"Total Rewards Earned: {quest_data_dict['experience']} XP and {quest_data_dict['gold']} G")

# ============================================================================
# VALIDATION
# ============================================================================

def validate_quest_prerequisites(quest_data_dict):
    """
    Validate that all quest prerequisites exist
    
    Checks that every prerequisite (that's not "NONE") refers to a real quest
    
    Returns: True if all valid
    Raises: QuestNotFoundError if invalid prerequisite found
    """
    # TODO: Implement prerequisite validation
    # Check each quest's prerequisite
    # Ensure prerequisite exists in quest_data_dict
    for quest_id, quest_data in quest_data_dict.items():
        prereq_id = quest_data.get('prerequisite')

        if prereq_id and prereq_id != "NONE":
            if prereq_id not in quest_data_dict:
                quest_name = quest_data.get('name', quest_id)
                raise QuestNotFoundError(f"Invalid prerequisite found for quest '{quest_data_dict['quest_name']}' (ID: {quest_data_dict['quest_id']})."
                                         f"Prerequisite ID '{quest_data_dict['prereq_id']}' does not exist in the quest data dictionary.")
            
    return True



# ============================================================================
# TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== QUEST HANDLER TEST ===")
    
    # Test data
    test_char = {
        'level': 1,
        'active_quests': [],
        'completed_quests': [],
        'experience': 0,
        'gold': 100
    }
    #
    test_quests = {
        'first_quest': {
            'quest_id': 'first_quest',
            'title': 'First Steps',
            'description': 'Complete your first quest',
            'reward_xp': 50,
            'reward_gold': 25,
            'required_level': 1,
            'prerequisite': 'NONE'
        }
    }
    #
    try:
        accept_quest(test_char, 'first_quest', test_quests)
        print("Quest accepted!")
    except QuestRequirementsNotMetError as e:
        print(f"Cannot accept: {e}")

