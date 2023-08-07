from django.db import models


class Institute(models.Model):
    """
    Represents an educational institute.
    """

    name = models.CharField(max_length=100, unique=True, help_text="Name of the institute.")
    description = models.TextField(blank=True, help_text="Description of the institute.")

    class Meta:
        verbose_name = "Institute"
        verbose_name_plural = "Institutes"

    def __str__(self):
        """
        Return a string representation of the institute.
        """
        return self.name
