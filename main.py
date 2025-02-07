import os
import math
import sys
from io import BytesIO

from PIL import Image, ImageDraw
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

# Folder containing the source images.
INPUT_IMAGES_DIR = "input_images"
# Output PDF file name.
OUTPUT_PDF = "output.pdf"
# Target diameter in millimeters.
TARGET_MM = 58
# DPI for image resizing (for print quality).
DPI = 300
# Convert 58mm to pixels (for Pillow processing).
TARGET_PX = int(TARGET_MM / 25.4 * DPI)
# Convert 58mm to PDF points (1 inch = 72 points; 25.4 mm = 1 inch).
TARGET_PD = TARGET_MM * 72 / 25.4

# PDF layout settings (in points).
MARGIN = 20  # margin from page borders
SPACING = 10  # spacing between images


def process_image(image_path: str) -> Image.Image:
    """
    Open an image, center-crop it to a square, resize to TARGET_PX x TARGET_PX,
    apply a circular mask, and composite it on a white background.
    """
    im = Image.open(image_path).convert("RGBA")
    width, height = im.size
    # Center-crop to square.
    min_side = min(width, height)
    left = (width - min_side) // 2
    top = (height - min_side) // 2
    right = left + min_side
    bottom = top + min_side
    im = im.crop((left, top, right, bottom))

    # Resize to target pixel dimensions.
    im = im.resize((TARGET_PX, TARGET_PX), resample=Image.Resampling.LANCZOS)

    # Create circular mask.
    mask = Image.new("L", (TARGET_PX, TARGET_PX), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, TARGET_PX, TARGET_PX), fill=255)

    # Apply mask to make the image circular.
    im.putalpha(mask)
    # Composite with a white background.
    background = Image.new("RGBA", (TARGET_PX, TARGET_PX), (255, 255, 255, 255))
    composite = Image.alpha_composite(background, im)

    # Convert back to RGB.
    return composite.convert("RGB")


def generate_pdf():
    """
    Process all images in INPUT_IMAGES_DIR, arrange them on A4 pages
    (in a grid layout) with each image drawn at a 58mm (TARGET_PD points) diameter,
    and save the result to OUTPUT_PDF.
    """
    if not os.path.exists(INPUT_IMAGES_DIR):
        print(f"Input images directory '{INPUT_IMAGES_DIR}' not found. Exiting...")
        sys.exit(1)

    processed_images = []
    image_files = sorted(os.listdir(INPUT_IMAGES_DIR))
    for filename in image_files:
        file_path = os.path.join(INPUT_IMAGES_DIR, filename)
        if os.path.isfile(file_path) and filename.lower().endswith(
            (".png", ".jpg", ".jpeg", ".bmp", ".gif")
        ):
            try:
                processed = process_image(file_path)
                processed_images.append(processed)
            except Exception as e:
                print(f"Error processing image {filename}: {e}")

    if not processed_images:
        print("No valid images found in the directory. Exiting...")
        sys.exit(1)

    # Create PDF in memory.
    pdf_buffer = BytesIO()
    page_width, page_height = A4  # dimensions in points

    c = canvas.Canvas(pdf_buffer, pagesize=A4)

    # Calculate grid layout: number of columns and rows per page.
    cols = math.floor((page_width - 2 * MARGIN + SPACING) / (TARGET_PD + SPACING))
    rows = math.floor((page_height - 2 * MARGIN + SPACING) / (TARGET_PD + SPACING))
    cols = max(cols, 1)
    rows = max(rows, 1)
    capacity = cols * rows

    for i, img in enumerate(processed_images):
        # Start a new page if the current one is full.
        if i % capacity == 0 and i != 0:
            c.showPage()

        current_page_index = i % capacity
        col_index = current_page_index % cols
        row_index = current_page_index // cols
        # Calculate position: PDF origin is bottom‑left.
        x = MARGIN + col_index * (TARGET_PD + SPACING)
        y = page_height - MARGIN - TARGET_PD - row_index * (TARGET_PD + SPACING)

        # Draw the PIL image directly.
        c.drawInlineImage(img, x, y, width=TARGET_PD, height=TARGET_PD)

    c.save()

    # Write pdf_buffer to a file.
    with open(OUTPUT_PDF, "wb") as f:
        f.write(pdf_buffer.getvalue())

    print(f"PDF generated successfully as '{OUTPUT_PDF}'.")


if __name__ == "__main__":
    generate_pdf()
