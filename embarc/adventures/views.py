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
    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid():
            form.save()
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
            return redirect('adventure_view', id=mission.adventure.id)
    else:
        form = MissionForm(instance=mission)

    return render(request, 'mission_edit.html', {'form': form})


def mission_delete(request, id):
    mission = get_object_or_404(Mission, pk=id)
    mission.delete()

    return redirect('adventure_view', id=mission.adventure.id)


def submission_add(request, parent_id, adventure_id):
    if request.method == 'POST':
        form = MissionForm(request.POST)
        if form.is_valid():
            form.save()
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
