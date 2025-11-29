def is_particulier(naam="", telefoon="", raw_text=""):
    naam = (naam or "").lower()
    raw_text = (raw_text or "").lower()

    makelaar_keywords = [
        "immo", "vastgoed", "estate", "agency", "makelaar",
        "bv", "bvba", "cvba", "kantoor"
    ]

    if any(k in naam for k in makelaar_keywords):
        return False

    if telefoon and telefoon.startswith("+32 9"):
        pass  # placeholder, hier kunnen we later makelaarslijst aan koppelen

    if "professioneel" in raw_text or "kantoor" in raw_text:
        return False

    return True

