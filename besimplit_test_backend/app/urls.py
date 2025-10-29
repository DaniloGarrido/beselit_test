from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, task_list, create_task, toggle_task, delete_task, edit_task, get_task_fragment, create_task_modal, edit_task_modal, delete_task_modal

router = DefaultRouter()
router.register(r'tasks', TaskViewSet)
# Rutas para htmx 
htmx_urlpatterns = [
    path('', task_list, name='task_list'),
    path('tasks/', task_list, name='task_list_htmx'),
    path('tasks/create-modal/', create_task_modal, name='create_task_modal'),
    path('tasks/<int:task_id>/edit-modal/', edit_task_modal, name='edit_task_modal'),
    path('tasks/<int:task_id>/delete-modal/', delete_task_modal, name='delete_task_modal'),
    path('tasks/create/', create_task, name='create_task'),
    path('tasks/<int:task_id>/toggle/', toggle_task, name='toggle_task'),
    path('tasks/<int:task_id>/delete/', delete_task, name='delete_task'),
    path('tasks/<int:task_id>/edit/', edit_task, name='edit_task'),
    path('tasks/<int:task_id>/', get_task_fragment, name='get_task_fragment'),
]
# Rutas para la API
api_urlpatterns = [
    path('api/', include(router.urls)),
]

urlpatterns = htmx_urlpatterns + api_urlpatterns