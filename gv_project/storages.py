from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage, SpooledTemporaryFile
import os

class MediaStorage(S3Boto3Storage):
    
    location = settings.AWS_MEDIA_LOCATION
    file_overwrite = False
    
    def _save_content(self, obj, content, parameters):
        
        content.seek(0, os.SEEK_SET)
        content_autoclose = SpooledTemporaryFile()
        content_autoclose.write(content.read())
        super(MediaStorage, self)._save_content(obj, content_autoclose, parameters)
        
        if not content_autoclose.closed:
            content_autoclose.close()