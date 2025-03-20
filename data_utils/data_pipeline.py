
"""
Idea: 
loop through ZHAW data dir and and extract text from files. 
Transform text to correct input format using Local LLM. Save input Data to DB

Steps:
    1. Extract Data from files (No duplicate files)
    2. Transform Data via local LLM (handel incorrect response)
    3. Load to DB
"""

# Set to True/False to include/exclude steps in the workflow
extract = False
transform = False
load_to_db = False
dir_path = "dir_path"


def scan_and_extract_files(root_dir: str = dir_path) -> None:
    pass


if __name__ == "__main__":
    if extract:
        scan_and_extract_files()
    if transform:
        pass
    if load_to_db:
        pass