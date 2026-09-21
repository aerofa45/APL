"""Optional: draw AST diagrams as PNG images for the report (needs Pillow).

Not needed to run the parser or the tests. It draws the same tree that
`emerald_parser.py <file> --diagram` prints, in Times New Roman, black on white.

    python make_diagram_images.py
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from ast_diagram import children, label
from emerald_parser import parse_source

FONT_PATHS = [
    "C:/Windows/Fonts/times.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/usr/share/fonts/truetype/msttcorefonts/Times_New_Roman.ttf",
]
SCALE = 2          # draw at 2x so the image stays sharp when scaled in a document
FONT_SIZE = 26 * SCALE
PAD = 12 * SCALE   # space around each label
GAP = 14 * SCALE   # minimum space between sibling subtrees
LEVEL = 74 * SCALE
MARGIN = 20 * SCALE

# (file name, source of one `let` statement whose value is drawn)
FIGURES = [
    ("ast_2_plus_3_times_4.png", "2 + 3 * 4"),
    ("ast_parenthesized.png", "(2 + 3) * 4"),
    ("ast_logical.png", "not (x > y) and true or false"),
]


def load_font():
    for path in FONT_PATHS:
        if Path(path).exists():
            return ImageFont.truetype(path, FONT_SIZE)
    raise SystemExit("Times New Roman was not found; edit FONT_PATHS in this script.")


def render(node, path, font):
    draw = ImageDraw.Draw(Image.new("RGB", (1, 1)))
    placed = []  # (label, center_x, depth, parent_index)

    def place(node, left, depth, parent):
        text = label(node)
        text_w = draw.textlength(text, font=font) + 2 * PAD
        index = len(placed)
        placed.append(None)
        kids = children(node)
        if not kids:
            center, right = left + text_w / 2, left + text_w
        else:
            cursor, centers = left, []
            for kid in kids:
                c, r = place(kid, cursor, depth + 1, index)
                centers.append(c)
                cursor = r + GAP
            center = (centers[0] + centers[-1]) / 2
            right = max(cursor - GAP, center + text_w / 2)
        placed[index] = (text, center, depth, parent)
        return center, right

    _, right = place(node, 0, 0, None)
    depth = max(p[2] for p in placed)
    width = int(right + 2 * MARGIN)
    height = int((depth + 1) * LEVEL + 2 * MARGIN)
    image = Image.new("RGB", (width, height), "white")
    pen = ImageDraw.Draw(image)

    def xy(p):
        return MARGIN + p[1], MARGIN + p[2] * LEVEL + LEVEL / 2 - 10 * SCALE

    for p in placed:
        if p[3] is not None:
            (px, py), (cx, cy) = xy(placed[p[3]]), xy(p)
            pen.line([(px, py + 18 * SCALE), (cx, cy - 18 * SCALE)], fill="black", width=2 * SCALE)
    for p in placed:
        x, y = xy(p)
        pen.text((x, y), p[0], font=font, fill="black", anchor="mm")
    image.save(path)


def main():
    out = Path(__file__).resolve().parent / "outputs"
    out.mkdir(exist_ok=True)
    font = load_font()
    for name, source in FIGURES:
        node = parse_source(f"let v = {source};").statements[0].value
        render(node, out / name, font)
        print(f"saved outputs/{name}")


if __name__ == "__main__":
    main()
