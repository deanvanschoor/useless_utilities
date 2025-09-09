from config import BASE_DIR, YAML_CONFIG , APP_FOLDER , APP_DIR
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)

PACKAGE_CONFIG = BASE_DIR / YAML_CONFIG

def app_dir_exist() -> bool:
    """Checks if the '.uu' directory exists in the user's home directory."""
    path: Path = APP_DIR
    logger.info(f"app_dir exists at {path}")
    return path.is_dir()  # returns True if exists, False otherwise

def create_app_dir() -> None:
    """Creates the '.uu' directory in the user's home directory."""
    try:
        path: Path = APP_DIR
        path.mkdir(exist_ok=True)
        logger.info(f"Created app_dir at {path}")
    except PermissionError:
        logger.critical(f"Permission denied creating directory: {path}")
        raise RuntimeError(f"Permission denied creating directory: {path}")
    
def config_yaml_exists() -> bool:
    """Checks if config.yaml or config.yml exists in the .uu directory."""
    app_path: Path = APP_DIR
    yaml_files = [YAML_CONFIG, "config.yml"]  
    # Return True if any of the files exist
    return any((app_path / f).is_file() for f in yaml_files)
        
def setup_app() -> None:
    """Run this to setup uu dir & logging"""
    if not app_dir_exist():
        create_app_dir()
    if not config_yaml_exists():
        dest_dir = APP_DIR / YAML_CONFIG
        shutil.copy(PACKAGE_CONFIG, dest_dir)
        logger.info(f"Copied default config.yaml to {dest_dir}")
        
   
        
