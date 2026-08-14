import os
from PIL import Image


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")
OUTPUT_FOLDERS = ("fit-1080p", "fit-720p", "crop-1080p", "crop-720p")
SIZE_1080 = (1920, 1080)
SIZE_720 = (1280, 720)
PAD_COLOR = (255, 255, 255)
JPEG_QUALITY = 85


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def convert_to_rgb(img):
    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, PAD_COLOR)
        background.paste(img, mask=img.split()[-1])
        return background
    if img.mode != "RGB":
        return img.convert("RGB")
    return img


def save_jpeg(img, output_path, quality=JPEG_QUALITY):
    img = convert_to_rgb(img)
    img.save(output_path, "JPEG", quality=quality, optimize=True, progressive=True)


def make_fit_image(img, target_width, target_height):
    """Scale to fit inside canvas; pad with white. No crop, no stretch."""
    img = convert_to_rgb(img)
    src_width, src_height = img.size
    scale = min(target_width / float(src_width), target_height / float(src_height))
    new_width = max(1, int(src_width * scale))
    new_height = max(1, int(src_height * scale))
    resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    canvas = Image.new("RGB", (target_width, target_height), PAD_COLOR)
    offset_x = (target_width - new_width) // 2
    offset_y = (target_height - new_height) // 2
    canvas.paste(resized, (offset_x, offset_y))
    return canvas


def make_crop_image(img, target_width, target_height):
    """Scale to cover canvas, then center-crop to exact size."""
    img = convert_to_rgb(img)
    src_width, src_height = img.size
    scale = max(target_width / float(src_width), target_height / float(src_height))
    new_width = max(1, int(src_width * scale))
    new_height = max(1, int(src_height * scale))
    resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    left = (new_width - target_width) // 2
    top = (new_height - target_height) // 2
    return resized.crop((left, top, left + target_width, top + target_height))


def safe_print(message):
    try:
        print(message)
    except UnicodeEncodeError:
        print(message.encode("ascii", errors="replace").decode("ascii"))


def process_image(input_path, output_dirs):
    try:
        with Image.open(input_path) as img:
            base_name = os.path.basename(input_path)
            name, _ext = os.path.splitext(base_name)
            variants = {
                "fit-1080p": make_fit_image(img, SIZE_1080[0], SIZE_1080[1]),
                "fit-720p": make_fit_image(img, SIZE_720[0], SIZE_720[1]),
                "crop-1080p": make_crop_image(img, SIZE_1080[0], SIZE_1080[1]),
                "crop-720p": make_crop_image(img, SIZE_720[0], SIZE_720[1]),
            }
            for folder_name, out_img in variants.items():
                ensure_dir(output_dirs[folder_name])
                save_jpeg(out_img, os.path.join(output_dirs[folder_name], f"{name}.jpg"))
            safe_print(f"Processed: {base_name}")
    except Exception as err:
        safe_print(f"Failed to process {input_path}: {err}")


def process_sources(root_folder):
    output_roots = {}
    for folder_name in OUTPUT_FOLDERS:
        output_roots[folder_name] = os.path.join(root_folder, folder_name)
        ensure_dir(output_roots[folder_name])

    # Images pasted directly in the root folder
    root_output_dirs = {folder_name: output_roots[folder_name] for folder_name in OUTPUT_FOLDERS}
    for entry in os.listdir(root_folder):
        full_path = os.path.join(root_folder, entry)
        if not os.path.isfile(full_path):
            continue
        if not entry.lower().endswith(IMAGE_EXTENSIONS):
            continue
        process_image(full_path, root_output_dirs)

    # Images inside source subfolders
    for entry in os.listdir(root_folder):
        full_path = os.path.join(root_folder, entry)
        if not os.path.isdir(full_path):
            continue
        if entry.lower() in OUTPUT_FOLDERS:
            continue

        for subdir, _, files in os.walk(full_path):
            rel = os.path.relpath(subdir, full_path)
            output_dirs = {}
            for folder_name in OUTPUT_FOLDERS:
                source_out = os.path.join(output_roots[folder_name], entry)
                target_dir = os.path.join(source_out, rel) if rel != "." else source_out
                ensure_dir(target_dir)
                output_dirs[folder_name] = target_dir

            for file_name in files:
                if not file_name.lower().endswith(IMAGE_EXTENSIONS):
                    continue
                src_path = os.path.join(subdir, file_name)
                process_image(src_path, output_dirs)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    process_sources(script_dir)
