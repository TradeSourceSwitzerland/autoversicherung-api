#!/usr/bin/env python3
from playwright.sync_api import sync_playwright

def scrape_praemie():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 1) Seite öffnen
        page.goto("https://www.comparis.ch/autoversicherung/default#content-2")

        # 2) Cookie‑Banner akzeptieren
        page.get_by_role("button", name="I Accept").click()

        # 3) Junglenker‑Profil wählen
        page.get_by_role("button", name="Junglenker unter 25 Jahren").click()

        # 4) Inverkehrssetzung anklicken
        page.get_by_role("group", name="Inverkehrssetzung*").locator("label").click()

        # 5) Datum ausfüllen
        page.locator('[data-test="DateInputFormik"]').fill("12.2021")

        # 6) Marke/Modell anklicken
        page.get_by_role("group", name="Marke/Modell oder Typenschein*").locator("label").click()

        # 7) Fahrzeugsuche ausfüllen
        page.locator('[data-test="TextInputFormik"]').fill("aston martin vantage v8")

        # 8) Genaue Auswahl aus der Autosuggest‑Liste
        page.get_by_role("listitem") \
            .filter(has_text="ASTON MARTIN V8 Vantage 4.7 AMR Sportshift321KW / 437HP2 Türen • Cabriolet •") \
            .get_by_role("mark") \
            .first \
            .click()

        # 9) Leasing anhaken
        page.locator('[data-test="RadioCheckbox"]').get_by_text("Leasing").click()

        # 10) Prämie berechnen
        page.get_by_role("button", name="Prämien berechnen", exact=True).click()

        # 11) Ergebnis anklicken (optional)
        page.get_by_text("CHF 2'387.90").click()

        # 12) Prämie auslesen
        price = page.text_content("text=/^CHF/")

        browser.close()
        return price

if __name__ == "__main__":
    prämie = scrape_praemie()
    print(f"→ Gefundene Prämie: {prämie}")
