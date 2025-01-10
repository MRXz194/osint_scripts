from PIL import Image
from exif import Image as ExifImage
import folium
import sys
import webbrowser
import os

def convert_to_degrees(value):
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)

def get_gps_coords(image_path):
    try:
        with open(image_path, 'rb') as img_file:
            img = ExifImage(img_file)
            
            if not hasattr(img, 'gps_latitude') or not hasattr(img, 'gps_longitude'):
                return None, None

            lat = convert_to_degrees(img.gps_latitude)
            lon = convert_to_degrees(img.gps_longitude)

            if img.gps_latitude_ref == "S":
                lat = -lat
            if img.gps_longitude_ref == "W":
                lon = -lon

            return lat, lon
    except Exception as e:
        print(f"Error: {str(e)}")
        return None, None

def create_map(latitude, longitude, image_path):
    m = folium.Map(location=[latitude, longitude], zoom_start=15)
    
    folium.Marker(
        [latitude, longitude],
        popup=f"Image Location<br>{os.path.basename(image_path)}",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)
    
    # Save map
    map_path = "image_location_map.html"
    m.save(map_path)
    return map_path

def main():
    if len(sys.argv) != 2:
        print("Usage: python img_detector.py <image_path>")
        return

    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Error: Image file '{image_path}' not found.")
        return

    print(f"Processing image: {image_path}")
    
    # Get GPS
    latitude, longitude = get_gps_coords(image_path)
    
    if latitude is None or longitude is None:
        print("No GPS data found.")
        return
    
    print(f"GPS Coordinates found:")
    print(f"Latitude: {latitude}")
    print(f"Longitude: {longitude}")
    
    # Create and open map
    map_path = create_map(latitude, longitude, image_path)
    print(f"\nCreated map at: {map_path}")
    print("Opening map ...")
    webbrowser.open(map_path)

if __name__ == "__main__":
    main()


#Pillow==10.1.0
#exif==1.6.0
#folium==0.15.0
# run script : python img-detector.py <image_path>
