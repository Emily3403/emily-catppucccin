import re
from pathlib import Path

base_persistent_config_dir = Path.home() / "configAndDotfiles/roles/gui_basic/tasks/dotfiles"
theme_output_dir = base_persistent_config_dir / "themes"
base_save_path = Path.cwd() / "themes"

download_chunk_size = 2 ** 16

base_theme = "catppuccin-macchiato-mauve-standard+default"

rgb_replacer = {
    # Rosewater
    "f4dbd6": "fb81ba",
    "244, 219, 214": "251, 129, 186",

    # Flamingo
    "f0c6c6": "9000a2",
    "240, 198, 198": "144, 0, 162",

    # Pink
    "f5bde6": "bd4298",
    "245, 189, 230": "189, 66, 152",

    # Mauve
    "c6a0f6": "8839ef",
    "198, 160, 246": "136, 57, 239",

    # Red
    "ed8796": "e14560",
    "237, 135, 150": "225, 69, 96",

    # Maroon
    "ee99a0": "e64553",
    "238, 153, 160": "230, 69, 83",

    # Peach
    "f5a97f": "ff9989",
    "245, 169, 127": "255, 153, 137",

    # Yellow
    "eed49f": "f7bb53",
    "238, 212, 159": "255, 229, 164",

    # Green
    "a6da95": "53aa3e",
    "166, 218, 149": "83, 170, 62",

    # Teal
    "8bd5ca": "179299",
    "139, 213, 202": "23, 146, 153",

    # Sky
    "91d7e3": "6ac8e3",
    "145, 215, 227": "106, 200, 227",

    # Sapphire
    "7dc4e4": "209fb5",
    "125, 196, 228": "32, 159, 181",

    # Blue
    "8aadf4": "7287fd",
    "138, 173, 244": "114, 135, 253",

    # Lavender
    "b7bdf8": "aa39a6",
    "183, 189, 248": "170, 57, 166",
}

rgb_replace_regex = re.compile(r'\b(' + '|'.join(map(re.escape, rgb_replacer.keys())) + r')\b')