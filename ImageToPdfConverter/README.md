## Image to PDF Converter

What this does
- Converts images from each source folder inside `ImageToPdfConverter` into one PDF per folder.
- Orders PDF pages by the first integer found in each image file name.
- Saves outputs under `output_pdfs/<folder-name>.pdf`.

Example sequencing
- `Slide 10 Fuel Cost Intelligence.jpg` → page for sequence **10**
- `Slide 11 Fuel Cost Intelligence.jpg` → page for sequence **11**
- Any file name works; if an integer is present, that number controls page order.
- Images with no integer are placed after the numbered ones (alphabetically).

Supported inputs
- `.jpg`, `.jpeg`, `.png`, `.webp`, `.bmp`, `.tif`, `.tiff`

How to use
1) Put images either:
   - Directly in `ImageToPdfConverter` → creates `output_pdfs/slides.pdf`, or
   - Inside a subfolder (e.g. `Fuel Cost Intelligence/`) → creates `output_pdfs/<folder name>.pdf`
   - Do NOT put images into `output_pdfs` (that is the output folder).
2) Run the converter:
   - Double-click `convert_images_to_pdf.bat`, or
   - Open PowerShell in this folder and run:
     ```powershell
     .\convert_images_to_pdf.bat
     ```
3) Find the PDF in `output_pdfs/`.

Notes
- Transparent images are flattened onto a white background before writing the PDF.
- Images pasted in the root become `slides.pdf`. Each subfolder becomes its own PDF.
- If you add or rename images later, run `convert_images_to_pdf.bat` again; the PDF is overwritten.
