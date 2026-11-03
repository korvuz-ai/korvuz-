from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG      = "#F7F5F0"   # warm paper (matches site body)
CARD    = "#F1EEE7"
INK     = "#2B2A26"
MUTED   = "#7A756A"
RULE    = "#DAD5C7"
TERRA   = "#BC7B4E"
SAGE    = "#6F8560"

TH = "/opt/korvuz-home/.tools/NotoSansThai.ttf"
EN = "/opt/korvuz-home/.tools/Inter.ttf"
R = ImageFont.Layout.RAQM


def f(path, size, weight):
    ft = ImageFont.truetype(path, size, layout_engine=R)
    ft.set_variation_by_name(weight)
    return ft


img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# --- soft geometric accents (minimal, no gradients) ---
d.ellipse([W - 250, -170, W + 170, 250], fill=CARD)          # top-right disc
d.ellipse([W - 148, 356, W - 36, 468], outline=SAGE, width=3)  # sage ring
d.rectangle([0, H - 14, W, H], fill=TERRA)                    # bottom bar

PAD = 84

# --- wordmark ---
d.text((PAD, 74), "KORVUZ", font=f(EN, 34, "Bold"), fill=TERRA)
d.text((PAD + 172, 84), "korvuz.site", font=f(EN, 22, "Medium"), fill=MUTED)

# --- headline (Thai) ---
y = 168
d.text((PAD, y), "รับทำเว็บ & วางระบบ", font=f(TH, 68, "Bold"), fill=INK)
d.text((PAD, y + 92), "Cloud DevOps", font=f(EN, 68, "ExtraBold"), fill=SAGE)

# --- rule ---
d.line([PAD, y + 200, PAD + 120, y + 200], fill=RULE, width=4)

# --- services ---
d.text((PAD, y + 232), "Static  ·  WordPress  ·  AWS  ·  CI/CD  ·  Automation",
       font=f(EN, 27, "Medium"), fill=MUTED)

# --- price pill ---
px, py = PAD, y + 292
label = "เริ่มต้น ฿8,000  ·  คำนวณราคาออนไลน์ได้ทันที"
pf = f(TH, 27, "SemiBold")
tw = d.textlength(label, font=pf)
d.rounded_rectangle([px, py, px + tw + 56, py + 62], radius=31, fill=CARD, outline=RULE, width=2)
d.text((px + 28, py + 14), label, font=pf, fill=TERRA)

img.save("/opt/korvuz-home/og-image.png", "PNG", optimize=True)
print("saved", img.size)
