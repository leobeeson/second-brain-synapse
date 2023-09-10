import os
import urllib.parse
import configparser


from src.custom_types import (
    proj_name, 
    proj_content,
    file_content
)


def list_project_folders(base_path: str) -> list[str]:
    """List all project folders."""
    # Ensure path exists
    if not os.path.exists(base_path):
        return []
    # List all directories in the given path
    return [dir for dir in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, dir))]


def format_project_name(name: proj_name) -> proj_name:
    """Format project name to be lower cased, spaces replaced with underscores, and URL-safe."""
    formatted_name = name.lower().replace(" ", "_")
    return urllib.parse.quote(formatted_name, safe='')


def read_md_file_exclude_code_blocks(file_path: str) -> file_content:
    """Read content of .md file and exclude content within code blocks."""
    content = []
    in_code_block = False

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            if line.startswith("```"):
                in_code_block = not in_code_block
                continue
            if not in_code_block:
                content.append(line)

    return '\n'.join(content)


def write_to_md_file(file_path: str, content: proj_content) -> None:
    """Write content to .md file."""
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def load_config_to_env(config_file: str):
    """Load config values into environment variables."""
    if not os.path.exists(config_file):
        raise FileNotFoundError(f"The config file '{config_file}' does not exist. Please provide a valid path to 'config.ini'.")

    config = configparser.ConfigParser()
    config.read(config_file)
    
    if not config.sections():
        raise ValueError(
            f"The config file '{config_file}' appears to be empty or not properly formatted.\n\n"
            "This package's 'config.ini' structure looks like:\n"
            "[DEFAULT]\n"
            "\n"
            "[DATA_PATHS]\n"
            "projects_dir = path/to/second_brain/root_folder\n"
            "project_memory_path = path/to/second_brain/root/memory_folder/project_memory.json\n\n"
            "Please ensure your 'config.ini' adheres to this structure."
        )

    for section in config.sections():
        for key, value in config.items(section):
            env_key = f"{section}_{key}".upper()
            os.environ[env_key] = value

    # For DEFAULT section
    for key, value in config.items("DEFAULT"):
        os.environ[key.upper()] = value
