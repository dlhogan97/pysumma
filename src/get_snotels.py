from metloom.pointdata import SnotelPointData
import geopandas as gpd
import os
# Download a shapefile of the state of Washington
gdf = gpd.read_file('../data/washington.geojson', driver='GeoJSON')

# Set variables
variables = [SnotelPointData.ALLOWED_VARIABLES.PRECIPITATIONACCUM, SnotelPointData.ALLOWED_VARIABLES.TEMP, 
             SnotelPointData.ALLOWED_VARIABLES.SWE, SnotelPointData.ALLOWED_VARIABLES.SNOWDEPTH]

# Get the Snotel data
if os.path.exists('../data/snotel_points.geojson'):
    snotel_point_gdf = gpd.read_file('../data/snotel_points.geojson', driver='GeoJSON')
else:
    points = SnotelPointData.points_from_geometry(gdf, variables)
    # Convert to a geopandas dataframe
    snotel_point_gdf = points.to_dataframe()
    # add the crs
    snotel_point_gdf.crs = "EPSG:4326"
    # Save to data folder if needed or open the file
    snotel_point_gdf.to_file('../data/snotel_points.geojson', driver='GeoJSON')

# Filter to list of desired snotels
snotel_list = ["Waterhole", "Wells Creek", "Stevens Pass", "Olallie Meadows", "Stampede Pass", "Morse Lake", "Paradise", "White Pass E.S."]
try:
    sel_snotel_point_gdf = snotel_point_gdf[snotel_point_gdf['name'].isin(snotel_list)]
    sel_snotel_point_gdf.to_file('../data/sel_snotel_points.geojson', driver='GeoJSON')
except KeyError:
    print('Check the names of the Snotel sites.')

