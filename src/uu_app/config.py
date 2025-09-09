from pathlib import Path

BASE_DIR = Path(__file__).parent 

APP_FOLDER = ".uu"

def get_app_dir(app_name = APP_FOLDER) -> Path:
    """Returns APP_FOLDER dir path in user's home directory
    
        Args:
            app_name (str): Name of application folder
    """
    return Path.home() / app_name

APP_DIR = get_app_dir()

YAML_CONFIG = "config.yaml"
