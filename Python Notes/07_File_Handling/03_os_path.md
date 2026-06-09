# OS & Path Operations — Files/Folders Manage Karna

## Simple Explanation (Hinglish)
Jab tum ML model train karte ho, toh tumhe:
- Multiple files padhni hoti hain (images, CSVs)
- Folders mein files organize karni hoti hain
- File paths build karne hote hain
- Check karna hota hai ki file exist karti hai ya nahi

`os` aur `pathlib` modules yahi sab karte hain — **operating system ke saath interact** karte hain.

## Theory
- `os` module: Purana tarika, files/folders ke saath kaam karta hai
- `pathlib` module: Modern tarika (Python 3.4+), recommended hai
- **Path**: File/folder ka address. Jaise `C:/data/images/train/`
- **Absolute path**: Poora address `C:/Users/name/data/file.csv`
- **Relative path**: Current location se address `./data/file.csv`

## Examples

```python
import os
from pathlib import Path

# ===== Check if file/folder exists =====
print(os.path.exists("data.csv"))      # True/False
print(Path("data.csv").exists())       # pathlib style

# ===== Join paths (safe tarika) =====
# ❌ Galat: path + "/" + filename (Linux/Windows issue)
# ✅ Sahi:
full_path = os.path.join("data", "images", "train", "img001.jpg")
full_path2 = Path("data") / "images" / "train" / "img001.jpg"
print(full_path)   # data\images\train\img001.jpg

# ===== List files in folder =====
for file in os.listdir("data"):
    print(file)

# pathlib se
for file in Path("data").iterdir():
    print(file.name)

# Sirf .csv files chahiye
csv_files = list(Path("data").glob("*.csv"))
print(csv_files)

# Recursively find all .json files
all_json = list(Path("data").rglob("*.json"))

# ===== Create/Delete folders =====
os.makedirs("new_folder/sub_folder", exist_ok=True)  # Recursive create
Path("another_folder/sub").mkdir(parents=True, exist_ok=True)

os.rmdir("empty_folder")        # Delete empty folder
# shutil.rmtree("folder")       # Delete folder with all files

# ===== File info =====
file_path = "data.csv"
print(os.path.getsize(file_path))    # File size in bytes
print(os.path.getmtime(file_path))   # Last modified time
print(Path(file_path).stat().st_size)

# ===== Split path =====
path = "C:/data/images/train/img001.jpg"
folder = os.path.dirname(path)    # C:/data/images/train
filename = os.path.basename(path)  # img001.jpg
name, ext = os.path.splitext(path) # ('...img001', '.jpg')

# pathlib style
p = Path(path)
print(p.parent)    # C:\data\images\train
print(p.name)      # img001.jpg
print(p.stem)      # img001
print(p.suffix)    # .jpg

# ===== Real-world ML use case =====
def organize_dataset(source_folder, train_ratio=0.8):
    """Split dataset into train/val folders"""
    all_files = list(Path(source_folder).glob("*.jpg"))
    split_idx = int(len(all_files) * train_ratio)
    
    train_files = all_files[:split_idx]
    val_files = all_files[split_idx:]
    
    # Create folders
    Path("dataset/train").mkdir(parents=True, exist_ok=True)
    Path("dataset/val").mkdir(parents=True, exist_ok=True)
    
    # Move files (simulate by printing)
    for f in train_files:
        print(f"Move {f.name} to dataset/train/")
    print(f"✅ Organized: {len(train_files)} train, {len(val_files)} val")

organize_dataset("raw_images")
```

## Dry Run
`Path("C:/data/images/train/img001.jpg")`:
```
.parent = C:\data\images\train
.name   = img001.jpg
.stem   = img001
.suffix = .jpg
.exists() → checks if file exists
.is_file() → True (file hai, folder nahi)
```

## Common Mistakes
1. **Backslash vs Forward slash**: Windows `\` uses but `\n` is newline. Always use `os.path.join()` ya `Path()`
2. **Forgetting `exist_ok=True`**: `os.makedirs()` error dega agar folder already exist karta hai
3. **Hardcoding paths**: `"C:/Users/..."` — deploy pe kaam nahi karega. Relative paths use karo

## Interview Notes
1. **`pathlib` is preferred** over `os.path` in modern Python (more intuitive)
2. **Cross-platform**: `pathlib` automatically handles Windows/Linux path differences
3. **ML workflow**: `glob` + `pathlib` = dataset files scan karne ka standard tarika

## Practice Questions (Sirf 5 -- Concept Clear Karne Wale)

1. **(Basic)** Check karo ki "data.csv" exist karti hai ya nahi.
2. **(Basic)** Folder ke saare files list karo.
3. **(Medium)** Function likho jo .jpg aur .png files count kare.
4. **(Medium)** pathlib se train/cat/ aur train/dog/ folders banao.
5. **(Hard)** Saare .jpeg files ko .jpg mein rename karo.