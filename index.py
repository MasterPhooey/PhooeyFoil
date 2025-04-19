# index.py
import os
import json
import urllib.parse
import re
from pathlib import Path
from config import (
    SWITCH_DIR, N64_DIR, DREAMCAST_DIR, PSP_DIR, GAMEBOY_DIR,
    GAMEBOYADVANCED_DIR, GAMEBOYCOLOR_DIR, NINTENDO_DIR,
    SEGA32X_DIR, GAMEGEAR_DIR, SEGAMASTERSYSTEM_DIR, MEGADRIVE_DIR,
    SUPERNINTENDO_DIR, GAMESAVES_DIR, THEMES_DIR,
    OUTPUT_DIR, PUBLIC_URL,
    SUCCESS_LINE1, SUCCESS_LINE2, SYSTEM_URL_PREFIX
)

OUTPUT_FILENAME = "main.json"

# Define a mapping for systems.
# Each system has: allowed extensions, the folder path, and the URL prefix.
system_mapping = {
    "Switch": {
       "extensions": ['nsp', 'xci', 'nsz', 'xcz'],
       "folder": SWITCH_DIR,
       "url_prefix": "Switch"
    },
    "N64": {
       "extensions": ['z64'],
       "folder": N64_DIR,
       "url_prefix": "N64"
    },
    "Dreamcast": {
       "extensions": ['chd'],
       "folder": DREAMCAST_DIR,
       "url_prefix": "Dreamcast"
    },
    "PSP": {
       "extensions": ['cso'],
       "folder": PSP_DIR,
       "url_prefix": "PSP"
    },
    "Gameboy": {
       "extensions": ['gb'],
       "folder": GAMEBOY_DIR,
       "url_prefix": "Gameboy"
    },
    "GameboyAdvanced": {
       "extensions": ['gba'],
       "folder": GAMEBOYADVANCED_DIR,
       "url_prefix": "GameboyAdvanced"
    },
    "GameboyColor": {
       "extensions": ['gbc'],
       "folder": GAMEBOYCOLOR_DIR,
       "url_prefix": "GameboyColor"
    },
    "Nintendo": {
       "extensions": ['nes'],
       "folder": NINTENDO_DIR,
       "url_prefix": "Nintendo"
    },
    "Sega32X": {
       "extensions": ['32x'],
       "folder": SEGA32X_DIR,
       "url_prefix": "Sega32X"
    },
    "Gamegear": {
       "extensions": ['gg'],
       "folder": GAMEGEAR_DIR,
       "url_prefix": "Gamegear"
    },
    "SegaMasterSystem": {
       "extensions": ['sms'],
       "folder": SEGAMASTERSYSTEM_DIR,
       "url_prefix": "SegaMasterSystem"
    },
    "Megadrive": {
       "extensions": ['md'],
       "folder": MEGADRIVE_DIR,
       "url_prefix": "Megadrive"
    },
    "Supernintendo": {
       "extensions": ['sfc'],
       "folder": SUPERNINTENDO_DIR,
       "url_prefix": "Supernintendo"
    },
    "Gamesaves": {
       "extensions": ['zip'],
       "folder": GAMESAVES_DIR,
       "url_prefix": "Gamesaves"
    }
}

def main():
    output = outputTinfoil()
    outputFilePath = Path(OUTPUT_DIR) / OUTPUT_FILENAME
    with open(outputFilePath, 'w') as f:
        json.dump(output, f, indent=4)
    print(f"Generated JSON output at {outputFilePath}")

def getFileList(path, allowed_exts):
    """Scans the given path and returns files with extensions matching allowed_exts."""
    files = []
    non_ascii_pattern = re.compile(r'[^\x00-\x7F]+')
    for root, _, filenames in os.walk(path, followlinks=True):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lstrip('.').lower()
            if ext in [e.lower() for e in allowed_exts]:
                filepath = os.path.join(root, filename)
                if non_ascii_pattern.search(filepath):
                    print(f"Skipping file {filepath}: contains non-ASCII characters")
                else:
                    # Return the relative path from the given folder.
                    files.append(os.path.relpath(filepath, path))
    return files

def getFileSize(filename):
    return os.path.getsize(filename)

def getURL(system, file):
    """
    Build URL under /<SYSTEM_URL_PREFIX>/<system>/<file>.
    """
    base = PUBLIC_URL.rstrip('/')
    file_enc = urllib.parse.quote(file, safe='/')
    return f"{base}/{SYSTEM_URL_PREFIX}/{system}/{file_enc}"

def outputTinfoil():
    output = {"total": 0, "files": [], "themes": [], "success": ""}

    total = 0
    for system, m in system_mapping.items():
        folder = m['folder']
        exts   = m['extensions']
        if not os.path.isdir(folder):
            continue
        for root, _, fnames in os.walk(folder, followlinks=True):
            for fn in fnames:
                if fn.lower().split('.')[-1] in exts:
                    rel = os.path.relpath(os.path.join(root, fn), folder)
                    size = os.path.getsize(os.path.join(folder, rel))
                    url  = getURL(system, rel)
                    output["files"].append({"url":url, "size":size})
                    total += 1

    # themes (always under the same prefix)
    theme_folder = THEMES_DIR
    if os.path.isdir(theme_folder):
        for root, _, fnames in os.walk(theme_folder, followlinks=True):
            for fn in fnames:
                if fn.lower().endswith('.zip'):
                    rel = os.path.relpath(os.path.join(root, fn), theme_folder)
                    url = getURL("Themes", rel)
                    output["themes"].append(url)

    output["total"]   = total
    output["success"] = os.getenv("SUCCESS_LINE1","") + "\n" + os.getenv("SUCCESS_LINE2","")
    return output

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = outputTinfoil()
    with open(os.path.join(OUTPUT_DIR, OUTPUT_FILENAME),'w') as f:
        json.dump(out, f, indent=4)

if __name__=="__main__":
    main()