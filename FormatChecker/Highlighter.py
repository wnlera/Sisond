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
    MARGIN = MistakeType("Неправильные отступы", color=WD_COLOR_INDEX.RED, weight=1)
    LINE_SPACING = MistakeType("Неправильный межстрочный интервал", color=WD_COLOR_INDEX.RED, weight=2)
    ALIGNMENT = MistakeType("Неправильное выравнивание", color=WD_COLOR_INDEX.RED, weight=3)
    TABLES = MistakeType("Неверно оформленная таблица", color=WD_COLOR_INDEX.RED, weight=4)
    PICTURES = MistakeType("Неверно оформленный рисунок", color=WD_COLOR_INDEX.RED, weight=5)
    FONTS = MistakeType("Неправильный шрифт", color=WD_COLOR_INDEX.RED, weight=999)


def highlight_mistake(mistakeType: MistakeType, paragraph: Paragraph=None, paragraphs: List[Paragraph]=None,
                      additional_info: str=""):
    if paragraphs is None:
        paragraphs = [paragraph]
    if paragraph is None:
        raise ValueError("Не было передано фрагмента документа")
    print(mistakeType.description)
    msg = mistakeType.description + additional_info
    info_para = paragraphs[0].insert_paragraph_before(msg)
    for run in info_para.runs:
        run.font.highlight_color = WD_COLOR_INDEX.PINK
    for para in paragraphs:
        for run in para.runs:
            run.font.highlight_color = mistakeType.color





