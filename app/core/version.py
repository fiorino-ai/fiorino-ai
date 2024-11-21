import subprocess
from pathlib import Path

def get_git_version():
    try:
        # Get the git tag
        tag = subprocess.check_output(['git', 'describe', '--tags', '--always']).decode('utf-8').strip()
        return tag
    except:
        # Fallback to reading from version file if git command fails
        version_file = Path(__file__).parent.parent.parent / 'VERSION'
        if version_file.exists():
            return version_file.read_text().strip()
        return "unknown"

# Export version
__version__ = get_git_version() 