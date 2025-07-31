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


def filter_teknologi_options(options):
    exclude = {
        "Generativ AI, Chatbot",
        "Generativ AI, IoT/sensorer"
    }
    filtered = []
    for opt in options:
        if not isinstance(opt, str):
            continue
        if opt.strip() in exclude:
            continue
        filtered.append(opt)
    return filtered


def get_fase_icon(fase):
    icons = {
        "Afventer/på pause": "⏸️",
        "Afvist": "❌",
        "I drift": "✅",
    }
    return icons.get(fase, "❓")
