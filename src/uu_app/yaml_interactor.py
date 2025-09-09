from config import BASE_DIR, YAML_CONFIG, APP_DIR
from pathlib import Path
import logging
import yaml


#setup logger
logger = logging.getLogger(__name__)

def fetch_yaml(dir: Path, yaml_file: str = YAML_CONFIG) -> dict :
    """
    Load and return YAML data from a specified file.

    Args:
        dir (Path): Directory where the YAML file is located.
        yaml_file (str, optional): Name of the YAML file to read.
                                   Defaults to "config.yaml".

    Returns:
        dict: Parsed YAML content as a Python dictionary.
    """
    yaml_path = dir / yaml_file
    try:
        with open(yaml_path, "r") as f:
            yaml_data = yaml.safe_load(f)
            logger.info(f"Fetched YAML data from {yaml_path}")
            return yaml_data
    except Exception as e:
        logger.critical(f"Could not fetch YAML file -> {yaml_path}",e, exc_info=True)
        raise Exception(f"Could not fetch YAML file -> {yaml_path} - {e}") from e
  

# Fetch YAML files
#app_yaml = fetch_yaml(APP_DIR, YAML_CONFIG)
#config_yaml = fetch_yaml(BASE_DIR, YAML_CONFIG)
