from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.adventure_index,
        name='adventures'
    ),
    path(
        'adventures/add',
        views.adventure_add,
        name='adventure_add'
    ),
    path(
        'adventures/edit/<int:id>',
        views.adventure_edit,
        name='adventure_edit'
    ),
    path(
        'adventures/delete/<int:id>',
        views.adventure_delete,
        name='adventure_delete'
    ),
    path(
        'missions/add/<int:adventure_id>',
        views.mission_add,
        name='mission_add'
    ),
    path(
        'missions/edit/<int:id>',
        views.mission_edit,
        name='mission_edit'
    ),
    path(
        'missions/delete/<int:id>',
        views.mission_delete,
        name='mission_delete'
    ),
    path(
        'submissions/add/<int:parent_id>/<int:adventure_id>',
        views.submission_add,
        name='submission_add'
    )
]
