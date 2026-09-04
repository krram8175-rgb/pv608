import sys
from PIL import Image, ImageDraw
import numpy as np

path = sys.argv[1]
im = Image.open(path).convert("RGB")
a = np.asarray(im).astype(int)
h, w, _ = a.shape

# ---- content_top: last blue/dark row in [120,380] ----
content_top = 0
for y in range(120, min(390, h)):
    row = a[y]
    r = row[:, 0].mean(); g = row[:, 1].mean(); b = row[:, 2].mean()
    if (b > 150 and b - r > 30) or (r < 65 and g < 65 and b < 75):
        content_top = y
content_top += 3

# ---- content_bottom: detect bottom toolbar / "Show Answer" area ----
# From bottom up, find first long dark strip (nav) then stop; else use h.
content_bottom = h
for y in range(h - 1, int(h * 0.55), -1):
    row = a[y]
    r = row[:, 0].mean(); g = row[:, 1].mean(); b = row[:, 2].mean()
    if r < 65 and g < 65 and b < 75:
        content_bottom = y

x0, x1 = 30, w - 30
strip = a[:, x0:x1, :]

def is_gap(y):
    seg = strip[y]
    r = seg[:, 0]; g = seg[:, 1]; b = seg[:, 2]
    mx = np.maximum(np.maximum(r, g), b)
    mn = np.minimum(np.minimum(r, g), b)
    neutral = (mx - mn) < 10
    grayval = (r > 224) & (r < 246)
    gray = neutral & grayval
    return gray.mean() > 0.75

gap = np.array([is_gap(y) for y in range(h)])

# group non-gap rows within [content_top, content_bottom] into bands,
# separated by gap runs of >=6 rows
bands = []
y = content_top
MINGAP = 6
while y < content_bottom:
    if gap[y]:
        y += 1
        continue
    start = y
    run_gap = 0
    while y < content_bottom:
        if gap[y]:
            run_gap += 1
            if run_gap >= MINGAP:
                break
        else:
            run_gap = 0
        y += 1
    end = y - run_gap
    if end - start > 12:
        bands.append((start, end))
    y += 1

print("content_top", content_top, "content_bottom", content_bottom)
for i, (s, e) in enumerate(bands):
    print(f"band {i}: y={s}-{e} h={e-s}")

# debug overlay (scaled)
dbg = im.copy()
d = ImageDraw.Draw(dbg)
for i, (s, e) in enumerate(bands):
    d.rectangle([x0, s, x1, e], outline=(255, 0, 0), width=3)
    d.text((x0 + 5, s + 2), str(i), fill=(255, 0, 0))
scale = 480.0 / w
dbg = dbg.resize((480, int(h * scale)))
dbg.save("/app/workdata/debug.png")
print("saved debug")
