import re


def filter_forvaltning_options(options):
    filtered = []
    for opt in options:
        if not isinstance(opt, str):
            continue
        if opt.strip() == "Social & Arbejdsmarked, Børn & Skole":
            continue
        parts = [x.strip() for x in opt.split(',')]
        if any("Stabe" in part for part in parts) and len(parts) > 1:
            continue
        filtered.append(opt)
    return filtered


def starts_with_letter(title):
    return bool(re.match(r'^[A-Za-zÆØÅæøå]', str(title).strip()))


def map_projekt_fase(fase):
    if fase in [
        "Igangværende - afklaring/opstart",
        "Igangværende - analyse/planlægning",
        "Igangværende - gennemførelse"
    ]:
        return "Igangværende"
    elif fase == "Idé":
        return None
    return fase


def map_forvaltning_forkortelse(forvaltning):
    mapping = {
        "Børn & Skole": "B&S",
        "Social & Arbejdsmarked": "SA",
        "Udvikling, Miljø & Teknik": "UMT",
        "Sundhed, Kultur & Omsorg": "SKO",
        "Social & Arbejdsmarked, Børn & Skole": "SA, B&S",
        "Stabe, Sundhed, Kultur & Omsorg": "Stabe, SKO",
        "Stabe, Udvikling, Miljø & Teknik": "Stabe, UMT",
        "Sundhed, Kultur & Omsorg, Stabe": "SKO, Stabe",
        "Udvikling, Miljø & Teknik, Stabe": "UMT, Stabe"
    }
    return mapping.get(forvaltning, forvaltning)


def get_fase_icon(fase):
    icons = {
        "Afventer/på pause": "⏸️",
        "Afvist": "❌",
        "I drift": "✅",
    }
    return icons.get(fase, "🔄")


def tokenize_teknologier(value):
    if not isinstance(value, str):
        return []
    return [t.strip() for t in re.split(r"\s*,\s*", value.strip()) if t.strip()]


def get_unique_teknologi_options(teknologi_values):
    unique = set()
    for v in teknologi_values:
        unique.update(tokenize_teknologier(v))
    return sorted(unique, key=str.casefold)


def row_contains_teknologi(value, teknologi):
    return teknologi in tokenize_teknologier(value)
