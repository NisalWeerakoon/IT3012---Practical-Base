"""Build a compact PDF from a practical's Markdown documentation."""
import re
import sys
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

source = Path(sys.argv[1])
target = source.with_suffix(".pdf")
styles = getSampleStyleSheet()
doc = SimpleDocTemplate(str(target), pagesize=A4, rightMargin=inch,
                        leftMargin=inch, topMargin=inch, bottomMargin=inch)
story = []
for raw in source.read_text(encoding="utf-8").splitlines():
    line = raw.strip()
    if not line:
        story.append(Spacer(1, 8))
        continue
    if line.startswith("# "):
        style, line = styles["Title"], line[2:]
    elif line.startswith("## "):
        style, line = styles["Heading2"], line[3:]
    else:
        style = styles["BodyText"]
    line = re.sub(r"`([^`]+)`", r"<font name='Courier'>\1</font>", line)
    story.append(Paragraph(line, style))
doc.build(story)
print(target)
