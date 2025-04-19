FROM python:3.9-slim

WORKDIR /app

# 1) Install Python deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 2) Copy app code + entrypoint
COPY . .

# 3) Create data dirs for mounts & output
RUN mkdir -p \
    data/switch data/n64 data/dreamcast data/psp \
    data/gameboy data/gameboyadvanced data/gameboycolor \
    data/nintendo data/sega32x data/gamegear \
    data/segamastersystem data/megadrive data/supernintendo \
    data/gamesaves data/themes data/output

# 4) Expose the port your app listens on
EXPOSE 4223

# 5) Entrypoint: scan → encrypt
ENTRYPOINT ["./entrypoint.sh"]

# 6) Use Gunicorn to serve the Flask app (3 workers, port 4223)
CMD ["gunicorn", "--bind", "0.0.0.0:4223", "app:app", "--workers", "10", "--timeout", "0"]