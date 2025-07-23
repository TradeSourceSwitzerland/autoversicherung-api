#!/usr/bin/env python3
from playwright.sync_api import sync_playwright

def scrape_praemie(profile, datum, fahrzeug, leasing):
    with sync_playwright() as p:
        # Headless + No‑Sandbox für Container‑Umgebungen
        browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
        page = browser.new_page()
        page.goto("https://www.comparis.ch/autoversicherung/default#content-2")

        # 1) Cookie‑Banner wegklicken
        try:
            page.get_by_role("button", name="I Accept").click()
        except:
            pass

        # 2) Profil wählen (dynamisch)
        page.get_by_role("button", name=profile, exact=True).click()

        # 3) Datum eingeben
        page.locator('[data-test="DateInputFormik"]').fill(datum)

        # 4) Fahrzeug eingeben + Autosuggest‑Auswahl
        page.locator('[data-test="TextInputFormik"]').fill(fahrzeug)
        page.get_by_role("listitem") \
            .filter(has_text=fahrzeug.split(" ")[0]) \
            .first \
            .click()

        # 5) Leasing auswählen (falls gewünscht)
        if leasing:
            page.locator('[data-test="RadioCheckbox"]') \
                .filter(has_text="Leasing") \
                .first \
                .click()

        # 6) Prämie berechnen
        page.get_by_role("button", name="Prämien berechnen", exact=True).click()

        # 7) Ergebnis auslesen
        price = page.text_content("text=/^CHF/")

        browser.close()
        return price

if __name__ == "__main__":
    # Beispiel‑Aufruf
    print(scrape_praemie(
        profile="Junglenker unter 25 Jahren",
        datum="12.2021",
        fahrzeug="Aston Martin Vantage V8",
        leasing=True
    ))
