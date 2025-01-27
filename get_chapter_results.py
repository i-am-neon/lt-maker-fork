import pickle
import sys
import os
import json

os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

def get_chapter_results(save_path: str) -> None:
    with open(save_path, 'rb') as f:
        data = pickle.load(f)
    # print(data)
    last_choice = data["game_vars"].get("_last_choice", "")

    # For kills: data["records"]["kills"] is typically a list of tuples:
    # [('KillRecord', {'turn':2, 'level_nid':'0', 'killer':'O\'Neill','killee':'Lute'}), ...]
    kills_list = []
    if "records" in data and isinstance(data["records"], dict):
        if "kills" in data["records"]:
            # We only care about the second element of each kill tuple
            # which is the dictionary of kill info
            kills_list = [kill_data[1] for kill_data in data["records"]["kills"]]

    result_dict = {
        "last_choice": last_choice,
        "kills": kills_list
    }
    # Print as JSON so the TS script can parse easily
    print(json.dumps(result_dict))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python get_chapter_results.py <save_file>")
    get_chapter_results(sys.argv[1])