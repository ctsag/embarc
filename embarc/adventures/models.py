from django.db import models


class Adventure(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=64)
    description = models.CharField(max_length=512, null=True, blank=True)

    objects = models.Manager()

    def percentage(self):
        total_mission_count = self.missions.count()
        percentage = 0

        if total_mission_count > 0:
            percentage = self.missions.exclude(completed='N').count() / total_mission_count * 100

        return round(percentage)

    def __str__(self):
        return f'{self.name} ({self.description[:24]}...)'


class Mission(models.Model):
    class Completed(models.TextChoices):
        NO = 'N', 'No'
        YES = 'Y', 'Yes'
        IMPOSSIBLE = 'I', 'Impossible'

    name = models.CharField(max_length=96)
    notes = models.CharField(max_length=512, null=True, blank=True)
    completed = models.CharField(max_length=1, choices=Completed, default=Completed.NO)
    adventure = models.ForeignKey(Adventure, on_delete=models.CASCADE, related_name='missions')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )

    objects = models.Manager()

    def __str__(self):
        return self.name
