#!/usr/bin/env python3
"""Generate Energie-Revolution-8911.pdf (German) from all repository markdown files."""

import markdown
import tempfile
import weasyprint

REPO_URL = "https://github.com/RaikoPulvermacher/Energy-Revolution/blob/main"
ZENODO_URL = "https://doi.org/10.5281/zenodo.18757232"


def read(filename):
    with open(filename, encoding="utf-8") as fh:
        return fh.read()


def md_to_html(text):
    return markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "toc", "nl2br"],
    )


def linkify_license(html):
    """Replace bare license text with a clickable link."""
    return html.replace(
        "Pulvermacher Open Research License (PORL) v1.0",
        f'<a href="{ZENODO_URL}">Pulvermacher Open Research License (PORL) v1.0</a>',
    )


# ── Read source files ────────────────────────────────────────────────────────
abstract_md = read("Abstract_DE.md")
beschreibung_md = read("Beschreibung.md")
beweisfuehrung_md = read("Beweisführung_8911.md")
beweis_vergleich_md = read("Beweis_Vergleich_Anomalien.md")
vorhersage_md = read("Vorhersage.md")
readme_md = read("README.md")
license_md = read("LICENSE")

# ── Convert Markdown → HTML ──────────────────────────────────────────────────
abstract_html = md_to_html(abstract_md)
beschreibung_html = md_to_html(beschreibung_md)
beweisfuehrung_html = md_to_html(beweisfuehrung_md)
beweis_vergleich_html = md_to_html(beweis_vergleich_md)
vorhersage_html = md_to_html(vorhersage_md)
readme_html = md_to_html(readme_md)
license_html = linkify_license(md_to_html(license_md))

