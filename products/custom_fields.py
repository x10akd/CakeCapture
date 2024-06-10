import boto3
from PIL import Image
import io
from django.db import models
from django.core.files.base import ContentFile

s3 = boto3.client('s3')

class CompressedImageField(models.ImageField):

    def __init__(self, *args, **kwargs):
        self.quality = kwargs.pop('quality', 85)
        super().__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        file = super().pre_save(model_instance, add)
        if file and hasattr(file, 'file'):
            # 打开图像并压缩
            image = Image.open(file)
            buffer = io.BytesIO()
            image.save(buffer, 'JPEG', quality=self.quality)
            buffer.seek(0)
            # 上传到S3
            s3.upload_fileobj(buffer, 'cakecapture', file.name, ExtraArgs={'ContentType': 'image/jpeg'})
            # 设置文件字段
            model_instance.__dict__[self.name] = file.name
        return file