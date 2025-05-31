import hashlib

token = 'CVFedarGsdfvtrshDARFBGstrf'

async def verify(mac,ap_hash,time):

    hashstr = mac +'!'+ token +'@'+ time
    newhash = hashlib.sha256(hashstr.encode('utf-8')).hexdigest()

    if ap_hash == newhash:
        return True
    else:
        return False