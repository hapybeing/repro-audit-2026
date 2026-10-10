# Agent B: dump the authors' exported docx tables as text rows (cells joined by " | ").
import sys, zipfile, re
for f in sys.argv[1:]:
    x = zipfile.ZipFile(f).read("word/document.xml").decode("utf8")
    print("=== " + f)
    for row in re.findall(r"<w:tr[ >].*?</w:tr>", x, flags=re.S):
        cells = [re.sub(r"<[^>]+>", "", c) for c in re.findall(r"<w:tc>.*?</w:tc>", row, flags=re.S)]
        print(" | ".join(cells))
