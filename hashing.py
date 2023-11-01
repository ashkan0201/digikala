import hashlib

def calculate_md5(string):
    
    md5_hash = hashlib.md5()
    md5_hash.update(string.encode('utf-8'))
    md5_hashed_string = md5_hash.hexdigest()

    return md5_hashed_string
