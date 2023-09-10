from src.custom_types import (
    proj_name,
    file_content,
    proj_content
)
from src.project_indexer import (
    gather_project_data,
    create_metadata_md_file,
    generate_semantic_summary,
    update_project_memory
)
from src.utils import (
    load_config_to_env
)


load_config_to_env("config.ini")


def main():
    # Gather project data
    projects_data: dict[proj_name, proj_content] = gather_project_data()

    # Process each project
    for project_name, content in projects_data.items():
        # Create metadata file with placeholders
        create_metadata_md_file(project_name)

        # Generate the semantic summary (using placeholder data for now)
        semantic_summary = generate_semantic_summary(project_name, "<PLACEHOLDER>", "<PLACEHOLDER>")

        # Update project memory
        update_project_memory(project_name, semantic_summary)

    print("Processing complete!")

if __name__ == "__main__":
    if False:
        import os
        os.chdir("src")
        from custom_types import (
            proj_name,
            file_content,
            proj_content
        )
        from project_indexer import (
            gather_project_data,
            create_metadata_md_file,
            generate_semantic_summary,
            update_project_memory
        )
    main()
