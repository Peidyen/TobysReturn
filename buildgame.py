import os
import subprocess

# Collect all .png and .wav files from the base directory
png_files = [f"{file};." for file in os.listdir(".") if file.endswith(".png")]
wav_files = [f"{file};." for file in os.listdir(".") if file.endswith(".wav")]

# Combine into a single list of --add-data arguments
add_data_args = []
for file in png_files + wav_files:
    add_data_args.extend(['--add-data', file])

# Run PyInstaller with these arguments
subprocess.run(['pyinstaller', '--onefile', '--windowed', 'ButtercupsBalloonAdventure.py'] + add_data_args)
