#!/usr/bin/python

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

import xml.etree.ElementTree as ET


config = configparser.RawConfigParser().read("bibli.conf")


def combiner_paths(path, extensions):
    fichiers = []
    for e in extensions:
        fichiers.extend(Path(path).glob(e))
    return fichiers


class Bibliotheque():
    def __init__(self, path) -> None:
        self.rapport_saved = self._open_bibli()
        self.path = path
        self.livres = self._extraire_livres_depuis_fichier(self.path)
        

        if self.rapport_saved == None:
            self.enregistrer_rapport_auteur( self._get_dict_livres_par_auteur(self.livres) )
            self.enregistrer_rapport_livres( self.livres )
            self.generer_toc()
        else:
            ajoute,retire = self._verif_changement(self.rapport_saved, self.livres)

            if len(ajoute) > 0 or len(retire) > 0:
                print("Livres ajoutés", ajoute)
                print("Livres retirés", retire)

                for l in retire:
                    print(l)
                    l.del_toc()

                for l in ajoute:
                    l.save_toc()

                self.enregistrer_rapport_auteur( self._get_dict_livres_par_auteur(self.livres) )
                self.enregistrer_rapport_livres( self.livres )

    def _open_bibli(self):
        if os.path.exists("rapport_auteurs.json"):
            with open("rapport_auteurs.json", "r") as file:
                livres_par_auteur = json.load(file)
                livres = []
                for auteur in livres_par_auteur:
                    for titre in livres_par_auteur[auteur]:
                        try:
                            livres.append(Livre(auteur=auteur, titre=titre))
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
        return {auteur: [livre.titre for livre in livres if livre.auteur == auteur] for auteur in auteurs}

    def enregistrer_rapport_auteur(self, livres_par_auteur):
        with open("rapport_auteurs.json", "w") as file:
            file.write( json.dumps(livres_par_auteur, indent=4) )

    def enregistrer_rapport_livres(self, livres):
        dict_livres = {l.titre: {"auteur": l.auteur, "fichier": str(l.path)} for l in livres }
        print(dict_livres)
        with open("rapport_livres.json", "w") as file:
            file.write( json.dumps(dict_livres, indent=4) )

    def generer_toc(self):
        for l in self.livres:
            l.save_toc()

    def _verif_changement(self, old, new):
        livres_ajoutes = new.difference(old)
        livres_enleves = old.difference(new)

        return livres_ajoutes, livres_enleves


class Livre():
    def __init__(self, auteur=None, titre=None, path=None) -> None:
        self.toc = None
        if path != None:
            self.path = path
            self.file_name = path.name
            self.auteur = None
            self.titre = None

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
                print("Pas de TOC")

    def _open_epub(self):
        with epub.open_epub(f'{self.path}') as book:
            metadata = book.opf.metadata
            auteur = metadata.creators[0][0]
            titre = metadata.titles[0][0]
            self.auteur = auteur
            self.titre = titre

        b = ebl.read_epub(self.path)
        toc_xml = b.get_item_with_href("toc.ncx").get_content()
        self.toc = toc_xml

        tree = ET.fromstring(toc_xml).findall("ncx/navMap/navPoint/navLabel/")
        print(tree)
        # print(tree.tag)

    def save_toc(self):
        if self.toc != None:
            with open(f"tocs/{self.titre}_toc.txt", "wb") as f:
                f.write(self.toc)

    def del_toc(self):
        Path(f"tocs/{self.titre}_toc.txt").unlink()
        del self

    def force_del(self):
        self.path.unlink()
        del self

    def __hash__(self) -> int:
        return hash((self.auteur, self.titre))

    def __eq__(self, __o: object) -> bool:
        return (self.auteur == __o.auteur and self.titre == __o.titre)


if __name__ == "__main__":
    args = sys.argv

    bibli = Bibliotheque("./livres/")
