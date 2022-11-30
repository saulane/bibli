# Table of Contents

* [bibli](#bibli)
* [modules](#modules)
* [modules.Bibliotheque](#modules.Bibliotheque)
  * [Bibliotheque](#modules.Bibliotheque.Bibliotheque)
    * [\_\_init\_\_](#modules.Bibliotheque.Bibliotheque.__init__)
    * [initialise](#modules.Bibliotheque.Bibliotheque.initialise)
    * [update](#modules.Bibliotheque.Bibliotheque.update)
    * [enregistrer\_rapport\_auteur](#modules.Bibliotheque.Bibliotheque.enregistrer_rapport_auteur)
    * [enregistrer\_rapport\_livres](#modules.Bibliotheque.Bibliotheque.enregistrer_rapport_livres)
    * [generer\_toc](#modules.Bibliotheque.Bibliotheque.generer_toc)
* [modules.Livre](#modules.Livre)
  * [Livre](#modules.Livre.Livre)
    * [\_\_init\_\_](#modules.Livre.Livre.__init__)
    * [recuperer\_info\_fichier](#modules.Livre.Livre.recuperer_info_fichier)
    * [save\_toc](#modules.Livre.Livre.save_toc)
    * [del\_toc](#modules.Livre.Livre.del_toc)
    * [force\_del](#modules.Livre.Livre.force_del)
* [modules.utils](#modules.utils)
  * [combiner\_paths](#modules.utils.combiner_paths)
  * [text\_to\_pdf](#modules.utils.text_to_pdf)

<a id="bibli"></a>

# bibli

<a id="modules"></a>

# modules

<a id="modules.Bibliotheque"></a>

# modules.Bibliotheque

<a id="modules.Bibliotheque.Bibliotheque"></a>

## Bibliotheque Objects

```python
class Bibliotheque()
```

<a id="modules.Bibliotheque.Bibliotheque.__init__"></a>

#### \_\_init\_\_

```python
def __init__(dossier_livre, dossier_rapports="rapports") -> None
```

Initiliase une instance de Biblioth├¿que
:dossier_livre est le dossier o├╣ se trouvent les fichiers des livres
:dossier_rapports est le dossier d'enregistrement des rapports, par d├®fauts on utilise de dossier 'rapports"

<a id="modules.Bibliotheque.Bibliotheque.initialise"></a>

#### initialise

```python
def initialise()
```

Initialise la biblioth├¿que ├á partir d'un dossier de livre

<a id="modules.Bibliotheque.Bibliotheque.update"></a>

#### update

```python
def update()
```

Met ├á jour la biblioth├¿que

<a id="modules.Bibliotheque.Bibliotheque.enregistrer_rapport_auteur"></a>

#### enregistrer\_rapport\_auteur

```python
def enregistrer_rapport_auteur(livres_par_auteur)
```

Enregistre le rapport contenant tous les auteurs et chacun de leurs livres

<a id="modules.Bibliotheque.Bibliotheque.enregistrer_rapport_livres"></a>

#### enregistrer\_rapport\_livres

```python
def enregistrer_rapport_livres(livres)
```

Enregistre le rapport contenant tous les livres

<a id="modules.Bibliotheque.Bibliotheque.generer_toc"></a>

#### generer\_toc

```python
def generer_toc()
```

G├®n├¿re les fichiers contenant la table des mati├¿res de chaque livre

<a id="modules.Livre"></a>

# modules.Livre

<a id="modules.Livre.Livre"></a>

## Livre Objects

```python
class Livre()
```

<a id="modules.Livre.Livre.__init__"></a>

#### \_\_init\_\_

```python
def __init__(auteur=None, titre=None, path=None, lang="fr", open=True) -> None
```

Cr├®e un livre ├á partir d'un fichier
:auteur est l'auteur du livre
:titre est le titre du livre
:path est le chemin du fichier du livre
:lang est la langue du livre
:open True pour r├®cup├®rer directement les infos depuis le fichier sp├®cifi├® en :path, False sinon

<a id="modules.Livre.Livre.recuperer_info_fichier"></a>

#### recuperer\_info\_fichier

```python
def recuperer_info_fichier()
```

Choisit la bonne fonction de r├®cup├®ration des donn├®es en fonction du type de fichier

<a id="modules.Livre.Livre.save_toc"></a>

#### save\_toc

```python
def save_toc(path)
```

Enregistre la table des mati├¿res en epub,txt et pdf dans le dossier sp├®cifier en :path

<a id="modules.Livre.Livre.del_toc"></a>

#### del\_toc

```python
def del_toc(dossier_rapports)
```

Supprime les tables des mati├¿res et l'objet

<a id="modules.Livre.Livre.force_del"></a>

#### force\_del

```python
def force_del()
```

Supprime le fichier originel du livre

<a id="modules.utils"></a>

# modules.utils

<a id="modules.utils.combiner_paths"></a>

#### combiner\_paths

```python
def combiner_paths(path, extensions)
```

Renvoie une liste de fichier finissant par les :extensions dans le dossier :path
:path chemin du dossier o├╣ lister les fichiers
:extensions extentions des fichiers ├á r├®cup├®rer (pdf, epub, txt, etc...)

<a id="modules.utils.text_to_pdf"></a>

#### text\_to\_pdf

```python
def text_to_pdf(text, filename)
```

Converti une chaine de caract├¿re en fichier pdf
:text chaine de caract├¿re ├á convertir
:filename fichier o├╣ enregistrer le document pdf

