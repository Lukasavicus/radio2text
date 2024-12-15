"""
# 1. Proposed Solution

# 2. Installation and configuration
```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install requests pydub
    brew install ffmpeg
```

# 3. Usage:
```sh
    python r2.py https://rrdns-megasistema.webnow.com.br/993fm.aac
```
"""

import requests
import time
from pydub import AudioSegment
from pydub.playback import play
import io
import os

import urllib3
import argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def save_audio_chunks(stream_url, chunk_duration=10, output_directory="audio_chunks"):
    """
    Save audio chunks of a live stream to separate files.
    
    Args:
        stream_url (str): The URL of the audio stream.
        chunk_duration (int): Duration of each chunk in seconds.
        output_directory (str): Directory to save the chunks.
    """
    os.makedirs(output_directory, exist_ok=True)  # Ensure output directory exists

    headers = {
        "accept": "*/*",
        "accept-encoding": "identity;q=1, *;q=0",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
        "connection": "keep-alive",
        "host": "rrdns-megasistema.webnow.com.br",
        "range": "bytes=0-",
        "referer": "https://rrdns-megasistema.webnow.com.br/993fm.aac",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
        "sec-fetch-dest": "video",
        "sec-fetch-mode": "no-cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    }


    try:
        print(f"Connecting to stream: {stream_url}")
        # response = requests.get(stream_url, stream=True, headers=headers, verify=False)
        response = requests.get(stream_url, stream=True, verify=False)
        response.raise_for_status()
        
        buffer = b""  # To store audio data
        chunk_size = 4096  # Read 4KB at a time
        audio_format = "mp3"  # Change as per your stream's format
        start_time = time.time()
        chunk_counter = 0
        
        print("Downloading and saving audio chunks...")
        for data in response.iter_content(chunk_size=chunk_size):
            buffer += data
            
            # Check if we've collected enough for one chunk
            elapsed_time = time.time() - start_time
            if elapsed_time >= chunk_duration:
                try:
                    # Create an AudioSegment from the buffer
                    audio_segment = AudioSegment.from_file(io.BytesIO(buffer))#, format=audio_format)
                    
                    # Save the chunk
                    chunk_filename = os.path.join(output_directory, f"chunk_{chunk_counter:04d}.{audio_format}")
                    audio_segment.export(chunk_filename, format=audio_format)
                    print(f"Saved: {chunk_filename}")
                    
                    # Reset the buffer and timers
                    buffer = b""
                    start_time = time.time()
                    chunk_counter += 1
                except Exception as e:
                    print(f"Error while processing audio: {e}")
                    buffer = b""

    except requests.exceptions.RequestException as e:
        print(f"Stream error: {e}")
    except Exception as e:
        print(f"Error while processing audio: {e}")

def make_cli():
    # STREAM_URL = "https://rrdns-megasistema.webnow.com.br/993fm.aac"
    parser = argparse.ArgumentParser(description="Save audio chunks of a live stream to separate files.")
    parser.add_argument("stream_url", type=str, help="The URL of the audio stream.")
    parser.add_argument("--chunk_duration", type=int, default=10, help="Duration of each chunk in seconds.")
    parser.add_argument("--output_directory", type=str, default="audio_chunks", help="Directory to save the chunks.")
    
    args = parser.parse_args()
    save_audio_chunks(args.stream_url, args.chunk_duration, args.output_directory)

def main():
    make_cli()

if __name__ == "__main__":
    main()