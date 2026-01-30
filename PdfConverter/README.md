## PDF to JPG Converter

What this does
- Converts every page of each PDF inside this folder tree to JPG images.
- Saves outputs next to each PDF inside an `output_images` subfolder.

How to use
1) Put or update your PDFs anywhere under this `PdfConverter` folder.
2) Run the converter:
   - Double-click `convert_pdfs.bat`, or
   - Open PowerShell in this folder and run:
     ```powershell
     .\convert_pdfs.bat
     ```
3) Check the `output_images` folder created alongside each PDF for the generated JPG files.

Notes
- Each page becomes a JPG file named like: `<PDF_NAME>_page_<N>.jpg`.
- The script balances quality and size; it may reduce quality or resize slightly to keep files smaller.
- If you add new PDFs later, just run `convert_pdfs.bat` again; new JPGs will be created.



