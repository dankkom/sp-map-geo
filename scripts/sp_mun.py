import os
import shutil
import tempfile
import unicodedata
import urllib.request as request
import zipfile
from contextlib import closing

import geopandas as gpd

# source: ftp://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2015/UFs/SP/sp_municipios.zip
url = (
    "ftp://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/"
    "malhas_municipais/municipio_2015/UFs/SP/sp_municipios.zip")
datadir = "sp_municipios"
zfilename = "sp_municipios.zip"
zfile = os.path.join(datadir, zfilename)
if not os.path.exists(zfile):
    with closing(request.urlopen(url)) as r:
        with open(zfile, "wb") as f:
            shutil.copyfileobj(r, f)

with tempfile.TemporaryDirectory() as tmp:
    with zipfile.ZipFile(zfile) as zf:
        zf.extractall(path=tmp)
        g = gpd.read_file(
            os.path.join(tmp, "35MUE250GC_SIR.shp"), encoding="utf-8")

g = g.assign(
    NM_MUNICIP_1=g["NM_MUNICIP"].apply(
        lambda s: ''.join(c for c in unicodedata.normalize('NFD', s)
                          if unicodedata.category(c) != 'Mn')
    )
)
g = g[["CD_GEOCMU", "NM_MUNICIP", "NM_MUNICIP_1", "geometry"]]
g.to_file(
    os.path.join(
        datadir,
        "sp_mun.shp"
    ),
    encoding="utf-8"
)
