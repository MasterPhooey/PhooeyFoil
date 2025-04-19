# app.py

import os, subprocess
from functools import wraps
from subprocess import CalledProcessError

from flask import (
    Flask, Blueprint, jsonify, abort,
    send_from_directory, request
)

from config import (
    SYSTEM_URL_PREFIX, SWITCH_DIR, N64_DIR, DREAMCAST_DIR, PSP_DIR,
    GAMEBOY_DIR, GAMEBOYADVANCED_DIR, GAMEBOYCOLOR_DIR,
    NINTENDO_DIR, SEGA32X_DIR, GAMEGEAR_DIR,
    SEGAMASTERSYSTEM_DIR, MEGADRIVE_DIR,
    SUPERNINTENDO_DIR, GAMESAVES_DIR,
    THEMES_DIR, OUTPUT_DIR
)

app = Flask(__name__)

# Build credentials map (multi‑user from env)
CREDENTIALS = {}
for pair in os.getenv("AUTH_CREDENTIALS","").split(","):
    if ":" in pair:
        u,p = pair.split(":",1)
        CREDENTIALS[u]=p

def basic_auth(req):
    auth = req.authorization
    if not auth:
        return False, "Shop requires authentication."
    if auth.username not in CREDENTIALS:
        return False, f'Unknown user "{auth.username}".'
    if CREDENTIALS[auth.username] != auth.password:
        return False, f'Incorrect password for user "{auth.username}".'
    return True, ""

def unauthorized_json(msg):
    r = jsonify({"error":msg})
    r.status_code = 401
    return r

def requires_auth(f):
    @wraps(f)
    def wrapped(*a,**k):
        ok,msg = basic_auth(request)
        if not ok:
            return unauthorized_json(msg)
        return f(*a,**k)
    return wrapped

# 1) Blueprint for all system/theme file routes
system_bp = Blueprint("system", __name__, url_prefix=f"/{SYSTEM_URL_PREFIX}")

@system_bp.route("/<system>/<path:filename>")
def serve_system_file(system, filename):
    routes = {
      "Switch": SWITCH_DIR, "N64":N64_DIR, "Dreamcast":DREAMCAST_DIR,
      "PSP":PSP_DIR, "Gameboy":GAMEBOY_DIR, "GameboyAdvanced":GAMEBOYADVANCED_DIR,
      "GameboyColor":GAMEBOYCOLOR_DIR, "Nintendo":NINTENDO_DIR,
      "Sega32X":SEGA32X_DIR, "Gamegear":GAMEGEAR_DIR,
      "SegaMasterSystem":SEGAMASTERSYSTEM_DIR, "Megadrive":MEGADRIVE_DIR,
      "Supernintendo":SUPERNINTENDO_DIR, "Gamesaves":GAMESAVES_DIR,
      "Themes": THEMES_DIR
    }
    folder = routes.get(system)
    if not folder or not os.path.isdir(folder):
        abort(404)
    return send_from_directory(folder, filename, as_attachment=True)

app.register_blueprint(system_bp)

# 2) /sh.tfl (protected, no random prefix)
@app.route("/sh.tfl")
@requires_auth
def serve_sh_tfl():
    path = os.path.join(OUTPUT_DIR, "sh.tfl")
    if not os.path.isfile(path):
        return jsonify({"error":"Encrypted catalog not found."}),404
    return send_from_directory(OUTPUT_DIR,"sh.tfl",as_attachment=True)

@app.route("/refresh", methods=["GET","POST"])
@requires_auth
def refresh_catalog():
    try:
        print("[refresh] Regenerating catalog…", flush=True)
        subprocess.run([sys.executable, "shopUp.py"], check=True)
    except CalledProcessError as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"success": "Catalog refreshed successfully"}), 200

if __name__=="__main__":
    app.run(host="0.0.0.0", port=4223)