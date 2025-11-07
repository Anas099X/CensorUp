import os, subprocess
import whisper_timestamped as whisper

#os.environ["PATH"] += os.pathsep + r"C:\Users\Anas\ffmpeg\bin"


def censor_media(model_type:str,input_media:str,blocked_words:list):

    # Load Whisper model
    model = whisper.load_model(model_type)

    media = input_media

    result = whisper.transcribe(model,media,language="en")
    #print(result)
    # Words you want to remove
    
    # Collect mute ranges
    mute_ranges = []
    for segment in result["segments"]:
        for word in segment["words"]:
            clean_word = word["text"].strip('.!?,":;`').lower()
            if clean_word in blocked_words:
                start = max(0, word["start"] - 0.15)
                end = word["end"] + 0.18
                mute_ranges.append((start, end))
                print(f"Muted word: {word['text']} timeline: {start}-{end}")

    if not mute_ranges:
        print("✅ No blocked words found. Skipping censorship.")
        return

    print("Mute ranges:", mute_ranges)

    # Build the FFmpeg audio filter
    volume_expr = " + ".join([f"between(t,{start},{end})" for start, end in mute_ranges])
    volume_filter = f"volume=enable='{volume_expr}':volume=0"

  #✅ Create truly separate output file in same folder
    folder = os.path.dirname(media)
    filename = os.path.basename(media)
    name, ext = os.path.splitext(filename)
    output_file = os.path.join(folder, f"{name}_censored{ext}")

    print(f"Input file: {media}")
    print(f"Output file: {output_file}")


    # Run FFmpeg command to mute audio in those ranges
    cmd = [
        "ffmpeg",
        "-i", media,
        "-af", volume_filter,
        "-c:v", "copy",    # don't touch video
        "-y",              # overwrite output
        output_file
    ]

    subprocess.run(cmd, check=True)
    print(f"✅ Censored video saved as: {output_file}")

    # Replace original file
    os.remove(media)
    os.rename(output_file, media)

    return media


#censor_video(input("Enter the path of the video to censor: ").strip())