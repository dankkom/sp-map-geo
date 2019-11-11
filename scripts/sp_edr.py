import geopandas as gpd
import pandas as pd
import unicodedata


# source: http://www.iea.sp.gov.br/out/distribuicao.html


d = pd.read_csv("tables/iea_sp_edr.csv")
d = d.rename(columns={"COD_IBGE": "CD_GEOCMU"})

g = gpd.read_file("BRA/SP/sp_municipios/sp_mun.shp", encoding="utf-8")
g.loc[:, "CD_GEOCMU"] = g["CD_GEOCMU"].astype(int)

gedr = g.merge(d, on=["CD_GEOCMU"], how="left")
gedr = gedr[["EDR", "geometry"]].dissolve(by="EDR")
gedr = gedr.reset_index()
gedr = gedr.assign(EDR_NOACCENT=gedr["EDR"].apply(
    lambda s: ''.join(c for c in unicodedata.normalize('NFD', s)
                          if unicodedata.category(c) != 'Mn')))
gedr = gedr[["EDR", "EDR_NOACCENT", "geometry"]]

gedr.to_file("sp_escritorios_de_desenvolvimento_rural/sp_edr.shp", encoding="utf-8")
