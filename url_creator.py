import requests, webbrowser, json
def urlcreator(path):
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}
    img_file = open(path, 'rb')
    header['Content-Type'] = 'multipart/form-data'
    files = {'file': ('Image.jpg', img_file, 'image/jpeg', {'Expires': '10'}) }
    res = requests.post('https://pasteboard.co/upload', files=files)
    uploaded_image_name = json.loads(res.content.decode('utf-8'))['fileName']
    url = 'https://gcdnb.pbrd.co/images/'+uploaded_image_name
    return url
