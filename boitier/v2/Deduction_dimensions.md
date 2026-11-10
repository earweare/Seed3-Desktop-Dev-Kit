# Dimensions déduites — méthode et limites

La photo est recalée sur les quatre trous H1–H4, d’entraxes connus 187 × 101 mm. Le facteur de correspondance est environ 9,77 pixels/mm. Les positions de toutes les commandes restent celles du KiCad. Les dimensions verticales ne sont pas obtenues par une mise à l’échelle de la vue de dessus : une hauteur n’a pas de projection métrique identifiable sans les paramètres de prise de vue.

| Ensemble | Indices croisés | Géométrie retenue | Niveau de certitude |
|---|---|---|---|
| VR1–VR8 | Empreinte 9 mm, 3 broches au pas 2,5 mm, deux attaches latérales ; photo : plaque métallique, fond bleu, axe rond cranté avec trait blanc | Famille Song Huei R0904N, corps 6,8 mm + couverture 0,8 ; axe Ø6, variante L25 déduite de la seconde photo | Position certaine ; famille plausible ; L25 soutenue par huit mesures perspective de 24,48 à25,21 mm |
| SW17/SW18 | 3 broches en ligne au pas 2,54 mm ; largeur de corps environ 5 mm ; bague et levier métalliques | Famille Dailywell 2M SPDT, corps 5,08 ×8,13 ×8,64 ; bague B1 5,59 ; levier T1 9,4 | Position certaine ; enveloppe cohérente avec plan de famille ; suffixe non confirmé |
| Six prises CV/Gate | Corps 9 mm, broches en ligne aux décalages -5 /3,5 /6,5 ; prise verticale 3,5 mm sur photo | Famille Thonkiconn PJ301M-12/WQP518MA : corps 10 mm, fût Ø6 ×5 | Forte concordance mécanique ; fournisseur exact non indiqué |
| RV1 | Empreinte nommée RK10J ; six contacts SMD ; disque Ø14 dans la sérigraphie et sur photo | ALPS RK10J12R dual SMD, enveloppe de famille hauteur 4,7 | Famille et diamètre bien contraints ; suffixe exact inconnu |
| Module A1 | STEP officiel Seed3, broches au pas 2,54 ; module amovible visible sur photo | Module STEP exact, implantation recalée sur rangées ; empilement déduit 11,5 mm (estimation 11,67) | Géométrie module documentée ; hauteur des supports estimée par la vue oblique |

Le fichier 3D exploite ces déductions au lieu de laisser les pièces absentes. Les corps n’ont pas été agrandis arbitrairement pour occuper une place sur la photo. Le capot comporte des ouvertures et du jeu pour tolérer les écarts de famille, mais ne couvre pas toutes les longueurs d’axe possibles (L15, L20, L25…). La deuxième photographie oblique a permis d’estimer les hauteurs par recalage de caméra : médiane des axes proche de 25 mm, dessous du module proche de 11,67 mm. Le suffixe fabricant exact reste non confirmé. Les valeurs déduites restent des estimations photographiques.

Plans utilisés : Song Huei R09N-003 version 1.5, Dailywell 2M Series, ALPS RK10J/RK14J. Les sources sont répertoriées dans LIRE_AVANT_IMPRESSION.md et chaque volume dans Provenance_composants.csv.

Le recalage perspective (16 sommets de boutons TL1105 de hauteur 7,5 mm +3 trous au niveau du PCB) est documenté dans Estimation_photo_oblique.json. Les points des axes sont relevés manuellement ; le modèle de caméra suppose une focale commune et un centre optique au centre de l’image, sans correction de distorsion. Une faible erreur de reprojection ne constitue pas à elle seule une garantie d’exactitude absolue des hauteurs.
