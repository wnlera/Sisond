from enum import Enum, auto, unique
from docx.text.paragraph import Paragraph
from docx.enum.text import WD_COLOR_INDEX
from typing import List


class MistakeType:
    def __init__(self,  description: str, color: WD_COLOR_INDEX, weight: int, prefix: str = "[Очипка] "):
        self.description = prefix + description
        self.color = color
        self.weight = weight


class Mistakes:
    IND_CONTENT = MistakeType("Нет титульной страницы", color=WD_COLOR_INDEX.RED, weight=0)
    MARGIN = MistakeType("Неправильные поля", color=WD_COLOR_INDEX.RED, weight=1)
    LINE_SPACING = MistakeType("Неправильный межстрочный интервал", color=WD_COLOR_INDEX.RED, weight=2)
    ALIGNMENT = MistakeType("Неправильное выравнивание", color=WD_COLOR_INDEX.RED, weight=3)
    TABLES = MistakeType("Неверно оформленная таблица", color=WD_COLOR_INDEX.RED, weight=4)
    PICTURES = MistakeType("Неверно оформленный рисунок", color=WD_COLOR_INDEX.RED, weight=5)
    FONTS = MistakeType("Неправильный шрифт", color=WD_COLOR_INDEX.RED, weight=999)


mistake_registry = []

def highlight_mistake(mistakeType: MistakeType, paragraph: Paragraph=None, paragraphs: List[Paragraph]=None,
                      additional_info: str=""):
    if paragraph is None and len(paragraphs) == 0: # and not Mistakes.MARGIN:
        raise ValueError("Не было передано фрагмента документа")
    if paragraphs is None:
        paragraphs = [paragraph]

    for i in range(len(mistake_registry)):
        if mistake_registry[i][1] == paragraphs and mistakeType == mistake_registry[i][0]:
            print("Dupe")
            return

    print(mistakeType.description)
    mistake_registry.append((mistakeType, paragraphs, additional_info))

def apply_highlight():
    for mistake_type, paras, add_info in mistake_registry:
        __highlight_mistake(mistake_type, paragraphs=paras, additional_info=add_info)
    clear_registry()

def __highlight_mistake(mistakeType: MistakeType, paragraphs: List[Paragraph]=None,
                      additional_info: str=""):
    msg = mistakeType.description + additional_info
    info_para = paragraphs[0].insert_paragraph_before(msg)
    for run in info_para.runs:
        run.font.highlight_color = WD_COLOR_INDEX.PINK
    for para in paragraphs:
        for run in para.runs:
            run.font.highlight_color = mistakeType.color

def clear_registry():
    mistake_registry.clear()





