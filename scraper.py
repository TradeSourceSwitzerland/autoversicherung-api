from playwright.sync_api import sync_playwright, TimeoutError

def scrape_praemie(profile, datum, fahrzeug, leasing):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("https://www.comparis.ch/autoversicherung/default#content-2")

        # 1) Versuch, den Cookie‑Banner wegzuklicken, falls vorhanden
        try:
            btn = page.get_by_role("button", name="I Accept", timeout=5000)
            btn.click()
        except TimeoutError:
            # Banner nicht gefunden – weiter ohne Klick
            pass

        # 2) Profil wählen
        page.get_by_role("button", name=profile).click()

        # 3) Datum eingeben
        page.locator('[data-test="DateInputFormik"]').fill(datum)

        # 4) Fahrzeug eingeben und Auswahl treffen
        text_input = page.locator('[data-test="TextInputFormik"]').first
        text_input.fill(fahrzeug)
        # etwas großzügiger suchen: ein Teil-Text matchen
        page.get_by_role("listitem").filter(has_text=fahrzeug.split(' ')[0]).first.click()

        # 5) Leasing auswählen (falls gewünscht)
        if leasing:
            try:
                page.get_by_text("Leasing").click()
            except TimeoutError:
                # Falls das Label anders heißt, ignoriere es
                pass

        # 6) Prämie berechnen
        page.get_by_role("button", name="Prämien berechnen", exact=True).click()

        # 7) Ergebnis auslesen
        try:
            price = page.text_content("text=/CHF/", timeout=10000)
        except TimeoutError:
            price = None

        browser.close()
    return price
