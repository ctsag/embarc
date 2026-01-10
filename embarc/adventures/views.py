import random
from django.shortcuts import get_object_or_404, redirect, render
from adventures.forms import AdventureForm, MissionForm
from adventures.models import Adventure, Mission


def adventure_index(request):
    return render(
        request,
        'adventures.html',
        {
            'adventures': Adventure.objects.all()
        }
    )


def adventure_view(request, id):
    adventure = get_object_or_404(Adventure, pk=id)

    return render(
        request,
        'adventure_view.html',
        {
            'adventure': adventure
        }
    )


def adventure_add(request):
    if request.method == 'POST':
        form = AdventureForm(request.POST)
        if form.is_valid():
            adventure = form.save()
            return redirect(adventure_view, adventure.id)
    else:
        form = AdventureForm()

    return render(request, 'adventure_add.html', {'form': form})


def adventure_edit(request, id):
    adventure = get_object_or_404(Adventure, pk=id)

    if request.method == 'POST':
        form = AdventureForm(request.POST, instance=adventure)
        if form.is_valid():
            form.save()
            return redirect(adventure_view, id)
    else:
        form = AdventureForm(instance=adventure)

    return render(request, 'adventure_edit.html', {'form': form})


def adventure_delete(request, id):
    adventure = get_object_or_404(Adventure, pk=id)
    adventure.delete()

    referer = request.META.get('HTTP_REFERER')

    if referer.endswith(f'/{id}'):
        return redirect(adventure_index)
    else:
        return redirect(referer)


def mission_add(request, adventure_id):
    adventure = get_object_or_404(Adventure, pk=adventure_id)

    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid():
            form.save()
            adventure.save()
            return redirect('mission_add', adventure_id=adventure_id)
    else:
        form = MissionForm(initial={'adventure': adventure_id})

    return render(
        request,
        'mission_add.html',
        {
            'form': form,
            'adventure_id': adventure_id
        }
    )


def mission_edit(request, id):
    mission = get_object_or_404(Mission, pk=id)

    if request.method == 'POST':
        form = MissionForm(request.POST, instance=mission)
        if form.is_valid():
            form.save()
            mission.adventure.save()
            return redirect('adventure_view', id=mission.adventure.id)
    else:
        form = MissionForm(instance=mission)

    return render(
        request,
        'mission_edit.html',
        {
            'form': form,
            'adventure_id': mission.adventure.id
        }
    )


def mission_duplicate(request, id):
    source_mission = get_object_or_404(Mission, pk=id)

    target_mission = Mission(
        name=f'[DUPLICATE] {source_mission.name}',
        adventure=source_mission.adventure
    )
    target_mission.save()

    for source_submission in source_mission.children.all():
        target_submission = Mission(
            name=source_submission.name,
            adventure=source_submission.adventure,
            parent=target_mission
        )
        target_submission.save()

        for source_submission_task in source_submission.children.all():
            target_task = Mission(
                name=source_submission_task.name,
                adventure=source_submission_task.adventure,
                parent=target_submission
            )
            target_task.save()

    return redirect(mission_edit, target_mission.id)


def mission_delete(request, id):
    mission = get_object_or_404(Mission, pk=id)
    mission.delete()
    mission.adventure.save()

    return redirect(request.META.get('HTTP_REFERER'))


def mission_random(request):
    missions = list(Mission.objects.filter(completed='N'))

    if missions:
        choices = random.sample(missions, min(4, len(missions)))
    else:
        choices = list()

    return render(
        request,
        'mission_random.html',
        {
            'missions': choices
        }
    )


def mission_cycle(request, id):
    mission = get_object_or_404(Mission, pk=id)

    if mission.completed == Mission.Completed.YES:
        mission.completed = Mission.Completed.IMPOSSIBLE
    elif mission.completed == Mission.Completed.NO:
        mission.completed = Mission.Completed.YES
    else:
        mission.completed = Mission.Completed.NO

    mission.save()
    mission.adventure.save()

    return redirect('adventure_view', id=mission.adventure.id)


def mission_reset(request, id):
    mission = get_object_or_404(Mission, pk=id)

    mission.completed = Mission.Completed.NO
    mission.save()
    mission.adventure.save()

    for submission in mission.children.all():
        submission.completed = Mission.Completed.NO
        submission.save()

    return redirect('adventure_view', id=mission.adventure.id)


def submission_add(request, parent_id, adventure_id):
    adventure = get_object_or_404(Adventure, pk=adventure_id)

    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid():
            form.save()
            adventure.save()
            return redirect('submission_add', parent_id=parent_id, adventure_id=adventure_id)
    else:
        form = MissionForm(initial={'adventure': adventure_id, 'parent': parent_id})

    return render(
        request,
        'mission_add.html',
        {
            'form': form,
            'adventure_id': adventure_id
        }
    )


def almost_there(request):
    adventures = list(Adventure.objects.all())

    adventures.sort(key=lambda adventure: adventure.percentage(), reverse=True)

    return render(
        request,
        'adventures.html',
        {
            'adventures': adventures[:8]
        }
    )


def last_modified(request):
    adventures = Adventure.objects.order_by('-last_modified')

    return render(
        request,
        'adventures.html',
        {
            'adventures': adventures[:8]
        }
    )
