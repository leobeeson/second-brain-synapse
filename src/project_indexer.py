import os
import tempfile
import time
import json


from custom_types import (
    proj_name, 
    proj_content,
    file_content
)
from utils import (
    list_project_folders, 
    format_project_name, 
    read_md_file_exclude_code_blocks
)


PROJECTS_DIR: str = os.environ("PROJECTS_DIR")
PROJECT_MEMORY_PATH: str = os.environ("PROJECT_MEMORY_PATH")


def gather_project_data(base_path: str = PROJECTS_DIR, project_folder: str = None) -> dict[proj_name, proj_content]:
    """Iterate over projects, format names, and gather .md file content."""
    project_data: dict = {}

    def gather_md_content_from_folder(folder_path: str) -> list[file_content]:
        """Recursively gather .md content from the folder and its subdirectories."""
        md_content: list[str] = []
        for entry in os.scandir(folder_path):
            if entry.is_file() and entry.name.endswith('.md'):
                file_name = os.path.basename(entry.path)
                md_content.append(f"# {file_name}")
                content: file_content = read_md_file_exclude_code_blocks(entry.path)
                md_content.append(content)
            elif entry.is_dir():
                md_content.extend(gather_md_content_from_folder(entry.path))
        return md_content

    # Determine the project folders to process
    project_folders: list[str] = [project_folder] if project_folder else list_project_folders(base_path)

    # Iterate over the determined project folders
    for proj_folder in project_folders:
        
        # Extract the project's name and format it
        project_name: proj_name = format_project_name(proj_folder)
        
        # Gather .md content from the project folder and its subdirectories
        project_folder_path: str = os.path.join(base_path, proj_folder)
        project_md_content: list[file_content] = gather_md_content_from_folder(project_folder_path)
        project_content: proj_content = "\n\n".join(project_md_content)
        project_data[project_name] = project_content

    return project_data


def create_temp_file_with_content(content: str) -> str:
    """Create a temporary text file with the given content and return its path."""
    # Create a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".md", mode="w+", encoding="utf-8")
    
    # Write the content to the temp file
    temp_file.write(content)
    temp_file_path = temp_file.name
    temp_file.close()

    return temp_file_path


def create_metadata_md_file(
        project_name: str, 
        base_path: str = PROJECTS_DIR, 
        summary: str = "<PLACEHOLDER>",
        topics: str = "<PLACEHOLDER>",
        index: str = "<PLACEHOLDER>",
        status: str = "<PLACEHOLDER>"
        ):
    """Create a metadata .md file for the project with placeholders for LLM content."""
    # Define the path for the metadata file
    metadata_file_path = os.path.join(base_path, project_name, f"00_{project_name}_meta.md")
    # Update first line of metadata file to update project name in case project name was changed by user since last indexing.
    markdown_deader = f"# Metadata for {project_name}"

    # Placeholder content for LLM
    placeholder_content = f"""
--------------------------------------------

## Update Date & Time
{time.strftime("%Y-%m-%d %H:%M:%S %Z")}

## Project Name
{project_name}

## Project Summary
{summary}

## Main Topics, Concepts, Named Entities, and Events
{topics}

## Content Index
{index}

## Project Status
{status}
"""
    # 1. Open the metadata file if it exists, or created if it doesn't.
    # 2. If the metadata file exists, replace the first line with the updated markdown header in `markdown_deader`. 
    # 3. If the metadata file does not exist, add `markdown_header` as the first line of the markdown file.
    # 4. Append `placeholder_content` to the metadata file, NOT overwriting any existing content.
    with open(metadata_file_path, 'w', encoding='utf-8') as file:
        # Open the metadata file if it exists, otherwise create it
        if os.path.exists(metadata_file_path):
            # Read the existing content
            with open(metadata_file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # Replace the first line with the updated markdown header
            lines[0] = markdown_deader + '\n'
            
            # Write back the modified content along with the new placeholder content
            with open(metadata_file_path, 'w', encoding='utf-8') as file:
                file.writelines(lines)
                file.write(placeholder_content)
        else:
            # If the metadata file does not exist, simply write the header and the placeholder content
            with open(metadata_file_path, 'w', encoding='utf-8') as file:
                file.write(markdown_deader + '\n')
                file.write(placeholder_content)


def generate_semantic_summary(project_name: str, summary: str = "<PLACEHOLDER>", topics: str = "<PLACEHOLDER>") -> str:
    """Generate the semantic summary for a project."""
    # Concatenate the project name, summary, and topics to form the semantic summary
    return f"{project_name}\n####\n{summary}\n####\n{topics}"


def update_project_memory(project_name: str, semantic_summary: str, memory_path: str = PROJECT_MEMORY_PATH):
    """Update or create entries in project_memory.json."""
    # Load existing memory content
    if os.path.exists(memory_path):
        with open(memory_path, 'r', encoding='utf-8') as file:
            memory_data = json.load(file)
    else:
        memory_data = {}

    # Update or create the entry for the project
    memory_data[project_name] = semantic_summary

    # Save the updated memory content
    with open(memory_path, 'w', encoding='utf-8') as file:
        json.dump(memory_data, file, ensure_ascii=False, indent=4)
