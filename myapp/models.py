from django.db import models
from django.contrib.sessions.models import Session


class SearchHistory(models.Model):
    session_key = models.CharField(db_index=True)
    query = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.session_key} - {self.query}"

    def __repr__(self) -> str:
        return f"{self.session_key} - {self.query}"
