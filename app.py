from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp
import os
import uuid

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


@app.route("/formats", methods=["POST"])
def get_formats():
    data = request.json
    url = data.get("url")

    ydl_opts = {"quiet": True}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

    formats = []
    for f in info["formats"]:
        formats.append({
            "format_id": f.get("format_id"),
            "ext": f.get("ext"),
            "resolution": (
                f"{f.get('width')}x{f.get('height')}"
                if f.get("height") else "audio"
            ),
            "fps": f.get("fps"),
            "vcodec": f.get("vcodec"),
            "acodec": f.get("acodec"),
            "url": f.get("url"),
            "filesize": f.get("filesize") or f.get("filesize_approx"),
        })

    return jsonify({
        "title": info.get("title"),
        "formats": formats
    })


@app.route("/download", methods=["POST"])
def download():
    data = request.json
    url = data["url"]
    format_id = data["format_id"]

    file_id = str(uuid.uuid4())

    ydl_opts = {
        "format": format_id,
        "outtmpl": f"{DOWNLOAD_DIR}/{file_id}.%(ext)s",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        filename = ydl.prepare_filename(info)

    return send_file(filename, as_attachment=True)


@app.route("/", methods=["GET"])
def myfun():
    return 'my app'
  
