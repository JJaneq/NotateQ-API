from .models import Files

from celery import shared_task

from django.utils import timezone


import logging

logger = logging.getLogger(__name__)
@shared_task
def check_remove_files():
    logger.info("Checking for files to remove...")
    files = Files.objects.all()
    if not files.exists():
        print("No files to check.")
        return
    for file in files:
        if file.delete_time is not None:
            if file.delete_time <= timezone.now():
                file.delete()