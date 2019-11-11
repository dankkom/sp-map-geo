import geopandas as gpd


# source: http://dados.prefeitura.sp.gov.br/dataset/distritos


sp = gpd.read_file("sp_capital_distritos/LAYER_DISTRITO/DEINFO_DISTRITO.shp", encoding="utf-8")
sp = sp[["NOME_DIST", "SIGLA_DIST", "COD_DIST", "geometry"]]

# Correct projection
sp = sp.to_crs({"init": "epsg:4326"})

sp.to_file("BRA/SP/sp_capital_distritos/sp_capital_distritos.shp", encoding="utf-8")
