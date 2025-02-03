import os
import subprocess

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    """
    Запуск Liquibase миграций
    """

    help = 'Запуск Liquibase миграций'

    def handle(self, *args, **kwargs):
        """
        Запуск Liquibase с указанными параметрами подключения к БД PostgreSQL.
        Проверяет наличие необходимых переменных окружения.
        """

        if not all([
            os.environ.get("POSTGRES_USER"),
            os.environ.get("POSTGRES_PASSWORD"),
            os.environ.get("POSTGRES_DATABASE"),
            os.environ.get("POSTGRES_HOST_DOCKER", "db"),
            os.environ.get("POSTGRES_PORT", "5432")
        ]):
            self.stderr.write(self.style.ERROR('Необходимо установить переменные окружения для подключения к PostgreSQL'))
            return

        db_user = os.environ.get("POSTGRES_USER")
        db_password = os.environ.get("POSTGRES_PASSWORD")
        db_name = os.environ.get("POSTGRES_DATABASE")
        db_host = os.environ.get("POSTGRES_HOST_DOCKER", "db")
        db_port = os.environ.get("POSTGRES_PORT", "5432")

        db_url = f"jdbc:postgresql://{db_host}:{db_port}/{db_name}"

        liquibase_command = [
            'liquibase',
            f'--driver=org.postgresql.Driver',
            f'--classpath=resources/postgresql-42.6.2.jar',
            f'--url={db_url}',
            f'--username={db_user}',
            f'--password={db_password}',
            f'--changeLogFile=resources/changelog.xml',
            'update'
        ]

        print(f"Liquibase command: {' '.join(liquibase_command)}")

        try:
            result = subprocess.run(liquibase_command, capture_output=True, text=True, check=True)

            if result.returncode == 0:
                self.stdout.write(self.style.SUCCESS('Миграции успешно применены'))
                self.stdout.write(result.stdout)
            else:
                self.stderr.write(self.style.ERROR('Ошибка миграций'))
                self.stderr.write(result.stderr)

        except subprocess.CalledProcessError as e:
            self.stderr.write(self.style.ERROR(f'Ошибка: {str(e)}'))
            self.stderr.write(f"Return code: {e.returncode}")
            self.stderr.write(e.stderr)

        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Ошибка: {str(e)}'))
