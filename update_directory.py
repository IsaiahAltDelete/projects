import os
import re

# --- Configuration ---
PROJECTS_LOCAL_DIR = r"C:\Users\Dizzy\Documents\Github\projects"  # Change as needed
GITHUB_USERNAME = "IsaiahAltDelete"
GITHUB_PROJECTS_BASE_URL = f"https://{GITHUB_USERNAME}.github.io/projects/"
HTML_FILE_PATH = "index.html"  # Path to your index.html file

# Built-in template for index.html in case markers are missing
TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Projects Directory</title>
  <!-- Google Fonts: Poppins -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap" rel="stylesheet">
  <!-- Material Icons -->
  <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
  <style>
    body {
      font-family: 'Poppins', sans-serif;
      background-color: #fff;
      color: #000;
      margin: 0;
      padding: 20px;
    }
    h1 {
      margin-bottom: 20px;
    }
    .projects-container {
      display: flex;
      flex-wrap: wrap;
      gap: 20px;
    }
    .project-folder {
      display: flex;
      flex-direction: column;
      align-items: center;
      width: 120px;
    }
    .project-folder a {
      text-decoration: none;
      color: inherit;
      display: flex;
      flex-direction: column;
      align-items: center;
      padding: 10px;
      border: 1px solid transparent;
      border-radius: 5px;
      transition: background-color 0.2s ease-in-out;
    }
    .project-folder a:hover {
      background-color: #f0f0f0;
    }
    .project-folder a:focus,
    .project-folder a:active {
      outline: none !important;
      border-color: transparent !important;
      box-shadow: none !important;
    }
    .project-folder a::-moz-focus-inner {
      border: 0;
    }
    .folder-icon {
      font-size: 72px;
      margin-bottom: 5px;
    }
    .project-name {
      font-size: 14px;
      text-align: center;
      word-wrap: break-word;
    }
  </style>
</head>
<body>
  <h1>My Projects</h1>
  <div class="projects-container" id="projects-list">
    <!-- PROJECTS_START -->
    <!-- PROJECTS_END -->
  </div>
</body>
</html>
"""

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

def remove_control_characters(text):
    """
    Removes most control characters from text except for newline (\n),
    carriage return (\r), and tab (\t). This will remove characters like STX.
    """
    # This regex removes characters in ranges:
    # \x00-\x08, \x0B-\x0C, \x0E-\x1F, and \x7F.
    return re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', text)

def update_html_directory(project_folders):
    """
    Updates the index.html file with the project folder links by replacing
    content between the PROJECTS_START and PROJECTS_END markers.
    If the markers are not found, re-create the file using the built-in template.
    """
    # Generate the HTML for all projects
    project_html_list = [generate_project_html(folder) for folder in project_folders]
    projects_html = "\n".join(project_html_list)

    # Try reading the current HTML file
    try:
        with open(HTML_FILE_PATH, "r", encoding="utf-8") as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"HTML file not found, creating a new one from the template.")
        html_content = TEMPLATE

    # Check if markers exist. If not, reset to the template.
    if "<!-- PROJECTS_START -->" not in html_content or "<!-- PROJECTS_END -->" not in html_content:
        print("Markers not found. Re-creating the HTML file from the template.")
        html_content = TEMPLATE

    # Use regex to replace content between markers
    pattern = r"(<!--\s*PROJECTS_START\s*-->).*?(<!--\s*PROJECTS_END\s*-->)"
    replacement = r"\1\n" + projects_html + "\n\2"
    updated_html, count = re.subn(pattern, replacement, html_content, flags=re.DOTALL)

    if count == 0:
        print("Error: Could not find the markers in the HTML file. Aborting update.")
        return

    # Remove unwanted control characters from the updated HTML
    updated_html = remove_control_characters(updated_html)

    with open(HTML_FILE_PATH, "w", encoding="utf-8") as f:
        f.write(updated_html)

    print("Successfully updated project directory in index.html")
    print("Updated project list:", project_folders)

if __name__ == "__main__":
    project_folders = get_project_folders()
    print("Detected project folders:", project_folders)  # Debug print
    update_html_directory(project_folders)
