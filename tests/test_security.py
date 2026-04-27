import pytest

from md2pdf.core.converters import pdf_converter
from md2pdf.core.converters.base_converter import BaseConverter
from md2pdf.core.converters.pdf_converter import PDFConverter
from md2pdf.core.processors.markdown_processor import MarkdownProcessor


@pytest.mark.unit
def test_custom_css_strips_style_tags_and_imports(temp_dir):
    md = temp_dir / "test.md"
    md.write_text(
        "---\n"
        "css: |\n"
        "  </STYLE><script>alert(1)</script>\n"
        "  @import url('https://example.test/font.css');\n"
        "  body { color: red; }\n"
        "---\n"
        "# Hello\n"
    )
    converter = BaseConverter(input_file=str(md))

    converter._read_markdown_content()

    assert "</style>" not in converter.custom_css.lower()
    assert "@import" not in converter.custom_css.lower()
    assert "body { color: red; }" in converter.custom_css


@pytest.mark.unit
def test_emoji_replacement_does_not_fall_back_to_cdn():
    html = MarkdownProcessor().process_markdown("Hello 😀")

    assert "twemoji.maxcdn.com" not in html
    assert "https://" not in html
    assert "😀" in html or "file://" in html


@pytest.mark.unit
def test_pdf_url_fetcher_blocks_remote_resources(monkeypatch, sample_markdown_file):
    monkeypatch.delenv("MD2PDF_ALLOW_REMOTE_RESOURCES", raising=False)
    monkeypatch.setattr(
        pdf_converter,
        "default_url_fetcher",
        lambda url, *args, **kwargs: {"url": url},
    )
    converter = PDFConverter(input_file=str(sample_markdown_file))

    fetcher = converter._make_url_fetcher()

    with pytest.raises(ValueError, match="Blocked remote resource"):
        fetcher("https://example.test/image.png")


@pytest.mark.unit
def test_pdf_url_fetcher_allows_input_dir_and_blocks_file_escape(monkeypatch, temp_dir):
    monkeypatch.delenv("MD2PDF_ALLOW_REMOTE_RESOURCES", raising=False)
    monkeypatch.setattr(
        pdf_converter,
        "default_url_fetcher",
        lambda url, *args, **kwargs: {"url": url},
    )
    input_dir = temp_dir / "input"
    outside_dir = temp_dir / "outside"
    input_dir.mkdir()
    outside_dir.mkdir()
    md = input_dir / "doc.md"
    md.write_text("# Hello\n")
    allowed = input_dir / "image.png"
    blocked = outside_dir / "secret.txt"
    allowed.write_bytes(b"fake")
    blocked.write_text("secret")
    converter = PDFConverter(input_file=str(md))

    fetcher = converter._make_url_fetcher()

    assert fetcher(allowed.resolve().as_uri()) == {"url": allowed.resolve().as_uri()}
    with pytest.raises(ValueError, match="outside allowed roots"):
        fetcher(blocked.resolve().as_uri())


@pytest.mark.unit
def test_xmp_watermark_is_xml_escaped(sample_markdown_file):
    converter = PDFConverter(
        input_file=str(sample_markdown_file),
        watermark='tenant <alpha> & "quoted"',
    )

    xmp = converter._build_xmp_metadata()

    assert "tenant &lt;alpha&gt; &amp; &quot;quoted&quot;" in xmp
    assert "tenant <alpha>" not in xmp
