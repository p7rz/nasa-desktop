import requests
import json
import os
import cv2
import socket
import random

api_count = 25

#get data form APOD site using requests
def get_data(api_key):
    raw_r = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}').text 
    r = json.loads(raw_r)
    return r

#get data by specific date
def data_by_date(api_key, date): #date fromat YYYY-MM-DD
    raw_r = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}&date={date}').text
    r = json.loads(raw_r)
    return r

#get data array
def data_by_count(api_key):
    raw_r  =requests.get(f'https://api.nasa.gov/planetary/apod?api_key={api_key}&count={api_count}').text
    r = json.loads(raw_r)
    return r

#get date, hdurl, mediatype and title api responses
def get_date(r):
    date = r['date']
    return date

def get_explaination(r):
    explaination = r['explanation']
    return explaination

def get_hdurl(r):
    hdurl = r['hdurl']
    return hdurl

def get_service_version(r): 
    service_version = r['service_version']
    return service_version

def get_media_type(r):
    media_type = r['media_type']
    return media_type

def get_title(r):
    title = r['title']
    return title

def get_url(r):
    url = r['url']
    return url

def get_thumbnail_url(r):
    thumbnail_url = r['thumbnail_url']
    return thumbnail_url

#Download the image, agent: Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0
def download_image(url, date):
    dir_path = get_absolute_path()
    full_path = os.path.join(dir_path, f'{date}.png')
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:12.0) Gecko/20100101 Firefox/12.0",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }
    if os.path.isfile(full_path):
        os.remove(full_path)

    raw_img = requests.get(url, headers).content
    with open(full_path, 'wb') as file:
        file.write(raw_img)
    return full_path

#Getting the path, if does not exist, create it
def get_absolute_path():
    picture_path = os.path.expanduser("~\\Pictures\\")
    directory = "NASAapod"
    apod_dir_path = os.path.join(picture_path, directory)

    if not os.path.isdir(apod_dir_path):
        os.makedirs(apod_dir_path)
    return os.path.abspath(apod_dir_path)

#converting image
def convert_image(path):
    norm_img_path = os.path.normpath(path)
    img_basename = os.path.basename(norm_img_path)
    path_without_extension = img_basename.split(".")[0]
    base_dir = os.path.dirname(norm_img_path)

    img = cv2.imread(path_without_extension)
    cv2.imwrite(f'{base_dir}/{path_without_extension}.png', img)

def is_connected():
    try:
        socket.create_connection(("1.1.1.1", 53))
        return True
    except OSError:
        pass
    return False