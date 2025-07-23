from playwright.sync_api import sync_playwright

def scrape_praemie(profile, datum, fahrzeug, leasing):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.comparis.ch/autoversicherung/default#content-2")

        # Cookie-Hinweis akzeptieren
        page.get_by_role("button", name="I Accept").click()

        # Profil wählen
        page.get_by_role("button", name=profile).click()

        # Datum eingeben
        page.locator('[data-test="DateInputFormik"]').fill(datum)

        # Fahrzeug eingeben und Auswahl treffen
        text_input = page.locator('[data-test="TextInputFormik"]').first
        text_input.fill(fahrzeug)
        page.get_by_role("listitem").filter(has_text=fahrzeug).first.click()

        # Leasing auswählen
        if leasing:
            page.get_by_text("Leasing").click()

        # Prämie berechnen
        page.get_by_role("button", name="Prämien berechnen", exact=True).click()

        # Ergebnis auslesen
        try:
            price = page.text_content("text=/CHF/", timeout=5000)
        except:
            price = None

        browser.close()
    return price
