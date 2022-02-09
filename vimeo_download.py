# Downloads a mp4 video from vimeo.com

import requests
import base64
import re
from tqdm import tqdm


# Open a video in the browser, open the Network Dev Tools tab, play the video and find 'master.json' in the Network connections list
master_json_url = 'https://87vod-adaptive.akamaized.net/.../master.json?query_string_ranges=1&base64_init=1'


def get_stream(stream_type):
    resp = requests.get(master_json_url)
    content = resp.json()

    # == Read
    updir_count = content['base_url'].count('..')
    m = re.search(f'^(.+/)([^/]+/){{{updir_count}}}[^/]+$', master_json_url)
    if not m:
        print('error no matching base_url')
        exit()
    base_url = m.groups()[0]
    
    heights = [(i, d['height']) for (i, d) in enumerate(content['video'])]
    idx, _ = max(heights, key=lambda item: item[1])

    video = content[stream_type][idx]
    stream_base_url = video['base_url']

    updir_count = stream_base_url.count('..')
    m = re.search(f'^(.+/)([^/]+/){{{updir_count}}}[^/]*$', base_url)
    if not m:
        print('error no matching stream base_url')
        exit()
    base_url = m.groups()[0]

    stream_base_url = stream_base_url.replace('../', '')
    video_base_url = base_url + stream_base_url
    print('base url:', video_base_url)

    # == Save
    print(video['id'])

    filename = stream_type + '_%s.mp4' % video['id']
    print('saving to %s' % filename)

    out_file = open(filename, 'wb')

    init_segment = base64.b64decode(video['init_segment'])
    out_file.write(init_segment)

    for segment in tqdm(video['segments']):
        segment_url = video_base_url + segment['url']
        resp = requests.get(segment_url, stream=True)
        if resp.status_code != 200:
            print('not 200!')
            print(resp)
            print(segment_url)
            break
        for chunk in resp:
            out_file.write(chunk)

    out_file.flush()
    out_file.close()


# ---------
get_stream('video')
get_stream('audio')
