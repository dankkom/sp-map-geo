import geopandas as gpd
import pandas as pd
import unicodedata


g = gpd.read_file("sp_municipios/sp_mun.shp", encoding="utf-8")
g.loc[:, "CD_GEOCMU"] = g["CD_GEOCMU"].astype(int)


sp = pd.read_csv("tables/seade_sp_municipios.csv")
sp = sp.rename(columns={"Código": "CD_GEOCMU", "Região Administrativa": "RA"})
sp = sp[["CD_GEOCMU", "RA"]]
sp.loc[:, "RA"] = sp["RA"].replace("^Região Administrativa( de | )", "", regex=True)
sp.loc[:, "RA"] = sp["RA"].replace("-", "São Paulo")

gra = g.merge(sp, on=["CD_GEOCMU"], how="left")
gra = gra[["CD_GEOCMU", "RA", "NM_MUNICIP", "geometry"]]

gra = gra.dissolve(by="RA").reset_index()[["RA", "geometry"]]

gra = gra.assign(
    RA_NOACCENT=gra["RA"].apply(
        lambda s: ''.join(c for c in unicodedata.normalize('NFD', s)
                          if unicodedata.category(c) != 'Mn')
    )
)
gra = gra[["RA", "RA_NOACCENT", "geometry"]]

gra.to_file("sp_regioes_administrativas/sp_ra.shp", encoding="utf-8")
