from .Livre import Livre
from .utils import combiner_paths

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
import pypandoc

import textwrap
from fpdf import FPDF


import logging
logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG)
logging.basicConfig(format='%(asctime)s %(message)s')

class Bibliotheque():
    def __init__(self, path) -> None:
        # self.rapport_saved = self._open_bibli()
        self.path = path
        self.livres = self._extraire_livres_depuis_fichier(self.path)

        # if self.rapport_saved == None:
        #     self.enregistrer_rapport_auteur( self._get_dict_livres_par_auteur(self.livres) )
        #     self.enregistrer_rapport_livres( self.livres )
        #     self.generer_toc()
        # else:
        #     ajoute,retire = self._verif_changement(self.rapport_saved, self.livres)

        #     if len(ajoute) > 0 or len(retire) > 0:
        #         print("Livres ajoutés", ajoute)
        #         print("Livres retirés", retire)

        #         for l in retire:
        #             l.del_toc()

        #         for l in ajoute:
        #             try:
        #                 l.save_toc()
        #             except:
        #                 logging.error(f"Impossible de sauvegarder la table des matières de {l.titre}")
        #                 continue

        #         self.enregistrer_rapport_auteur( self._get_dict_livres_par_auteur(self.livres) )
        #         self.enregistrer_rapport_livres( self.livres )

    def initialise(self):
        self.enregistrer_rapport_auteur( self._get_dict_livres_par_auteur(self.livres) )
        self.enregistrer_rapport_livres( self.livres )
        self.generer_toc()

    def update(self):
        self.rapport_saved = self._open_bibli()
        if self.rapport_saved != None:
            ajoute,retire = self._verif_changement(self.rapport_saved, self.livres)
            if len(ajoute) > 0 or len(retire) > 0:
                # print("Livres ajoutés", ajoute)
                # print("Livres retirés", retire)

                for l in retire:
                    logging.debug(f"{l} retiré")
                    l.del_toc()

                for l in ajoute:
                    logging.debug(f"{l} ajouté")
                    try:
                        l.save_toc()
                    except:
                        logging.error(f"Impossible de sauvegarder la table des matières de {l.titre}")
                        continue

                self.enregistrer_rapport_auteur( self._get_dict_livres_par_auteur(self.livres) )
                self.enregistrer_rapport_livres( self.livres )

    def _open_bibli(self):
        if os.path.exists("rapport_livres.json"):
            with open("rapport_livres.json", "r", encoding="utf-8") as file:
                livres_json = json.load(file)
                livres = []
                for titre in livres_json:
                    try:
                        livres.append(Livre(auteur=livres_json[titre]["auteur"], titre=titre, path=livres_json[titre]["fichier"], lang=livres_json[titre]["langue"], open=False))
                    except ValueError as e:
                        print(e)
                        continue           
                livres = set( livres )
                return livres
        else:
            return None

    def _extraire_livres_depuis_fichier(self, path):
        paths = combiner_paths(path, ("*.pdf", "*.epub"))
        res = [Livre(path=path) for path in paths]
        livres = set(res)
            
        return livres

    def _get_auteurs_set(self, livres):
        return set(map(lambda x: getattr(x, "auteur"), livres))
        
    def _get_dict_livres_par_auteur(self, livres):
        auteurs = self._get_auteurs_set(livres)
        return {auteur: {livre.titre: str(livre.path) for livre in livres if livre.auteur == auteur} for auteur in auteurs}

    def enregistrer_rapport_auteur(self, livres_par_auteur):
        with open("rapport_auteurs.json", "w", encoding="utf-8") as file:
            file.write( json.dumps(livres_par_auteur, indent=4, ensure_ascii=False) )

    def enregistrer_rapport_livres(self, livres):
        dict_livres = {l.titre: {"auteur": l.auteur, "fichier": str(l.path), "langue": l.lang} for l in livres }
        with open("rapport_livres.json", "w", encoding="utf-8") as file:
            file.write( json.dumps(dict_livres, indent=4, ensure_ascii=False) )

    def generer_toc(self):
        for l in self.livres:
            try:
                l.save_toc()
            except Exception as e:
                logging.error(f"Impossible de sauvegarder la table des matières de {l.titre}, {l.path} |  {e}")
                continue
        # pypandoc.convert_file('tocs/*.txt', 'pdf')
        

    def _verif_changement(self, old, new):
        livres_ajoutes = new.difference(old)
        livres_enleves = old.difference(new)

        return livres_ajoutes, livres_enleves



def text_to_pdf(text, filename):
    a4_width_mm = 210
    pt_to_mm = 0.35
    fontsize_pt = 10
    fontsize_mm = fontsize_pt * pt_to_mm
    margin_bottom_mm = 10
    character_width_mm = 7 * pt_to_mm
    width_text = a4_width_mm / character_width_mm

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.set_auto_page_break(True, margin=margin_bottom_mm)
    pdf.add_page()
    pdf.set_font(family='Courier', size=fontsize_pt)
    splitted = text.split('\n')

    for line in splitted:
        lines = textwrap.wrap(line, width_text)

        if len(lines) == 0:
            pdf.ln()

        for wrap in lines:
            pdf.cell(0, fontsize_mm, wrap, ln=1)

    pdf.output(filename, 'F')