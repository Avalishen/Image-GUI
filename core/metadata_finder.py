from PIL import Image
from PIL.ExifTags import TAGS


def convert_to_degrees(value):
    """Преобразует координаты из формата (градусы, минуты, секунды) в десятичные градусы"""
    degrees = value[0]
    minutes = value[1]
    seconds = value[2]
    return degrees + (minutes / 60.0) + (seconds / 3600.0)


def get_all_metadata(image_path: str):
    """Извлекает все метаданные из изображения"""

    try:
        image = Image.open(image_path)
        exif_data = image.getexif()

        if not exif_data:
            return {"success": False, "message": "Метаданные отсутствуют"}

        result = {"success": True}

        result["filename"] = image_path.split("/")[-1].split("\\")[-1]
        result["format"] = image.format
        result["mode"] = image.mode
        result["size"] = f"{image.size[0]}x{image.size[1]}"

        exif_info = image.getexif()
        exif_dict = {}

        for tag_id, value in exif_info.items():
            tag_name = TAGS.get(tag_id, tag_id)
            exif_dict[tag_name] = value

        result["exif"] = exif_dict

        camera_info = {}
        if "Make" in exif_dict:
            camera_info["make"] = str(exif_dict["Make"])
        if "Model" in exif_dict:
            camera_info["model"] = str(exif_dict["Model"])
        if "Software" in exif_dict:
            camera_info["software"] = str(exif_dict["Software"])

        if camera_info:
            result["camera"] = camera_info

        # Настройки съёмки
        shooting_settings = {}
        if "FNumber" in exif_dict:
            shooting_settings["aperture"] = str(exif_dict["FNumber"])
        if "ExposureTime" in exif_dict:
            shooting_settings["exposure"] = str(exif_dict["ExposureTime"])
        if "ISOSpeedRatings" in exif_dict:
            shooting_settings["iso"] = str(exif_dict["ISOSpeedRatings"])
        if "FocalLength" in exif_dict:
            shooting_settings["focal_length"] = str(exif_dict["FocalLength"])
        if "Flash" in exif_dict:
            shooting_settings["flash"] = str(exif_dict["Flash"])

        if shooting_settings:
            result["shooting"] = shooting_settings

        if "DateTimeOriginal" in exif_dict:
            result["datetime"] = str(exif_dict["DateTimeOriginal"])
        elif "DateTime" in exif_dict:
            result["datetime"] = str(exif_dict["DateTime"])

        gps_info = exif_data.get_ifd(0x8825)

        if gps_info:
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
                result["date"] = str(gps_info[29])

            if 7 in gps_info:
                hours = int(gps_info[7][0])
                minutes = int(gps_info[7][1])
                seconds = float(gps_info[7][2])
                result["time"] = f"{hours}:{minutes}:{seconds:.2f}"

        other_info = {}
        if "Orientation" in exif_dict:
            orientation_map = {
                1: "Горизонтально",
                3: "Повернуто на 180°",
                6: "Повернуто на 90° по часовой",
                8: "Повернуто на 90° против часовой"
            }
            other_info["orientation"] = orientation_map.get(exif_dict["Orientation"], str(exif_dict["Orientation"]))

        if "ColorSpace" in exif_dict:
            color_space_map = {
                1: "sRGB",
                65535: "Uncalibrated"
            }
            other_info["color_space"] = color_space_map.get(exif_dict["ColorSpace"], str(exif_dict["ColorSpace"]))

        if "Copyright" in exif_dict:
            other_info["copyright"] = str(exif_dict["Copyright"])

        if "Artist" in exif_dict:
            other_info["artist"] = str(exif_dict["Artist"])

        if other_info:
            result["other"] = other_info

        return result

    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"success": False, "error": str(e)}

def remove_metadata(image_path: str, output_path: str):

    try:
        image = Image.open(image_path)

        image_data = list(image.getdata())

        image_without_exif = Image.new(image.mode, image.size)
        image_without_exif.putdata(image_data)
        image_without_exif.save(output_path)

        return {"success": True, "message": "Все метаданные успешно удалены", "output_path": output_path}

    except FileNotFoundError:
        return {"success": False, "error": "Файл не найден"}

    except Exception as e:
        return {"success": False, "error": str(e)}