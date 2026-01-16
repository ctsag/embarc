from django.db import models


class Adventure(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512)
    last_modified = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    def percentage(self):
        total_mission_count = self.missions.exclude(completed=Mission.Completed.IMPOSSIBLE).count()
        completed_mission_count = self.missions.filter(completed=Mission.Completed.YES).count()
        percentage = 0

        if total_mission_count > 0:
            percentage = completed_mission_count / total_mission_count  * 100

        return round(percentage)

    def __str__(self):
        return f'{self.name} ({self.description[:24]}...)'


class Mission(models.Model):
    class Meta:
        ordering = ['position']

    class Completed(models.TextChoices):
        NO = 'N', 'No'
        YES = 'Y', 'Yes'
        IMPOSSIBLE = 'I', 'Impossible'

    name = models.CharField(max_length=96)
    notes = models.CharField(max_length=512, null=True, blank=True)
    completed = models.CharField(max_length=1, choices=Completed, default=Completed.NO)
    position = models.IntegerField(default=0)
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE, related_name='missions')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    objects = models.Manager()

    def next_position(self):
        if self.parent:
            filter = Mission.objects.filter(parent=self.parent)
        else:
            filter = Mission.objects.filter(adventure=self.adventure)

        if filter:
            max_position = filter.aggregate(models.Max('position'))['position__max']
            return max_position + 1
        else:
            return 1

    def __str__(self):
        return self.name
