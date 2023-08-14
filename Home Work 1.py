from pathlib import Path
import shutil


def un_pack(link):
    list_dir = Path(link)
    root_dir = Path(link)

    for item in root_dir.glob('**/*'):
        if item.is_file():
            new_path = root_dir / item.name
            shutil.move(item, new_path)

    images_dir = list_dir / 'images'                        # Create link for images
    images_dir.mkdir(parents=True, exist_ok=True)           # Create directory for images

    documents_dir = list_dir / 'documents'                  # Create link for documents
    documents_dir.mkdir(parents=True, exist_ok=True)        # Create directory for documents

    video_dir = list_dir / 'video'                          # Create link for video
    video_dir.mkdir(parents=True, exist_ok=True)            # Create directory for video

    audio_dir = list_dir / 'audio'                          # Create link for audio
    audio_dir.mkdir(parents=True, exist_ok=True)            # Create directory for audio

    archives_dir = list_dir / 'archives'                    # Create link for archives
    archives_dir.mkdir(parents=True, exist_ok=True)         # Create directory for archives

    for file in list_dir.glob('*'):
        if file.is_dir():
            print(f"{file}is directory ")
            file.rename(list_dir / file.name)

    for elem in list_dir.glob('*'):

        if elem.suffix.lower() in ['.jpeg', '.png', '.jpg', '.svg']:
            print(f'{elem} is images')
            new_dir_img = images_dir / elem.name
            elem.rename(new_dir_img)

        elif elem.suffix.lower() in ['.doc', '.docx', '.txt', '.pdf', '.xlsx', '.pptx']:
            print(f'{elem} is documents')
            new_dir_doc = documents_dir / elem.name
            elem.rename(new_dir_doc)

        elif elem.suffix.lower() in ['.mp3', '.ogg', '.wav', '.amr']:
            print(f'{elem} is audio')
            new_dir_aud = audio_dir / elem.name
            elem.rename(new_dir_aud)

        elif elem.suffix.lower() in ['.avi', '.mp4', '.mov', '.mkv']:
            print(f'{elem} is video')
            new_dir_vid = video_dir / elem.name
            elem.rename(new_dir_vid)

        elif elem.suffix.lower() in ['.zip', '.gz', '.tar']:
            print(f'{elem} is archives')
            new_dir_arc = archives_dir / elem.name
            elem.rename(new_dir_arc)

        else:
            pass
un_pack('/home/yehor/Desktop/New Folder (copy)')