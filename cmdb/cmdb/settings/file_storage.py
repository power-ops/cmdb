# from django.core.files.base import ContentFile
# from django.core.files.storage import default_storage
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
import time
import random


# https://docs.djangoproject.com/en/3.0/ref/settings/#std:setting-DEFAULT_FILE_STORAGE
# DEFAULT_FILE_STORAGE =[]


class FileStorage(FileSystemStorage):
    def __init__(self, location=settings.MEDIA_ROOT, base_url=settings.MEDIA_URL):
        super(FileStorage, self).__init__(location, base_url)

    def _save(self, name, content):
        ext = os.path.splitext(name)
        fn = time.strftime('%Y%m%d%H%M%S')
        yearmonth = time.strftime('%Y%m')
        day = time.strftime('%d')
        fn = fn + '_%d' % random.randint(10000, 99999)
        name = os.path.join(self.location, yearmonth, day, ext[0] + "_" + fn + ext[1])
        return super(FileStorage, self)._save(name, content)
