<p align="center">
  <img src="https://raw.githubusercontent.com/MasterPhooey/PhooeyFoil/refs/heads/main/images/phooeyfoil.png" alt="PhooeyFoil Logo" width="300">
</p>

<h1 align="center">PhooeyFoil</h1>


**Description:**  
Your Own Tinfoil Shop. Serves Games, RetroArch ROMs, Game Saves and Tinfoil themes.

Current Docker image: `masterphooey/phooeyfoil:latest`

---

## Supported Systems & Extensions

- **Switch**: `.nsp`, `.xci`, `.nsz`, `.xcz`  
- **N64**: `.z64`  
- **Dreamcast**: `.chd`  
- **PSP**: `.cso`  
- **Game Boy**: `.gb`  
- **Game Boy Advance**: `.gba`  
- **Game Boy Color**: `.gbc`  
- **Nintendo** (NES): `.nes`  
- **Sega 32X**: `.32x`  
- **Game Gear**: `.gg`  
- **Sega Master System**: `.sms`  
- **Mega Drive**: `.md`  
- **Super Nintendo**: `.sfc`  
- **Game Saves**: `.zip`  

## Tinfoil Themes

Tinfoil theme `.zip` files will appear in the Tinfoil options menu.

---
## Notes:

- **Tinfoil Themes will only install with the NSP installed version of Tinfoil**
- **Roms will only show up if you have Retroarch Installed and Setup**
---
## Quick Start

```
docker run -d \
  -p 4223:4223 \
  --env-file .env \
  -v /host/path/to/output:/app/data/output \
  -v /host/path/to/switch:/app/data/switch:ro \
  -v /host/path/to/n64:/app/data/n64:ro \
  -v /host/path/to/dreamcast:/app/data/dreamcast:ro \
  -v /host/path/to/psp:/app/data/psp:ro \
  -v /host/path/to/gameboy:/app/data/gameboy:ro \
  -v /host/path/to/gameboyadvanced:/app/data/gameboyadvanced:ro \
  -v /host/path/to/gameboycolor:/app/data/gameboycolor:ro \
  -v /host/path/to/nintendo:/app/data/nintendo:ro \
  -v /host/path/to/sega32x:/app/data/sega32x:ro \
  -v /host/path/to/gamegear:/app/data/gamegear:ro \
  -v /host/path/to/segamastersystem:/app/data/segamastersystem:ro \
  -v /host/path/to/megadrive:/app/data/megadrive:ro \
  -v /host/path/to/supernintendo:/app/data/supernintendo:ro \
  -v /host/path/to/gamesaves:/app/data/gamesaves:ro \
  -v /host/path/to/themes:/app/data/themes:ro \
  masterphooey/phooeyfoil:latest
```

---

## Configuration

Copy the sample environment file:

```
cp .env.sample .env
```

Edit `.env` to set:

```
# Base URL where the service will be reachable (no trailing slash)
PUBLIC_URL=http://localhost:4223

# Basic Auth credentials, comma-separated user:pass pairs
AUTH_CREDENTIALS=admin:changeme,guest:guest123,alice:retro4life

# Success message—line 1 (default: Welcome to PhooeyFoil)
SUCCESS_LINE1=Welcome to PhooeyFoil

# Success message—line 2 (default: Your Switch Shop)
SUCCESS_LINE2=Your Switch Shop
```

---

## Endpoints

- **Encrypted Catalog**  
  `GET /sh.tfl`  
  Download the `sh.tfl` catalog file (protected by Basic Auth).
  
- **Un-Encrypted Catalog (If Enabled)**  
  `GET /sh.json`  
  Download the `sh.json` catalog file (protected by Basic Auth)
  
  **Adding to Tinfoil:**  
  1. Copy the full catalog URL, e.g.:  
     `http://localhost:4223/sh.tfl`
     or
     `http://localhost:4223/sh.json` 
  3. On your Switch, open Tinfoil and go to the **FileBrowser** tab.  
  4. Select **New** (➖ icon). 
  5. Enter the catalog URL and login.  
  6. Tinfoil will load the shop and display available titles.

- **Manual Refresh** (If you dont want to restart your docker)  
  `GET|POST /refresh`  
  Regenerate `sh.json` and `sh.tfl` on demand (protected by Basic Auth).

  **Via curl:**   
  ```
  curl -u admin:changeme -X POST http://localhost:4223/refresh
  ```


---
