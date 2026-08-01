import os
import re
from PIL import Image


IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff")
OUTPUT_FOLDER_NAME = "output_pdfs"
INTEGER_PATTERN = re.compile(r"\d+")


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def extract_sequence_number(file_name):
    """Return the first integer found in the file name, if any."""
    match = INTEGER_PATTERN.search(file_name)
    if match is None:
        return None
    return int(match.group())


def get_sort_key(file_name):
    """
    Sort numbered images by their integer, then by name.
    Images without an integer come after numbered ones, alphabetically.
    """
    sequence_number = extract_sequence_number(file_name)
    if sequence_number is None:
        return (1, 0, file_name.lower())
    return (0, sequence_number, file_name.lower())


def convert_to_rgb(img):
    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.split()[-1])
        return background
    if img.mode != "RGB":
        return img.convert("RGB")
    return img


def collect_image_paths(source_folder):
    image_paths = []
    for subdir, _, files in os.walk(source_folder):
        for file_name in files:
            if file_name.lower().endswith(IMAGE_EXTENSIONS):
                image_paths.append(os.path.join(subdir, file_name))
    image_paths.sort(key=lambda path: get_sort_key(os.path.basename(path)))
    return image_paths


def images_to_pdf(image_paths, output_pdf_path):
    if not image_paths:
        print(f"No images found for: {output_pdf_path}")
        return
    opened_images = []
    try:
        for image_path in image_paths:
            img = Image.open(image_path)
            img.load()
            opened_images.append(convert_to_rgb(img))
            sequence_number = extract_sequence_number(os.path.basename(image_path))
            sequence_label = str(sequence_number) if sequence_number is not None else "n/a"
            print(f"  Page order: [{sequence_label}] {os.path.basename(image_path)}")
        first_image = opened_images[0]
        remaining_images = opened_images[1:]
        first_image.save(
            output_pdf_path,
            "PDF",
            resolution=100.0,
            save_all=True,
            append_images=remaining_images,
        )
        print(f"Saved PDF ({len(opened_images)} pages): {output_pdf_path}")
    except Exception as err:
        print(f"Failed to create {output_pdf_path}: {err}")
    finally:
        for img in opened_images:
            img.close()


def collect_root_image_paths(root_folder):
    image_paths = []
    for entry in os.listdir(root_folder):
        full_path = os.path.join(root_folder, entry)
        if not os.path.isfile(full_path):
            continue
        if entry.lower().endswith(IMAGE_EXTENSIONS):
            image_paths.append(full_path)
    image_paths.sort(key=lambda path: get_sort_key(os.path.basename(path)))
    return image_paths


def convert_folders_to_pdf(root_folder):
    output_root = os.path.join(root_folder, OUTPUT_FOLDER_NAME)
    ensure_dir(output_root)
    root_images = collect_root_image_paths(root_folder)
    if root_images:
        output_pdf_path = os.path.join(output_root, "slides.pdf")
        print("\nConverting images in root folder")
        images_to_pdf(root_images, output_pdf_path)
    for entry in os.listdir(root_folder):
        full_path = os.path.join(root_folder, entry)
        if not os.path.isdir(full_path):
            continue
        if entry.lower() == OUTPUT_FOLDER_NAME.lower():
            continue
        image_paths = collect_image_paths(full_path)
        if not image_paths:
            print(f"Skipped empty folder: {entry}")
            continue
        output_pdf_path = os.path.join(output_root, f"{entry}.pdf")
        print(f"\nConverting folder: {entry}")
        images_to_pdf(image_paths, output_pdf_path)


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    convert_folders_to_pdf(script_dir)
