from .Livre import Livre
from .utils import combiner_paths

import os
from pathlib import Path
import json
from ebooklib.utils import debug

import logging

class Bibliotheque():
    def __init__(self, dossier_livre, dossier_rapports="rapports") -> None:
        self.dossier_livre = dossier_livre
        self.livres = self._extraire_livres_depuis_fichier(self.dossier_livre)

        if not os.path.isdir(dossier_rapports):
            os.mkdir(dossier_rapports)
        self.dossier_rapports = dossier_rapports


    def initialise(self):
        self.enregistrer_rapport_auteur( self._get_dict_livres_par_auteur(self.livres) )
        self.enregistrer_rapport_livres( self.livres )
        self.generer_toc()

    def update(self):
        logging.debug("Mise à jour des livres")
        self.rapport_saved = self._open_bibli()
        if self.rapport_saved != None:
            ajoute,retire = self._verif_changement(self.rapport_saved, self.livres)
            if len(ajoute) > 0 or len(retire) > 0:
                # print("Livres ajoutés", ajoute)
                # print("Livres retirés", retire)

                for l in retire:
                    logging.debug(f"{l} retiré")
                    l.del_toc(self.dossier_rapports)

                for l in ajoute:
                    logging.debug(f"{l} ajouté")
                    try:
                        l.save_toc(self.dossier_rapports)
                    except:
                        logging.error(f"Impossible de sauvegarder la table des matières de {l.titre}")
                        continue

                self.enregistrer_rapport_auteur( self._get_dict_livres_par_auteur(self.livres) )
                self.enregistrer_rapport_livres( self.livres )

    def _open_bibli(self):
        if os.path.exists(f"{self.dossier_rapports}/rapport_livres.txt"):
            with open(f"{self.dossier_rapports}/rapport_livres.txt", "r", encoding="utf-8") as file:
                livres_json = json.load(file)
                livres = []
                for titre in livres_json:
                    try:
                        livre = Livre(auteur=livres_json[titre]["auteur"], titre=titre, path=livres_json[titre]["fichier"], lang=livres_json[titre]["langue"], open=False)
                        livres.append(livre)
                    except ValueError as e:
                        print(e)
                        continue           
                livres = set( livres )
                return livres
        else:
            logging.error(f"Le chemin d'accès n'existe pas, veuillez vérifier que le fichier: {self.dossier_rapports}/rapport_livres.txt, existe bien")
            raise Exception("Bibliotèque introuvable, vérifier le chemin d'accès aux rapports")

    def _extraire_livres_depuis_fichier(self, path):
        paths = combiner_paths(path, ("*.pdf", "*.epub"))
        res = [Livre(path=path) for path in paths]
        for l in res:
            l.recuperer_info_fichier()
        livres = set(res)
            
        return livres

    def _get_auteurs_set(self, livres):
        return set(map(lambda x: getattr(x, "auteur"), livres))
        
    def _get_dict_livres_par_auteur(self, livres):
        auteurs = self._get_auteurs_set(livres)
        return {auteur: {livre.titre: str(livre.path) for livre in livres if livre.auteur == auteur} for auteur in auteurs}

    def enregistrer_rapport_auteur(self, livres_par_auteur):
        with open(f"{self.dossier_rapports}/rapport_auteurs.txt", "w", encoding="utf-8") as file:
            file.write( json.dumps(livres_par_auteur, indent=4, ensure_ascii=False) )

    def enregistrer_rapport_livres(self, livres):
        dict_livres = {l.titre: {"auteur": l.auteur, "fichier": str(l.path), "langue": l.lang} for l in livres }
        with open(f"{self.dossier_rapports}/rapport_livres.txt", "w", encoding="utf-8") as file:
            file.write( json.dumps(dict_livres, indent=4, ensure_ascii=False) )

    def generer_toc(self):
        for l in self.livres:
            try:
                l.save_toc(self.dossier_rapports)
            except Exception as e:
                logging.error(f"Impossible de sauvegarder la table des matières de {l.titre}, {l.path} |  {e}")
                continue
        # pypandoc.convert_file('tocs/*.txt', 'pdf')
        

    def _verif_changement(self, old, new):
        livres_ajoutes = new.difference(old)
        livres_enleves = old.difference(new)

        return livres_ajoutes, livres_enleves