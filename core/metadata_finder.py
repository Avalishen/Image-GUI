from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS


def convert_to_degrees(value):

    degrees = value[0]
    minutes = value[1]
    seconds = value[2]

    return degrees + (minutes / 60.0) + (seconds / 3600.0)


def get_gps_data(image_path: str):
    """Извлекает геоданные из изображения"""

    try:
        image = Image.open(image_path)
        exif_data = image.getexif()

        if not exif_data:
            return {"success": False, "message": "Метаданные отсутствуют"}

        gps_info = exif_data.get_ifd(0x8825)

        if not gps_info:
            return {"success": False, "message": "Геоданные отсутствуют"}

        result = {
            "success": True,
            "raw_data": dict(gps_info)
        }

        if 2 in gps_info and 1 in gps_info:
            lat = convert_to_degrees(gps_info[2])
            if gps_info[1] == "S":
                lat = -lat
            result["latitude"] = lat

            lat_deg = float(gps_info[2][0])
            lat_min = float(gps_info[2][1])
            lat_sec = float(gps_info[2][2])
            result["latitude_dms"] = f"{lat_deg}° {lat_min}' {lat_sec:.2f}\""

        if 4 in gps_info and 3 in gps_info:
            lon = convert_to_degrees(gps_info[4])
            if gps_info[3] == 'W':
                lon = -lon
            result["longitude"] = lon

            lon_deg = float(gps_info[4][0])
            lon_min = float(gps_info[4][1])
            lon_sec = float(gps_info[4][2])
            result["longitude_dms"] = f"{lon_deg}° {lon_min}' {lon_sec:.2f}\""

        if 6 in gps_info:
            result["altitude"] = float(gps_info[6])

        if 29 in gps_info:
            result["date"] = gps_info[29]

        if 7 in gps_info:
            hours = int(gps_info[7][0])
            minutes = int(gps_info[7][1])
            seconds = float(gps_info[7][2])
            result["time"] = f"{hours}:{minutes}:{seconds:.2f}"

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

