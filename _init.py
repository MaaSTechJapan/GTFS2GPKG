# %%
import os
from io import StringIO
import zipfile

import pandas as pd    
import geopandas as gpd

# %%
def gtfs2gpkg(gtfs: str):
    dfs = {}
    with zipfile.ZipFile(gtfs, 'r') as f:
        for fn in f.namelist():
            dfs[fn.split('.')[0]] = gpd.GeoDataFrame(
                pd.read_csv(StringIO(f.read(fn).decode(encoding="UTF-8"))),
                geometry=gpd.GeoSeries(),
                crs="EPSG:4326"
            )

    # stopsの処理
    dfs['stops'].set_geometry(gpd.points_from_xy(dfs['stops'].stop_lon, dfs['stops'].stop_lat, crs="EPSG:4326"), inplace=True)
    # shapesの処理
    dfs['shapes'].set_geometry(gpd.points_from_xy(dfs['shapes'].shape_pt_lon, dfs['shapes'].shape_pt_lat, crs="EPSG:4326"), inplace=True)
 
    ofn = f"{os.path.splitext(gtfs)[0]}.gpkg"
    for k, v in dfs.items():
        v.to_file(ofn, driver='GPKG', layer=k) 
    
    return(ofn)

# gtfs2gpkg("odpt-GTFS/ToeiBus-GTFS.zip")

# %%
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Create GeoPackage(GPKG) from zipeed GTFS')
    parser.add_argument('gtfs', help='Zipped GTFS File Path, e.g. Toei.zip')
    args = parser.parse_args()

    ofn = gtfs2gpkg(args.gtfs)
    
    print(ofn)