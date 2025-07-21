import pandas as pd
import folium
import geopandas as gpd
import geoplot
import matplotlib.pyplot as plt

m = folium.Map(location=[35.6828387, 139.7594549], zoom_start=14)

# マーカーを追加
folium.Marker(
    location=[35.6828387, 139.7594549],
    popup="東京タワー",
    icon=folium.Icon(icon="star", color="red")
).add_to(m)
# m.save("./BasicLanguage/Python/marker_map.html")

# shpデータ取得を取得して、geometry

# 全世界の地図データ取得
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
world = gpd.read_file(url)
print(world.head())
print(world.columns)
world.plot(column='SOVEREIGNT', cmap='viridis', edgecolor='white', linewidth=1.0, figsize=(10, 10))
plt.show()
world.to_file("./BasicLanguage/Python/world_map.png")

# タイトルと表示
plt.title('World Map Colored by Population Density')
plt.show()

df = pd.DataFrame(
    {
        "City": ["Buenos Aires", "Brasilia", "Santiago", "Bogota", "Caracas"],
        "Country": ["Argentina", "Brazil", "Chile", "Colombia", "Venezuela"],
        "Latitude": [-34.58, -15.78, -33.45, 4.60, 10.48],
        "Longitude": [-58.66, -47.91, -70.66, -74.08, -66.86],
    }
)

gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.Longitude, df.Latitude), crs="EPSG:4326"
)
#print(gdf.head())

# We restrict to South America.
ax = world.clip([-90, -55, -25, 15]).plot(color="white", edgecolor="black")
gdf.plot(ax=ax, color="red")
plt.title("South American Continent")
plt.show()