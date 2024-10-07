import os

HITS_PATH = './hits/'

def save_hit(config_name, user, password, parse_hit):
    """Appends the hit to the hits file."""
    os.makedirs(HITS_PATH, exist_ok=True)
    hit_file = os.path.join(HITS_PATH, f'{config_name}_hits.txt')
    
    with open(hit_file, 'a') as f:
        f.write(f"{user}:{password},{parse_hit}\n")
