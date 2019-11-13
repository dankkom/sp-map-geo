import geopandas as gpd
import pandas as pd
import unicodedata
import os


datadir = "sp_regioes_administrativas"
sp_mun_dir = "sp_municipios"
sp_shp_path = os.path.join(sp_mun_dir, "sp_mun.shp")
sp_mun_table_path = os.path.join("tables", "seade_sp_municipios.csv")

g = gpd.read_file(sp_shp_path, encoding="utf-8")
g.loc[:, "CD_GEOCMU"] = g["CD_GEOCMU"].astype(int)

sp = pd.read_csv(sp_mun_table_path)
sp = sp.rename(columns={"Código": "CD_GEOCMU", "Região Administrativa": "RA"})
sp = sp[["CD_GEOCMU", "RA"]]
sp.loc[:, "RA"] = sp["RA"].replace(
    "^Região Administrativa( de | )",
    "",
    regex=True
)
sp.loc[:, "RA"] = sp["RA"].replace("-", "São Paulo")

gra = g.merge(sp, on=["CD_GEOCMU"], how="left")
gra = gra[["CD_GEOCMU", "RA", "NM_MUNICIP", "geometry"]]
gra = gra.dissolve(by="RA").reset_index()[["RA", "geometry"]]
gra = gra.assign(
    RA_1=gra["RA"].apply(
        lambda s: ''.join(c for c in unicodedata.normalize('NFD', s)
                          if unicodedata.category(c) != 'Mn')
    )
)
gra = gra[["RA", "RA_1", "geometry"]]

gra.to_file(
    os.path.join(
        datadir,
        "sp_ra.shp"
    ),
    encoding="utf-8"
)
