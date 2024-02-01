import streamlink, json
import sys, requests, os
from urllib.parse import urljoin

def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))

def get_master_playlist(url):
    try:
        streams = streamlink.streams(url)
        return streams["best"].multivariant.uri
    except:
        return ""

def get_variant_playlist(url, quality="best"):
    try:
        streams = streamlink.streams(url)
        return streams[quality].url
    except:
        return ""


def main():
    f = open(sys.argv[1], "r")
    data = json.load(f)
    #backup_options = data["backup"]
    #output_type = data["output"]["type"]
    folder_name = data["output"]["folder"]
    current_dir = os.getcwd()
    folder = os.path.join(current_dir, folder_name)
    os.makedirs(folder, exist_ok=True)
    channels = data["channels"]
    for channel in channels:
        master_playlist = get_master_playlist(channel["url"])
        if master_playlist:
            channel_file_path = os.path.join(folder, channel["slug"])
            channel_file_path = channel_file_path + ".m3u8"
            r = requests.get(master_playlist)
            if r.status_code == 200:
                channel_file = open(channel_file_path, "w+")
                playlist_text = ""
                for line in r.iter_lines():
                    line = line.decode()
                    if not line.startswith("http") and not line.startswith("#"):
                        fixed_line = urljoin(r.url, line)
                        playlist_text += fixed_line
                    else:
                        playlist_text += line
                    playlist_text += "\n"
                channel_file.write(playlist_text)
            else:
                print("No available streams found for", channel["name"])
if __name__=="__main__": 
    main() 
