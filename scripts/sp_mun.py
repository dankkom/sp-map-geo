import geopandas as gpd
import unicodedata


# source: ftp://geoftp.ibge.gov.br/organizacao_do_territorio/malhas_territoriais/malhas_municipais/municipio_2015/UFs/SP/sp_municipios.zip


g = gpd.read_file("sp_municipios/35MUE250GC_SIR.shp", encoding="utf-8")

g = g.assign(
    NM_MUNICIP_NOACCENT=g["NM_MUNICIP"].apply(
        lambda s: ''.join(c for c in unicodedata.normalize('NFD', s)
                          if unicodedata.category(c) != 'Mn')
    )
)
g = g[["CD_GEOCMU", "NM_MUNICIP", "NM_MUNICIP_NOACCENT", "geometry"]]

g.to_file("sp_municipios/sp_mun.shp", encoding="utf-8")
