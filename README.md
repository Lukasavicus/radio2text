# Radio2Text

## 1. Introduction:
This project is a set of scripts to download data from a streamed radio over internet service and extract relevant info about it.
The name of the scripts were inspired in Star Wars droids, "R2-D2" (R2 - Radio To / T2 - Text), "K-2SO" (Anality**K**s) and C-3PO (the "Talk-like-a-human droid).
<br>
<img src="3.DOCS/favicon.jpg" style="width: 100px; height: 100px">
<br>

## 2. Usage:
The scripts are written in Python 3.7 and use the following libraries:
- requests
- pydub
- SpeechRecognition
- pyaudio

To install the required libraries use the following command:
```bash
    pip install -r requirements.txt
```
Besides the libraries, the scripts also require the ffmpeg library to be installed in the system. To install it use the following command:
```bash
    # For linux:
    sudo apt-get install ffmpeg 
    # -----------------------
    # For mac:
    brew install ffmpeg
```

### 2.1. Scripts:
#### 2.1.1. R2:
R2 is the module that downloads the audio from a given stream URL and saves it to a file. It does that by using the requests library to download the audio and the pydub library to save it to a file. Fo usage refer to the following example:
```bash
    python3 R2.py -stream_url http://stream.url --output_directory audio_chunks --chunk_duration 10
```
\* Obs.: By default each file will have a duration of 10 seconds and will be saved in the audio_chunks directory with the name "chunk_#.mp3". The chunk duration can be changed by the user.

#### 2.1.2. T2:
T2 is the module that transcribes the audio from a given audio file or an origin folder and saves it to a text file or a destination folder. It does that by using the SpeechRecognition library to transcribe the audio. For usage refer to the following example:

```bash
    # Example 1 - Transcribing a single file:
    python3 T2.py --file audio.mp3 --dest_folder transcription_chunks --extension mp3 --delete_after_transcription --verbose --language en-US

    # Example 2 - Transcribing all files in a folder:
    python3 T2.py --orig_folder audio_chunks --dest_folder transcription_chunks --delete_after_transcription --language en-US

    # Example 3 - Transcribing all files and monitore the folder for new files:
    python3 T2.py --orig_folder audio_chunks --dest_folder transcription_chunks --extension mp3 --delete_after_transcription --verbose --interval 10 --keep_alive --language en-US
```
\* Obs.: By default the transcriptions will be saved in the transcription_chunks directory with the name "transcription_#.txt". The user can change the extension of the files and the language of the transcription.

#### 2.1.3. K-2SO:
K-2SO is the module that analyses the transcriptions and extract relevant information from it. It does that by using the pandas library to read the transcriptions and extract the relevant information. For usage refer to the following example:

```bash
    # TODO: transform this ipython command into a bash command - look for 
    python3 K-2SO.py --orig_folder transcription_chunks --dest_folder analysis_chunks --delete_after_analysis --verbose
```

#### 2.1.4. C-3PO:
C-3PO is the module that generates a text file with the transcriptions of the audio files. It does that by using the pandas library to read the transcriptions and generate a text file with the transcriptions. For usage refer to the following example:

```bash
    python3 C3PO.py "2.silver/2024-12-11-11-00/transcription_chunks" "3.gold/2024-12-11-11-00/answers.json"
```

## 3. License:
This project is licensed under the MIT License - see the LICENSE.md file for details.

## 4. Next Steps:
- [ ] Create config files to store the parameters of the scripts.
- [ ] Create a bash script to run the scripts (for demo purposes).
- [ ] Create a Pipeline orchestrated by Apache Airflow (using Astronomer CLI - for learning purposes).
- [ ] Create a bash script to install the required libraries and the ffmpeg library.
- [ ] Refine the method to extract relevant information from the transcriptions (using NLP? C3PO script).