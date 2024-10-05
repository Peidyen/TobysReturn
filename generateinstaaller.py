import os
import subprocess

# Use the current directory for assets
assets_directory = "."  # This means the current working directory (base directory)

# Name of the script you want to package
script_name = "TobysReturn.py"  # Your main Python game script

# Only include specific asset file types (e.g., .png, .wav)
asset_extensions = ['.png', '.gif', '.wav', '.mp3', '.txt']  # Extend with more types if necessary

# Initialize the base PyInstaller command
pyinstaller_command = ['pyinstaller', '--onefile', '--windowed', script_name]

# Function to generate the add-data command for each asset file in the assets directory
def add_data_commands(directory):
    add_data = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext in asset_extensions:
                file_path = os.path.join(root, file)
                # Adjusting the separator based on the OS (replace ; with : on Linux/Mac)
                separator = ';' if os.name == 'nt' else ':'
                add_data.append(f'--add-data={file_path}{separator}{os.path.relpath(root, directory)}')
    return add_data

# Get all the --add-data commands for your assets
add_data_options = add_data_commands(assets_directory)

# Add the asset options to the base PyInstaller command
pyinstaller_command.extend(add_data_options)

# Print the command to check if everything looks good (optional)
print(f"Generated PyInstaller command: {' '.join(pyinstaller_command)}")

# Run the generated PyInstaller command
try:
    subprocess.run(pyinstaller_command, check=True)
    print("Packaging completed successfully!")
except subprocess.CalledProcessError as e:
    print(f"Error during packaging: {e}")
