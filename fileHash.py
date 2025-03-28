import hashlib
import os
from macros import OBJECTS_DIR
def hashObj(data: bytes, type_: str='blob')->str:
    header=f'{type_}_{len(data)}\0'.encode()
    fullObj = header+data
    oID = hashlib.sha1(fullObj).hexdigest()
    path = os.path.join(OBJECTS_DIR, oID)
#     print(oID,'oid')
    with open(path, 'wb') as f:
        f.write(fullObj)


    return oID