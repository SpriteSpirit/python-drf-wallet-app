import subprocess
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Запуск Liquibase миграций'

    def handle(self, *args, **kwargs):
        try:
            result = subprocess.run([
                'liquibase',
                '--defaultsFile=resources/liquibase.properties',
                'update'
            ], capture_output=True, text=True)

            if result.returncode == 0:
                self.stdout.write(self.style.SUCCESS('Миграции успешно применены'))
                self.stdout.write(result.stdout)
            else:
                self.stderr.write(self.style.ERROR('Ошибка миграций'))
                self.stderr.write(result.stderr)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка: {str(e)}'))
