from .utils import combiner_paths, text_to_pdf


import os
import sys
from PyPDF2 import PdfFileReader
import epub
from pathlib import Path
import ebooklib.epub as ebl
import json
import configparser
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from ebooklib.utils import debug

from bs4 import BeautifulSoup as bs

import aspose.words as aw
import pypandoc

import logging
logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')


class Livre():
    def __init__(self, auteur=None, titre=None, path=None, lang="fr", open=True) -> None:
        self.toc = None
        if path != None:
            self.path = path
            if isinstance(path, Path):
                self.file_name = path.name
            else:
                self.file_name = Path(path).name
            self.auteur = auteur
            self.titre = titre
            self.lang = lang

            if open==True:
                if path.suffix == ".pdf":
                    self._open_pdf()
                elif path.suffix == ".epub":
                    self._open_epub()

            if self.titre == None:
                self.titre = self.file_name
        else:
            self.auteur = auteur
            self.titre = titre

        if self.auteur == None:
            self.auteur = "Sans Auteur"

        if self.titre == None:
            raise ValueError(f"Impossible de récupérer le titre du livre, {titre}")

    def __repr__(self) -> str:
        return f"{self.titre} par {self.auteur}"

    def _open_pdf(self):
        with self.path.open(mode='rb') as f:
            pdf = PdfFileReader(f, strict=False)
            information = pdf.metadata
            self.auteur = information.author
            self.titre = information.title
            parser = PDFParser(f)
            document = PDFDocument(parser)

            # Recupère la TOC du document
            try:
                outlines = document.get_outlines()

                content = []
                for (level,title,dest,a,se) in outlines:
                    content.append(f"{title}")
                self.toc = bytes("\n".join(content), encoding='utf-8')
            except Exception as e:
                # logging.warning("Pas de table des matières pour", self.titre)
                self.toc = None
                pass
                

    def _open_epub(self):
        with epub.open_epub(f'{self.path}') as book:
            metadata = book.opf.metadata
            auteur = metadata.creators[0][0]
            titre = metadata.titles[0][0]
            self.auteur = auteur
            self.titre = titre
            self.lang = metadata.languages[0]

        b = ebl.read_epub(self.path)


        toc_xml = b.get_item_with_href("toc.ncx").get_content()
        toc_parsed = bs(toc_xml, features="xml").find_all("navPoint")
        toc_parsed = list(map(  lambda x: x.find("text").text,toc_parsed))

        toc_pretty = bytes("\n".join(toc_parsed), "utf-8")
        self.toc = toc_pretty

    def save_toc(self):
        if self.toc != None:
            with open(f"tocs/{self.titre}_toc.txt", "wb") as f:
                f.write(self.toc)
            
            
            text_to_pdf(self.toc.decode("utf-8"), f"tocs/{self.titre}_toc.pdf")

            # pypandoc.convert_text(self.toc.decode("utf-8"), format="md", to="epub", outputfile=f"tocs/{self.titre}_toc.epub")


            # doc = aw.Document()
            # builder = aw.DocumentBuilder(doc)
            # builder.writeln(self.toc.decode("utf-8"))

            # doc.save(f"C:\\Users\\raves\\Documents\\Dev\\bibli\\tocs\\{self.titre}_toc.pdf")

    def del_toc(self):
        if os.path.isfile(f"tocs/{self.titre}_toc.txt"):
            Path(f"tocs/{self.titre}_toc.txt").unlink()
        del self

    def force_del(self):
        self.path.unlink()
        del self

    def __hash__(self) -> int:
        return hash((self.auteur, self.titre, self.lang))

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Livre):
            return (self.auteur == __o.auteur and self.titre == __o.titre and self.lang == __o.lang)
        else:
            raise ValueError(f"Can't compare Livre to {type(__o)}")