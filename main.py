from fasthtml.common import *
from fasthtml.components import *
from censor_script import censor_media
from storage_script import upload_media, delete_media
from url_downloader_script import download_video
import os, threading
from typing import Optional
import base64
from urllib.parse import urlparse

# Initialize FastHTML App
app = FastHTML()
rt = app.route
os.makedirs("uploads", exist_ok=True)

Defaults = (
    Link(
        rel="stylesheet",
        href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@latest/dist/tabler-icons.min.css"
    ),
    Link(href="https://cdn.jsdelivr.net/npm/daisyui@5", rel="stylesheet", type="text/css"),
    Link(href="https://cdn.jsdelivr.net/npm/daisyui@5.0.0/themes.css", rel="stylesheet", type="text/css"),
    Script(src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"),
    # htmx for hx- attributes
    Script(src="https://cdn.jsdelivr.net/npm/htmx.org@2.0.8/dist/htmx.min.js"),
    # SEO meta tags
    Title("CensorNow — Automatic Profanity Censorship, No Signup Required"),
    Meta(name="viewport", content="width=device-width, initial-scale=1"),
    Meta(name="description", content="CensorNow automatically censors profanity and unwanted words from audio and video. Upload or link your media, provide words to censor, and download the censored result."),
    Meta(name="keywords", content="censor, audio censor, video censor, profanity filter, content moderation, automatic censoring"),
    Meta(property="og:title", content="CensorNow — Automatic Audio/Video Profanity Censoring"),
    Meta(property="og:description", content="Upload or link audio/video and automatically censor specified words. Fast processing, flexible inputs, privacy-focused."),
    Meta(property="og:type", content="website"),
    Meta(name="twitter:card", content="summary_large_image"),
)

@rt('/')
def get(sess):
 
 navbar = Div(
                Div(
                    "🤫 CensorNow", 
                    cls="text-2xl text-info font-bold navbar-start"
                ),
                Div(
                    A(I(cls="ti ti-brand-github-filled text-lg")," Github", href="https://github.com/Anas099X", cls="btn"),
                    cls="text-warning font-bold navbar-end space-x-5 drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]"
                ),
                cls="navbar bg-ghost py-2 fixed z-50"  # reduced navbar padding
            )   

 first_hero = Div(

    # Main content
    Div(
        Div(
            Div("🎬 Upload your Audio/Video File to Censor it Automatically!", cls="text-2xl font-bold text-netural mb-4"),
            Form(    
            Div(
                Input(type="file" ,name="file",cls="file-input"),
                Div("OR",cls="divider lg:divider-horizontal"),
                Input(type="text", name="url",placeholder="🌐 Enter a YouTube / Facebook / Instagram / TikTok URL",cls="input input-bordered w-96"),
                cls="flex w-full flex-col lg:flex-row"
            ),
            Textarea(type="text", name="censor_words",placeholder="🗣️ Enter words to censor seperated by commas (ex. badword1,badword2)",cls="input input-bordered w-full mt-5"),
            Div("Supported URL platforms: YouTube, Facebook, Instagram, TikTok", cls="text-sm opacity-70 mt-2 mb-2"),
            Button("🤫 Censor Now",cls="btn btn-info mt-5"),
            hx_post="/censor",
            hx_target="this",
            hx_swap="outerHTML",
            # connect the indicator (kept for clarity; event listeners also handle show/hide)
            hx_indicator="#htmx-indicator",
            enctype="multipart/form-data",
            ),
            cls="card-body"
        ),
        cls="card bg-base-300 hero-content text-center mx-auto my-auto w-full max-w-1/2 justify-center"
    ),
    cls="hero min-h-screen mb-0 rounded-b-3xl")
 

 second_hero = Div(

    # SEO-friendly About + Features + Q&A
    Div(
        Div("About CensorNow", cls="text-3xl font-bold mb-2"),
        Div(
            "CensorNow helps you automatically remove or mask profanity and undesired words from audio and video. "
            "Upload a file or provide a direct URL, list words to censor, and get a downloadable censored media file. "
            "Designed for content creators, educators, and platforms that want a quick, private way to sanitize media.",
            cls="text-base mb-5 w-full mx-auto"
        ),

        # Features grid
        Div(
            Div(
                Div("⚡ Fast & Accurate", cls="text-lg font-semibold"),
                Div("AI-assisted transcription and precise censoring with minimal manual work.", cls="text-sm"),
                cls="card p-4"
            ),
            Div(
                Div("🔗 Flexible Inputs", cls="text-lg font-semibold"),
                Div("Upload files or provide a direct URL to media hosted elsewhere.", cls="text-sm"),
                cls="card p-4"
            ),
            Div(
                Div("🔒 Privacy-first", cls="text-lg font-semibold"),
                Div("No Signup Required. Files are processed and then automatically removed within hour of upload; no unnecessary retention.", cls="text-sm"),
                cls="card p-4"
            ),
            cls="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6"
        ),

        # Q&A / FAQ section
        Div(
            Div("Frequently Asked Questions", cls="text-xl font-semibold mb-3"),
            Div(
                Div(Div("Q: How long does processing take?", cls="font-bold"), Div("A: Small files usually process within seconds to a minute. Larger files depend on duration and server load.", cls="mb-4")),
                Div(Div("Q: What formats are supported?", cls="font-bold"), Div("A: Common audio/video formats (mp3, wav, mp4, mov). If you provide a direct URL, CensorNow will attempt to fetch supported media.", cls="mb-4")),
                Div(Div("Q: Are my files kept?", cls="font-bold"), Div("A: By default, files are stored temporarily for processing and automatically removed after completion with an hour. Do not upload sensitive data you are not comfortable sharing.", cls="mb-4")),
                cls="prose max-w-none"
            ),
            cls="mb-6"
        ),
        cls="card bg-base-300 hero-content text-left mx-auto my-auto w-full max-w-4xl p-6"
    ),
    cls="hero bg-base-300 min-h-screen mb-0 rounded-b-3xl"
)
 

 # simple full-screen indicator (hidden by default; shown by htmx events)
 htmx_indicator = Div(
        Div(
            Div(cls="loading loading-lg"),  # daisyui spinner
            Div("Processing...", cls="mt-3 text-white"),
            cls="text-center"
        ),
        id="htmx-indicator",
        cls="htmx-indicator fixed inset-0 bg-black/50 flex items-center justify-center z-50"
    )

 return Title("Flarebase - The Spark Your Backend Needs."),Div(
            Head(Defaults,navbar),
            
            Body(
                Main(
                    first_hero,
                    second_hero,
                    htmx_indicator,  # include indicator in page
                ),
                data_theme="silk",
                cls="bg-base-200"
            )
        )




@rt('/censor')
async def post(file: Optional[UploadFile] = None, url: str = "", censor_words: str = ""):
 
 
 if file is not None:
  #read input file
  file_bytes = file.file.read()
  base64_file = base64.b64encode(file_bytes).decode("utf-8")

  #save file to uploads folder
  file_name = file.filename

  with open(os.path.join("uploads", file_name), "wb") as f:
    f.write(base64.b64decode(base64_file))

  file_path = os.path.join("uploads", file_name)
 elif url != "" and file is None:
  #download file from url
    file_path = download_video(url)

 else:
   return Div(Div("⚠️ Please provide a file or a URL to censor.", cls="alert alert-error"),A("Refresh Site",cls="btn btn-soft btn-error mt-3",href="/"))   

 #log feedback
 print(f"Censoring file: {file_path}")

 #censor words list
 words_censor_list = censor_words.split(",")
 print(words_censor_list) 

 #censor file
 censored_file = censor_media("small",file_path,words_censor_list) 

 download_link = upload_media(censored_file)

 #remove uploaded and censored files
 os.remove(file_path)

 #upload file to cloud
 return Div(A("📼 Download Censored Video",cls="btn btn-success",href=download_link), A("Refresh Site",cls="btn btn-soft btn-error ml-4",href="/"))

#start background deletion thread
threading.Thread(target=delete_media, daemon=True).start()

serve()