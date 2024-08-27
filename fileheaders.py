import re

FILE_HEADER_MAPPING = {
    b'\xFF\xD8\xFF': '.jpeg',
    b'\x89PNG\r\n\x1a\n': '.png',
    b'GIF87a': '.gif',
    b'GIF89a': '.gif',
    b'\x50\x4B\x03\x04': '.zip',
    b'\x42\x4D': '.bmp',
    b'\x4D\x4D\x00\x2A': '.tiff',
    b'\x00\x00\x00 ftyp': '.mp4',
    b'Rar!\x1a\x07\x01\x00': '.rar',
    b'PK\x03\x04\x14\x00\x06\x00': '.docx',
    b'PK\x03\x04\n\x00\x00\x00': '.xlsx',
    b'\xef\xbb\xbfUPE |': '.csv',
    b'%PDF-1.7': '.pdf',
}


if __name__ == '__main__':
    ori_name = "【高清剧集网发布 www.DDHDTV.com】唐朝诡事录之西行[全40集][国语音轨+简繁英字幕].2024.1080p.WEB-DL.DDP5.1.H264-ParkTV"
    replaced_text = re.sub("^【?[\u4e00-\u9fa5|a-zA-Z|0-9|\s]+(?:www\.)?[\w\-]+(?:\.[\w\-]+)+[\w\-\._~:/?#[\]@!$&'()*+,;=]*】?", "", ori_name)

    print(replaced_text)
