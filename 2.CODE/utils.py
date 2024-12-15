from pydub import AudioSegment
import os
import math

def combine_audio_files(file_list, output_file):
    combined = AudioSegment.empty()
    
    for file in file_list:
        audio = AudioSegment.from_file(file)
        combined += audio
    
    combined.export(output_file, format="mp3")


def split_files_into_chunks(folder, num_chunks, extension_filter):
    files = [f for f in os.listdir(folder) if f.endswith(extension_filter)]
    files.sort()
    chunk_size = math.ceil(len(files) / num_chunks)
    return [files[i:i + chunk_size] for i in range(0, len(files), chunk_size)]

def test_split_files_into_chunks():
    folder = "/Users/lucassilva/Documents/0.LUKE/2.PROJECTS/radio2txt/audio_chunks"
    num_chunks = 10
    extension_filter = ".mp3"
    chunks = split_files_into_chunks(folder, num_chunks, extension_filter)
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i + 1}: {chunk}")
        combine_audio_files([os.path.join(folder, file) for file in chunk], f"chunk_{i + 1}.mp3")

if __name__ == "__main__":
    test_split_files_into_chunks()