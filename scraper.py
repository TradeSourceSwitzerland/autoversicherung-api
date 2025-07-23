from playwright.sync_api import sync_playwright, TimeoutError

def scrape_praemie(profile, datum, fahrzeug, leasing):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.comparis.ch/autoversicherung/default#content-2")

        # 1) Versuch, den Cookie‑Banner wegzuklicken, falls vorhanden
        try:
            # timeout jetzt in click(), nicht in get_by_role()
            page.get_by_role("button", name="I Accept").click(timeout=5000)
        except TimeoutError:
            pass  # Banner nicht gefunden

        # 2) Profil wählen
        page.get_by_role("button", name=profile).click()

        # 3) Datum eingeben
        page.locator('[data-test="DateInputFormik"]').fill(datum)

        # 4) Fahrzeug eingeben und Auswahl treffen
        text_input = page.locator('[data-test="TextInputFormik"]').first
        text_input.fill(fahrzeug)
        page.get_by_role("listitem") \
            .filter(has_text=fahrzeug.split(' ')[0]) \
            .first \
            .click()

        # 5) Leasing auswählen (falls gewünscht)
        if leasing:
            try:
                page.get_by_text("Leasing").click()
            except TimeoutError:
                pass  # Checkbox nicht gefunden

        # 6) Prämie berechnen
        page.get_by_role("button", name="Prämien berechnen", exact=True).click()

        # 7) Ergebnis auslesen
        try:
            price = page.text_content("text=/CHF/", timeout=10000)
        except TimeoutError:
            price = None

        # Logging für Render-Logs
        if price:
            print(f"Found price: {price}")
        else:
            print("⚠️ Preis nicht gefunden")

        browser.close()
    return price
