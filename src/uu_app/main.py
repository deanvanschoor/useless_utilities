from logging_config import setup_logging
from setup_app import setup_app
from password_remover import password_remover
# from other_module import other_function
import sys

# Function registry
FUNCTIONS = {
    'pr': password_remover,
    'password': password_remover,
    # 'other': other_function,
}

def main():
    setup_logging()
    setup_app()
    
    if len(sys.argv) < 3:
        print("Usage: python main.py <function> <path>")
        print(f"Available functions: {', '.join(FUNCTIONS.keys())}")
        sys.exit(1)
    
    func_alias = sys.argv[1]
    path_input = sys.argv[2]
    
    if func_alias in FUNCTIONS:
        FUNCTIONS[func_alias](path_input)
    else:
        print(f"Unknown function: {func_alias}")
        print(f"Available functions: {', '.join(FUNCTIONS.keys())}")
        sys.exit(1)

if __name__ == "__main__":
    main()