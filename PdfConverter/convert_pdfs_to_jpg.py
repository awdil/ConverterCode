import os
import fitz  # PyMuPDF
from PIL import Image

# Function to convert each page of a PDF to JPG with improved quality and size control
def pdf_to_jpg(pdf_path, output_folder, max_file_size_kb=200):
    # Open the PDF file
    pdf_document = fitz.open(pdf_path)

    # Loop through each page of the PDF
    for page_num in range(pdf_document.page_count):
        # Get the page
        page = pdf_document.load_page(page_num)

        # Render the page to a pixmap with higher DPI for better quality
        # Default DPI is usually around 150, we'll use 300 for better quality
        dpi = 300
        pix = page.get_pixmap(matrix=fitz.Matrix(dpi/72, dpi/72))

        # Convert the pixmap to a PIL image
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

        # Save the image as JPG with quality optimization
        output_path = os.path.join(output_folder, f"{os.path.basename(pdf_path)}_page_{page_num + 1}.jpg")

        # Start with high quality and optimize, then reduce if file is too large
        quality = 95
        img.save(output_path, "JPEG", quality=quality, optimize=True, progressive=True)

        # Check file size and reduce quality if needed
        file_size_kb = os.path.getsize(output_path) / 1024

        # If file is still too large, reduce quality in steps
        while file_size_kb > max_file_size_kb and quality > 60:
            quality -= 10
            img.save(output_path, "JPEG", quality=quality, optimize=True, progressive=True)
            file_size_kb = os.path.getsize(output_path) / 1024

        # If still too large, resize the image more aggressively
        if file_size_kb > max_file_size_kb:
            # Try with a smaller size first (aim for ~150-180KB to have buffer)
            target_kb = max_file_size_kb * 0.8  # Leave 20% buffer
            resize_factor = (target_kb / file_size_kb) ** 0.7  # More aggressive reduction
            new_width = max(600, int(img.width * resize_factor))  # Minimum width for readability
            new_height = max(400, int(img.height * resize_factor))  # Minimum height for readability

            # Resize and save with quality 75
            img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            img_resized.save(output_path, "JPEG", quality=75, optimize=True, progressive=True)

            # Check final size
            file_size_kb = os.path.getsize(output_path) / 1024

            # If still too large, reduce quality further
            if file_size_kb > max_file_size_kb:
                img_resized.save(output_path, "JPEG", quality=65, optimize=True, progressive=True)
                file_size_kb = os.path.getsize(output_path) / 1024

        print(f"Saved: {os.path.basename(output_path)} ({file_size_kb:.1f} KB)")

# Function to iterate through directories and convert all PDFs
def convert_pdfs_in_folders(root_folder):
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith('.pdf'):
                pdf_path = os.path.join(subdir, file)
                output_folder = os.path.join(subdir, "output_images")  # Save output images here
                os.makedirs(output_folder, exist_ok=True)

                # Convert PDF to JPG
                pdf_to_jpg(pdf_path, output_folder)
                print(f"Converted {pdf_path} to JPGs in {output_folder}")

# Provide the root folder that contains your multiple folders and PDFs
root_folder = os.getcwd()  # Get the current working directory
convert_pdfs_in_folders(root_folder)
