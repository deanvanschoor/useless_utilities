from config import APP_DIR
import msoffcrypto
import os
import tempfile
from pathlib import Path
import logging
from yaml_interactor import fetch_yaml

logger = logging.getLogger(__name__)

def remove_excel_password_inplace(file_path, password):
    dir_name = Path(file_path).resolve().parent
    file_ext = file_path.suffix
    temp_path = None    
    try:
        # Create named temp file
        with tempfile.NamedTemporaryFile(mode="w+b", suffix=file_ext, dir=dir_name, delete=False) as temp_file:
            temp_path = temp_file.name
            
            with open(file_path, "rb") as f_in:
                office_file = msoffcrypto.OfficeFile(f_in)
                office_file.load_key(password=password)
                office_file.decrypt(temp_file)
        
        # Replace original with decrypted temp file
        os.replace(temp_path, file_path)
        logger.info(f"Password removed in place on {file_path}")
        return True
    except msoffcrypto.exceptions.DecryptionError as e:
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
                logger.info(f"attempting cleanup of temp file: {temp_path} relates to {file_path}")
            except OSError:
                logger.warning(f"could not cleanup of temp file: {temp_path} relates to {file_path}")
                pass  # Best effort cleanup
        return False
        
    except Exception as e:
        # Always clean up temp file on any error
        if temp_path and os.path.exists(temp_path):
            try:
                os.unlink(temp_path)
                logger.info(f"attempting cleanup of temp file: {temp_path} relates to {file_path}")
            except OSError:
                logger.warning(f"could not cleanup of temp file: {temp_path} relates to {file_path}")
                pass  # Best effort cleanup
        #raise e
        logger.error(f"error removing password from {file_path}",e)
        return False

def password_remover(path):
    input_path = Path(path)                   
    files = list(input_path.parent.glob(input_path.name))

    config_dict = fetch_yaml(APP_DIR)
    passwords = config_dict['password_remover']['passwords']

    for file in files:
        for password in passwords:
            print(file,password)
            pass_removed = remove_excel_password_inplace(file, password)
            if pass_removed is True:
                print(f"Password removed from {file.stem}")
                break  # Stop trying other passwords for this file
            continue
 
#path = "D:\Projects\utilities\dev\*.xlsx"  # input into function

    