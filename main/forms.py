from django.forms import ModelForm
from main.models import ManganJogja

class MoodEntryForm(ModelForm):
    class Meta:
        model = ManganJogja
        fields = ["menu", "desc", "nama_resto"]