from .logging_config import setup_logging
from .setup_app import setup_app
from .password_remover import password_remover
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

if __name__ == "__main__":
    main()