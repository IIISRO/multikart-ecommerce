from django.core.management.base import BaseCommand
from core.models import BlockedIp
class Command(BaseCommand):
    help = 'Block ip'

    def add_arguments(self, parser):
        parser.add_argument('ip', type=str, help='Block ip')

    def handle(self, *args, **kwargs):
        ip = kwargs['ip']
        BlockedIp.objects.create(ip=ip)


