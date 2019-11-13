import geopandas as gpd
import pandas as pd
import unicodedata
import os

# source: http://www.iea.sp.gov.br/out/distribuicao.html

datadir = "sp_escritorios_de_desenvolvimento_rural"
sp_mun_dir = "sp_municipios"
sp_shp_mun = os.path.join(sp_mun_dir, "sp_mun.shp")
sp_mun_table_path = os.path.join("tables", "iea_sp_edr.csv")

g = gpd.read_file(sp_shp_mun, encoding="utf-8")
g.loc[:, "CD_GEOCMU"] = g["CD_GEOCMU"].astype(int)

edr = pd.read_csv(sp_mun_table_path)
edr = edr.rename(columns={"COD_IBGE": "CD_GEOCMU"})

gedr = g.merge(edr, on=["CD_GEOCMU"], how="left")
gedr = gedr[["EDR", "geometry"]].dissolve(by="EDR")
gedr = gedr.reset_index()
gedr = gedr.assign(EDR_1=gedr["EDR"].apply(
    lambda s: ''.join(c for c in unicodedata.normalize('NFD', s)
                          if unicodedata.category(c) != 'Mn')))
gedr = gedr[["EDR", "EDR_1", "geometry"]]

gedr.to_file(
    os.path.join(
        datadir,
        "sp_edr.shp"
    ),
    encoding="utf-8"
)
