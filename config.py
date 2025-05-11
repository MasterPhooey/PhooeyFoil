# config.py
import os
import secrets
from dotenv import load_dotenv

load_dotenv()

# where to store your random prefix so it survives restarts
OUTPUT_DIR  = "/app/data/output"
PREFIX_FILE = os.path.join(OUTPUT_DIR, "system_prefix.txt")

# load existing or generate+save a new one
if not os.path.isdir(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)
if os.path.exists(PREFIX_FILE):
    with open(PREFIX_FILE, "r") as f:
        SYSTEM_URL_PREFIX = f.read().strip()
else:
    SYSTEM_URL_PREFIX = secrets.token_urlsafe(8)  # e.g. "XyZ9_abQ"
    with open(PREFIX_FILE, "w") as f:
        f.write(SYSTEM_URL_PREFIX)

UNENCRYPTED_ENDPOINT = os.getenv("UNENCRYPTED_ENDPOINT", "no").lower() in ("yes", "true", "1")

# ─── Fixed In‑Container Paths ────────────────────────────
SWITCH_DIR       = "/app/data/switch"
N64_DIR          = "/app/data/n64"
DREAMCAST_DIR    = "/app/data/dreamcast"
PSP_DIR          = "/app/data/psp"
GAMEBOY_DIR      = "/app/data/gameboy"
GAMEBOYADVANCED_DIR = "/app/data/gameboyadvanced"
GAMEBOYCOLOR_DIR = "/app/data/gameboycolor"
NINTENDO_DIR     = "/app/data/nintendo"
SEGA32X_DIR      = "/app/data/sega32x"
GAMEGEAR_DIR     = "/app/data/gamegear"
SEGAMASTERSYSTEM_DIR = "/app/data/segamastersystem"
MEGADRIVE_DIR    = "/app/data/megadrive"
SUPERNINTENDO_DIR= "/app/data/supernintendo"
GAMESAVES_DIR    = "/app/data/gamesaves"

THEMES_DIR       = "/app/data/themes"

PUBLIC_URL = os.getenv("PUBLIC_URL", "http://localhost:4223")

# Always use this path for your public key, relative to the project root.
PUBLIC_KEY_PATH          = os.path.join(os.path.dirname(__file__), "public.key")

SUCCESS_LINE1 = os.getenv("SUCCESS_LINE1", "Welcome to PhooeyFoil")
SUCCESS_LINE2 = os.getenv("SUCCESS_LINE2", "Your Switch Shop")