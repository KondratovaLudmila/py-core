from sys import argv
from pathlib import Path
from shutil import unpack_archive

FORMATS_DICT = {"images": {'JPEG', 'PNG', 'JPG', 'SVG'},
                "video": {'AVI', 'MP4', 'MOV', 'MKV'},
                "documents": {'DOC', 'DOCX', 'TXT', 'PDF', 'XLSX', 'PPTX'},
                "audio": {'MP3', 'OGG', 'WAV', 'M4A','AMR'},
                "archives": {'ZIP', 'GZ', 'TAR'},
                }
CYRILLIC_SYMBOLS = "абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ"
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "ya", "je", "i", "ji", "g")

TRANS_DICT = {}

def gen_trans_dict():

    for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
        TRANS_DICT[ord(c)] = l
        TRANS_DICT[ord(c.upper())] = l.upper()


def is_valid_path(path: Path) -> bool:

    return path.exists() and path.is_dir()


def normalize(name: str) -> str:
    normalized_name = ""

    if not TRANS_DICT:
        gen_trans_dict()
    
    for char in name:
        if char.isalnum():
            normalized_name += TRANS_DICT.get(ord(char), char)
        else:
            normalized_name += "_"
    
    return normalized_name

def get_target_folder(extension: str) -> str:

    new_folder = ""

    extension = extension.upper()
    for file_type in FORMATS_DICT:
        if extension in FORMATS_DICT[file_type]:
            new_folder = file_type
            break

    return new_folder

def generate_unique_name(file_path: Path) -> Path:
    
    new_path = file_path
    start_name = file_path.name.removesuffix(file_path.suffix)
    idx = 0
    while new_path.exists():
        idx += 1
        new_name = start_name + str(idx) + new_path.suffix
        new_path = new_path.with_name(new_name)

    return new_path

def gen_formats_path_set(home_dir: Path) -> set:
    
    formats_path_set = set()

    for file_type in FORMATS_DICT:
        formats_path_set.add(home_dir.joinpath(file_type))

    return formats_path_set


def sort_files(cur_dir: Path, home_dir: Path) -> list:
    
    unknown_formats = set()
    known_formats = set()
    dont_touch_set = gen_formats_path_set(home_dir)

    for cur_path in cur_dir.iterdir():
        
        if cur_path in dont_touch_set:
            continue
        
        new_name = normalize(cur_path.stem)
        if cur_path.is_file():
            new_name += cur_path.suffix
            extension = cur_path.suffix.removeprefix(".").upper()
            target_folder = get_target_folder(extension)
            
            if target_folder == "":
                target_path = cur_path.parent
                unknown_formats.add(extension)
            else:
                target_path = home_dir.joinpath(target_folder)
                known_formats.add(extension)
            
            if not target_path.exists():
                target_path.mkdir()

            target_path = target_path.joinpath(new_name)
            if target_path != cur_path:
                target_path = generate_unique_name(target_path)
                cur_path.rename(target_path)
        
        elif cur_path.is_dir():
            new_known, new_unknown = sort_files(cur_path, home_dir)
            known_formats.update(new_known)
            unknown_formats.update(new_unknown)

            if not any(cur_path.iterdir()):
                try:
                    cur_path.rmdir()
                except OSError:
                    print(f"Can not remove directory {cur_path}")
            elif new_name != cur_path.name:
                renamed_path = cur_path.rename(cur_path.parent.joinpath(new_name))
                dont_touch_set.add(renamed_path)

    return known_formats, unknown_formats

def postprocessing(home_dir: Path):

    path_set = gen_formats_path_set(home_dir)

    for folder in path_set:

        if folder.name == "archives":
            for arch in folder.iterdir():
                if arch.is_dir():
                    continue
                unpack_archive(arch, folder.joinpath(arch.stem))
                arch.unlink()
                
        print(f"{folder.name}")
        for obj in folder.iterdir():
            print("{:<5}{}".format("", obj.name))


def main() -> bool:
    if len(argv) < 2:
        print("There is no directory for sorting!")
        return False
    
    working_dir = Path(argv[1])

    if not is_valid_path(working_dir):
        print("Your path not valid or not a directory!")
        return False

    known_file_formats, unknown_file_formats = sort_files(working_dir, working_dir)

    postprocessing(working_dir)

    print(f"Known file formats: {','.join(known_file_formats)}")
    print(f"Unknown file formats: {','.join(unknown_file_formats)}")

    return True

if __name__ == '__main__':
    
    main()