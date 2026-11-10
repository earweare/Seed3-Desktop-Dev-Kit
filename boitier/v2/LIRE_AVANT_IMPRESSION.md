# Seed3 Desktop — carte peuplée et boîtier mécanique v2

Unités : millimètres. Le fichier à ouvrir dans Rhino est **Assemblage_Seed3_complet.step**. Il contient le socle, le capot, les 16 prolongateurs de boutons et la carte avec ses composants nommés séparément. Les STEP sont des solides CAO, pas des images générées.

## Contenu
- Assemblage_Seed3_complet.step : assemblage complet dans un repère commun.
- Carte_Seed3_peuplee.step : carte et composants seuls.
- Boitier_Seed3.step : socle, capot et poussoirs seuls.
- Socle.stl, Capot.stl : pièces imprimables séparées, unités mm. Ne pas importer le STL en mètres.
- Poussoir_x16.stl : une pièce à imprimer 16 fois. Prolongateur libre captif ; il ne se clipse pas sur la touche jaune.
- Comparaison_photo_KiCad.png : centres XY superposés à la photo fournie.
- Vue_3D_board.png, Vue_carte_dessus.png : rendus calculés depuis la géométrie CAO.
- Vue_3D_assembled.png, Vue_3D_exploded.png : rendus du boîtier assemblé et éclaté.
- Implantation_KiCad_mm.csv : coordonnées de toutes les empreintes.
- Provenance_composants.csv : origine et degré de précision de chaque pièce.
- Verification_geometrie.json : résultats de vérification des STL et intersections avec les composants modélisés.
- Sources/ : scripts paramétriques, modèles utilisés, KiCad/BOM de référence et licences disponibles.

## Géométrie certaine
PCB officiel Rev4 : 197 × 111 × 1,6 mm, coins de rayon 2,5 mm. Quatre perçages de fixation Ø3,5, entraxes 187 × 101 mm. Positions et rotations des empreintes extraites du KiCad, sans les réinterpréter depuis la photo. Le repère CAO est situé au coin inférieur gauche de la carte vue du dessus : X vers la droite, Y vers l'arrière, Z vers le haut. PCB inférieur Z=8 ; PCB supérieur Z=9,6.

Tous les composants montés du KiCad sont représentés ; seules les empreintes de fiduciels, QR et logo de sérigraphie ne sont pas des volumes. Les pistes, sérigraphies, logements de contact internes et soudures ne sont pas reproduits. Les perçages du PCB représentés sont ceux de fixation ; ce STEP est une référence mécanique, pas un dossier de fabrication du circuit imprimé.

Enveloppe du boîtier : 209 × 123 × 34 mm ; façade basse Z=24, protections audio/MIDI Z=34 ; protection Seed3 abaissée à Z=29,5. Fond 2,4 mm ; carte à plat, sans inclinaison imposée aux connecteurs. Deux demi-coques séparées à Z=10. Aucun connecteur n'est déporté. Casque devant ; MIDI et molette à droite ; USB et microSD à gauche ; audio derrière ; CV/Gate sur le dessus.

## Ce qui est documenté, et ce qui ne l'est pas
Le modèle du module **Seed3 Rev5** est fourni par Daisy. Le projet appelle encore l'empreinte historique « Daisy Seed Rev4 » ; le modèle utilisé est bien le Seed3 photographié. Les quatre NMJ6HCD2 utilisent le STEP Neutrik, recalé sur le dessin fabricant et les broches du KiCad. Les USB4110GFA et TF-01A utilisent les STEP inclus dans le dépôt ; les axes des imports et le décalage microSD ont été rétablis. Les composants CMS utilisent les enveloppes nominales des bibliothèques STEP KiCad. Les boutons TL1105SPF250Q sont reconstruits à partir du dessin E-Switch (hauteur totale 7,5 mm). Les DIN sont reconstruits d'après l'enveloppe Switchcraft 57PC5F ; détails de contacts simplifiés.

