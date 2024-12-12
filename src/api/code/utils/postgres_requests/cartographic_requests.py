#api/utils/postgres_requests/cartographic_requests.py


# Lib
###


"""
REQUESTS
- Contains POSTGRES requests for the API
"""



"""
Queries that return data
"""


 # Params: $1: lat, $2: lon, $3: rayon, $4: source_parcellaire, $5: projection, $6: emplacement
query_get_rpg_location = (
    "SELECT rpg.culture, rpg.bio2 AS bio, rpg.legende, rpg.couleur, CONCAT('RPG ', $4) AS source, $6 AS emplacement, "
    "((st_area(st_transform(rpg.geometry, CAST($5 AS INTEGER))))/10000) AS aire, rpg.geometry "
    "FROM ( "
    "SELECT rc.libelle_culture AS culture, r.bio2, rg.libelle_apicole AS legende, rg.couleur, "
    "st_intersection(ST_MakeValid(r.geometry), (SELECT "
    "st_transform(ST_Buffer(st_transform(st_SetSRID "
    "(ST_point($2, $1), 4326), CAST($5 AS INTEGER)), $3, 10), 4326))) AS geometry "
    "FROM registre_parcellaire_graphique r "
    "JOIN rpg_code_culture rc ON r.code_culture=rc.code_culture "
    "JOIN rpg_typologie_apicole rg ON rc.code_apicole=rg.code_apicole "
    "WHERE r.annee_rpg=$4 and st_intersects(r.geometry, (SELECT st_transform(ST_Buffer(st_transform(st_SetSRID "
    "(ST_point($2, $1), 4326), CAST($5 AS INTEGER)), $3, 10), 4326))) "
    ") rpg"
)

# Params: $1: lat, $2: lon, $3: rayon, $4: source_parcellaire, $5: projection, $6: emplacement
query_get_clc_location = (
    "SELECT clc.legende, clc.couleur, CONCAT('CLC ', $4) AS source, $6 AS emplacement, "
    "((st_area(st_transform(clc.geometry, CAST($5 AS INTEGER))))/10000) AS aire, clc.geometry "
    "FROM ( "
    "SELECT lc.libelle_clc AS legende, lc.couleur, "
    "st_intersection(ST_MakeValid(c.geometry), (SELECT "
    "st_transform(ST_Buffer(st_transform(st_SetSRID "
    "(ST_point($2, $1), 4326), CAST($5 AS INTEGER)), $3, 10), 4326))) AS geometry "
    "FROM corine_land_cover c "
    "JOIN libelle_clc lc ON lc.code_18=c.code_18 "
    "WHERE c.annee_clc=$4 and st_intersects(c.geometry, (SELECT st_transform(ST_Buffer(st_transform(st_SetSRID "
    "(ST_point($2, $1), 4326), CAST($5 AS INTEGER)), $3, 10), 4326))) "
    ") clc"
)


# query_get_foretV2_location = (
#     "SELECT fv.legende, fv.couleur, 'Forêt V2' AS source, $6 AS emplacement, "
#     "((st_area(st_transform(fv.geometry, CAST($5 AS INTEGER))))/10000) AS aire, fv.geometry "
#     "FROM ( "
#     "SELECT c.legende_foret AS legende, c.couleur, "
#     "st_intersection(ST_MakeValid(f.geometry), (SELECT "
#     "st_transform(ST_Buffer(st_transform(st_SetSRID "
#     "(ST_point($2, $1), 4326), CAST($5 AS INTEGER)), $3, 10), 4326))) AS geometry "
#     "FROM foret_v2 f "
#     "JOIN code_tfv c ON c.code_tfv=f.code_tfv "
#     "WHERE st_intersects(f.geometry, (SELECT st_transform(ST_Buffer(st_transform(st_SetSRID "
#     "(ST_point($2, $1), 4326), CAST($5 AS INTEGER)), $3, 10), 4326))) "
#     ") fv"
# )