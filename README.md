# Projet d'algo : le decoupeur, partie 1.

Bienvenue dans le projet d'algo.

Pour cette première partie, on vous propose de prendre en main
la petite bibliothèque de géométrie fournie (minigeo) et
de réaliser une première découpe.


On considérera ici essentiellement trois types d'objets:

- les points, codés comme des **tuples** de coordonnées ;
- les segments, de la classe **Segment** (dans le plan) ;
- les facettes, de la classe **Facette** (des triangles dans l'espace).


On vous demande de compléter le fichier *decoupe.py* qui charge un modèle 3D
au format **STL** (attention, le format binaire et non le format ascii) puis coupe
le modèle en tranches situées sur des multiples de l'épaisseur donnée en argument.
Chaque tranche est ainsi composée d'un ensemble de segments du plan horizontal 
à la hauteur souhaitée, stocké dans un vecteur (list python).
Vous devez compléter la fonction **decoupe** qui renvoie
un vecteur de vecteur de segments, trié de la hauteur la plus basse à la hauteur la plus haute.

Le programme se charge alors de réaliser l'affichage des différentes tranches dans le terminal (sous **kitty**).

On vous fournit différents modèles pour tester dans le répertoire *stl*.
Ces fichiers sont visualisables dans n'importe quel visualiseur de fichiers STL comme par exemple meshlab.
Pour faire simple vous pouvez démarrer avec le fichier *cube.stl* qui contient un cube d'un centimètre de haut.
En coupant sur une épaisseur de 0.1 vous devrez donc obtenir une dizaine de carrés.
Le prmier carré à hauteur 0, le suivant à hauteur 0.1, puis 0.2, ...

Vous devrez faire attention au coût au pire cas de votre algorithme et viser une complexité la plus basse
possible.


Dans ce projet, nous recontrerons sans doute notre pire ennemi : l'imprecision des calculs à l'aide des flottants.
Une partie du code fournie est relativement complexe, à cause de ces flottants et nous espérons ainsi passer entre 
les mailles du filet mais ce ne sera pas forcément toujours le cas, en particulier si vous téléchargez des modèles 3d
sur internet pour tester.

