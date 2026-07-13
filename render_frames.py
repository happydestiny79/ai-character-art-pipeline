#!/usr/bin/env python3
"""Render demo frames for AI Character Art Pipeline demo video."""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1280, 720
FONT_SIZE = 40
SMALL_FONT = 28
TINY_FONT = 22
OUT = "/home/jimmy/hermes-gbrain-content/deploy/ai-character-art-pipeline/frames"
os.makedirs(OUT, exist_ok=True)

# Colors
BG = (20, 22, 28)
ACCENT = (120, 80, 255)     # purple
ACCENT2 = (0, 200, 200)     # teal
WHITE = (240, 240, 245)
GRAY = (140, 140, 160)
CARD_BG = (30, 34, 42)

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

def rounded_box(draw, xy, radius=12, fill=CARD_BG, outline=None):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline)

def draw_title_bar(draw, text, y=20):
    """Draw a small title/step indicator at the top."""
    # Step indicator bubble
    draw.rounded_rectangle([40, y, 200, y + 36], radius=18, fill=ACCENT)
    draw.text((52, y + 5), "DEMO", fill="white", font=load_font(SMALL_FONT))
    draw.text((210, y + 5), text, fill=GRAY, font=load_font_regular(SMALL_FONT))

def draw_character_slot(draw, x, y, w, h, label="", filled=False):
    """Draw a card/frame placeholder for a character image."""
    color = ACCENT if filled else (50, 54, 64)
    rounded_box(draw, [x, y, x + w, y + h], radius=8, fill=color)
    if label:
        tw = draw.textlength(label, font=load_font_regular(TINY_FONT))
        draw.text((x + (w - tw) // 2, y + h + 8), label, fill=GRAY, font=load_font_regular(TINY_FONT))

def draw_face(draw, cx, cy, r, expression="neutral"):
    """Draw a simple cartoon face showing different expressions."""
    # Head
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(220, 180, 140), outline=(60, 40, 20), width=2)
    # Eyes
    eye_y = cy - r//4
    eye_spacing = r//3
    if expression in ["happy", "playful"]:
        # ^ ^ eyes
        draw.arc([cx - eye_spacing - 5, eye_y - 8, cx - eye_spacing + 5, eye_y + 2], 180, 360, fill=(30, 30, 30), width=2)
        draw.arc([cx + eye_spacing - 5, eye_y - 8, cx + eye_spacing + 5, eye_y + 2], 180, 360, fill=(30, 30, 30), width=2)
    elif expression in ["sad", "worried"]:
        # . . eyes
        draw.ellipse([cx - eye_spacing - 4, eye_y - 3, cx - eye_spacing + 4, eye_y + 3], fill=(30, 30, 30))
        draw.ellipse([cx + eye_spacing - 4, eye_y - 3, cx + eye_spacing + 4, eye_y + 3], fill=(30, 30, 30))
    elif expression == "surprised":
        # O O eyes
        draw.ellipse([cx - eye_spacing - 5, eye_y - 5, cx - eye_spacing + 5, eye_y + 5], fill=(30, 30, 30))
        draw.ellipse([cx + eye_spacing - 5, eye_y - 5, cx + eye_spacing + 5, eye_y + 5], fill=(30, 30, 30))
    elif expression == "sleepy":
        # - - eyes
        draw.line([cx - eye_spacing - 6, eye_y, cx - eye_spacing + 6, eye_y], fill=(30, 30, 30), width=2)
        draw.line([cx + eye_spacing - 6, eye_y, cx + eye_spacing + 6, eye_y], fill=(30, 30, 30), width=2)
    else:
        # normal o o
        draw.ellipse([cx - eye_spacing - 4, eye_y - 3, cx - eye_spacing + 4, eye_y + 3], fill=(30, 30, 30))
        draw.ellipse([cx + eye_spacing - 4, eye_y - 3, cx + eye_spacing + 4, eye_y + 3], fill=(30, 30, 30))
    # Mouth
    mouth_y = cy + r//3
    if expression == "happy":
        draw.arc([cx - r//3, mouth_y - 5, cx + r//3, mouth_y + 10], 0, 180, fill=(180, 60, 60), width=2)
    elif expression == "sad":
        draw.arc([cx - r//3, mouth_y - 5, cx + r//3, mouth_y + 10], 180, 360, fill=(180, 60, 60), width=2)
    elif expression == "surprised":
        draw.ellipse([cx - 6, mouth_y - 3, cx + 6, mouth_y + 8], fill=(180, 60, 60))
    elif expression == "curious":
        draw.arc([cx - r//4, mouth_y - 3, cx + r//4, mouth_y + 5], 0, 360, fill=(180, 60, 60), width=2)
    elif expression == "worried":
        draw.arc([cx - r//3, mouth_y - 3, cx + r//3, mouth_y + 5], 0, 180, fill=(180, 60, 60), width=2)
    elif expression == "sleepy":
        draw.arc([cx - r//4, mouth_y, cx + r//4, mouth_y + 5], 180, 360, fill=(180, 60, 60), width=2)
    elif expression == "playful":
        draw.arc([cx - r//3, mouth_y - 5, cx + r//3, mouth_y + 15], 0, 180, fill=(180, 60, 60), width=2)
    else:  # neutral
        draw.line([cx - r//3, mouth_y, cx + r//3, mouth_y], fill=(180, 60, 60), width=2)

def draw_body(draw, cx, y, h, color=(100, 120, 200)):
    """Simple body shape."""
    # body
    draw.rounded_rectangle([cx - 20, y, cx + 20, y + h], radius=8, fill=color)
    # arms
    draw.rounded_rectangle([cx - 40, y + 10, cx - 20, y + h//2 + 10], radius=6, fill=color)
    draw.rounded_rectangle([cx + 20, y + 10, cx + 40, y + h//2 + 10], radius=6, fill=color)

# ===== FRAME GENERATION =====

def frame_01_title():
    """Title card."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # Decorative circles
    draw.ellipse([W//2 - 200, H//2 - 250, W//2 - 50, H//2 - 100], fill=(120, 80, 255, 40), outline=ACCENT, width=2)
    draw.ellipse([W//2 + 50, H//2 - 200, W//2 + 200, H//2 - 50], fill=(0, 200, 200, 30), outline=ACCENT2, width=2)
    # Title
    font_title = load_font(56)
    font_sub = load_font_regular(SMALL_FONT)
    t = "AI Character Art Pipeline"
    tw = draw.textlength(t, font=font_title)
    draw.text(((W - tw) // 2, H//2 - 60), t, fill=WHITE, font=font_title)
    # Subtitle
    s = "One reference image → Full character bible"
    sw = draw.textlength(s, font=font_sub)
    draw.text(((W - sw) // 2, H//2 + 20), s, fill=GRAY, font=font_sub)
    # Badge
    draw.rounded_rectangle([W//2 - 100, H//2 + 70, W//2 + 100, H//2 + 110], radius=20, fill=ACCENT)
    draw.text((W//2 - 44, H//2 + 78), "by Elston Gunn", fill="white", font=load_font_regular(TINY_FONT))
    img.save(f"{OUT}/frame_001_title.png")

def frame_02_input():
    """Step 1: Drop in one reference image."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_title_bar(draw, "Step 1: Input")
    # Reference image placeholder (center)
    cx, cy = W//2, H//2 - 20
    r = 100
    draw_face(draw, cx, cy - 20, r, "neutral")
    draw_body(draw, cx, cy + r - 10, 80)
    # Frame around it
    draw.rounded_rectangle([cx - r - 20, cy - r - 40, cx + r + 20, cy + r + 60], radius=12, outline=ACCENT, width=3)
    # Label
    draw.text((cx - 70, cy + r + 80), "REFERENCE IMAGE", fill=ACCENT, font=load_font_regular(SMALL_FONT))
    # Arrow down
    y_arrow = cy + r + 130
    draw.polygon([(cx - 15, y_arrow), (cx, y_arrow + 25), (cx + 15, y_arrow)], fill=ACCENT2)
    # Output label
    draw.text((cx - 100, y_arrow + 35), "→ Full Pipeline Ready", fill=ACCENT2, font=load_font(SMALL_FONT))
    img.save(f"{OUT}/frame_02_input.png")

def frame_03_expression():
    """Step 2: Expression sheet - 2x4 grid of faces."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_title_bar(draw, "Step 2: Expression Sheet")
    # Title
    draw.text((50, 70), "Expression Grid (2 × 4)", fill=WHITE, font=load_font(FONT_SIZE))
    # Draw 8 expressions in 2x4 grid
    expressions = ["happy", "sad", "surprised", "curious", "worried", "sleepy", "playful", "neutral"]
    cols, rows = 4, 2
    cell_w, cell_h = 240, 240
    start_x, start_y = (W - (cols * cell_w + (cols - 1) * 20)) // 2, 130
    for i, expr in enumerate(expressions):
        col = i % cols
        row = i // cols
        x = start_x + col * (cell_w + 20)
        y = start_y + row * (cell_h + 20)
        # Card bg
        rounded_box(draw, [x, y, x + cell_w, y + cell_h], radius=10, fill=CARD_BG)
        # Face
        cx_cell = x + cell_w // 2
        cy_cell = y + cell_h // 2 - 10
        draw_face(draw, cx_cell, cy_cell, 40, expr)
        # Label
        draw.text((x + 10, y + cell_h - 30), expr.upper(), fill=GRAY, font=load_font_regular(TINY_FONT))
    img.save(f"{OUT}/frame_03_expression.png")

def frame_04_turnaround():
    """Step 3: Turnaround - 5 poses."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_title_bar(draw, "Step 3: Turnaround")
    draw.text((50, 70), "5-Angle Turnaround", fill=WHITE, font=load_font(FONT_SIZE))
    # 5 pose slots
    poses = ["Front", "3/4 Front", "Side", "3/4 Back", "Rear"]
    n = 5
    slot_w = 200
    gap = 30
    total_w = n * slot_w + (n - 1) * gap
    start_x = (W - total_w) // 2
    y = 150
    for i, pose in enumerate(poses):
        x = start_x + i * (slot_w + gap)
        rounded_box(draw, [x, y, x + slot_w, y + 300], radius=10, fill=CARD_BG)
        # Simple character silhouette showing rotation
        cx2, cy2 = x + slot_w // 2, y + 140
        # Different width per angle suggests rotation
        widths = [40, 30, 20, 30, 40]
        w_p = widths[i]
        draw.rounded_rectangle([cx2 - w_p//2, cy2 - 40, cx2 + w_p//2, cy2 + 40], radius=w_p//3, fill=(150, 120, 200))
        # Head
        draw.ellipse([cx2 - 20, cy2 - 70, cx2 + 20, cy2 - 30], fill=(200, 170, 140))
        # Label
        draw.text((x + 20, y + 310), pose, fill=GRAY, font=load_font_regular(TINY_FONT))
        # Arrow connecting them
        if i < n - 1:
            ax1 = x + slot_w
            ax2 = x + slot_w + gap
            draw.line([(ax1, cy2), (ax2, cy2)], fill=ACCENT2, width=2)
            draw.polygon([(ax2 - 5, cy2 - 5), (ax2, cy2), (ax2 - 5, cy2 + 5)], fill=ACCENT2)
    # Checkmark at end
    draw.ellipse([start_x + total_w + 30, y + 130, start_x + total_w + 70, y + 170], fill=(0, 200, 100))
    draw.text((start_x + total_w + 38, y + 140), "✓", fill="white", font=load_font(FONT_SIZE))
    img.save(f"{OUT}/frame_04_turnaround.png")

def frame_05_actions():
    """Step 4: Action poses."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_title_bar(draw, "Step 4: Action Poses")
    draw.text((50, 70), "Custom Action Poses", fill=WHITE, font=load_font(FONT_SIZE))
    # 3 action poses side by side
    actions = ["Running", "Jumping", "Casting"]
    poses_d = [
        # Running
        [(-30, 0), (20, -10), (10, 20), (-10, 30)],
        # Jumping
        [(0, -20), (20, -15), (-10, -10), (15, 15)],
        # Casting
        [(-20, -10), (30, -10), (10, 10), (20, 5)]
    ]
    poses_colors = [ACCENT, ACCENT2, (255, 180, 50)]
    for idx, (action, pos_data, col) in enumerate(zip(actions, poses_d, poses_colors)):
        cx2 = 200 + idx * 380
        cy2 = 320
        # Card
        rounded_box(draw, [cx2 - 140, cy2 - 150, cx2 + 140, cy2 + 150], radius=12, fill=CARD_BG, outline=col)
        # Body
        draw_body(draw, cx2, cy2 - 30, 70, col)
        # Head
        draw_face(draw, cx2, cy2 - 100, 30, "happy" if idx == 0 else "neutral")
        # Motion lines
        for dx, dy in pos_data:
            draw.line([(cx2 + dx, cy2 + dy), (cx2 + dx + 20, cy2 + dy + 20)], fill=col, width=2)
        # Label
        draw.text((cx2 - 40, cy2 + 170), action.upper(), fill=col, font=load_font(SMALL_FONT))
    img.save(f"{OUT}/frame_05_actions.png")

def frame_06_bible():
    """Step 5: Character Bible output."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw_title_bar(draw, "Step 5: Output")
    draw.text((50, 70), "Compiled Character Bible", fill=WHITE, font=load_font(FONT_SIZE))
    # Document mockup
    doc_x, doc_y = W//2 - 400, 130
    doc_w, doc_h = 800, 460
    rounded_box(draw, [doc_x, doc_y, doc_x + doc_w, doc_y + doc_h], radius=10, fill=CARD_BG, outline=ACCENT)
    # Title
    draw.text((doc_x + 30, doc_y + 20), "Character Bible: Lila", fill=WHITE, font=load_font(SMALL_FONT))
    draw.line([(doc_x + 30, doc_y + 55), (doc_x + doc_w - 30, doc_y + 55)], fill=(60, 64, 74), width=1)
    # Content lines
    lines = [
        ("Character:", "Lila"),
        ("Style:", "Cartoon / Adventure"),
        ("Palette:", "#FF6B6B, #4ECDC4, #2C3E50"),
        ("", ""),
        ("Assets:", ""),
        ("  ✓ Expression Sheet (2×4 grid)", ""),
        ("  ✓ 5-Angle Turnaround", ""),
        ("  ✓ Action Poses (3 variants)", ""),
        ("  ✓ Prompt Templates (locked)", ""),
    ]
    for i, (label, val) in enumerate(lines):
        y_pos = doc_y + 75 + i * 34
        if label:
            draw.text((doc_x + 40, y_pos), label, fill=GRAY, font=load_font_regular(TINY_FONT))
        if val:
            lw = draw.textlength(label, font=load_font_regular(TINY_FONT))
            draw.text((doc_x + 40 + lw + 8, y_pos), val, fill=WHITE, font=load_font_regular(TINY_FONT))
        # Checkmarks for assets
        if label.startswith("  ✓"):
            draw.text((doc_x + 40, y_pos), label, fill=(0, 200, 100), font=load_font_regular(TINY_FONT))
    # Arrow from reference input to document
    draw.text((doc_x + 30, doc_y + doc_h - 40), "← From one reference image", fill=ACCENT2, font=load_font_regular(TINY_FONT))
    img.save(f"{OUT}/frame_06_bible.png")

def frame_07_cta():
    """Call to action / final card."""
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    # Big checkmark
    draw.ellipse([W//2 - 60, H//2 - 180, W//2 + 60, H//2 - 60], fill=(0, 200, 100))
    draw.text((W//2 - 23, H//2 - 135), "✓", fill="white", font=load_font(72))
    # Title
    draw.text((W//2 - 200, H//2 - 30), "AI Character Art Pipeline", fill=WHITE, font=load_font(FONT_SIZE))
    # Available text
    draw.text((W//2 - 130, H//2 + 30), "Available now on Agensi", fill=ACCENT2, font=load_font_regular(SMALL_FONT))
    # Tagline
    draw.text((W//2 - 200, H//2 + 80), "One image → Full character consistency", fill=GRAY, font=load_font_regular(SMALL_FONT))
    # Price
    draw.rounded_rectangle([W//2 - 80, H//2 + 130, W//2 + 80, H//2 + 170], radius=20, fill=ACCENT)
    draw.text((W//2 - 50, H//2 + 138), "$7.99", fill="white", font=load_font(SMALL_FONT))
    img.save(f"{OUT}/frame_007_cta.png")

if __name__ == "__main__":
    frame_01_title()
    frame_02_input()
    frame_03_expression()
    frame_04_turnaround()
    frame_05_actions()
    frame_06_bible()
    frame_07_cta()
    print("Done — 7 frames rendered.")