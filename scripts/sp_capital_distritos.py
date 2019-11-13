import os
import shutil
import tempfile
import urllib.request as request
import zipfile
from contextlib import closing

import geopandas as gpd

# source: http://dados.prefeitura.sp.gov.br/dataset/distritos

url = (
    "http://dados.prefeitura.sp.gov.br/dataset/"
    "af41e7c4-ae27-4bfc-9938-170151af7aee/resource/"
    "9e75c2f7-5729-4398-8a83-b4640f072b5d/download/layerdistrito.zip")
datadir = "sp_capital_distritos"
zfilename = "layerdistrito.zip"
zfile = os.path.join(datadir, zfilename)
if not os.path.exists(zfile):
    with closing(request.urlopen(url)) as r:
        with open(zfile, "wb") as f:
            shutil.copyfileobj(r, f)

with tempfile.TemporaryDirectory() as tmp:
    with zipfile.ZipFile(zfile) as zf:
        zf.extractall(path=tmp)
        g = gpd.read_file(
            os.path.join(
                tmp,
                "LAYER_DISTRITO",
                "DEINFO_DISTRITO.shp"
            ),
            encoding="utf-8"
        )

sp = g[["NOME_DIST", "SIGLA_DIST", "COD_DIST", "geometry"]]

# Correct projection
sp = sp.to_crs({"init": "epsg:4326"})

sp.to_file(
    os.path.join(
        datadir,
        "sp_capital_distritos.shp",
    ),
    encoding="utf-8"
)
