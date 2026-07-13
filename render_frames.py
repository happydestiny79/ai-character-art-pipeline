#!/usr/bin/env python3
"""Render demo frames for AI Character Art Pipeline — using actual fox character art."""

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import os

W, H = 1280, 720
OUT = "/home/jimmy/hermes-gbrain-content/deploy/ai-character-art-pipeline/frames"
FOX_PATH = "/home/jimmy/hermes-gbrain-content/deploy/ai-character-art-pipeline/fox-art-crop.png"
os.makedirs(OUT, exist_ok=True)

# Colors
BG = (16, 18, 24)
ACCENT = (120, 80, 255)      # purple
ACCENT2 = (0, 200, 200)      # teal
ACCENT3 = (255, 180, 50)     # gold
WHITE = (240, 240, 245)
GRAY = (140, 140, 160)

def load_font(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", size)
    except:
        return ImageFont.load_default()

def load_font_regular(size):
    try:
        return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", size)
    except:
        return ImageFont.load_default()

def draw_gradient_bg(draw, w, h, top_color=BG, bottom_color=(25, 28, 38)):
    for y in range(h):
        t = y / h
        r = int(top_color[0] + (bottom_color[0] - top_color[0]) * t)
        g = int(top_color[1] + (bottom_color[1] - top_color[1]) * t)
        b = int(top_color[2] + (bottom_color[2] - top_color[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

def paste_with_glow(canvas, img, x, y, glow_color=(40, 55, 90), glow_radius=15, border_color=(70, 100, 170)):
    """Paste an image with a soft glow behind it and a subtle border."""
    bw, bh = img.size
    # Glow background
    draw = ImageDraw.Draw(canvas)
    draw.rounded_rectangle([x-6, y-6, x+bw+6, y+bh+6], radius=10, fill=glow_color, outline=border_color, width=2)
    # Dark overlay then image
    overlay = Image.new('RGB', (bw, bh), (20, 22, 28))
    canvas.paste(overlay, (x, y))
    canvas.paste(img, (x, y))

def draw_step_badge(draw, label, x=40, y=20):
    """Blue-purple step indicator."""
    bbox = load_font_regular(20).getbbox(label)
    lw = bbox[2] - bbox[0]
    pw, ph = lw + 24, 32
    draw.rounded_rectangle([x, y, x+pw, y+ph], radius=16, fill=ACCENT)
    draw.text((x+12, y+5), label, fill="white", font=load_font_regular(20))

def draw_bottom_bar(draw, text="Elston Gunn"):
    """Bottom branding bar."""
    font = load_font_regular(16)
    bbox = font.getbbox(text)
    tw = bbox[2] - bbox[0]
    cx = W - tw - 24
    cy = H - 32
    draw.rounded_rectangle([cx-8, cy-4, cx+tw+8, cy+24], radius=12, fill=(35, 42, 58), outline=(65, 80, 110))
    draw.text((cx, cy+1), text, fill=(160, 180, 210), font=font)

def frame_01_title():
    """Title card with fox art hero."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H)

    fox = Image.open(FOX_PATH)
    fox_resized = fox.resize((900, 506), Image.LANCZOS)
    paste_with_glow(img, fox_resized, (W-900)//2, 80, glow_color=(35, 45, 72), glow_radius=12)

    # Top left: title
    font_title = load_font(36)
    font_tag = load_font(20)
    draw.text((40, 25), "AI CHARACTER ART", fill=WHITE, font=font_title)
    draw.text((40, 65), "PIPELINE", fill=ACCENT2, font=font_title)
    draw.rounded_rectangle([40, 102, 200, 108], radius=3, fill=ACCENT2)

    # Bottom left: tagline
    draw.text((40, H-70), "One reference image → Full character consistency", fill=GRAY, font=font_tag)

    draw_bottom_bar(draw)
    img.save(f"{OUT}/frame_001_title.png")
    print("  frame_001_title ✓")

def frame_02_input():
    """Step 1: Drop in one reference image — show fox art as output."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H, bottom_color=(20, 22, 30))

    draw_step_badge(draw, "Step 1: Input Image")

    fox = Image.open(FOX_PATH)

    # Left side: "Reference" (smaller, desaturated)
    ref_w, ref_h = 360, 203
    ref = fox.resize((ref_w, ref_h), Image.LANCZOS)
    # Desaturate it
    ref_desat = ref.convert("L").convert("RGB")
    paste_with_glow(img, ref_desat, 80, 180, glow_color=(30, 35, 55), border_color=(70, 80, 100))
    draw.text((80, 140), "YOUR REFERENCE", fill=GRAY, font=load_font_regular(18))
    draw.text((80, 400), "One image of your character", fill=GRAY, font=load_font_regular(16))

    # Arrow
    arrow_x, arrow_y = 500, 340
    draw.line([(450, arrow_y), (510, arrow_y)], fill=ACCENT2, width=3)
    draw.polygon([(510, arrow_y-8), (520, arrow_y), (510, arrow_y+8)], fill=ACCENT2)
    draw.text((460, arrow_y+10), "AI", fill=ACCENT2, font=load_font(24))

    # Right side: "Output" (fox art fully colored)
    out_w, out_h = 480, 270
    out = fox.resize((out_w, out_h), Image.LANCZOS)
    paste_with_glow(img, out, 600, 150, glow_color=(45, 55, 85), border_color=(100, 145, 220))
    draw.text((600, 110), "FULL CHARACTER", fill=ACCENT, font=load_font_regular(18))
    draw.text((600, 440), "Consistent art, multiple poses", fill=GRAY, font=load_font_regular(16))

    draw_bottom_bar(draw)
    img.save(f"{OUT}/frame_02_input.png")
    print("  frame_02_input ✓")

def frame_03_showcase():
    """Step 2: Full character art — large fox art with detail callouts."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H, bottom_color=(20, 22, 30))

    draw_step_badge(draw, "Step 2: Generated Art")

    fox = Image.open(FOX_PATH)

    # Main art panel — large size on the left
    main_w, main_h = 640, 480
    main = fox.resize((main_w, main_h), Image.LANCZOS)
    paste_with_glow(img, main, 40, 100, glow_color=(35, 45, 72), border_color=(80, 110, 170))

    # Right panel: feature callouts
    features = [
        ("🎨", "Full Color", "Rich character art with\nconsistent palette"),
        ("🎭", "Expressive", "Character details and\npersonality captured"),
        ("📐", "Scalable", "Works for any art style\nor character type"),
    ]

    for i, (icon, title, desc) in enumerate(features):
        y = 110 + i * 170
        # Feature card
        draw.rounded_rectangle([730, y, 1220, y+150], radius=10, fill=(28, 32, 44), outline=(50, 58, 76))
        draw.text((750, y+15), icon, fill=WHITE, font=load_font(28))
        draw.text((790, y+16), title, fill=WHITE, font=load_font(22))
        # Description
        for li, line in enumerate(desc.split("\n")):
            draw.text((750, y+50+li*22), line, fill=GRAY, font=load_font_regular(16))

    draw_bottom_bar(draw)
    img.save(f"{OUT}/frame_03_showcase.png")
    print("  frame_03_showcase ✓")

def frame_04_expression():
    """Step 3: Expression details — crop face area of fox art."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H, bottom_color=(20, 22, 30))

    draw_step_badge(draw, "Step 3: Expression Sheet")

    fox = Image.open(FOX_PATH)
    fw, fh = fox.size

    # Crop the face area (top-center portion of the fox art)
    face_crop = fox.crop((fw//4, fh//6, 3*fw//4, fh//2))
    face_w, face_h = face_crop.size

    # Create 4 expression variants by color-shifting / flipping
    # We'll show the same face in a 2x2 grid with different overlays
    exp_w, exp_h = 280, 250
    gap = 30
    start_x = (W - (2 * exp_w + gap)) // 2
    start_y = 110

    expressions = [
        ("HAPPY", ACCENT2),
        ("NEUTRAL", ACCENT),
        ("SERIOUS", (255, 100, 100)),
        ("PLAYFUL", ACCENT3),
    ]

    face_resized = face_crop.resize((exp_w, exp_h), Image.LANCZOS)

    for i, (label, color) in enumerate(expressions):
        col = i % 2
        row = i // 2
        x = start_x + col * (exp_w + gap)
        y = start_y + row * (exp_h + gap + 20)

        # Card
        draw.rounded_rectangle([x-4, y-4, x+exp_w+4, y+exp_h+34], radius=10, fill=(25, 28, 38), outline=(45, 52, 68))
        img.paste(face_resized, (x, y))

        # Label with color accent
        draw.rounded_rectangle([x+8, y+exp_h-36, x+exp_w-8, y+exp_h-8], radius=8, fill=color)
        draw.text((x+14, y+exp_h-30), label, fill="white", font=load_font_regular(20))

    # Title
    draw.text((50, 420), "Expressiveness preserved from", fill=GRAY, font=load_font_regular(18))
    draw.text((50, 442), "your single reference image", fill=GRAY, font=load_font_regular(18))

    draw_bottom_bar(draw)
    img.save(f"{OUT}/frame_04_expression.png")
    print("  frame_04_expression ✓")

def frame_05_details():
    """Step 4: Character details — showcase zoomed portions."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H, bottom_color=(20, 22, 30))

    draw_step_badge(draw, "Step 4: Full Character Bible")

    fox = Image.open(FOX_PATH)
    fw, fh = fox.size

    # Three detail crops from different areas of the fox art
    crops = [
        ("Character Design", fox.crop((fw//3, fh//3, 2*fw//3, 2*fh//3)), "Core character\ndesign & proportions"),
        ("Color Palette", fox.crop((0, 0, fw//2, fh//2)), "Rich color palette\nextracted automatically"),
        ("Style Reference", fox.crop((fw//2, fh//3, fw, 2*fh//3)), "Consistent style\nacross all outputs"),
    ]

    for i, (title, crop, desc) in enumerate(crops):
        x = 50 + i * 420
        y = 90
        cw, ch = 350, 260
        resized = crop.resize((cw, ch), Image.LANCZOS)

        # Card
        draw.rounded_rectangle([x, y, x+cw+20, y+ch+80], radius=10, fill=(25, 28, 38), outline=(45, 52, 68))
        img.paste(resized, (x+10, y+10))

        # Title
        draw.text((x+12, y+ch+20), title, fill=WHITE, font=load_font(20))

        # Description
        for li, line in enumerate(desc.split("\n")):
            draw.text((x+12, y+ch+48+li*20), line, fill=GRAY, font=load_font_regular(16))

    draw_bottom_bar(draw)
    img.save(f"{OUT}/frame_05_details.png")
    print("  frame_05_details ✓")

def frame_06_cta():
    """Call to action — fox art with final card."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H)

    fox = Image.open(FOX_PATH)
    fox_resized = fox.resize((640, 360), Image.LANCZOS)
    paste_with_glow(img, fox_resized, 40, 60, glow_color=(35, 45, 72))

    # Right panel: CTA
    draw.text((740, 100), "AI Character Art", fill=WHITE, font=load_font(32))
    draw.text((740, 140), "Pipeline", fill=ACCENT2, font=load_font(32))

    # Features checklist
    features = [
        "✓ One reference image only",
        "✓ Consistent character art",
        "✓ Expression sheets & turnarounds",
        "✓ Multi-style support",
        "✓ Instant export",
    ]
    for i, feat in enumerate(features):
        y_pos = 190 + i * 34
        draw.text((750, y_pos), feat, fill=GRAY, font=load_font_regular(18))

    # Price badge
    draw.rounded_rectangle([740, 370, 940, 420], radius=20, fill=ACCENT)
    draw.text((765, 378), "$7.99", fill="white", font=load_font(28))

    # Available text
    draw.text((740, 440), "Available now on", fill=GRAY, font=load_font_regular(18))
    draw.text((740, 465), "Agensi", fill=ACCENT2, font=load_font(24))

    draw_bottom_bar(draw)
    img.save(f"{OUT}/frame_06_cta.png")
    print("  frame_06_cta ✓")

def frame_07_end():
    """End card — prompt to action."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_gradient_bg(draw, W, H)

    # Big checkmark
    draw.ellipse([W//2 - 55, H//2 - 175, W//2 + 55, H//2 - 65], fill=(0, 200, 100))
    draw.text((W//2 - 23, H//2 - 132), "✓", fill="white", font=load_font(72))

    draw.text((W//2 - 195, H//2 - 30), "AI Character Art Pipeline", fill=WHITE, font=load_font(28))
    draw.text((W//2 - 130, H//2 + 25), "Available now on Agensi", fill=ACCENT2, font=load_font_regular(22))
    draw.text((W//2 - 215, H//2 + 65), "One image → Full character consistency", fill=GRAY, font=load_font_regular(18))

    # Badge
    draw.rounded_rectangle([W//2 - 75, H//2 + 110, W//2 + 75, H//2 + 150], radius=20, fill=ACCENT)
    draw.text((W//2 - 42, H//2 + 118), "$7.99", fill="white", font=load_font(22))

    draw_bottom_bar(draw)
    img.save(f"{OUT}/frame_007_end.png")
    print("  frame_007_end ✓")

if __name__ == "__main__":
    print("Rendering frames with fox character art...")
    frame_01_title()
    frame_02_input()
    frame_03_showcase()
    frame_04_expression()
    frame_05_details()
    frame_06_cta()
    frame_07_end()
    print("Done — 7 frames rendered.")