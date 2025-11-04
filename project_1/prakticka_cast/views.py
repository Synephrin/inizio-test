from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .forms import SearchedPhrase
from bs4 import BeautifulSoup
import requests
import csv


# Create your views here.

def index(request):
    # Zachycení metody POST a hledaného výrazu
    if request.method == "POST":
        form = SearchedPhrase(request.POST)
        # Validace formuláře pomocí Djanga
        if form.is_valid():
            base_url = f"http://www.google.com/search?q={form.cleaned_data["input_text"]}"
            data = find_soup(base_url)
            return save_csv(data)
    form = SearchedPhrase()
    return render(request, "prakticka_cast/index.html",{
                  "search_form": form
                  })

# Nalezení článků
def find_soup(url_link):
    response = requests.get(url_link)
    web = response.text
    soup = BeautifulSoup(web, "html.parser")


    articles = soup.find_all("div")
    data = []
    for a in articles:
        headline = a.find("h3")
        link = a.find("a")


        if headline and link:
            data.append({
                "title": headline.get_text(strip=True),
                "url": link["href"],
            })
    return data[1::3]

def save_csv(data):
    response = HttpResponse(content_type="text/csv; charset=utf-8")
    response["Content-Disposition"] = 'attachment; filename="results.csv"'

    writer = csv.DictWriter(response, fieldnames=["title", "url"])
    writer.writeheader()
    writer.writerows(data)
    return response
