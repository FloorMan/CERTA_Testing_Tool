from PIL import Image, ImageDraw, ImageFont # Make sure you have Pillow installed
import re
import os


Images = ["c:/Users/DiegoAguirre/Desktop/TP-004_Dry_run/C114/Screenshots/" + f for f in os.listdir("c:/Users/DiegoAguirre/Desktop/TP-004_Dry_run/C114/Screenshots")]
#print(Images)
#Images_loaded = [Image.open(image) for image in Images]


pdf_path = "c:/Users/DiegoAguirre/Desktop/TP-004_Dry_run/C114/FinishedDocs/114DryRun.pdf"


highest_test_case = 104
highest_steps = 30

sortedImages = []

# Per test case, we order it by test step and then appended letter (a, b, or c)
for test_case in range(highest_test_case):
    pattern_test = re.compile(rf".*Screenshots/{test_case}-.*") # For the test case
    
    test_steps = [test for test in Images if pattern_test.match(test)]
    if len(test_steps) == 0:
        continue

    sorted = []
    for step in range(1, highest_steps):
        pattern_step = re.compile(rf".*_{step}[a-z].png") # For the step
        matched = [test for test in test_steps if pattern_step.match(test)]
        sorted.extend(matched)
    #print(sorted)
    
    sortedImages.extend(sorted)

#print(sortedImages)

TARGET_WIDTH = 800
TARGET_HEIGHT = 1000
CAPTION_HEIGHT = 40
FONT_SIZE = 24

def process_image_with_caption(image_path, caption):
    # Open and resize image
    img = Image.open(image_path).convert("RGB")
    img.thumbnail((TARGET_WIDTH, TARGET_HEIGHT - CAPTION_HEIGHT), Image.LANCZOS)
    
    # Create white background
    background = Image.new("RGB", (TARGET_WIDTH, TARGET_HEIGHT), (255, 255, 255))
    # Center image
    x = (TARGET_WIDTH - img.width) // 2
    y = (TARGET_HEIGHT - CAPTION_HEIGHT - img.height) // 2
    background.paste(img, (x, y))
    
    # Draw caption
    draw = ImageDraw.Draw(background)
    try:
        font = ImageFont.truetype("arial.ttf", FONT_SIZE)
    except:
        font = ImageFont.load_default()
    bbox = draw.textbbox((0,0), caption, font=font)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    text_x = (TARGET_WIDTH - text_width) // 2
    text_y = TARGET_HEIGHT - CAPTION_HEIGHT + (CAPTION_HEIGHT - text_height) // 2
    draw.text((text_x, text_y), caption, fill=(0, 0, 0), font=font)
    return background

# Prepare processed images with captions
processed_images = []
for img_path in sortedImages:
    caption = os.path.basename(img_path)
    processed = process_image_with_caption(img_path, caption)
    processed_images.append(processed)



#loadedImages = [Image.open(image) for image in processed_images]

processed_images[0].save(pdf_path, "PDF", resolution=100.0, save_all=True, append_images=processed_images[1:])



#pdf_path = "C:\Users\DiegoAguirre\Desktop\TP-004_Dry_run\C114\PDFs\C114_20250106-093249.pdf"
#pdf = Image.open(pdf_path)
#pdf.save(pdf_path, save_all=True, append_images=images)


