import os
import shutil
import subprocess
import colorama

color = colorama.Fore

def remove_directory_contents(directory):
    if os.path.isdir(directory):
        for file in os.listdir(directory):
            if file != '__init__.py':
                os.remove(os.path.join(directory, file))

def reset_db():
    # Remove __pycache__ directories
    for root, dirs, _ in os.walk('.'):
        for dir in dirs:
            if dir == '__pycache__':
                shutil.rmtree(os.path.join(root, dir))

    # Remove the database file
    if os.path.exists('db.sqlite3'):
        os.remove('db.sqlite3')

    # Remove migrations from both app and authentication directories
    remove_directory_contents(os.path.join('app', 'migrations'))
    remove_directory_contents(os.path.join('user', 'migrations'))

    # Create new migrations
    if subprocess.run(['python', 'manage.py', 'makemigrations']).returncode == 0:
        print(color.GREEN + "[+] Created migrations file successfully." + color.RESET)
    else:
        print(color.RED + "[-] Failed to create migrations file." + color.RESET)

    # Apply migrations
    if subprocess.run(['python', 'manage.py', 'migrate']).returncode == 0:
        print(color.GREEN + "[+] Applied migrations successfully." + color.RESET)
    else:
        print(color.RED + "[-] Failed to apply migrations." + color.RESET)

if __name__ == '__main__':
    reset_db()