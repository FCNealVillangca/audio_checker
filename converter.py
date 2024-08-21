import os
from pydub import AudioSegment
from pydub.effects import normalize


def convert_audio_files(src_folder, dist_folder, sample_rate, prefix):

    # Create the destination folder if it doesn't exist
    if not os.path.exists(dist_folder):
        os.makedirs(dist_folder)

    # Get the highest index number in the destination folder
    index = 1
    while os.path.exists(os.path.join(dist_folder, f"{prefix}-{index}.wav")):
        index += 1

    # Iterate over all files in the source folder
    for filename in os.listdir(src_folder):
        # Get the file extension
        file_ext = os.path.splitext(filename)[-1]

        # Check if the file is an audio file
        if file_ext in ['.mp3', '.wav', '.ogg', '.m4a']:
            # Load the audio file
            audio_file = AudioSegment.from_file(
                os.path.join(src_folder, filename))

            # Check if the file is above 3 seconds in length
            if len(audio_file) >= 3000:  # 3000ms = 3 seconds
                # Convert to mono
                mono_audio_file = audio_file

                # Normalize the audio
                normalized_audio_file = normalize(mono_audio_file)

                # Add 200ms silence to the start and end of the clip
                silence = AudioSegment.silent(duration=200)
                padded_audio_file = silence + normalized_audio_file + silence

                # Resample to the specified sample rate
                resampled_audio_file = padded_audio_file.set_frame_rate(
                    sample_rate)

                # Save the resampled audio file with a new name
                output_filename = f"{prefix}-{index}.wav"
                output_file = os.path.join(dist_folder, output_filename)
                resampled_audio_file.export(output_file, format="wav")

                print(f"Converted {filename} to {output_file}")

                # Remove the original file from the source folder
                os.remove(os.path.join(src_folder, filename))

                index += 1
            else:
                print(f"Skipping {filename} (less than 3 seconds)")


# Read the new filename prefix from a .txt file
with open('name.txt', 'r') as f:
    new_file_name = f.read().strip()

# Example usage:
src_folder = "src"
dist_folder = "dist"
sample_rate = 44100
prefix = new_file_name

convert_audio_files(src_folder, dist_folder, sample_rate, prefix)

print("\n \n \n You can close the window now")

while True:
    pass
