# CensorUp

> Open-source automatic audio & video profanity censoring web app

Short, privacy-focused tool to automatically censor specified words in uploaded or linked audio/video files. Built with FastHTML, Pocketbase and small helper scripts to download, process, and upload media.

**Features**
- Fast, local processing of audio/video to mask or remove profane words
- Accepts file uploads or media URLs (YouTube, Facebook, Instagram, TikTok)
- Temporary storage in `uploads/` and automatic background deletion
- Simple web UI — no signup required

**Repository structure**
- `main.py` — FastHTML web app and endpoints
- `censor_script.py` — media transcription/censoring logic
- `url_downloader_script.py` — downloads media from URLs
- `storage_script.py` — uploads censored file to pocketbase storage and removes it after while to save space
- `requirements.txt` — Python dependencies

**Quick start**

1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

2. Run the app

```bash
python main.py
```

3. Open your browser at http://127.0.0.1:8000 (or the address printed by the app)

**How to use**
- On the homepage you can either upload an audio/video file or paste a supported media URL.
- Enter a comma-separated list of words to censor (for example: `badword1,badword2`).
- Click the "Censor Now" button. The processing indicator will show while the app runs.
- After processing you will get a download link for the censored media.

**Endpoints**
- `GET /` — App homepage and UI (see `main.py`)
- `POST /censor` — Accepts uploaded file form-data or a `url` + `censor_words` field. Returns a download link to the censored file.

**Notes on files & privacy**
- The app stores incoming media in `uploads/` temporarily. `main.py` creates the folder if it does not exist.
- Processed files are removed after upload; `storage_script.py` also runs a background deletion thread. Do not upload sensitive material you are not comfortable sharing.

**Development**
- Edit the censoring logic in `censor_script.py`.
- Edit downloader behavior in `url_downloader_script.py`.
- The UI is defined in `main.py` using FastHTML components.

**Contributing**
Contributions are welcome. Please open issues or pull requests with improvements, bug fixes, or new features.

**License**
This project is open-source. Add an appropriate license file (for example, MIT) if you plan to publish.

**Acknowledgements**
- Built with FastHTML and other lightweight helpers. See `requirements.txt` for third-party packages.

If you'd like, I can also add an example `LICENSE` file and a short `CONTRIBUTING.md`.
