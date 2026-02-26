#!/usr/bin/env python3
"""Generate Energy-Revolution-8911.pdf from all repository markdown files."""

import re
import markdown
import weasyprint


# ── Math & citation helpers ──────────────────────────────────────────────────

def _math_to_html(expr):
    """Convert simple LaTeX subscripts/superscripts inside an expression."""
    # F_{n-1} → F<sub>n-1</sub>
    expr = re.sub(r'([A-Za-z])_\{([^}]+)\}', r'\1<sub>\2</sub>', expr)
    # F_n → F<sub>n</sub>
    expr = re.sub(r'([A-Za-z])_([A-Za-z0-9])', r'\1<sub>\2</sub>', expr)
    # F^{n} → F<sup>n</sup>
    expr = re.sub(r'([A-Za-z])\^\{([^}]+)\}', r'\1<sup>\2</sup>', expr)
    # F^n → F<sup>n</sup>
    expr = re.sub(r'([A-Za-z])\^([A-Za-z0-9])', r'\1<sup>\2</sup>', expr)
    return expr


def preprocess(text):
    """Remove cite markers and convert LaTeX math to HTML before Markdown pass."""
    # Strip [cite: ...] annotation markers
    text = re.sub(r'\s*\[cite:[^\]]+\]', '', text)

    # Display math: $$...$$ → <p class="display-math">...</p>
    def _disp(m):
        expr = _math_to_html(m.group(1).strip())
        return f'\n<p class="display-math">{expr}</p>\n'
    text = re.sub(r'\$\$(.+?)\$\$', _disp, text, flags=re.DOTALL)

    # Inline math: $...$ → <span class="math">...</span>
    def _inl(m):
        expr = _math_to_html(m.group(1))
        return f'<span class="math">{expr}</span>'
    text = re.sub(r'\$(?!\$)([^\$\n]+?)\$', _inl, text)

    return text

REPO_URL = "https://github.com/RaikoPulvermacher/Energy-Revolution/blob/main"
ZENODO_URL = "https://doi.org/10.5281/zenodo.18757232"


def read(filename):
    with open(filename, encoding="utf-8") as fh:
        return fh.read()


def md_to_html(text):
    return markdown.markdown(
        preprocess(text),
        extensions=["tables", "fenced_code", "toc", "nl2br"],
    )


def linkify_license(html):
    """Replace bare license text with a clickable link."""
    return html.replace(
        "Pulvermacher Open Research License (PORL) v1.0",
        f'<a href="{ZENODO_URL}">Pulvermacher Open Research License (PORL) v1.0</a>',
    )


# ── Read source files ────────────────────────────────────────────────────────
abstract_md = read("Abstract.md")
description_md = read("Description.md")
proof_md = read("Proof_8911.md")
proof_comparison_md = read("Proof_Comparison_Anomalies.md")
prediction_md = read("Prediction.md")
readme_md = read("README.md")
license_md = read("LICENSE")

# ── Convert Markdown → HTML ──────────────────────────────────────────────────
abstract_html = md_to_html(abstract_md)
description_html = md_to_html(description_md)
proof_html = md_to_html(proof_md)
proof_comparison_html = md_to_html(proof_comparison_md)
prediction_html = md_to_html(prediction_md)
readme_html = md_to_html(readme_md)
license_html = linkify_license(md_to_html(license_md))

