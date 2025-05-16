
# 🚗 Rush Hour - Jeu de logique en Python (Pygame)

Ce projet est une reproduction du célèbre jeu **Rush Hour**, développée en Python à l'aide de la bibliothèque **Pygame**. Le but du jeu est de faire sortir la voiture rouge en la déplaçant sur une grille encombrée d'autres véhicules.


## 🛠️ Installation

### 1. Prérequis

Assurez-vous d'avoir Python 3.7 ou supérieur installé.

### 2. Installer les dépendances

Ouvrez un terminal à la racine du projet et exécutez :

```
pip install pygame
```
## 🎮 Comment jouer

* Lancez le jeu avec :

```
python main.py
```

* Le menu principal vous permet de choisir :

  * **Niveau 1 à 3** : niveaux prédéfinis.
  * **Niveau Aléatoire** : un niveau généré dynamiquement et **toujours résoluble**.

* **Commandes de jeu :**

  * Cliquez d'abord sur une voiture pour la sélectionner.
  * Utilisez ensuite les **flèches directionnelles** du clavier pour la déplacer.

* Le but est de faire sortir la **voiture rouge** vers la droite.

## 🧩 Description des boutons

Sur le panneau latéral à droite :

* **Solution** : Affiche automatiquement une solution du niveau.
* **Recharger** : Réinitialise le niveau actuel.
* **Menu** : Retourne à l'écran de sélection de niveau.

## 📐 Génération des niveaux aléatoires

Les niveaux générés aléatoirement sont **garantis jouables** : ils ont été construits de manière à **assurer qu'une solution existe toujours**.


## 🧠 Le solveur

Le bouton **"Solution"** utilise un **algorithme de type Breadth-First Search (BFS)** (recherche en largeur) pour trouver une solution.

* L'algorithme garantit une **solution correcte**, mais **pas forcément en un nombre minimum de coups** (solution non optimale dans tous les cas).
* Cela permet d'assurer une résolution rapide même sur des niveaux complexes.


## 📁 Arborescence du projet

```
.
├── main.py
├── ui/
│   └── gui.py
|   └── assets/
│       ├── car1.png
│       ├── car.png   ← voiture rouge
│       ├── truck.png
│       └── menu.png  ← fond du menu
└── game/
    ├── board.py
    ├── levels.py
    ├── solver.py
    └── level_generator.py

```

## 📸 Aperçu
![image](https://github.com/user-attachments/assets/fcfe88fd-c301-446b-88c3-0fdd89bb7885)

![image](https://github.com/user-attachments/assets/7d41a51c-8546-4c35-a997-a5cb33089505)


