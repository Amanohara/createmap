from osgeo import gdal, ogr, osr
import os
"""
平面直角座標系に存在するDXFをGeoJSONに変換して、
XYZ tilesの地理院地図（標準地図）上にプロットする
"""
def main(dammy, input, zahyo):
    # DXFの座標系を認識させる
    dxf_epsg = heimenchokkaku_no(zahyo)
    # DXFからGeoJSONに変換
    dxf2geojson(input, str(dxf_epsg), 'output.geojson')
    # 作成したGeoJSONの四隅の座標を抽出する（地理院タイル取得用）

    # 地理院タイルを取得してGeoTiffを作成する

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


def zahyo_conv(input, zahyo):
    # 平面直角座標系からEPSG:4326に変換する（地理院マップ用）

    pass

def get_gsimap(lat1, lat2, lon1, lon2):
    pass

def merge(img_file):
    pass