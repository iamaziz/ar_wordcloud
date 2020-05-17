# A tiny wrapper around `wordcloud.WordCloud` to support Arabic WordCloud
# Author: Aziz Alto - iamaziz.alto@gmail.com"
# Date: May, 17 2020
import os
from typing import List
from pathlib import Path
from typing import Dict
from functools import wraps

import wordcloud
import matplotlib.pyplot as plt
from arabic_reshaper import reshape
from bidi.algorithm import get_display

from ._fonts import ArabicFonts


THIS_DIR = Path(__file__).parent.absolute()
STOPWORDS = set(map(str.strip, open(os.path.join(THIS_DIR, "stopwords")).readlines()))


class ArabicWordCloud(wordcloud.WordCloud):
    def __init__(self, **kwargs):
        self.fonts = ArabicFonts()
        self.FONT_FILE = self.fonts.default_font
        super().__init__(font_path=self.FONT_FILE, **kwargs)
        self.STOPWORDS = STOPWORDS  # for arabic, and self.stopwords for english

    @staticmethod
    def reshape_rtl(s: str) -> str:
        return get_display(reshape(s))

    def remove_stop_words(self, words: List[str]) -> List[str]:
        return [w for w in words if w not in self.STOPWORDS]

    @wraps(wordcloud.WordCloud.generate_from_frequencies)
    def from_dict(
        self, words: Dict[str, int], ignore_stopwords: bool = False, **kwargs
    ):
        selected = list(words.keys())
        if ignore_stopwords:
            selected = self.remove_stop_words(list(words.keys()))

        d = {self.reshape_rtl(k): words[k] for k, v in zip(selected, words.values())}
        self.generate_from_frequencies(d, **kwargs)
        return self

    @wraps(wordcloud.WordCloud.generate)
    def from_text(self, text: str, ignore_stopwords: bool = False):
        # TODO: clean text
        if ignore_stopwords:
            text = " ".join(self.remove_stop_words(text.split()))
        self.generate(self.reshape_rtl(text))
        return self

    def from_file(self, input_file: str):
        with open(input_file, "r") as f:
            text = f.read()
        return self.from_text(text)

    def plot(self, wc: wordcloud.WordCloud, **kwargs):
        plt.figure(figsize=(kwargs.get("width", 14), kwargs.get("height", 7)))
        plt.imshow(wc, interpolation="bilinear")
        t = kwargs.get("title")
        if t:
            plt.title(self.reshape_rtl(t))
        plt.axis("off")
        plt.show()
