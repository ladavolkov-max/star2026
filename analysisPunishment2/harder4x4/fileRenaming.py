import os
from pathlib import Path

if __name__ == "__main__":
    folderPath = "./analysis4x4MazeReg/data2"
    targetDir = Path(folderPath)
    if not targetDir.exists() or not targetDir.is_dir():
        print(f"Error: The path '{folderPath}' is not a valid directory.")
        exit
    
    i = 40
    for filePath in targetDir.iterdir():
        if filePath.is_file():
            newName = f"batch{i}.txt"
            newFilePath = targetDir / newName
            try:
                filePath.rename(newFilePath)
                print(f"Renamed: '{filePath.name}' -> '{newName}'")
                i += 1
            except Exception as e:
                print(f"Failed to rename '{filePath.name}': {e}")
