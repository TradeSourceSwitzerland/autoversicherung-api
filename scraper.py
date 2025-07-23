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
            page.get_by_role("button", name="I Accept").click(timeout=5000)
        except:
            pass

        # 2) Profil wählen (dynamisch!)
        page.get_by_role("button", name=profile).click(timeout=5000)

        # 3) Datum eingeben
        page.locator('[data-test="DateInputFormik"]').fill(datum)

        # 4) Fahrzeug eingeben + Autosuggest
        page.locator('[data-test="TextInputFormik"]').fill(fahrzeug)
        page.get_by_role("listitem") \
            .filter(has_text=fahrzeug.split(" ")[0]) \
            .first \
            .click(timeout=5000)

        # 5) Leasing, falls gewünscht
        if leasing:
            page.locator('[data-test="RadioCheckbox"]') \
                .filter(has_text="Leasing") \
                .first \
                .click(timeout=5000)

        # 6) Prämie berechnen
        page.get_by_role("button", name="Prämien berechnen", exact=True) \
            .click(timeout=5000)

        # 7) Ergebnis auslesen
        price = page.text_content("text=/^CHF/", timeout=10000)
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
