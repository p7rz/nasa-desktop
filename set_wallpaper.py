from logging import error
import wallpaper_utility
from plyer import notification
from random import choice


from parser import download_image, get_data, data_by_count, get_date, get_hdurl, get_media_type, get_url, is_connected
#write a fix for the date clusterfuck
def wallpaper_change_procedure():
    r = get_data(wallpaper_utility.APOD_API_KEY)
    print(r)
    url = get_url(r)
    print(url)
    media_type = get_media_type(r)
    if media_type == 'image':
        hd_url = get_hdurl(r) or get_working_image()
    else:
        hd_url = get_working_image()
    print(hd_url)
    wallpaper_img_path = download_image(hd_url, get_date(r))
    print(wallpaper_img_path)
    wallpaper_utility.changeBG(wallpaper_img_path)
    notification.notify(title=wallpaper_utility.SERVICE_NAME, message="Wallpaper changed", timeout=30)

def get_working_image():
    response_array = data_by_count(wallpaper_utility.APOD_API_KEY)
    print('Digging through archives')
    archive_response_list = []
    #print(response_array)

    for res in  response_array:
        try:
            hdurl = get_hdurl(res)
            archive_response_list.append(hdurl)
        except:
            pass
    
    if len(archive_response_list) == 0:
        notification.notify(title=wallpaper_utility.SERVICE_NAME, message='Archive retrival failed', timeout=30)
        return error
    else:
        return choice(archive_response_list)
    
if __name__ == "__main__":
    print("Program starting")
    if not is_connected():
        print("Internet connection failed")
        notification.notify(title=wallpaper_utility.SERVICE_NAME, message='Internet connection failed')
    else:
        print('Connected to internet')
        wallpaper_change_procedure()