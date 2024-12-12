1. Contexte et Objectifs

Problématique de l'Application

Les rendements de miel à la ruche ont largement diminué ces dernières décennies. Dans un contexte de changement climatique, la capacité des apiculteurs à s’adapter aux aléas des conditions dans lesquelles se fait leur production est un facteur clé pour la durabilité de leur activité. 
L’ouverture et l’accès à des données pertinentes pour comprendre et anticiper l’activité des abeilles permet l’émergence de services utiles pour sauvegarder l’apiculture, telle que l’application BeeGIS (https://appli.itsap.asso.fr/app/01-beegis) proposée par l’ITSAP – Institut de l’abeille.

A l’origine développée pour un nombre restreint d’agents techniques et scientifiques membres ou partenaires de l’ITSAP - Institut de l’abeille, BeeGIS a été construite sur des fondations simples au regard de la gestion des données. 
Identifiée par les apiculteurs professionnels comme service pertinent pour leur activité, notre application a ensuite été mise à disposition gratuitement. Elle s’oriente aujourd’hui vers des fonctionnalités de gestion de cheptel qui impliquent la collecte de données dont certaines à caractère personnel. Dans ce nouveau contexte, il est impératif de revoir les tenants et aboutissant de la gestion des flux entrants et sortants de BeeGIS afin de garantir la sécurité des données des utilisateurs, les performances et la robustesse du service, ainsi que son potentiel évolutif dans le cadre d’une profession qui doit constamment s’adapter aux changements.

Les étapes du projet concerné par ce cahier des charges sont :
1.	Expertise de la gestion des données mises à disposition et collectées par BeeGIS ;
2.	Proposition d’une nouvelle architecture de données répondant aux standards en matière de  Data Engineering, et plus globalement de service ;
3.	Développement de la nouvelle architecture dans une logique isofonctionelle pour l’applicatif BeeGIS.
4.	Implémentation d’un nouveau flux de données météorologiques démontrant l’évolutivité et la robustesse de la nouvelle architecture.
5.	Développement d’un système de Machine Learning entre données météorologiques et données de gain de poids des ruches issues de capteurs automatisés. Les sorties du modèle se traduiront en indices et seront mis à disposition des utilisateurs – apiculteurs en guise d'outil d’aide à la décision pour le positionnement de leurs ruches.


Besoin métier exprimés

La production de miel par les colonies d’abeille domestique est très dépendante des conditions qui caractérisent leur aire de butinage à portée des ruches. Ces conditions peuvent impliquer différents stress : alimentaires, chimiques et en matière de “bioagresseurs” (prédateurs, parasites, virus, etc.).
Le métier d’apiculteur consiste (entre autres) à stimuler les colonies d’abeilles pour maximiser la population en entrée de miellée (période de montée de nectar par les plantes à intérêt mellifère), puis à positionner les ruches dans des secteurs propices à la production ciblée. Les emplacements à proximité de cultures adéquates correspondent à la production de miels monofloraux (comme la lavande) tandis que les miels dits polyfloraux (miel de montagne, de printemps, toutes fleurs, etc.) seront produits dans des milieux plus naturels, préférentiellement éloignés des grandes cultures. Le choix d’emplacement est un aspect primordial de la gestion de ruche, tant il conditionne ce qui peut être produit ainsi que les risques encourus par les abeilles.
En début de période de production, les ruches sont équipées de hausses dans lesquelles les colonies stockeront le nectar. Ces hausses représentent un espace supplémentaire que la colonie doit réguler, notamment du point de vue thermique, ce qui implique une dépense d’énergie conséquente pour les ouvrières de la ruche. Pour cette raison, dans la majorité des cas une seule hausse par ruche est positionnée en entrée de miellée, et l’apiculteur met en place différentes stratégies pour déterminer le moment optimal pour venir les récolter, et éventuellement en positionner de nouvelles si la miellée se poursuit.
Les stratégies mises en place pour déterminer une date de récolte prévisionnelle peuvent varier, allant de la simple expertise par l’apiculteur des ressources florales et des prévisions météo à la mise en place de capteurs connectés (balances automatiques) en passant par un réseau humain. L’enjeu économique de cette prise de décision est important car il impacte non seulement les quantités de miel produites et l'état de santé des ruches, mais aussi le coût en carburant et en temps de travail car les emplacements de production peuvent être très éloignés du siège de l’exploitation.
Le choix d’emplacement est donc primordial pour tout apiculteur transhumant (soit la majorité des apiculteurs professionnels). Les prises de décisions relatives à cet aspect nécessitent une lecture éclairée de nombreuses informations, telles que le type de ressources florales à portée des ruchers et les conditions météorologiques. Ces dernières ont un double impact : en amont de la miellée, elles conditionnent les quantités de nectar que produiront les plantes, tandis qu’au cours de la miellée, elles conditionnent la capacité des abeilles à aller récolter cette ressource (le vol étant inhibé par les vents violents ainsi que les précipitations).

L'application web BeeGIS a trouvé un écho auprès des professionnels de l'apiculture car elle facilite l’accès à des données qui conditionnent le choix d’emplacement. Actuellement, il s’agit uniquement de données d’occupation du sol qui, bien que ouvertes et mises à disposition sur le site www.geoportail.fr de l’Institut Géographique National (IGN), n’étaient pas travaillées pour l’usage spécifique des apiculteurs. BeeGIS propose en effet un traitement de données pertinent pour l’activité apicole en :
-	Incluant différentes couches cartographiques afin d’offrir une vision exhaustive (parcelles agricoles, forêts, hydrographie, etc.) ;
-	Simplifiant les données du parcellaire agricole par regroupement des types de cultures pour conserver uniquement celles à intérêt mellifère (diminution de 360 à 70 catégories) ;
-	Réalisant un “découpage” des surfaces pour conserver uniquement ce qui est à proximité des ruches (le rayon de l’aire est déterminé par l’apiculteur – utilisateur entre 500 m et 3 km) ;
-	Proposant des visualisations résumant la composition de l’aire de butinage de chaque rucher (surface par catégorie) et en proposant une comparaison graphique des emplacements positionnés sur une carte.

L’application BeeGIS est aujourd’hui utilisée par plus de 5000 apiculteurs qui font remonter des demandes d’évolution, notamment pour l’intégration d’un espace personnel impliquant la collecte de données à caractère personnel. Cette fréquentation est à mettre en perspective avec le nombre d’apiculteurs professionnels (6000 d’après les pouvoirs publics) et de loisirs (environ 55000). BeeGIS s’adresse majoritairement aux apiculteurs professionnels transhumants.
Afin de continuer à développer le service offert aux apiculteurs par l’application BeeGIS, l’ITSAP - Institut de l’abeille a besoin de :
-	Sécuriser les flux de données entrants et sortants de l’application ;
-	Optimiser les performances de son service ;
-	Intégrer de nouveaux flux de données ;
-	Proposer des indices synthétiques en guise d’outils d’aide à la décision à destination des apiculteurs.




Parties Prenantes

Sur proposition d’Alexandre Dangléant de réaliser ce projet comme fil rouge de la formation Data Engineer (Bootcamp Septembre 2024) auprès de Datascientest, l’équipe constituée soumettra un rendu d’architecture à intégrer en production au sein de la plateforme BeeGIS.

Commanditaire de l’Application : 
ITSAP – Institut de l’abeille (https://itsap.asso.fr/), association à but non lucratif (Loi 1901) reconnue d’intérêt général, qualifiée Institut Technique Agricole en janvier 2023.
SIRET : 43916045800022
Les mentions légales dans BeeGIS (je ne sais pas s’il est nécessaire d’aller aussi loin) :
ÉDITEUR 
ITSAP – Institut de l’Abeille, Association déclarée régie par la loi du 1er juillet 1901 
SIRET : 43916045800022
Siège social : 149 rue de Bercy 75012 PARIS 
Email : appli@itsap.asso.fr
Directeur de la publication : Monsieur Axel DECOURTYE en sa qualité de Directeur Général.

HÉBERGEUR 
CTIG INRAE
INRAE Domaine de Vilvert 78352 JOUY-EN-JOSAS CEDEX


Administrateur de l’Application :
Lors de la phase de développement, l’équipe en charge répond aux besoins d’administration de l’infrastructure. En production, le commanditaire est responsable de désigner les administrateurs responsables de la maintenance du système et de la sécurité des données.

Utilisateurs de l’Application :
BeeGIS cible les apiculteurs, professionnels comme amateurs, soucieux d’obtenir des informations fiables et utiles leur permettant d’optimiser leur production tout en réduisant les risques liés à la perte de cheptel de colonies d’abeilles domestiques.
Contexte d'Utilisation

BeeGIS est accessible en ligne, diffusée via une Interface Utilisateur (UI) affichée sous format de page web et disponible par navigation. Elle s’appuiera sur des données stockées ou “requêtée” selon la fonctionnalité intégrée provenant de la source de données fournie.
L’architecture définie dans le présent document doit permettre de faire évoluer le contexte dans le futur, par exemple par le biais de l’utilisation des routes de l’API via d’autres plateformes ou moyens d’utilisation.
L'accès au constituant architecturel contenant les données, l’API et les modèles de Machine Learning est sécurisé et strictement réservé aux administrateurs désignés par le commanditaire.

Ethique et RGPD

Lors de l’enregistrement d’un nouvel utilisateur, sont stockés son nom d’utilisateur (pseudonyme) et son mot de passe (hashé dans la base de données, aucun mot de passe n’est conservé en “clair”).
L’utilisateur peut ajouter des données (optionnelles) dont certaines sont soumises aux règlementations en vigueur sur le stockage et l’utilisation de données à caractère personnel.
Ces données peuvent être : 
-	Adresse : comprenant rue, ville, pays ;
-	Coordonnées : comprenant téléphone, email ;
-	Emplacements de ruchers : coordonnées GPS. En cas de présence de ruches, la réglementation impose que le numéro d’apiculteur doit figurer sur le rucher. Ce numéro peut servir à réidentifier l’apiculteur après démarches auprès des pouvoirs publics.

Les données issues des capteurs des ruches sont liées à l’utilisateur propriétaire. Elles possèdent un caractère de géolocalisation (latitude, longitude) utilisé dans le cadre de la transformation de données et de l’entrainement de modèles de Machine Learning. En aucun cas ces données ne sont utilisées à des fins de prospection, traçabilité des biens d’un apiculteur, ou divulguées au public sur l’application BeeGis.

L’utilisateur est informé lors de sa navigation sur la plateforme applicative de son droit d’accès aux données, de rectification et de suppression.
Il est également informé du temps de conservation des données et du délai de suppression de ces dernières.
La suppression des données entraine le droit à l’oubli et aucune donnée ne peut être restaurée après une demande de suppression.
Lors de la phase de développement, les données tests sont conservées sur le territoire de l’Union Européenne.
Lors de la phase de production, le commanditaire est responsable du respect des obligations légales qui lui incombe et du devoir d’information de l’utilisation des données utilisateur, notamment en cas de migration du stockage des données vers d’autres régions du monde.
Le commanditaire est tenu d’informer ses utilisateurs des mesures prises en cas de changement ou de nouvelle règlementation dans les pays d’exploitation de l’application.
Infrastructure actuelle

Descriptif

L’architecture actuelle est composée d’une machine virtuelle exécutant de manière non containerisée un serveur web et un moteur de base de données Postgres.
La communication de la Web app vers la base de données passe par du code langage R qui effectue la connexion et les requêtes directement vers la base de données.
Un utilisateur de l’application accède à la web app par son navigateur et peut utiliser la carte afin d’obtenir diverses informations sur un lieu et périmètre donnés. Cette demande d’information est transmise directement à la base pour retourner les résultats de la demande.
