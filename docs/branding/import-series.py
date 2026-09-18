"""One-time import of checksum-pinned artwork sources from the companion repository."""
from pathlib import Path
from urllib.request import urlopen
import hashlib
BASE='https://raw.githubusercontent.com/lhfer/meoo-article-to-video/d21e7c9343ca340ea3efc09246673c3ff26ba77b/docs/branding/'
FILES={
'render.py':'3675e57a77a5e5dc8740c2cd65105a7cdece0e076292adb0022d84f365917dfe',
'source/meoo-logo.png':'f6f565b955b4b2fb294717e4b326c40c1c87123826cf174cdece5d28f79b2fa5',
'source/meoo-icon.png':'209b2c6bafe805c44c9b205778d960c5dcab083b07595b1424f8b53198ffadef',
'source/meoo-mascot.gif':'403f30881aa93a809f04c302d93b81f3f8cd85a55b89c2c6277da5da070f8bdc',
'source/meoo-mascot-poster.png':'89c7fa687feda3c303ad87f5c058672e86e697c01dab3d13e7ee330d8d822f32'}
root=Path(__file__).resolve().parent
for name,expected in FILES.items():
    with urlopen(BASE+name,timeout=30) as response:data=response.read(2_000_000)
    if hashlib.sha256(data).hexdigest()!=expected:raise ValueError(f'Checksum mismatch: {name}')
    p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
    print('Verified:',name)
