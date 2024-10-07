import os

COMBO_PATH = './combos/'

def list_combos():
    """Lists all combo files in the combo directory."""
    return [f for f in os.listdir(COMBO_PATH) if f.endswith('.txt')]

def load_combos(combo_file):
    """Loads the user:pass combos from the selected file."""
    with open(os.path.join(COMBO_PATH, combo_file), 'r') as f:
        return [line.strip().split(':') for line in f if ':' in line]
