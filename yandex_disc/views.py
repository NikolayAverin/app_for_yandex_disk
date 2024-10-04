import os
from pathlib import Path
import requests
from typing import Optional, Dict, Any
from django.shortcuts import render, redirect
from dotenv import load_dotenv
from yandex_disc.forms import PublicLincForm

YANDEX_DISC_TOKEN = os.getenv("YANDEX_DISC_TOKEN")

def get_files(public_key: str) -> Optional[Dict[str, Any]]:
    """Получение списка файлов по публичной ссылке."""
    url = f'https://cloud-api.yandex.net/v1/disk/public/resources?public_key={public_key}'
    headers = {
        'Authorization': f'OAuth {YANDEX_DISC_TOKEN}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None


def download_file(request, file_link: str):
    """Загрузка файлов на ПК."""
    headers = {
        'Authorization': f'OAuth {YANDEX_DISC_TOKEN}'
    }
    response = request.get(file_link, headers=headers, stream=True)
    response.raise_for_status()
    file_name = file_link.split("/")[-1]
    with open(file_name, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)
    return redirect("index")


def index(request):
    """Контроллер для страницы index.html."""
    if request.method == "POST":
        form = PublicLincForm(request.POST)
        if form.is_valid():
            public_link = form.cleaned_data["public_link"]
            files = get_files(public_link)
            if files is not None:
                return render(request, "yandex_disc/files_list.html", {"files": files.get("_embedded", {}).get("items", []), "public_link": public_link})
    else:
        form = PublicLincForm()
    return render(request, "yandex_disc/index.html", {"form": form})
