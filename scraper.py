from playwright.sync_api import sync_playwright, TimeoutError

def scrape_praemie(profile, datum, fahrzeug, leasing):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.comparis.ch/autoversicherung/default#content-2")

        # 1) Cookie‑Banner wegklicken (5 s Timeout)
        try:
            page.get_by_role("button", name="I Accept").click(timeout=5000)
        except TimeoutError:
            pass

        # 2) Profil wählen (5 s Timeout)
        try:
            page.get_by_role("button", name=profile).click(timeout=5000)
        except TimeoutError:
            print(f"⚠️ Profil‑Button '{profile}' nicht gefunden")
            browser.close()
            return None

        # 3) Datum eingeben
        try:
            page.locator('[data-test="DateInputFormik"]').fill(datum, timeout=5000)
        except TimeoutError:
            print("⚠️ Datumseingabe nicht möglich")
            browser.close()
            return None

        # 4) Fahrzeug eingeben + Suggest-Auswahl (5 s Timeout)
        try:
            text_input = page.locator('[data-test="TextInputFormik"]').first
            text_input.fill(fahrzeug, timeout=5000)
            page.get_by_role("listitem") \
                .filter(has_text=fahrzeug.split(' ')[0]) \
                .first \
                .click(timeout=5000)
        except TimeoutError:
            print(f"⚠️ Fahrzeug‑Suggest für '{fahrzeug}' nicht gefunden")
            browser.close()
            return None

        # 5) Leasing anklicken (falls gewünscht, 5 s Timeout)
        if leasing:
            try:
                leasing_locator = page.locator('[data-test="RadioCheckbox"]') \
                                      .filter(has_text="Leasing") \
                                      .first
                leasing_locator.click(timeout=5000)
            except TimeoutError:
                print("⚠️ Leasing‑Checkbox nicht gefunden")

        # 6) Prämie berechnen (5 s Timeout)
        try:
            page.get_by_role("button", name="Prämien berechnen", exact=True).click(timeout=5000)
        except TimeoutError:
            print("⚠️ Prämien berechnen‑Button nicht gefunden")
            browser.close()
            return None

        # 7) Ergebnis auslesen (10 s Timeout)
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
