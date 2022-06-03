import base64

from django.core.files.base import ContentFile


def base64ToFile(base):
    format, filestr = base.split(';base64,')
    ext = format.split('/')[-1]
    data = ContentFile(base64.b64decode(filestr), name='temp.' + ext)
    return {'data': data, 'ext': ext}
