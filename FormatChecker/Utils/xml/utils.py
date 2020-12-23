from lxml import etree
from lxml.etree import Element

"""
Todo: задокументировать
"""


def get_xml_repr(file):
    """
    Читает внутренний файл в xml
    :param file: файл
    :return: xml root
    """
    xml_repr = etree.parse(file).getroot()
    return xml_repr


def xml_compare_theme_latin_font(xml_theme: Element, font):
    if xml_theme is None:
        raise AttributeError("Нет xml файла")

    for x in xml_theme:
        for i in x:
            if "fontScheme" in i.tag:
                xml_theme = i
                break

    if xml_theme is None:
        raise AttributeError("Нет fontScheme в xml файле")

    theme_fonts = []
    for elem in xml_theme:
        for font_entry in elem:
            if "latin" in font_entry.tag:
                theme_fonts.append(font_entry)

    for theme_font in theme_fonts:
        if theme_font.attrib["typeface"] != font:
            return False
    return True


def get_default_font_is_ok(theme_xml_root, document_xml_text):  # pure
    """
    :param theme_xml_root: xml root для темы
    :param document_xml_text: plain text документа
    :return: True if document body does not contain any text formatted with default theme or default theme font is Time. Else returns False.
    """
    # TRUE IF OK

    theme_font_is_times = xml_compare_theme_latin_font(theme_xml_root, "Times New Roman")
    #
    # # todo: тоже парсить надо, они могут меняться местами
    # bad_string = ["asciiTheme=\"minorHAnsi\" w:hAnsiTheme=\"minorHAnsi\" w:cstheme=\"minorHAnsi\"",
    #               "asciiTheme=\"majorHAnsi\" w:hAnsiTheme=\"majorHAnsi\" w:cstheme=\"majorHAnsi\""]
    # doc_contains_default_theme = bad_string[0] in document_xml_text or bad_string[1] in document_xml_text
    #
    # return not doc_contains_default_theme \
    #        or doc_contains_default_theme and theme_font_is_times
    return theme_font_is_times


def get_theme_run(document_xml_root):  # pure
    """
    :param file: name file to analyse
    :return: True if any run contain theme, else returns False
    """

    run_theme = {}
    auto_content = False

    for x in document_xml_root:
        for elem in x:
            if not elem.tag.endswith('}p'):
                continue

            for p in elem:
                if not (p.tag.endswith('pPr') or p.tag.endswith('}r')):
                    continue

                for pPr in p:
                    if pPr.tag.endswith('tabs'):
                        for tab in pPr:
                            tab_attrib = tab.attrib
                            for key in tab_attrib.keys():
                                if key.endswith("leader"):
                                    auto_content = True
                    else:
                        auto_content = False

                    if pPr.tag.endswith('rPr') and auto_content is False:
                        for rPr in pPr:
                            if not rPr.tag.endswith('rFonts'):
                                continue
                            rPr_attrib = rPr.attrib
                            for key in rPr_attrib.keys():
                                # if key.endswith('cstheme'):
                                #     run_theme["cstheme"] = rPr_attrib[key]
                                #     print(rPr)
                                if key.endswith('hAnsiTheme'):
                                    run_theme["hAnsiTheme"] = rPr_attrib[key]
                                # elif key.endswith('eastAsiaTheme'):
                                #     run_theme["eastAsiaTheme"] = rPr_attrib[key]
                                elif key.endswith('asciiTheme'):
                                    run_theme["asciiTheme"] = rPr_attrib[key]

    if len(run_theme) != 0:
        return True
    else:
        return False


def get_styles_with_theme(style_xml_root):  # pure
    """
    :param style_xml_root: xml root для стилей документа
    :return: dict with key: style id, value: theme
    """

    # style_font = {'cstheme': '',
    #               'hAnsiTheme': '',
    #               'eastAsiaTheme': '',
    #               'asciiTheme': ''}
    style_font = {}
    styles_with_theme = {}
    style_id = 0
    # styles_id = {style_id: style_font}

    style_contains_theme = False
    # print(style_xml_root.tag)
    for x in style_xml_root:
        # print(x.tag)
        if 'style' in x.tag:
            attributes = x.attrib
            for key in attributes.keys():
                if key.endswith('styleId'):
                    style_id = attributes[key]
        for style in x:
            if style.tag.endswith('rPr'):
                for rPr in style:
                    # print(rPr.tag)
                    if rPr.tag.endswith('rFonts'):
                        rPr_attrib = rPr.attrib
                        for key in rPr_attrib.keys():
                            if key.endswith('cstheme'):
                                style_font["cstheme"] = rPr_attrib[key]
                            elif key.endswith('hAnsiTheme'):
                                style_font["hAnsiTheme"] = rPr_attrib[key]
                            elif key.endswith('eastAsiaTheme'):
                                style_font["eastAsiaTheme"] = rPr_attrib[key]
                            elif key.endswith('asciiTheme'):
                                style_font["asciiTheme"] = rPr_attrib[key]
                        if len(
                                style_font) == 4:  # возможно, правильнее проверять только тех, у кого asciiTheme и hAnsiTheme
                            styles_with_theme[style_id] = style_font
                        style_font = {}

    return styles_with_theme


def get_font_from_fonttable(fonttable_xml_root):  # pure
    fonts_fonttable = []

    if fonttable_xml_root is None:
        raise AttributeError("Нет xml файла")

    for x in fonttable_xml_root:
        font_attrib = x.attrib
        for key in font_attrib:
            if key.endswith('name'):
                fonts_fonttable.append(font_attrib[key])
    return fonts_fonttable


def get_toc_text(document_xml_root):
    toc_texts = []
    # toc_doc

    if document_xml_root is None:
        raise AttributeError("Нет xml файла")

    for elem in document_xml_root:
        for p in elem:
            for tag in p:
                if 'hyperlink' in tag.tag:
                    for r in tag:
                        if 't' in r.tag:
                            for t in r:
                                if t.text:
                                    toc_texts.append(t.text)
    return toc_texts