# ── Build full HTML document ─────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <title>Energy-Revolution-8911: Resistance as a Mathematical Phase Error</title>
  <style>
    @page {{
      size: A4;
      margin: 25mm 20mm 25mm 20mm;
      @bottom-center {{
        content: counter(page);
        font-size: 9pt;
        color: #555;
      }}
    }}
    body {{
      font-family: "DejaVu Sans", Arial, sans-serif;
      font-size: 10.5pt;
      line-height: 1.65;
      color: #1a1a1a;
      orphans: 3;
      widows: 3;
    }}
    h1, h2, h3, h4 {{
      font-family: "DejaVu Sans", Arial, sans-serif;
      color: #0d3b66;
      page-break-after: avoid;
      break-after: avoid;
    }}
    a {{
      color: #1565c0;
      text-decoration: underline;
    }}
    /* ── cover page ── */
    .cover {{
      page: cover;
      text-align: center;
      padding-top: 80mm;
    }}
    @page cover {{
      margin: 0;
      @bottom-center {{ content: none; }}
    }}
    .cover h1 {{
      font-size: 22pt;
      line-height: 1.3;
      color: #0d3b66;
      margin-bottom: 10mm;
    }}
    .cover .subtitle {{
      font-size: 12pt;
      color: #444;
      margin-bottom: 20mm;
    }}
    .cover .author {{
      font-size: 11pt;
      color: #222;
    }}
    /* ── abstract ── */
    .abstract-box {{
      border-left: 4px solid #1565c0;
      padding: 8pt 14pt;
      background: #f0f4fb;
      margin: 12pt 0 18pt 0;
      page-break-inside: avoid;
      break-inside: avoid;
    }}
    .abstract-box h2 {{
      font-size: 12pt;
      margin-top: 0;
    }}
    /* ── table of contents ── */
    .toc {{
      page-break-after: always;
      break-after: always;
    }}
    .toc h2 {{
      font-size: 14pt;
      border-bottom: 2px solid #0d3b66;
      padding-bottom: 4pt;
      margin-bottom: 12pt;
    }}
    .toc ol {{
      list-style: none;
      padding-left: 0;
      counter-reset: toc-counter;
    }}
    .toc ol li {{
      margin: 6pt 0;
      font-size: 11pt;
    }}
    .toc ol li a {{
      color: #1565c0;
      text-decoration: none;
    }}
    .toc ol li a:hover {{
      text-decoration: underline;
    }}
    /* ── content sections ── */
    .section {{
      page-break-before: always;
      break-before: always;
    }}
    .section h1 {{
      font-size: 16pt;
      border-bottom: 2px solid #0d3b66;
      padding-bottom: 4pt;
    }}
    /* ── prevent mid-content page cuts ── */
    table {{
      border-collapse: collapse;
      width: 100%;
      margin: 10pt 0;
      font-size: 9.5pt;
      page-break-inside: avoid;
      break-inside: avoid;
    }}
    th, td {{
      border: 1px solid #aaa;
      padding: 5pt 8pt;
      text-align: left;
    }}
    th {{
      background: #dbe7f5;
      font-weight: bold;
    }}
    li {{
      page-break-inside: avoid;
      break-inside: avoid;
    }}
    blockquote {{
      border-left: 3px solid #ccc;
      margin: 0;
      padding-left: 12pt;
      color: #555;
      page-break-inside: avoid;
      break-inside: avoid;
    }}
    pre {{
      page-break-inside: avoid;
      break-inside: avoid;
    }}
    code {{
      font-family: "DejaVu Sans Mono", monospace;
      font-size: 9pt;
      background: #f5f5f5;
      padding: 1pt 3pt;
    }}
    hr {{
      border: none;
      border-top: 1px solid #ccc;
      margin: 14pt 0;
    }}
    /* ── math notation ── */
    .math {{
      font-style: italic;
    }}
    .display-math {{
      text-align: center;
      font-style: italic;
      margin: 12pt 0;
      font-size: 11pt;
      page-break-inside: avoid;
      break-inside: avoid;
    }}
  </style>
</head>
<body>

<!-- ══════════════════════════════════════════════════════════════════
     COVER PAGE
═══════════════════════════════════════════════════════════════════ -->
<div class="cover">
  <h1>Energy-Revolution-8911:<br/>Resistance as a Mathematical Phase Error</h1>
  <p class="subtitle">A work on procedural F<sub>N</sub> resonance<br/>
  as an alternative to Euler damping</p>
  <p class="author">
    <strong>Raiko Pulvermacher</strong><br/>
    E-Mail: <a href="mailto:Pulvermacher.Raiko@web.de">Pulvermacher.Raiko@web.de</a><br/>
    ORCID: <a href="https://orcid.org/0009-0003-9431-1001">0009-0003-9431-1001</a><br/>
    OSF: <a href="https://osf.io/py42t/">https://osf.io/py42t/</a>
  </p>
</div>

<!-- ══════════════════════════════════════════════════════════════════
     ABSTRACT
═══════════════════════════════════════════════════════════════════ -->
<div id="abstract" class="section">
  <h1>Abstract</h1>
  <div class="abstract-box">
    {abstract_html}
  </div>
</div>

<!-- ══════════════════════════════════════════════════════════════════
     TABLE OF CONTENTS
