"""Downloads Arabic fonts"""
# Date: May, 17 2020
import os
from functools import lru_cache
from glob import glob
from typing import Dict
from pathlib import Path

import requests

THIS_DIR = Path(__file__).parent.absolute()


class ArabicFonts:

    FONTS_FOLDER = os.path.join(THIS_DIR, "fonts")
    _FONTS_URLS = [
        "https://noto-website-2.storage.googleapis.com/pkgs/NotoNaskhArabic-unhinted.zip",
        "https://noto-website-2.storage.googleapis.com/pkgs/NotoSansArabic-unhinted.zip",
        "https://noto-website-2.storage.googleapis.com/pkgs/NotoKufiArabic-unhinted.zip",
        # TODO add more fonts from https://www.google.com/get/noto
    ]

    def __init__(self, font: str = ""):
        if not os.path.exists(self.FONTS_FOLDER):
            os.mkdir(self.FONTS_FOLDER)
        for url in self._FONTS_URLS:
            self._download_zip_file(url)
        self.available_fonts = list(self._available_fonts.keys())
        assert font in self.available_fonts or font is "", self._font_error
        self.default_font = self._available_fonts[font] if font else ""

    def __repr__(self) -> str:
        return str(self.available_fonts)

    @property
    def _available_fonts(self) -> Dict[str, str]:
        font_paths = glob(f"{self.FONTS_FOLDER}/*.ttf")
        font_names = [f.split("/")[-1] for f in font_paths]
        return {n: p for n, p in zip(font_names, font_paths)}

    @lru_cache(None)
    def _download_zip_file(self, url_of_zip_font):
        out_fname = url_of_zip_font.split("/")[-1]
        out_fname = os.path.join(self.FONTS_FOLDER, out_fname)
        if os.path.isfile(out_fname):
            return

        print(f"downloading and unzipping arabic font: {out_fname} .. ")
        r = requests.get(url_of_zip_font)
        with open(out_fname, "wb") as out:
            out.write(r.content)

        self._unzip_file(zipped_file=out_fname)

    def _unzip_file(self, zipped_file):
        from zipfile import ZipFile

        with ZipFile(zipped_file, "r") as zipped:
            zipped.extractall(f"{self.FONTS_FOLDER}/")

    @property  # type: ignore
    def _font_error(self) -> str:
        return (
            "بالله أتأكد ان اسم الخط المُدخل صحيح"
            + "\nPlease make sure the selected font name is correct!"
        )
