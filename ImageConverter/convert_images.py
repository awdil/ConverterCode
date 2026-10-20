
import os
from PIL import Image, ImageOps


# Image settings
IMAGE_SIZES = {
    "720p": {"max_height": 720, "quality": 80},
    "1080p": {"max_height": 1080, "quality": 85},
    "1536p": {"max_width": 1536, "max_height": 1536, "quality": 85},
    "2048p": {"max_width": 2048, "max_height": 2048, "quality": 90},
}

SUPPORTED_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp")


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def get_target_size(width, height, settings):
    max_width = settings.get("max_width")
    max_height = settings["max_height"]

    # Maintain aspect ratio and never upscale.
    scale = min(1.0, max_height / height)

    if max_width is not None:
        scale = min(scale, max_width / width)

    return (
        max(1, int(width * scale)),
        max(1, int(height * scale)),
    )


def save_jpeg(img, output_path, quality):
    if img.mode in ("RGBA", "LA") or (
        img.mode == "P" and "transparency" in img.info
    ):
        img = img.convert("RGBA")
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.getchannel("A"))
        img = background

    elif img.mode != "RGB":
        img = img.convert("RGB")

    img.save(
        output_path,
        "JPEG",
        quality=quality,
        optimize=True,
        progressive=True
    )


def compress_image(input_path, output_dirs):
    try:
        with Image.open(input_path) as source:
            img = ImageOps.exif_transpose(source)
            width, height = img.size

            base_name = os.path.basename(input_path)
            name, _ = os.path.splitext(base_name)

            for size_name, settings in IMAGE_SIZES.items():
                new_width, new_height = get_target_size(
                    width, height, settings
                )

                if (new_width, new_height) == (width, height):
                    resized_img = img
                else:
                    resized_img = img.resize(
                        (new_width, new_height),
                        Image.Resampling.LANCZOS
                    )

                output_dir = output_dirs[size_name]
                ensure_dir(output_dir)

                output_path = os.path.join(
                    output_dir, f"{name}.jpg"
                )

                save_jpeg(
                    resized_img,
                    output_path,
                    settings["quality"]
                )

                print(
                    f"  {size_name}: "
                    f"{new_width}x{new_height}"
                )

            print(f"Processed: {base_name}\n")

    except Exception as e:
        print(f"Failed to process {input_path}: {e}")


def process_sources(root_folder):

    # Create output folders
    output_roots = {}

    for size_name in IMAGE_SIZES:
        output_root = os.path.join(root_folder, size_name)
        ensure_dir(output_root)
        output_roots[size_name] = output_root

    # Ignore generated output folders
    excluded_folders = {
        name.lower() for name in IMAGE_SIZES
    }

    # Process each source folder
    for entry in os.listdir(root_folder):
        full_path = os.path.join(root_folder, entry)

        if not os.path.isdir(full_path):
            continue

        if entry.lower() in excluded_folders:
            continue

        for subdir, _, files in os.walk(full_path):

            rel = os.path.relpath(subdir, full_path)

            output_dirs = {}

            for size_name, output_root in output_roots.items():

                target_dir = os.path.join(
                    output_root,
                    entry
                )

                if rel != ".":
                    target_dir = os.path.join(
                        target_dir, rel
                    )

                ensure_dir(target_dir)
                output_dirs[size_name] = target_dir

            for file in files:

                if not file.lower().endswith(
                    SUPPORTED_EXTENSIONS
                ):
                    continue

                src_path = os.path.join(subdir, file)

                compress_image(
                    src_path,
                    output_dirs
                )


if __name__ == "__main__":

    script_dir = os.path.dirname(
        os.path.abspath(__file__)
    )

    process_sources(script_dir)
