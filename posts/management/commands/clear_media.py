from django.core.management.base import BaseCommand
from posts.models import PostMedia


class Command(BaseCommand):
    help = "Delete all PostMedia records (one-time cleanup for Cloudinary)"

    def handle(self, *args, **kwargs):
        count = PostMedia.objects.count()
        PostMedia.objects.all().delete()
        self.stdout.write(
            self.style.SUCCESS(f"Deleted {count} PostMedia records")
        )
