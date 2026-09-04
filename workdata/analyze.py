import sys
from PIL import Image
import numpy as np

path = sys.argv[1]
im = Image.open(path).convert("RGB")
a = np.asarray(im).astype(int)
h, w, _ = a.shape
print("size", w, h)

# blue nav detection -> content_top
def classify(y):
    row = a[y]
    r = row[:,0].mean(); g = row[:,1].mean(); b = row[:,2].mean()
    return r,g,b

# find content_top: last blue-ish or dark row in [120, 360]
content_top = 0
for y in range(120, min(380, h)):
    r,g,b = classify(y)
    if (b > 150 and b - r > 30) or (r < 60 and g < 60 and b < 70):
        content_top = y
content_top += 2
print("content_top", content_top)

# Left-column sampling (x=45..95) to detect gap vs card
left = a[:, 45:95, :]
def rowtype(y):
    seg = left[y]
    r = seg[:,0].mean(); g = seg[:,1].mean(); b = seg[:,2].mean()
    # white card: all high ~>247
    if r>246 and g>246 and b>246:
        return 'W', (int(r),int(g),int(b))
    # neutral gray gap: 225..244 and near-neutral
    if 218 < r < 246 and abs(r-g)<6 and abs(g-b)<6:
        return 'G', (int(r),int(g),int(b))
    return 'X', (int(r),int(g),int(b))

# print compressed run-length of rowtypes from content_top to h
prev=None; start=content_top
runs=[]
for y in range(content_top, h):
    t,_ = rowtype(y)
    if t!=prev:
        if prev is not None:
            runs.append((prev,start,y-1,y-start))
        prev=t; start=y
runs.append((prev,start,h-1,h-start))
for t,s,e,ln in runs:
    if ln>=8:
        print(f"{t} y={s}-{e} len={ln}")
