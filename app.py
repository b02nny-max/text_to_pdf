from flask import Flask, render_template, request, send_file
from weasyprint import HTML, CSS
import tempfile, os

app = Flask(__name__)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

FONT_CSS = f"""
@font-face {{
  font-family: 'Noto';
  src: url('file://{BASE_DIR}/fonts/NotoSans-Regular.ttf');
}}
@font-face {{
  font-family: 'NotoBold';
  src: url('file://{BASE_DIR}/fonts/NotoSans-Bold.ttf');
}}
@font-face {{
  font-family: 'NotoArabic';
  src: url('file://{BASE_DIR}/fonts/NotoSansArabic-Regular.ttf');
}}
@font-face {{
  font-family: 'NotoDeva';
  src: url('file://{BASE_DIR}/fonts/NotoSansDevanagari-Regular.ttf');
}}
@font-face {{
  font-family: 'NotoTamil';
  src: url('file://{BASE_DIR}/fonts/NotoSansTamil-Regular.ttf');
}}
@font-face {{
  font-family: 'NotoCJK';
  src: url('file://{BASE_DIR}/fonts/NotoSansCJK-Regular.ttc');
}}
@font-face {{
  font-family: 'NotoEmoji';
  src: url('file://{BASE_DIR}/fonts/NotoColorEmoji.ttf');
}}

body {{
  font-family: Noto, NotoArabic, NotoDeva, NotoTamil, NotoCJK, NotoEmoji;
  font-size: 14px;
  line-height: 1.6;
}}

.page {{
  page-break-after: always;
  padding: 48px;
}}

@page {{
  size: A4;
  margin: 20mm;
}}
"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate-pdf", methods=["POST"])
def generate_pdf():
    html_content = request.json["html"]

    full_html = f"""
    <html>
    <head>
      <meta charset="utf-8">
      <style>{FONT_CSS}</style>
    </head>
    <body>
      {html_content}
    </body>
    </html>
    """

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    HTML(string=full_html, base_url=BASE_DIR).write_pdf(tmp.name)

    return send_file(
        tmp.name,
        as_attachment=True,
        download_name="document.pdf"
    )

if __name__ == "__main__":
    app.run(debug=True)
