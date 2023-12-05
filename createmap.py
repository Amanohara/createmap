from osgeo import gdal, ogr, osr
import os
import json
from pyproj import CRS, Transformer
from shapely.geometry import shape
"""
平面直角座標系に存在するDXFをGeoJSONに変換して、
XYZ tilesの地理院地図（標準地図）上にプロットする
"""
def main(dammy, input, zahyo):
    # DXFの座標系を認識させる
    dxf_epsg = heimenchokkaku_no(zahyo)
    # DXFからGeoJSONに変換
    dxf2geojson(input, dxf_epsg, 'output.geojson')
    # 作成したGeoJSONの四隅の座標を抽出する（地理院タイル取得用）
    map_minx, map_maxx, map_miny, map_maxy = getmaprange('output,geojson', dxf_epsg)
    # 地理院タイルを取得してGeoTiffを作成する
    get_gsimap(map_minx, map_maxx, map_miny, map_maxy)
    # 地理院地図とGeoJSONを重ねた画像を作成する

    pass

def heimenchokkaku_no(zahyo):
    # 座標系からEPSGコードを取得
    heimen_epsg={"1":6669,"2":6670,"3":6671,"4":6672,"5":6673,"6":6674,
                    "7":6675,"8":6676,"9":6677,"10":6678,"11":6679,"12":6680,
                    "13":6681,"14":6682,"15":6683,"16":6684,"17":6685,"18":6686,"19":6687}
    epsg = heimen_epsg[int(zahyo)]
    return epsg


def dxf2geojson(input_dxf:str, zahyo:int, output_file:str):
    # DXFからGeoJSONに変換
    # DXFファイルを読み込む
    driver = ogr.GetDriverByName('DXF')
    input_data = driver.Open(input_dxf, 0) # 0 means read-only

    # 出力ファイル用のGeoJSONドライバを取得
    output_driver = ogr.GetDriverByName('GeoJSON')

    # 出力ファイルが既に存在する場合は削除
    if os.path.exists(output_file):
        output_driver.DeleteDataSource(output_file)

    # 新しいGeoJSONファイルを作成
    output_data = output_driver.CreateDataSource(output_file)
    output_layer = output_data.CreateLayer('layer', geom_type=ogr.wkbPoint)

    # EPSG:6677の座標系を設定
    source_srs = osr.SpatialReference()
    source_srs.ImportFromEPSG(int(zahyo))
    output_layer.SetSpatialRef(source_srs)

    # フィーチャをコピー
    in_layer = input_data.GetLayer()
    for feature in in_layer:
        output_layer.CreateFeature(feature)
    pass


def getmaprange(input, epsg):
    # GeoJSONを平面直角座標系から緯度経度にEPSG:4326に変換して四隅の座標を求める（地理院マップ用）
    with open('input', 'r') as f:
        data = json.load(f)
    source_crs = CRS("EPSG:6677")
    target_crs = CRS("EPSG:4326")
    transformer = Transformer.from_crs(source_crs, target_crs)
    for feature in data['features']:
        geometry = shape(feature['geometry'])
        transformed_coords = [transformer.transform(*coord) for coord in geometry.coords]
    minx, miny = min(transformed_coords, key=lambda coord: (coord[0], coord[1]))
    maxx, maxy = max(transformed_coords, key=lambda coord: (coord[0], coord[1]))
    # ジオメトリの四隅の座標が分かったので、適当に加算する。
    # 現時点では1秒（40m）分の幅を加える。1秒は0.0167足せばよい
    map_minx = minx + 0.0167
    map_miny = miny + 0.0167
    map_maxx = maxx + 0.0167
    map_maxy = maxy + 0.0167
    return map_minx, map_maxx, map_miny, map_maxy

def get_gsimap(lon1, lon2, lat1, lat2):

    pass

def merge(img_file):
    pass