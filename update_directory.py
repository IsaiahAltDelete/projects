import os
import re

# --- Configuration ---
PROJECTS_LOCAL_DIR = r"C:\Users\Dizzy\Documents\Github\projects"  # Change as needed
GITHUB_USERNAME = "IsaiahAltDelete"
GITHUB_PROJECTS_BASE_URL = f"https://{GITHUB_USERNAME}.github.io/projects/"
HTML_FILE_PATH = "index.html"  # Path to your index.html file

def get_project_folders():
    """
    Scans the PROJECTS_LOCAL_DIR for folders containing 'index.html',
    skipping the '.git' folder and any folder that starts with a dot.
    Returns a sorted (case-insensitive) list of project folder names.
    """
    project_folders = []
    if not os.path.isdir(PROJECTS_LOCAL_DIR):
        print(f"Error: Directory not found: {PROJECTS_LOCAL_DIR}")
        return project_folders

    for item in os.listdir(PROJECTS_LOCAL_DIR):
        # Skip '.git' or any folder starting with a dot
        if item == ".git" or item.startswith('.'):
            continue

        project_path = os.path.join(PROJECTS_LOCAL_DIR, item)
        if os.path.isdir(project_path):
            index_html_path = os.path.join(project_path, "index.html")
            if os.path.exists(index_html_path):
                project_folders.append(item)
    # Sort alphabetically (case-insensitive)
    return sorted(project_folders, key=lambda x: x.lower())

def generate_project_html(project_name):
    """
    Generates HTML for a single project folder.
    """
    project_url = GITHUB_PROJECTS_BASE_URL + project_name + "/"
    html = f'''
    <div class="project-folder">
      <a href="{project_url}" class="project-link">
        <i class="material-icons folder-icon">folder</i>
        <span class="project-name">{project_name}</span>
      </a>
    </div>
    '''
    return html

def update_html_directory(project_folders):
    """
    Updates the index.html file with the project folder links by replacing
    content between the PROJECTS_START and PROJECTS_END markers.
    """
    # Generate the HTML for all projects
    project_html_list = [generate_project_html(folder) for folder in project_folders]
    projects_html = "\n".join(project_html_list)

    try:
        with open(HTML_FILE_PATH, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: HTML file not found: {HTML_FILE_PATH}")
        return

    print("HTML content BEFORE update:")
    print(html_content)

    # Use regex to replace content between markers
    pattern = r"(<!--\s*PROJECTS_START\s*-->)(.*?)(<!--\s*PROJECTS_END\s*-->)"
    replacement = r"\1\n" + projects_html + "\n\3"
    updated_html, count = re.subn(pattern, replacement, html_content, flags=re.DOTALL)

    if count == 0:
        print("Error: Could not find the markers in the HTML file. Make sure they are intact!")
        return

    with open(HTML_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(updated_html)

    print("HTML content AFTER update:")
    print(updated_html)
    print("Successfully updated project directory in index.html")

if __name__ == "__main__":
    project_folders = get_project_folders()
    print("Detected project folders:", project_folders)  # Debug print
    if project_folders:
        update_html_directory(project_folders)
    else:
        print("No projects found with index.html files.")