**La BOM publique ne donne pas tout :** P-10K-B-R, les deux toggles et les six prises CV/Gate ne comportent pas de référence fabricant complète. Leur implantation XY est exacte, mais certaines hauteurs/variantes sont des hypothèses explicites dans le CSV. Les potentiomètres ont été affinés par rapprochement avec le plan Song Huei R0904N : corps 6,8 mm, couverture 0,8 mm, axe rond cranté Ø6 avec repère blanc comme sur la photo, hauteur totale L25 déduite du recalage de la photo oblique (huit résultats de 24,48 à 25,21 mm). Les jacks CV correspondent à l’enveloppe de la famille PJ301M-12/WQP518MA : corps 10 mm, fût 5 mm, hauteur totale proche de 15 mm sur la vue oblique. Les interrupteurs sont reconstruits selon la famille Dailywell 2M : corps 5,08 × 8,13 × 8,64 mm, bague B1 de 5,59 mm et levier T1 de 9,4 mm. Ce sont des déductions de familles compatibles, et non des identifications certaines des références montées. Voir Deduction_dimensions.md. RV1 est reconstruit selon la famille ALPS RK10J12R (molette Ø14), suffixe exact absent de la BOM. Le connecteur casque a l'enveloppe de l'empreinte CUI et une hauteur nominale de 5 mm. L'empilement amovible du Seed3 est déduit à 11,5 mm (estimation photogrammétrique 11,67 mm) au-dessus de la face supérieure de la carte ; les barrettes de support sont une représentation simplifiée.

La vue oblique est recalée sur 16 boutons de hauteur connue et trois trous de fixation : elle permet une estimation des hauteurs, pas une certification métrologique. La reconstruction n'est donc pas un jumeau métrologique certifié de l'exemplaire physique.

## Vérification et montage prototype
Les solides du socle et du capot ont été vérifiés et leurs STL sont fermés, orientés correctement et chacun d'un seul tenant. Les collisions boîtier/composants ont été recherchées sur les solides BREP utilisés ; le rapport indique le résultat. Cette vérification ne remplace pas la mesure des variantes de composants mentionnées ci-dessus ni un essai physique.

1. Imprimer le socle et vérifier d'abord l'alignement des quatre fixations de la carte.
2. Fixer le PCB avec 4 vis M3 × 8 dans les avant-trous Ø2,6 ; tarauder doucement ou adapter au procédé. Ne pas forcer la carte pour aligner les vis.
3. Présenter le capot sans serrer et contrôler l'accès aux prises, les hauteurs des axes et le dégagement de la molette. Les ouvertures latérales sont volontairement élargies pour le branchement de fiches moulées.
4. Introduire les 16 poussoirs par dessous le capot, collerette vers l'intérieur. Ils reposent librement sur les touches jaunes ; course nominale du switch 0,25 mm, jeu nominal au-dessus de la collerette 0,3 mm. Vérifier l'absence de pression permanente et le retour de chaque touche avant fermeture. Ne pas coller les poussoirs.
5. Fermer avec 2 vis M3 × 20 à l'avant et 2 M3 × 30 à l'arrière ; têtes cylindriques Ø6 maximum, hauteur 2 mm maximum pour affleurer, sinon utiliser têtes basses et ajuster la longueur. Les avant-trous de la base doivent être adaptés à l'imprimante ; ne pas utiliser de vis trop longues.
6. Ajouter quatre patins adhésifs sous le socle. Les petites ouvertures LED sont en visée directe ; des guides optiques transparents Ø3 peuvent être ajoutés après ajustement de longueur. Aucun guide opaque n'est imposé.

PETG ou ABS/ASA ; buse 0,4, couches 0,2, au moins 4 périmètres. Socle fond sur le plateau, sans support principal. Le capot à plusieurs niveaux nécessite des supports localisés selon l'orientation retenue ; protéger les trous de guidage et les nettoyer après impression. Poussoirs : couche fine et contrôle du coulissement Ø6 dans Ø6,6 ; support local sous la collerette si nécessaire. C'est un prototype à ajuster, pas une validation d'industrialisation. Le démontage du capot donne accès à Boot/Reset ; les USB restent accessibles boîtier fermé.

## Sources
- KiCad : https://github.com/daisyaudio/Seed3-DevKit-Desktop
  Commit : 94347176c7909f41db8ab8139eb632ea7d0ecab9 ; production Rev4 2026-06-18.
