def upload_file(path: str, file):
    pass

def download_file(path: str) -> bytes:
    with open(path, 'rb') as f:
        return f.read()
