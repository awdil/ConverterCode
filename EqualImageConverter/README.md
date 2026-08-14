## Equal Image Converter (fixed width × height)

What this does
- Separate tool from `ImageConverter` — use this when every image must share the same size.
- For each source folder, creates **four** output versions:
  - `fit-1080p/` — **1920×1080**, scale to fit + white padding (no crop)
  - `fit-720p/` — **1280×720**, scale to fit + white padding (no crop)
  - `crop-1080p/` — **1920×1080**, scale to cover + center crop
  - `crop-720p/` — **1280×720**, scale to cover + center crop

Fit vs Crop
| Mode | Result | Best for |
|------|--------|----------|
| **Fit** | Full image visible, white bars if aspect differs | Slides, UI, no content loss |
| **Crop** | Fills the frame edge-to-edge, edges may be trimmed | Photos, thumbnails, galleries |

Supported inputs
- `.jpg`, `.jpeg`, `.png`, `.webp`

How to use
1) Put images either:
   - Directly in `EqualImageConverter` → outputs go into the four folders at the top level, or
   - Inside a subfolder (e.g. `Gallery 2025`) → outputs go under `<output>/<folder name>/`
   - Do NOT put images into `fit-1080p`, `fit-720p`, `crop-1080p`, or `crop-720p`.
2) Run:
   - Double-click `convert_equal_images.bat`, or
   - In PowerShell:
     ```powershell
     .\convert_equal_images.bat
     ```
3) Find outputs in the four folders above.

Notes
- Transparent images are flattened onto white before saving as JPG.
- Re-run anytime; existing outputs are overwritten.
- For variable-width compression only (no fixed canvas), use `ImageConverter` instead.