# ── Build full HTML document ─────────────────────────────────────────────────
HTML = f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8"/>
  <title>Energie-Revolution-8911: Widerstand als mathematischer Phasenfehler</title>
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
    }}
    h1, h2, h3, h4 {{
      font-family: "DejaVu Sans", Arial, sans-serif;
      color: #0d3b66;
      page-break-after: avoid;
    }}
    p, li, blockquote {{
      orphans: 3;
      widows: 3;
    }}
    /* Keep description blocks together – no mid-paragraph breaks */
    .section > p,
    .section > ul,
    .section > ol,
    .section > blockquote {{
      page-break-inside: avoid;
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
    }}
    .abstract-box h2 {{
      font-size: 12pt;
      margin-top: 0;
    }}
    /* ── table of contents ── */
    .toc {{
      page-break-after: always;
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
    }}
    .toc ol li {{
      margin: 6pt 0;
      font-size: 11pt;
    }}
    .toc ol li a {{
      color: #1565c0;
      text-decoration: none;
    }}
    /* ── content sections ── */
    .section {{
      page-break-before: always;
    }}
    .section h1 {{
      font-size: 16pt;
      border-bottom: 2px solid #0d3b66;
      padding-bottom: 4pt;
    }}
    table {{
      border-collapse: collapse;
      width: 100%;
      margin: 10pt 0;
      font-size: 9.5pt;
      page-break-inside: avoid;
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
    blockquote {{
      border-left: 3px solid #ccc;
      margin: 0;
      padding-left: 12pt;
      color: #555;
    }}
  </style>
</head>
<body>

<!-- ══════════════════════════════════════════════════════════════════
     TITELSEITE
═══════════════════════════════════════════════════════════════════ -->
<div class="cover">
  <h1>Energie-Revolution-8911:<br/>Widerstand als mathematischer Phasenfehler</h1>
  <p class="subtitle">Eine Arbeit zur prozessualen F<sub>N</sub>-Resonanz<br/>
  als Alternative zur Euler-Dämpfung</p>
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
     INHALTSVERZEICHNIS
═══════════════════════════════════════════════════════════════════ -->
<div id="toc" class="toc section">
  <h2>Inhaltsverzeichnis</h2>
  <ol>
    <li><a href="#abstract">Abstract</a></li>
    <li><a href="#beschreibung">1. Spezifikation der F<sub>N</sub>-Prozessmechanik</a></li>
    <li><a href="#beweisfuehrung">2. Mathematischer Beweis der F<sub>N</sub>-Sättigung vs. Euler-Dämpfung</a></li>
    <li><a href="#beweis-vergleich">3. Beweis-Vergleich: F<sub>N</sub>-Logik vs. 300 Jahre Euler-Irrtum</a></li>
    <li><a href="#vorhersage">4. Die Vorhersage: Warum wir 89 % unserer Energie verschwenden</a></li>
    <li><a href="#readme">5. Projekt-README (Energy-Revolution)</a></li>
    <li><a href="#license">6. Lizenz – Pulvermacher Open Research License (PORL) v1.0</a></li>
  </ol>
  <hr/>
  <p style="font-size:9pt; color:#555;">
    Quellcode &amp; Dateien:
    <a href="{REPO_URL}/Beschreibung.md">Beschreibung.md</a> ·
    <a href="{REPO_URL}/Beweisf%C3%BChrung_8911.md">Beweisführung_8911.md</a> ·
    <a href="{REPO_URL}/Beweis_Vergleich_Anomalien.md">Beweis_Vergleich_Anomalien.md</a> ·
    <a href="{REPO_URL}/Vorhersage.md">Vorhersage.md</a> ·
    <a href="{REPO_URL}/README.md">README.md</a> ·
    <a href="{REPO_URL}/LICENSE">LICENSE</a>
  </p>
</div>

<!-- ══════════════════════════════════════════════════════════════════
     1. BESCHREIBUNG
═══════════════════════════════════════════════════════════════════ -->
<div id="beschreibung" class="section">
  <p style="font-size:8.5pt; color:#777; margin-bottom:6pt;">
    Quelldatei: <a href="{REPO_URL}/Beschreibung.md">Beschreibung.md</a>
  </p>
  {beschreibung_html}
</div>

<!-- ══════════════════════════════════════════════════════════════════
     2. BEWEISFÜHRUNG 8911
═══════════════════════════════════════════════════════════════════ -->
<div id="beweisfuehrung" class="section">
  <p style="font-size:8.5pt; color:#777; margin-bottom:6pt;">
    Quelldatei: <a href="{REPO_URL}/Beweisf%C3%BChrung_8911.md">Beweisführung_8911.md</a>
  </p>
  {beweisfuehrung_html}
</div>

<!-- ══════════════════════════════════════════════════════════════════
     3. BEWEIS-VERGLEICH ANOMALIEN
═══════════════════════════════════════════════════════════════════ -->
<div id="beweis-vergleich" class="section">
  <p style="font-size:8.5pt; color:#777; margin-bottom:6pt;">
    Quelldatei: <a href="{REPO_URL}/Beweis_Vergleich_Anomalien.md">Beweis_Vergleich_Anomalien.md</a>
  </p>
  {beweis_vergleich_html}
</div>

<!-- ══════════════════════════════════════════════════════════════════
     4. VORHERSAGE
═══════════════════════════════════════════════════════════════════ -->
<div id="vorhersage" class="section">
  <p style="font-size:8.5pt; color:#777; margin-bottom:6pt;">
    Quelldatei: <a href="{REPO_URL}/Vorhersage.md">Vorhersage.md</a>
  </p>
  {vorhersage_html}
</div>

<!-- ══════════════════════════════════════════════════════════════════
     5. README
═══════════════════════════════════════════════════════════════════ -->
<div id="readme" class="section">
  <p style="font-size:8.5pt; color:#777; margin-bottom:6pt;">
    Quelldatei: <a href="{REPO_URL}/README.md">README.md</a>
  </p>
  {readme_html}
</div>

<!-- ══════════════════════════════════════════════════════════════════
     6. LIZENZ
═══════════════════════════════════════════════════════════════════ -->
<div id="license" class="section">
  <p style="font-size:8.5pt; color:#777; margin-bottom:6pt;">
    Quelldatei: <a href="{REPO_URL}/LICENSE">LICENSE</a> ·
    DOI: <a href="{ZENODO_URL}">{ZENODO_URL}</a>
  </p>
  {license_html}
</div>

</body>
</html>
"""

# ── Write HTML and generate PDF ──────────────────────────────────────────────
with tempfile.NamedTemporaryFile(
    mode="w", suffix=".html", encoding="utf-8", delete=False
) as fh:
    fh.write(HTML)
    tmp_html = fh.name

print("HTML written – generating PDF …")
weasyprint.HTML(filename=tmp_html).write_pdf(
    "Energie-Revolution-8911.pdf"
)
print("PDF created: Energie-Revolution-8911.pdf")
