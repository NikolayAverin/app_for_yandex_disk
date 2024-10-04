from django import forms


class PublicLincForm(forms.Form):
    """Форма для ввода публичной ссылки."""
    public_link = forms.CharField(max_length=300, label="Публичная ссылка")