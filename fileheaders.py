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