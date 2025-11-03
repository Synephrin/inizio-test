from django.shortcuts import render
from django.http import HttpResponseRedirect
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
            find_soup(base_url)
            return HttpResponseRedirect("/")
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
    save_csv(data)

def save_csv(data):
    new_data = data[1::3]
    with open("results.csv", "w", encoding="UTF-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title","url"])
        writer.writeheader()
        writer.writerows(new_data)
