import random
from docx.document import Document
from docx.oxml.table import CT_Tbl
from docx.oxml.text.paragraph import CT_P
from docx.table import _Cell, Table
from docx.text.paragraph import Paragraph
import re
import docx
from zipfile import ZipFile
from xml.dom.minidom import parseString


def file_check_interface(file, mock=True):
    if mock:
        return mock_return()
    return check_file(file)


def mock_return():
    is_wrong = random.random() < 0.4
    res = [1 for x in range(5)]
    if is_wrong:
        for i in range(len(res)):
            if random.random() < 0.5:
                res[i] = 2
    return res


# ======================================================================
doc_style = docx.Document('style.docx')


def check_file(file_path):
    file_path = docx.Document(file_path)


def default_font(file):
    with ZipFile(file, 'r') as z:
        data = z.read('word/theme/theme1.xml')  # todo: а я говорил
        data = str(data)

    default_text_font = False
    default_header_font = False

    if "majorFont><a:latin typeface=\"Times New Roman\"" in data:
        default_header_font = True

    if "minorFont><a:latin typeface=\"Times New Roman\"" in data:
        default_text_font = True

    z.close()
    return default_header_font, default_header_font


def find_content(file):
    ind_para_content = 0
    for i in range(len(file.paragraphs) + 1):
        while not (file.paragraphs[i].text == "Содержание"
                   and file.paragraphs[i + 1].style.name == "toc 1"
                   or file.paragraphs[i + 1].text.startswith("Введение")):
            i += 1
        ind_para_content = i
        break
    if ind_para_content == 0:
        print("Отсутствует содержание")

    return ind_para_content


def field_check(file):
    field = []
    for section in file.sections:
        if abs(section.bottom_margin.cm - 2) > 0.001:
            field[0] = field[0] + 1
        elif abs(section.top_margin.cm - 2) > 0.001:
            field[1] = field[1] + 1
        elif abs(section.left_margin.cm - 3) > 0.001:
            field[2] = field[2] + 1
        elif abs(section.right_margin.cm - 1) > 0.001:
            field[3] = field[3] + 1
    return field


def iter_block_items(parent):
    """
    Yield each paragraph and table child within *parent*, in document order.
    Each returned value is an instance of either Table or Paragraph. *parent*
    would most commonly be a reference to a main Document object, but
    also works for a _Cell object, which itself can contain paragraphs and tables.
    """
    if isinstance(parent, Document):
        parent_elm = parent.element.body
    elif isinstance(parent, _Cell):
        parent_elm = parent._tc
    else:
        raise ValueError("something's not right")

    for child in parent_elm.iterchildren():
        DOMTree = parseString(child.xml)  # TODO: тут поле для оптимизаций
        data = DOMTree.documentElement
        nodelist = data.getElementsByTagName('pic:blipFill')  # TODO: а что насчет формул? Mathtype и вордовские
        if len(nodelist) >= 1:
            for pic in nodelist:
                yield "##########################Картииинка"
        elif isinstance(child, CT_P):
            yield Paragraph(child, parent)
        elif isinstance(child, CT_Tbl):
            yield Table(child, parent)


def iter_tables_context(parent):
    para = None
    for elem in iter_block_items(parent):
        if isinstance(elem, Paragraph):
            para = elem
        elif isinstance(elem, Table):
            yield (para, elem)


def iter_pics_context(parent):
    pic = None
    for elem in iter_block_items(parent):
        if isinstance(elem, str):
            pic = elem
        elif isinstance(elem, Paragraph) and pic:
            yield (elem, pic)
            pic = None
        # else:
        #     raise Exception("Элемент не параграф и не картинка")


def check_tables(parent):
    table_pattern = re.compile(r"Таблица \d+(\.\d+)* – [^а-я].+\.")
    for elem in iter_tables_context(parent):
        txt = elem[0].text if elem[0] else "НЕТ ТЕКСТА"
        valid_table = re.fullmatch(table_pattern, txt)
        if valid_table:
            print(txt, " \tХорошая таблица")
        else:
            print(txt, " \tПлохая таблица")


def check_pics(parent):
    pic_pattern = re.compile(r"Рисунок \d+(\.\d+)* – [^а-я].+\.")
    for elem in iter_pics_context(parent):
        txt = elem[0].text if elem[0] else "НЕТ ТЕКСТА"
        valid_table = re.fullmatch(pic_pattern, txt)
        if valid_table:
            print(txt, " \tХорошая картинка")
        else:
            print(txt, " \tПлохая картинка")


def shorten(s):
    return f"\"{s}\"" if len(s) < 25 else f"\"{s[:25]}...\""


def check_font(file):
    ok_fonts = {"Times New Roman"}
    fonts = set()
    ind_cont = find_content(file)

    for para in file.paragraphs[ind_cont:]:
        # para-level
        para_font = None
        style = para.style
        while not para_font:
            try:
                para_font = style.font.name
                style = style.base_style
            except Exception as e:
                print(e)
                break
        if para_font not in ok_fonts:
            print(f"Paragraph-level incorrect font: {para_font} near {shorten(para.text)}")
            # fonts.add(para_font)
            # para: None
            # run: написано

            # run-level
            for run in para.runs:
                font = run.font.name
                print(font, para_font)
                if font not in ok_fonts:
                    wrong_font = True
                    print(f"Run-level incorrect font: {font} near {shorten(run.text)}")
                    # break
# ======================================================================


if __name__ == "__main__":
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    print(file_check_interface(file_path, mock=False))
