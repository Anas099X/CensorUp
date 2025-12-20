import yt_dlp




def download_video(url):


 # Set basic download options
 options = {
    'outtmpl': 'uploads/%(title)s.%(ext)s',  # Save file as video title
    "format": "best"}

 # Create downloader
 with yt_dlp.YoutubeDL(options) as ydl:
    ydl.download([url])

 return ydl.prepare_filename(ydl.extract_info(url, download=False))


