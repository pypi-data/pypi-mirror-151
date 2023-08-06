from .zhtml import FunctionalPage, Page, Placeholder, _element


__all__ = ['Page', 'Placeholder', 'FunctionalPage']


def font_face(**kwargs) -> str:
    """@font-face (CSS)"""
    indent_str = ' ' * 4

    font_family = kwargs['font_family']
    font_family = f"'{font_family}'" if ' ' in font_family else font_family

    url = kwargs['url']
    font_format = kwargs['format']

    font_face_css = '\n@font-face {\n'
    font_face_css += f"{indent_str}font-family: {font_family};\n"
    font_face_css += f"{indent_str}font-style: {kwargs['font_style']};\n"
    font_face_css += f"{indent_str}font-weight: {kwargs['font_weight']};\n"
    font_face_css += f"{indent_str}font-display: {kwargs['font_display']};\n"
    font_face_css += f"{indent_str}src: url('{url}') format('{font_format}');\n"
    font_face_css += '}\n'

    return font_face_css


def link(indent=0, **attributes):
    """<link>"""
    return _element('link', None, indent, True, **attributes)


def style(content, indent=0, **attributes):
    """<style>"""
    return _element('style', content, indent, False, **attributes)


def anchor(content, link, indent=0, **attributes):
    """<anchor>"""
    return _element('a', content, indent, True, href=link, **attributes)


def button(content, indent=0, **attributes):
    """<button>"""
    return _element('button', content, indent, True, **attributes)


def heading(content, indent=0, **attributes):
    """<h1>"""
    return _element('h1', content, indent, True, **attributes)


def section_heading(content, indent=0, **attributes):
    """<h2>"""
    return _element('h2', content, indent, True, **attributes)


def details_heading(content, indent=0, **attributes):
    """<h3>"""
    return _element('h3', content, indent, True, **attributes)


def content_heading(content, indent=0, **attributes):
    """<h4>"""
    return _element('h4', content, indent, True, **attributes)


def summary(content, indent=0, **attributes):
    """<summary>"""
    return _element('summary', content, indent, True, **attributes)


def paragraph(content, indent=0, **attributes):
    """<p>"""
    return _element('p', content, indent, False, **attributes)


def details(content, indent=0, **attributes) -> str:
    """<details>"""
    return _element('details', content, indent, False, **attributes)


def main(content, indent=0, **attributes) -> str:
    """<main>"""
    return _element('main', content, indent, False, **attributes)


def nav(content, indent=0, **attributes) -> str:
    """<nav>"""
    return _element('nav', content, indent, False, **attributes)


def section(content, indent=0, **attributes) -> str:
    """<section>"""
    return _element('section', content, indent, False, **attributes)


def header(content, indent=0, **attributes) -> str:
    """<header>"""
    return _element('header', content, indent, False, **attributes)


def footer(content, indent=0, **attributes) -> str:
    """<footer>"""
    return _element('footer', content, indent, False, **attributes)


def division(content, indent=0, **attributes) -> str:
    """<div>"""
    return _element('div', content, indent, False, **attributes)


def table_datum(content, indent=0, **attributes) -> str:
    """<td>"""
    return _element('td', content, indent, True, **attributes)


def table_row(content, indent=0, **attributes) -> str:
    """<tr>"""
    return _element('tr', content, indent, False, **attributes)


def table_body(content, indent=0, **attributes) -> str:
    """<tbody>"""
    return _element('tbody', content, indent, False, **attributes)


def table_header(content, indent=0, **attributes) -> str:
    """<thead>"""
    return _element('thead', content, indent, False, **attributes)


def table(content, indent=0, **attributes) -> str:
    """<table>"""
    return _element('table', content, indent, True, **attributes)


def horizontal_rule(indent=0, **attributes) -> str:
    """<hr>"""
    return _element('hr', None, indent, False, **attributes)


def line_break(indent=0, **attributes) -> str:
    """<br>"""
    return _element('br', None, indent, False, **attributes)


def list_item(content, indent=0, inline=True, **attributes):
    """<li>"""
    return _element('li', content, indent, inline, **attributes)


def unordered_list(content, indent=0, **attributes):
    """<ul>"""
    return _element('ul', content, indent, False, **attributes)


def ordered_list(content, indent=0, **attributes):
    """<ul>"""
    return _element('ol', content, indent, False, **attributes)


def union(*elements):
    elements_union = '\n'.join(elements)
    if '\n\n' in elements_union:
        elements_union = elements_union.replace('\n\n', '\n')

    return elements_union


def preload_font(font_url: str):
    font_type = 'font/' + font_url.split('.')[-1]

    preload_attributes = {'rel': 'preload',
                          'href': font_url,
                          'as': 'font',
                          'type': font_type,
                          'crossorigin': True}

    return link(**preload_attributes)


heading1 = heading
heading2 = section_heading
heading3 = details_heading
heading4 = content_heading
