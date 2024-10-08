import signal
import sys
from config_loader import list_configs, load_config
from combo_loader import list_combos, load_combos
from hit_handler import save_hit
from request_processor import process_combo
from tqdm import tqdm

def signal_handler(sig, frame):
    """Handles Ctrl+C and returns to the main menu."""
    print("\nExiting to main menu...")
    main_menu()

def main_menu():
    """Main menu to select config and combo file."""
    while True:
        print("\nSelect a config file:")
        configs = list_configs()
        for idx, config in enumerate(configs):
            print(f"{idx}. {config}")
        
        try:
            choice = int(input("Choose a config file (0 to exit): "))
            if choice == 0:
                sys.exit(0)
            selected_config = configs[choice]
            config = load_config(selected_config)

            print("\nSelect a combo file:")
            combos = list_combos()
            for idx, combo in enumerate(combos):
                print(f"{idx}. {combo}")
            
            combo_choice = int(input("Choose a combo file: "))
            selected_combo = combos[combo_choice]
            combo_list = load_combos(selected_combo)

            run_bruteforce(config, combo_list, selected_config)
        except (ValueError, IndexError):
            print("Invalid choice. Please try again.")

def run_bruteforce(config, combo_list, selected_config):
    config_name_without_ext = os.path.splitext(selected_config)[0]  # Get the config name without extension
    for combo in tqdm(combo_list, desc="Processing combos"):
        result = process_combo(config, combo, config_name_without_ext)  # Pass the config name without extension
        if result == "ban":
            print("Ban detected. Stopping the bruteforce.")
            break
        elif result == "hit":
            print("Hit found!")
        elif result == "fail":
            print("Failed attempt.")

