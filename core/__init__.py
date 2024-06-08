from __future__ import absolute_import, unicode_literals

# 導入 Celery 應用
from .celery import app as celery_app

__all__ = ('celery_app',)
