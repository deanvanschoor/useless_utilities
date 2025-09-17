from pathlib import Path

path = r'D:\Projects\padata-agent\padata'

input_path = Path(path)                   


files = list(input_path.parent.glob(input_path.name))

print(files)