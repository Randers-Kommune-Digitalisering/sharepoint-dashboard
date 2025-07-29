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
