from pydantic import BaseModel

class DnListModel(BaseModel):
    codename : str
    oem : str
    device : str
    last_updated : int
    version : str
    changelog_url : str

class variantDataModel(BaseModel):
    maintainer: str
    oem: str
    device: str
    filename: str
    download: str
    timestamp: int
    md5: str
    sha256: str
    size: int
    version: str
    buildtype: str
    forum: str
    gapps: str
    firmware:str
    modem: str
    bootloader: str
    recovery: str
    paypal: str
    telegram: str
    dt: str
    "common-dt"
    kernel: str
