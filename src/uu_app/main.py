from .logging_config import setup_logging
from .setup_app import setup_app
from .password_remover import password_remover
from .run_sql_scripts import run_sql_scripts
import sys

def main():
    setup_logging()
    setup_app()
    
    if len(sys.argv) < 2:
        print("Usage: pr <path>")
        print("Example: pr 'D:\\Projects\\utilities\\dev\\*.xlsx'")
        sys.exit(1)
    
    path_input = sys.argv[1]
    password_remover(path_input)
    
def run_sql():
    setup_logging()
    setup_app()
    
    if len(sys.argv) < 2:
        print("Usage: rs <path>")
        print("Example: rs 'D:\\Projects\\utilities\\dev'")
        sys.exit(1)
    
    path_input = sys.argv[1]
    run_sql_scripts(path_input)

if __name__ == "__main__":
    main()