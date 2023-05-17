from measurements.utils import import_from_csv
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Import danych z pliku csv."

    def add_arguments(self, parser):
        parser.add_argument("file_name", type=str, help="nazwa pliku csv")

    def handle(self, *args, **options):
        n = options["file_name"]

        print(import_from_csv(n))
