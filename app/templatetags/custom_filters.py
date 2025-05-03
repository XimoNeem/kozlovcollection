from django import template
import re

register = template.Library()

@register.filter
def replace_newlines(value):
    value = value.replace("</div><div>", " | ")  # Заменяем </div><div> между блоками
    value = value.replace("<div>", " | ")
    value = value.replace("</div>", "")
    return value

@register.filter
def replace_bullets(value):
    value = value.replace(" • ", "\u00A0")
    return value

@register.filter
def remove_prefix(value):
    """Удаляет префикс вида 'M.1 •' в начале строки"""
    return re.sub(r"^M\.\d+\s*•\s*", "", value)

@register.filter
def extract_prefix(value):
    """Оставляет только префикс вида 'M.1'"""
    match = re.match(r"^(M\.\d+)", value)
    return match.group(1) if match else ""