═══════════════════════════════════════════════════════════════════ -->
<div id="toc" class="toc section">
  <h2>Table of Contents</h2>
  <ol>
    <li><a href="#abstract">Abstract</a></li>
    <li><a href="#description">1. Specification of the F<sub>N</sub> Process Mechanics (Description)</a></li>
    <li><a href="#proof">2. Mathematical Proof of F<sub>N</sub> Saturation vs. Euler Damping (Proof 8911)</a></li>
    <li><a href="#proof-comparison">3. Proof Comparison: F<sub>N</sub> Logic vs. 300 Years of Euler Error</a></li>
    <li><a href="#prediction">4. The Prediction: Why We Waste 89% of Our Energy</a></li>
    <li><a href="#readme">5. Project README (Energy-Revolution)</a></li>
    <li><a href="#license">6. License – Pulvermacher Open Research License (PORL) v1.0</a></li>
  </ol>
  <hr/>
  <p style="font-size:9pt; color:#555;">
    Source code &amp; files:
    <a href="{REPO_URL}/Description.md">Description.md</a> ·
    <a href="{REPO_URL}/Proof_8911.md">Proof_8911.md</a> ·
    <a href="{REPO_URL}/Proof_Comparison_Anomalies.md">Proof_Comparison_Anomalies.md</a> ·
    <a href="{REPO_URL}/Prediction.md">Prediction.md</a> ·
    <a href="{REPO_URL}/README.md">README.md</a> ·
    <a href="{REPO_URL}/LICENSE">LICENSE</a>
  </p>
</div>

<!-- ══════════════════════════════════════════════════════════════════
     1. DESCRIPTION
═══════════════════════════════════════════════════════════════════ -->
<div id="description" class="section">
  <p style="font-size:8.5pt; color:#777; margin-bottom:6pt;">
    Source file: <a href="{REPO_URL}/Description.md">Description.md</a>
  </p>
  {description_html}
</div>

<!-- ══════════════════════════════════════════════════════════════════
     2. PROOF 8911
═══════════════════════════════════════════════════════════════════ -->
<div id="proof" class="section">
  <p style="font-size:8.5pt; color:#777; margin-bottom:6pt;">
    Source file: <a href="{REPO_URL}/Proof_8911.md">Proof_8911.md</a>
  </p>
  {proof_html}
</div>

<!-- ══════════════════════════════════════════════════════════════════
     3. PROOF COMPARISON ANOMALIES
═══════════════════════════════════════════════════════════════════ -->
<div id="proof-comparison" class="section">
  <p style="font-size:8.5pt; color:#777; margin-bottom:6pt;">
    Source file: <a href="{REPO_URL}/Proof_Comparison_Anomalies.md">Proof_Comparison_Anomalies.md</a>
  </p>
  {proof_comparison_html}
</div>

<!-- ══════════════════════════════════════════════════════════════════
     4. PREDICTION
═══════════════════════════════════════════════════════════════════ -->
<div id="prediction" class="section">
  <p style="font-size:8.5pt; color:#777; margin-bottom:6pt;">
    Source file: <a href="{REPO_URL}/Prediction.md">Prediction.md</a>
  </p>
  {prediction_html}
</div>

<!-- ══════════════════════════════════════════════════════════════════
     5. README
═══════════════════════════════════════════════════════════════════ -->
<div id="readme" class="section">
  <p style="font-size:8.5pt; color:#777; margin-bottom:6pt;">
    Source file: <a href="{REPO_URL}/README.md">README.md</a>
  </p>
  {readme_html}
</div>

<!-- ══════════════════════════════════════════════════════════════════
     6. LICENSE
═══════════════════════════════════════════════════════════════════ -->
<div id="license" class="section">
  <p style="font-size:8.5pt; color:#777; margin-bottom:6pt;">
    Source file: <a href="{REPO_URL}/LICENSE">LICENSE</a> ·
    DOI: <a href="{ZENODO_URL}">{ZENODO_URL}</a>
  </p>
  {license_html}
</div>

</body>
</html>
"""

# ── Write HTML and generate PDF ──────────────────────────────────────────────
with open("/tmp/Energy-Revolution-8911.html", "w", encoding="utf-8") as fh:
    fh.write(HTML)

print("HTML written – generating PDF …")
weasyprint.HTML(filename="/tmp/Energy-Revolution-8911.html").write_pdf(
    "Energy-Revolution-8911.pdf"
)
print("PDF created: Energy-Revolution-8911.pdf")
