## Image Converter (to 1080p and 720p JPG)

What this does
- Converts all images in every source folder inside `ImageConverter` (except `1080p` and `720p`).
- Outputs JPEG files only, no cropping, aspect ratio preserved.
- Two outputs with mirrored folder names and structure:
  - `ImageConverter/1080p/<source>/.../*.jpg`
  - `ImageConverter/720p/<source>/.../*.jpg`

Supported inputs
- `.jpg`, `.jpeg`, `.png`, `.webp` (others are ignored)

How to use
1) Put or update your images inside a folder under `ImageConverter` (e.g., `Exhibition Gallery 2025`).
   - Do NOT put images directly into `1080p` or `720p` (these are output folders).
2) Run the converter:
   - Double-click `convert_images.bat`, or
   - Open PowerShell in this folder and run:
     ```powershell
     .\convert_images.bat
     ```
3) Find the results in `1080p/<your folder>/...` and `720p/<your folder>/...`.

Notes
- Images smaller than the target height (1080 or 720) are not upscaled; they are just saved as optimized JPG.
- Transparent images are flattened onto white background before saving to JPG.
- If you add new images later, just run `convert_images.bat` again; existing outputs will be overwritten.

Related tool
- For fixed equal width/height (pad or crop), use `EqualImageConverter` instead.
