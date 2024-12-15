"""

---
## 2. Installing:
```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install requests pydub SpeechRecognition
    pip install ffmpeg-downloader
    ffdl install --add-path
```

## 3. Usage:
```sh
    python t2.py --orig_folder audio_chunks --dest_folder transcription_chunks --verbose --language pt-BR --keep_alive
```

"""
import os
import speech_recognition as sr
from pydub import AudioSegment
import io
import time
import argparse

# Function to perform speech recognition # pt-BR
def speech_to_text(audio_segment, language="en-US"):
    """Convert audio to text using SpeechRecognition library.

    Args:
        audio_segment (AudioSegment): AudioSegment object.

    Returns:
        str: Transcribed text.
    """
    recognizer = sr.Recognizer()
    try:
        # Convert AudioSegment to WAV for recognition
        with io.BytesIO() as wav_buffer:
            audio_segment.export(wav_buffer, format="wav")
            wav_buffer.seek(0)
            
            # Use recognizer to process audio
            with sr.AudioFile(wav_buffer) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language=language)
                return text
    except Exception as e:
        print(f"Error in speech recognition: {e}")
        return ""

def transcribe_file(file_path, dest_folder, extension="mp3", delete_after_transcription=False, verbose=True, language="en-US"):
    """Transcribe a single audio file.

    Args:
        file_path (str): Path to the audio file.
        dest_folder (str): Path to the folder to save transcriptions.
        extension (str): File extension of the audio file (default is "mp3").
        delete_after_transcription (bool): Whether to delete the audio file after transcription (default is False).
        verbose (bool): Whether to print verbose output (default is True).
        language (str): Language code for speech recognition (default is "en-US").
    """
    os.makedirs(dest_folder, exist_ok=True)  # Ensure output directory exists
    filename = os.path.basename(file_path)
    dest_file_path = os.path.join(dest_folder, f"{os.path.splitext(filename)[0]}.txt")
    if not os.path.exists(dest_file_path):
        try:
            if verbose: print(f"Processing file: {file_path}")
            audio_segment = AudioSegment.from_file(file_path, format=extension)
            transcription = speech_to_text(audio_segment, language=language)
            if verbose: print(f"Transcription for {filename}: {transcription}")
            
            # save transcription to a file
            with open(dest_file_path, "w") as text_file:
                text_file.write(transcription)

            if delete_after_transcription:
                os.remove(file_path)
                if verbose: print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

def monitor_and_transcribe(orig_folder, dest_folder="transcription_chunks", extension="mp3", delete_after_transcription=False, verbose=True, interval=30, keep_alive=True, language="en-US"):
    """Monitor a folder for new audio files and transcribe them.

    Args:
        orig_folder (str): Path to the folder containing audio files.
        dest_folder (str): Path to the folder to save transcriptions.
        extension (str): File extension to filter by (default is "mp3").
        delete_after_transcription (bool): Whether to delete the audio file after transcription (default is False).
        verbose (bool): Whether to print verbose output (default is True).
        interval (int): Time interval in seconds to wait between checks (default is 10).
        keep_alive (bool): Whether to continuously monitor the folder (default is True).
        language (str): Language code for speech recognition (default is "en-US").
    """
    os.makedirs(dest_folder, exist_ok=True)  # Ensure output directory exists

    def transcribe_files():
        for filename in os.listdir(orig_folder):
            if filename.endswith(f".{extension}"):
                file_path = os.path.join(orig_folder, filename)
                transcribe_file(file_path, dest_folder, extension, delete_after_transcription, verbose, language)

    if keep_alive:
        while True:
            transcribe_files()
            time.sleep(interval)
    else:
        transcribe_files()

def make_cli():
    parser = argparse.ArgumentParser(description="Monitor a folder for new audio files and transcribe them.")
    parser.add_argument("--orig_folder", type=str, help="Path to the folder containing audio files.")
    parser.add_argument("--file", type=str, help="Path to a single audio file to transcribe.")
    parser.add_argument("--dest_folder", type=str, default="transcription_chunks", help="Path to the folder to save transcriptions.")
    parser.add_argument("--extension", type=str, default="mp3", help="File extension to filter by (default is 'mp3').")
    parser.add_argument("--delete_after_transcription", action="store_true", help="Delete the audio file after transcription.")
    parser.add_argument("--verbose", action="store_true", help="Print verbose output.")
    parser.add_argument("--interval", type=int, default=10, help="Time interval in seconds to wait between checks (default is 10).")
    parser.add_argument("--keep_alive", action="store_true", help="Continuously monitor the folder.")
    parser.add_argument("--language", type=str, default="en-US", help="Language code for speech recognition (default is 'en-US').")

    args = parser.parse_args()

    if args.file and args.orig_folder:
        parser.error("Cannot use --file and --orig_folder at the same time.")
    if args.file and (args.keep_alive or args.interval != 10 or args.extension != "mp3"):
        parser.error("--file cannot be used with --keep_alive, --interval, or --extension parameters.")
    
    return args

def main():
    args = make_cli()
    
    if args.file:
        transcribe_file(
            file_path=args.file,
            dest_folder=args.dest_folder,
            extension=args.extension,
            delete_after_transcription=args.delete_after_transcription,
            verbose=args.verbose,
            language=args.language
        )
    else:
        monitor_and_transcribe(
            orig_folder=args.orig_folder,
            dest_folder=args.dest_folder,
            extension=args.extension,
            delete_after_transcription=args.delete_after_transcription,
            verbose=args.verbose,
            interval=args.interval,
            keep_alive=args.keep_alive,
            language=args.language
        )

if __name__ == "__main__":
    main()
