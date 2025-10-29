from django.core.management.base import BaseCommand
from app.models import Task

class Command(BaseCommand):
    help = 'Carga 10 tareas iniciales en la base de datos.'

    def handle(self, *args, **kwargs):
        if Task.objects.count() == 0:
            for i in range(1, 11):
                Task.objects.create(title=f'Tarea Inicial {i}', description=f'Descripción de la tarea inicial {i}.', completed=False)
            self.stdout.write(self.style.SUCCESS('Se han cargado 10 tareas iniciales exitosamente.'))
        else:
            self.stdout.write(self.style.WARNING('Ya existen tareas en la base de datos. No se cargaron tareas iniciales.'))