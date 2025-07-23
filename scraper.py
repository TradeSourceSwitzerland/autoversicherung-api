from playwright.sync_api import sync_playwright, TimeoutError

def scrape_praemie(profile, datum, fahrzeug, leasing):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.comparis.ch/autoversicherung/default#content-2")

        # 1) Cookie‑Banner wegklicken
        try:
            page.get_by_role("button", name="I Accept").click(timeout=5000)
        except TimeoutError:
            pass

        # 2) Profil wählen
        page.get_by_role("button", name=profile).click()

        # 3) Datum eingeben
        page.locator('[data-test="DateInputFormik"]').fill(datum)

        # 4) Fahrzeug eingeben + Suggest-Auswahl
        text_input = page.locator('[data-test="TextInputFormik"]').first
        text_input.fill(fahrzeug)
        page.get_by_role("listitem") \
            .filter(has_text=fahrzeug.split(' ')[0]) \
            .first \
            .click()

        # 5) Leasing anklicken (falls gewünscht)
        if leasing:
            try:
                leasing_locator = page.locator('[data-test="RadioCheckbox"]') \
                                      .filter(has_text="Leasing") \
                                      .first
                leasing_locator.click(timeout=5000)
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
