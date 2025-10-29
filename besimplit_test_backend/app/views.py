from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, QueryDict, HttpResponseBadRequest
from rest_framework import viewsets
from .models import Task
from .serializers import TaskSerializer
from django.views.decorators.http import require_http_methods
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt

#Vistas para HTMX
# Vista para la página principal
def task_list(request):
    tasks = Task.objects.all()
    total_tasks_count = Task.objects.count()
    status_filter = request.GET.get('status')
    search_query = request.GET.get('q')

    if status_filter == 'completed':
        tasks = tasks.filter(completed=True)
    elif status_filter == 'pending':
        tasks = tasks.filter(completed=False)

    if search_query:
        tasks = tasks.filter(title__icontains=search_query) | tasks.filter(description__icontains=search_query)

    tasks_count = tasks.count()
    if request.headers.get('HX-Request'):
        if request.headers.get('HX-Target-List'):
            return render(request, 'app/task_list_content.html', {'tasks': tasks})
        print(f"HTMX request received. Tasks: {tasks}")
        return render(request, 'app/task_management_section.html', {'tasks': tasks, 'tasks_count': tasks_count, 'total_tasks_count': total_tasks_count, 'status_filter': status_filter, 'search_query': search_query})
    return render(request, 'app/index.html', {'tasks': tasks, 'tasks_count': tasks_count, 'total_tasks_count': total_tasks_count, 'status_filter': status_filter, 'search_query': search_query})

# Vista HTMX para abrir el modal de crear tarea
@require_http_methods(['GET'])
def create_task_modal(request):
    return render(request, 'app/modal_base.html', {
        'content': render(request, 'app/create_task_form.html').content.decode()
    })

# Vista HTMX para abrir el modal de editar tarea
@require_http_methods(['GET'])
def edit_task_modal(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    context = {
        'task': task
    }
    return render(request, 'app/modal_base.html', {
        'modal_title': 'Editar Tarea',
        'content': render_to_string('app/task_edit_form.html', context, request=request)
    })

def delete_task_modal(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    context = {
        'task': task
    }
    return render(request, 'app/modal_base.html', {
        'modal_title': 'Confirmar Eliminación',
        'content': render_to_string('app/delete_confirmation_modal.html', context, request=request)
    })

# Vista HTMX para crear tarea
@require_http_methods(['POST'])
def create_task(request):
    title = request.POST.get('title')
    description = request.POST.get('description')

    if not title or not description:
        response = render(request, 'app/create_task_form.html', {'error': "El título y la descripción no pueden estar vacíos.", 'title': title, 'description': description})
        response['HX-Retarget'] = '#modal-body'
        response['HX-Reswap'] = 'innerHTML'
        return response

    task = Task.objects.create(title=title, description=description)
    response = render(request, 'app/task_fragment.html', {'task': task})
    response['HX-Trigger'] = 'taskCreated, closeModal'
    return response

# Vista HTMX para obtener un fragmento de tarea individual
@require_http_methods(['GET'])
def get_task_fragment(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    return render(request, 'app/task_fragment.html', {'task': task})

# Vista HTMX para editar tarea
@require_http_methods(['GET', 'PUT'])
def edit_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    if request.method == 'GET':
        return render(request, 'app/task_edit_form.html', {'task': task})
    elif request.method == 'PUT':
        data = QueryDict(request.body).dict()
        title = data.get('title')
        description = data.get('description')

        if not title or not description:
            response = render(request, 'app/task_edit_form.html', {'task': task, 'error': "El título y la descripción no pueden estar vacíos.", 'title': title, 'description': description})
            response['HX-Retarget'] = '#modal-body'
            response['HX-Reswap'] = 'innerHTML'
            return response
        task.title = title
        task.description = description
        task.save()
        response = render(request, 'app/task_fragment.html', {'task': task})
        response['HX-Trigger'] = 'taskUpdated, closeModal'
        return response

# Vista HTMX para marcar tarea como completada pendiente
@require_http_methods(['PUT'])
def toggle_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = not task.completed
    task.save()
    return render(request, 'app/task_fragment.html', {'task': task})

# Vista HTMX para eliminar tarea
@require_http_methods(['DELETE'])
def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.delete()
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'taskDeleted, closeModal'
    return response


# ViewSet para la API RESTful
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
