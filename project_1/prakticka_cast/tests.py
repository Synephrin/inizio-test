from django.test import TestCase, Client
from unittest.mock import patch, Mock
from .views import find_soup, save_csv
from .forms import SearchedPhrase
import os
import csv

# Test formuláře
class SearchedPhraseFormTests(TestCase):
    def test_valid_form(self):
        # Formulář je validní při zadání textu
        form_data = {"input_text": "django testování"}
        form = SearchedPhrase(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["input_text"], "django testování")

    def test_valid_form_empty_input(self):
        # Formulář není validní, pokud je vstup prázdný
        form_data = {"input_text": ""}
        form = SearchedPhrase(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("input_text", form.errors)


# Test pro views a jeho metody
class FindSoupTests(TestCase):
    @patch("prakticka_cast.views.requests.get")
    def test_find_soup_extracts_articles(self, mock_get):
        # Otestování parsování HTML a volání save__csv
        html = """
        <html>
            <body>
                <div>
                    <h3>Nadpis článku 1</h3>
                    <a href="https://example.com/1">Link 1</a>
                    <div class="VwiC3b">Popis 1</div>
                </div>
                <div>
                    <h3>Nadpis článku 2</h3>
                    <a href="https://example.com/2">Link 2</a>
                </div>
            </body>
        </html>
        """
        mock_response = Mock()
        mock_response.text = html
        mock_get.return_value = mock_response

        find_soup("https://fake-url.com")
        # Ověření vzniku csv souboru
        self.assertTrue(os.path.exists("results.csv"))

        # Kontrola obsahu csv
        with open("results.csv", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertIn("title", reader.fieldnames)
            self.assertIn("url", reader.fieldnames)
            self.assertTrue(len(rows) >= 1)
            os.remove("results.csv")

# Test metody Get pro zobrazení a Post pro odeslání dat
class IndexViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_request_render_form(self):
        # Get by měl zobrazit stránku s formulářem
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<form")

    @patch("prakticka_cast.views.find_soup")
    def test_post_valid_form_calls_find_soup(self, mock_find_soup):
        # POST zavolá funkci find_soup
        response = self.client.post("/", {"input_text": "python"})
        self.assertEqual(response.status_code, 302)
        mock_find_soup.assert_called_once()



