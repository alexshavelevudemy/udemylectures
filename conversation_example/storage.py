
"""
This module provide functionality to save and get user state
You can store it in memory or on disk (file, db, redis etc)
"""


IN_MEMORY_STORAGE = {}


def get_current_state(user_id):
    return IN_MEMORY_STORAGE.get(user_id)


def set_user_state(user_id, state):
    IN_MEMORY_STORAGE[user_id] = state
