import subprocess
import re
import tempfile
import logging
from pathlib import Path
import chardet

from .manage_sql_connection import get_sql_credentials

logger = logging.getLogger(__name__)


def detect_file_encoding(file_path):
    with open(file_path, "rb") as f:
        raw_data = f.read()
        result = chardet.detect(raw_data)
        return result.get("encoding") or "utf-8"

def run_sql_scripts(path):
    """
    Executes all SQL scripts in the specified directory using sqlcmd.

    For each script:
        - Prints "Running <script_name>..."
        - Shows the number of rows affected for each statement (e.g., "9055 rows affected")
        - Stops execution immediately if any script fails

    Parameters:
        path (str): Path to the directory containing .sql files.

    Returns:
        bool: True if all scripts ran successfully, False if execution stopped due to a failure.

    Behavior:
        - Scripts are executed in alphanumeric order.
    """
    connection_details = get_sql_credentials()

    sql_dir = Path(path)
    if not sql_dir.exists():
        logger.error(f"SQL directory not found: {sql_dir}")
        print(f"SQL directory not found: {sql_dir}")
        return False

    sql_files = sorted(sql_dir.glob("*.sql"))
    if not sql_files:
        logger.warning(f"No SQL files found in {sql_dir}")
        print(f"No SQL files found in {sql_dir}")
        return True

    for sql_file in sql_files:
        logger.info(f"Running {sql_file.name}")
        print(f"\nRunning {sql_file.name}...")

        encoding = detect_file_encoding(sql_file)

        # Convert to UTF-8 with BOM if necessary
        with open(sql_file, "r", encoding=encoding, errors="replace") as src:
            content = src.read()

        with tempfile.NamedTemporaryFile(delete=False, suffix=".sql", mode="w", encoding="utf-8-sig") as tmp:
            tmp.write(content)
            tmp_file = tmp.name

        cmd = [
            "sqlcmd",
            "-S", connection_details['server'],
            "-d", connection_details['database'],
            "-U", connection_details['user'],
            "-P", connection_details['password'],
            "-i", tmp_file,
            "-b",  # exit on error
            "-V", "1",
            "-h", "-1",  # no headers
            "-W",
            "-I",
            "-f", "65001",  # tell sqlcmd we're using UTF-8
        ]

        try:
            result = subprocess.run(
                cmd,
                check=True,
                capture_output=True,
                text=True
            )

            rows_affected = re.findall(r"(\d+)\s+rows affected", result.stdout)
            if rows_affected:
                for idx, val in enumerate(rows_affected, 1):
                    print(f"  Statement {idx}: {val} rows affected")
            else:
                print("  No rows affected")

        except subprocess.CalledProcessError as e:
            logger.error(f"{sql_file.name} failed:\n{e.stdout}")
            print(f"\nERROR: {sql_file.name} failed to run!")
            print(e.stdout)
            return False  # stop execution immediately
        finally:
            Path(tmp_file).unlink(missing_ok=True)

    print(f"\n{sql_dir.name}>>All scripts ran successfully!")
    return True
