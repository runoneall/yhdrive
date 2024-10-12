import os
import requests, hashlib
from collections import OrderedDict

def Upload(FileContent:bytes, Token:str) -> dict:

    # Get Info
    uTokenUrl = "https://chat-go.jwzhd.com/v1/misc/qiniu-token2"
    uToken = requests.get(
        uTokenUrl, 
        headers={"token": Token}
    ).json()["data"]["token"]
    uHostUrl = f"https://api.qiniu.com/v4/query?ak={uToken.split(':')[0]}&bucket=chat68-file"
    uHost = requests.get(uHostUrl).json()["hosts"][0]["up"]["domains"][0]

    # Upload File
    FileMd5 = hashlib.md5(FileContent)
    Key = FileMd5.hexdigest()
    Params = OrderedDict([
        ("token", (None, uToken)),
        ("key", (None, Key)),
        ("file", (None, FileContent))
    ])
    RepJson = requests.post("https://"+uHost, files=Params).json()

    # Return Result
    return RepJson

def Download(Key:str) -> bytes:
    DownloadLink = f"https://chat-file.jwznb.com/{Key}"
    Headers = {"referer":"http://myapp.jwznb.com"}
    RepContent = requests.get(DownloadLink, headers=Headers)
    return RepContent.content