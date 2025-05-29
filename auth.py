import hashlib

token = 'CVFedarGsdfvtrshDARFBGstrf'

def verify(mac,ap_hash,time):

    str = mac +'!'+ token +'@'+ time
    hash = hashlib.sha256(str.encode('utf-8')).hexdigest()

    if ap_hash == hash:
        return True
    else:
        return False