- Seed3 : https://docs.daisy.audio/hardware/Seed3/
  https://daisy.nyc3.cdn.digitaloceanspaces.com/products/seed3/Seed3-models.zip
- Neutrik : https://www.neutrik.co.jp/jp/product/nmj6hcd2
- E-Switch : dessin J100206, TL1105SPF250Q, révision B du 15/09/2023, distribué par Mouser.
- Switchcraft : https://www.switchcraft.com/female-din-right-angle-pc-mount-5-contacts-at-180-contact-arrangement-f/57pc5f/
- ALPS : catalogue RK10J/RK14J, dessin RK10J12R, copie de documentation fabricant distribuée par Akizuki.
- Modèles CMS : KiCad kicad-packages3D, https://github.com/KiCad/kicad-packages3D ; modèles nominaux génériques.

Les modèles fabricants restent soumis à leurs conditions d'origine. Les fichiers KiCad sont accompagnés de la licence CERN-OHL-P-2.0 du dépôt. Les scripts CAO du boîtier et de reconstruction créés pour ce travail peuvent être modifiés pour le prototypage.

Sources complémentaires de déduction :
- https://www.song-huei.com/proimages/PDF/R0904N.pdf
- https://www.dailywell.com.tw/en/product/Sub-miniature-toggle-switches_2M-Series.html
- https://www.mouser.com/datasheet/2/979/dailywell_10012019_2M_Series-1660477.pdf
- https://www.thonk.co.uk/shop/thonkiconn/

## Affinage avec la deuxième photographie
L’ajustement d’une caméra perspective sur les sommets des seize boutons TL1105 (7,5 mm) et trois fixations du PCB donne une erreur de reprojection RMS d’environ 0,94 pixel. Les sommets des huit axes se placent entre 24,48 et 25,21 mm au-dessus du PCB : la variante L25 remplace L20. Le plan supérieur du module Seed3 est estimé à 13,27 mm ; moins son épaisseur 1,601 mm, le dessous est à environ 11,67 mm. L’empilement retenu est 11,5 mm, et l’ouverture USB de service est agrandie en conséquence. Les sommets des six prises CV/Gate sont estimés entre 14,7 et 15,4 mm : fût nominal de 5 mm retenu sur un corps de 10 mm. Cette cohérence entre plusieurs composants constitue une vérification indépendante des premières hypothèses, avec une incertitude d’environ 0,5–1 mm à garder pour ces déductions, et non une tolérance d’usinage certifiée.
Voir Estimation_photo_oblique.json et Comparaison_photo_oblique.png.

## Révision v2 : dégagement du premier potentiomètre
Le coin vertical de la protection Seed3 est remplacé par une échancrure conique à 45°, centrée sur VR1. Le rayon libre vaut 7 mm au niveau Z=24 et 12,5 mm au niveau Z=29,5. Avec un axe Ø6, cela laisse respectivement 4 et 9,5 mm de dégagement radial vers cette protection, contre environ 0,7 mm au coin de la v1. La protection du module est abaissée de 4,5 mm : le sommet de l'axe la dépasse désormais de 5,1 mm. La paroi inclinée conserve 2,4 mm d'épaisseur normale. Les composants et leurs positions ne changent pas.

Des boutons additionnels Ø12–14 peuvent être envisagés, avec leur bord inférieur au moins 3 mm au-dessus de la façade basse (Z≥27). Le rayon dégagé vaut alors 10 mm, soit au moins 3 mm de jeu devant cette protection pour un bouton Ø14. L'entraxe des potentiomètres est d'environ 15,28 mm : un Ø14 laisse environ 1,28 mm entre deux boutons voisins. Aucun bouton additionnel n'est fourni ni modélisé ; sa fixation sur l'axe reste à choisir et à vérifier.

Voir Vue_3D_detail.png et le champ ergonomie_v2 de Verification_geometrie.json. La vérification donne un jeu minimal Seed3/capot de 0,975 mm sur les solides modélisés ; ces jeux restent dépendants des hauteurs estimées de l'assemblage physique.
