"""Build the fully offline HTML from editable source files. Python 3, no deps."""
from pathlib import Path

root = Path(__file__).resolve().parent
html = (root / 'src/index.html').read_text(encoding='utf-8')
for marker, filename in [('/*__CSS__*/', 'style.css'), ('/*__CORE__*/', 'generator.js'), ('/*__UI__*/', 'ui.js')]:
    html = html.replace(marker, (root / 'src' / filename).read_text(encoding='utf-8'))
(root / 'Primer3_Input_Builder.html').write_text(html, encoding='utf-8')
print(root / 'Primer3_Input_Builder.html')
