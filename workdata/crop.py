import sys
from PIL import Image
import numpy as np

def detect_bands(a, h, w):
    content_top = 0
    for y in range(120, min(390, h)):
        row = a[y]
        r = row[:, 0].mean(); g = row[:, 1].mean(); b = row[:, 2].mean()
        if (b > 150 and b - r > 30) or (r < 65 and g < 65 and b < 75):
            content_top = y
    content_top += 3
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
        gray = ((mx - mn) < 10) & (r > 224) & (r < 246)
        return gray.mean() > 0.75

    gap = np.array([is_gap(y) for y in range(h)])
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
            bands.append([start, end])
        y += 1
    return bands, content_top, content_bottom


def crop_question(path, outprefix):
    im = Image.open(path).convert("RGB")
    a = np.asarray(im).astype(int)
    h, w, _ = a.shape
    bands, ct, cb = detect_bands(a, h, w)
    if len(bands) < 6:
        print("WARN few bands", path, len(bands))
    # pad bottoms to catch "% users" pills, pad tops slightly, clamp to neighbors
    padded = []
    for i, (s, e) in enumerate(bands):
        top = s - 8
        bot = e + 20
        if i > 0:
            top = max(top, bands[i - 1][1] + 3)
        if i < len(bands) - 1:
            bot = min(bot, bands[i + 1][0] - 3)
        top = max(top, ct)
        bot = min(bot, cb)
        padded.append((top, bot))
    x0, x1 = 20, w - 18
    names = ["question", "opt_a", "opt_b", "opt_c", "opt_d", "solution"]
    for idx, name in enumerate(names):
        s, e = padded[idx]
        crop = im.crop((x0, s, x1, e))
        # normalize width to 691
        tw = 691
        th = int(crop.height * tw / crop.width)
        crop = crop.resize((tw, th), Image.LANCZOS)
        out = f"/app/backend/chapter_images/{outprefix}_{name}.png"
        crop.save(out)
    print("done", outprefix, "bands", len(bands))


if __name__ == "__main__":
    mapping = {
        "src/Screenshot_2026-09-02-11-49-35-23.jpg": "sf_q1",
        "src/Screenshot_2026-09-02-11-53-24-99.jpg": "sf_q2",
        "src/Screenshot_2026-09-02-11-53-38-64.jpg": "sf_q3",
        "src/Screenshot_2026-09-02-11-53-51-80.jpg": "sf_q4",
    }
    import os
    os.chdir("/app/workdata")
    for path, pref in mapping.items():
        crop_question(path, pref)
