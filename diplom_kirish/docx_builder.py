# -*- coding: utf-8 -*-
"""
Sof Python (zipfile) yordamida standart .docx (OOXML) hujjat quruvchi.
Tashqi paketlarsiz. A4, Times New Roman, sarlavha/abzas/formula/jadval.
"""
import zipfile
import time


def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


class Docx:
    def __init__(self, font="Times New Roman", size_pt=14):
        self.body = []
        self.font = font
        self.sz = str(int(size_pt * 2))   # half-points
        self.sz_small = str(int(12 * 2))

    # --- ichki yordamchilar -------------------------------------------------
    def _run(self, text, bold=False, italic=False, size=None, sub=False, sup=False):
        sz = size if size else self.sz
        rpr = '<w:rPr>'
        rpr += f'<w:rFonts w:ascii="{self.font}" w:hAnsi="{self.font}" w:cs="{self.font}"/>'
        if bold:
            rpr += '<w:b/>'
        if italic:
            rpr += '<w:i/>'
        if sub:
            rpr += '<w:vertAlign w:val="subscript"/>'
        if sup:
            rpr += '<w:vertAlign w:val="superscript"/>'
        rpr += f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/>'
        rpr += '</w:rPr>'
        return f'<w:r>{rpr}<w:t xml:space="preserve">{esc(text)}</w:t></w:r>'

    def _runs_from_segments(self, segments):
        """segments: [(text, {bold,italic,sub,sup}), ...]"""
        out = ""
        for seg in segments:
            if isinstance(seg, str):
                out += self._run(seg)
            else:
                text, opts = seg
                out += self._run(text, **opts)
        return out

    # --- ommaviy metodlar ---------------------------------------------------
    def heading(self, text, level=1):
        sz = {1: "32", 2: "28", 3: "26"}.get(level, "28")
        before = "240" if level == 1 else "180"
        after = "120"
        rpr = (f'<w:rPr><w:rFonts w:ascii="{self.font}" w:hAnsi="{self.font}" w:cs="{self.font}"/>'
               f'<w:b/><w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>')
        ppr = (f'<w:pPr><w:keepNext/><w:spacing w:before="{before}" w:after="{after}"/>'
               f'<w:jc w:val="left"/></w:pPr>')
        p = (f'<w:p>{ppr}<w:r>{rpr}'
             f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')
        self.body.append(p)

    def para(self, segments, align="both", indent_first=True, spacing_after="120"):
        if isinstance(segments, str):
            segments = [segments]
        ind = '<w:ind w:firstLine="567"/>' if indent_first else ''
        ppr = (f'<w:pPr><w:spacing w:after="{spacing_after}" w:line="276" w:lineRule="auto"/>'
               f'{ind}<w:jc w:val="{align}"/></w:pPr>')
        runs = self._runs_from_segments(segments)
        self.body.append(f'<w:p>{ppr}{runs}</w:p>')

    def formula(self, segments, number=None):
        """Markazlangan formula. number berilsa o'ngga raqam qo'yiladi."""
        if isinstance(segments, str):
            segments = [segments]
        runs = self._runs_from_segments(segments)
        if number:
            # tab bilan o'ngga raqam
            tabs = '<w:tabs><w:tab w:val="right" w:pos="9360"/></w:tabs>'
            ppr = (f'<w:pPr>{tabs}<w:spacing w:before="120" w:after="120"/>'
                   f'<w:jc w:val="center"/></w:pPr>')
            runs += '<w:r><w:tab/></w:r>' + self._run(f'({number})')
            self.body.append(f'<w:p>{ppr}{runs}</w:p>')
        else:
            ppr = ('<w:pPr><w:spacing w:before="120" w:after="120"/>'
                   '<w:jc w:val="center"/></w:pPr>')
            self.body.append(f'<w:p>{ppr}{runs}</w:p>')

    def caption(self, text):
        rpr = (f'<w:rPr><w:rFonts w:ascii="{self.font}" w:hAnsi="{self.font}" w:cs="{self.font}"/>'
               f'<w:sz w:val="{self.sz_small}"/><w:szCs w:val="{self.sz_small}"/></w:rPr>')
        ppr = ('<w:pPr><w:spacing w:before="60" w:after="120"/>'
               '<w:jc w:val="center"/></w:pPr>')
        p = (f'<w:p>{ppr}<w:r>{rpr}'
             f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')
        self.body.append(p)

    def table(self, headers, rows, widths=None, caption=None):
        if caption:
            rpr = (f'<w:rPr><w:rFonts w:ascii="{self.font}" w:hAnsi="{self.font}" w:cs="{self.font}"/>'
                   f'<w:sz w:val="{self.sz_small}"/><w:szCs w:val="{self.sz_small}"/></w:rPr>')
            ppr = '<w:pPr><w:spacing w:before="120" w:after="40"/><w:jc w:val="right"/></w:pPr>'
            self.body.append(f'<w:p>{ppr}<w:r>{rpr}'
                             f'<w:t xml:space="preserve">{esc(caption)}</w:t></w:r></w:p>')
        ncol = len(headers)
        if widths is None:
            widths = [int(9360 / ncol)] * ncol

        def cell(text, bold=False, align="center"):
            sz = self.sz_small
            rpr = (f'<w:rPr><w:rFonts w:ascii="{self.font}" w:hAnsi="{self.font}" w:cs="{self.font}"/>'
                   + ('<w:b/>' if bold else '')
                   + f'<w:sz w:val="{sz}"/><w:szCs w:val="{sz}"/></w:rPr>')
            ppr = (f'<w:pPr><w:spacing w:after="0" w:line="240" w:lineRule="auto"/>'
                   f'<w:jc w:val="{align}"/></w:pPr>')
            return (f'<w:p>{ppr}<w:r>{rpr}'
                    f'<w:t xml:space="preserve">{esc(text)}</w:t></w:r></w:p>')

        def tc(content, w):
            tcpr = (f'<w:tcPr><w:tcW w:w="{w}" w:type="dxa"/>'
                    '<w:vAlign w:val="center"/></w:tcPr>')
            return f'<w:tc>{tcpr}{content}</w:tc>'

        # jadval xossalari + chegaralar
        borders = ('<w:tblBorders>'
                   '<w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                   '<w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                   '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                   '<w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                   '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                   '<w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
                   '</w:tblBorders>')
        tblpr = (f'<w:tblPr><w:tblW w:w="9360" w:type="dxa"/>'
                 f'<w:jc w:val="center"/>{borders}'
                 '<w:tblLook w:val="04A0"/></w:tblPr>')
        grid = '<w:tblGrid>' + ''.join(f'<w:gridCol w:w="{w}"/>' for w in widths) + '</w:tblGrid>'

        # sarlavha qatori
        hdr_cells = ''.join(tc(cell(h, bold=True), widths[i]) for i, h in enumerate(headers))
        hdr_row = f'<w:tr><w:trPr><w:tblHeader/></w:trPr>{hdr_cells}</w:tr>'

        body_rows = ""
        for row in rows:
            cells = ''.join(tc(cell(str(c)), widths[i]) for i, c in enumerate(row))
            body_rows += f'<w:tr>{cells}</w:tr>'

        self.body.append(f'<w:tbl>{tblpr}{grid}{hdr_row}{body_rows}</w:tbl>')
        # jadvaldan keyin bo'sh abzas
        self.body.append('<w:p><w:pPr><w:spacing w:after="120"/></w:pPr></w:p>')

    def bullet(self, segments, spacing_after="60"):
        if isinstance(segments, str):
            segments = [segments]
        ppr = (f'<w:pPr><w:spacing w:after="{spacing_after}" w:line="276" w:lineRule="auto"/>'
               f'<w:ind w:left="567" w:hanging="284"/><w:jc w:val="both"/></w:pPr>')
        runs = self._run("\u2013  ") + self._runs_from_segments(segments)
        self.body.append(f'<w:p>{ppr}{runs}</w:p>')

    def page_break(self):
        self.body.append('<w:p><w:r><w:br w:type="page"/></w:r></w:p>')

    def spacer(self):
        self.body.append('<w:p><w:pPr><w:spacing w:after="80"/></w:pPr></w:p>')

    # --- saqlash ------------------------------------------------------------
    def save(self, path):
        document = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
            '<w:body>'
            + ''.join(self.body)
            + '<w:sectPr>'
              '<w:pgSz w:w="11906" w:h="16838"/>'
              '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701" '
              'w:header="720" w:footer="720" w:gutter="0"/>'
              '<w:cols w:space="720"/>'
            '</w:sectPr>'
            '</w:body></w:document>'
        )

        content_types = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            '<Override PartName="/docProps/core.xml" '
            'ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            '<Override PartName="/docProps/app.xml" '
            'ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
            '</Types>'
        )

        rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" '
            'Target="word/document.xml"/>'
            '<Relationship Id="rId2" '
            'Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" '
            'Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" '
            'Target="docProps/app.xml"/>'
            '</Relationships>'
        )

        doc_rels = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" '
            'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" '
            'Target="styles.xml"/>'
            '</Relationships>'
        )

        styles = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:docDefaults><w:rPrDefault><w:rPr>'
            f'<w:rFonts w:ascii="{self.font}" w:hAnsi="{self.font}" w:cs="{self.font}"/>'
            f'<w:sz w:val="{self.sz}"/><w:szCs w:val="{self.sz}"/>'
            '<w:lang w:val="en-US"/>'
            '</w:rPr></w:rPrDefault></w:docDefaults>'
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
            '<w:name w:val="Normal"/><w:qFormat/>'
            f'<w:rPr><w:rFonts w:ascii="{self.font}" w:hAnsi="{self.font}" w:cs="{self.font}"/>'
            f'<w:sz w:val="{self.sz}"/><w:szCs w:val="{self.sz}"/></w:rPr>'
            '</w:style>'
            '</w:styles>'
        )

        now = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        core = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<cp:coreProperties '
            'xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" '
            'xmlns:dcterms="http://purl.org/dc/terms/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
            '<dc:title>II BOB. Hisobiy qism</dc:title>'
            '<dc:creator>Diplom ishi</dc:creator>'
            f'<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>'
            f'<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>'
            '</cp:coreProperties>'
        )

        app = (
            '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n'
            '<Properties '
            'xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
            '<Application>Kiro</Application></Properties>'
        )

        with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr("[Content_Types].xml", content_types)
            z.writestr("_rels/.rels", rels)
            z.writestr("word/document.xml", document)
            z.writestr("word/_rels/document.xml.rels", doc_rels)
            z.writestr("word/styles.xml", styles)
            z.writestr("docProps/core.xml", core)
            z.writestr("docProps/app.xml", app)
