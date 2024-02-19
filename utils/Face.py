from sever.settings import STATIC_FILES_DIR_FACE, STATIC_FILES_DIR_FILE, FFMPEF_PATH

import subprocess


def get_file_face(input_file, output_file, time=0, size='100x100', quality=50):
    time_str = f'{int(time // 3600):02d}:{int((time % 3600) // 60):02d}:{time % 60:06.3f}'
    input_file=str(input_file)
    output_file=str(output_file)
    cmd = [
        FFMPEF_PATH,
        '-i', input_file,
        '-ss', time_str,
        '-vframes', '1',
        '-vf', f'scale={size}:force_original_aspect_ratio=decrease',
        '-q:v', str(quality),
        '-f', 'image2',
        output_file,
        '-y'
    ]
    try:
        subprocess.run(cmd, check=True)
        return True
    except subprocess.CalledProcessError as e:
        return False


def creatFace(md5):
    files = list(STATIC_FILES_DIR_FACE.glob(f"{md5}.*"))
    if len(files) > 0:
        return True
    else:
        file=STATIC_FILES_DIR_FILE / md5
        icon=STATIC_FILES_DIR_FACE / f"{md5}.icon"
        preview=STATIC_FILES_DIR_FACE / f"{md5}.preview"
        if (get_file_face(file, icon, time=0, size='200x200', quality=5)
                and get_file_face(file, preview, time=0, size='2000x2000', quality=5)):
            return True
    return False

