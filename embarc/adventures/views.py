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
            form.save()
            return redirect('adventures')
    else:
        form = AdventureForm()

    return render(request, 'adventure_add.html', {'form': form})


def adventure_edit(request, id):
    adventure = get_object_or_404(Adventure, pk=id)
    is_callback = request.GET.get('ref') == 'callback'

    if request.method == 'POST':
        form = AdventureForm(request.POST, instance=adventure)
        if form.is_valid():
            form.save()
            if is_callback:
                return redirect('adventure_view', id=id)
            else:
                return redirect('adventures')
    else:
        form = AdventureForm(instance=adventure)

    context = {'form': form, 'callback': id} if is_callback else {'form': form}
    return render(request, 'adventure_edit.html', context)


def adventure_delete(request, id):
    adventure = get_object_or_404(Adventure, pk=id)
    adventure.delete()

    return redirect(adventure_index)


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


def mission_delete(request, id):
    mission = get_object_or_404(Mission, pk=id)
    mission.delete()
    mission.adventure.save()

    return redirect('adventure_view', id=mission.adventure.id)


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
        mission.completed = Mission.Completed.NO
    elif mission.completed == Mission.Completed.NO:
        mission.completed = Mission.Completed.IMPOSSIBLE
    else:
        mission.completed = Mission.Completed.YES

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
