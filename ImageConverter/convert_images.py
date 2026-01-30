import os
from PIL import Image


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def get_target_size(img_width, img_height, target_max_height):
    if img_height <= target_max_height:
        return img_width, img_height
    ratio = target_max_height / float(img_height)
    return int(img_width * ratio), target_max_height


def save_jpeg(img, output_path, quality):
    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        img = background
    elif img.mode != "RGB":
        img = img.convert("RGB")
    img.save(output_path, "JPEG", quality=quality, optimize=True, progressive=True)


def save_png(img, output_path):
    if img.mode == "P":
        img = img.convert("RGBA")
    img.save(output_path, "PNG", optimize=True, compress_level=9)


def compress_image(input_path, output_dir_1080, output_dir_720, jpeg_quality_1080=85, jpeg_quality_720=80):
    try:
        with Image.open(input_path) as img:
            width, height = img.size

            # 1080p output
            new_w_1080, new_h_1080 = get_target_size(width, height, 1080)
            img_1080 = img if (new_w_1080, new_h_1080) == (width, height) else img.resize((new_w_1080, new_h_1080), Image.Resampling.LANCZOS)

            # 720p output
            new_w_720, new_h_720 = get_target_size(width, height, 720)
            img_720 = img if (new_w_720, new_h_720) == (width, height) else img.resize((new_w_720, new_h_720), Image.Resampling.LANCZOS)

            base_name = os.path.basename(input_path)
            name, ext = os.path.splitext(base_name)

            ensure_dir(output_dir_1080)
            ensure_dir(output_dir_720)

            # Always output JPEG regardless of source format
            out_1080 = os.path.join(output_dir_1080, f"{name}.jpg")
            out_720 = os.path.join(output_dir_720, f"{name}.jpg")
            save_jpeg(img_1080, out_1080, jpeg_quality_1080)
            save_jpeg(img_720, out_720, jpeg_quality_720)

            print(f"Processed: {base_name}")
    except Exception as e:
        print(f"Failed to process {input_path}: {e}")


def process_sources(root_folder):
    output_1080_root = os.path.join(root_folder, "1080p")
    output_720_root = os.path.join(root_folder, "720p")
    ensure_dir(output_1080_root)
    ensure_dir(output_720_root)

    # Treat every subfolder (except 1080p/720p) as a source collection of images
    for entry in os.listdir(root_folder):
        full_path = os.path.join(root_folder, entry)
        if not os.path.isdir(full_path):
            continue
        if entry.lower() in ("1080p", "720p"):
            continue

        # Mirror this source folder name inside both outputs
        out_1080_dir = os.path.join(output_1080_root, entry)
        out_720_dir = os.path.join(output_720_root, entry)
        ensure_dir(out_1080_dir)
        ensure_dir(out_720_dir)

        # Walk files
        for subdir, _, files in os.walk(full_path):
            # Recreate relative path under outputs
            rel = os.path.relpath(subdir, full_path)
            target_1080_dir = os.path.join(out_1080_dir, rel) if rel != "." else out_1080_dir
            target_720_dir = os.path.join(out_720_dir, rel) if rel != "." else out_720_dir
            ensure_dir(target_1080_dir)
            ensure_dir(target_720_dir)

            for file in files:
                if not file.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                    continue
                src_path = os.path.join(subdir, file)
                compress_image(src_path, target_1080_dir, target_720_dir)


if __name__ == "__main__":
    # Run from the script directory (ImageConverter)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    process_sources(script_dir)


