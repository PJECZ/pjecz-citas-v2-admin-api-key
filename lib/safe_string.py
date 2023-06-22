"""
Safe string
"""
from datetime import date
import re

from unidecode import unidecode

CURP_REGEXP = r"^[A-Z]{4}\d{6}[A-Z]{6}[A-Z0-9]{2}$"
EMAIL_REGEXP = r"^[\w.-]+@[\w.-]+\.\w+$"
PASSWORD_REGEXP = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,24}$"
TELEFONO_REGEXP = r"^[1-9]\d{9}$"


def safe_clave(input_str):
    """Safe clave"""
    if not isinstance(input_str, str):
        raise ValueError
    new_string = input_str.strip().upper()
    regexp = re.compile("^[A-Z0-9-]{2,16}$")
    if regexp.match(new_string) is None:
        raise ValueError
    return new_string


def safe_curp(input_str, search_fragment=False):
    """Safe CURP"""
    if not isinstance(input_str, str):
        return ValueError
    input_str = input_str.strip()
    if input_str == "":
        return ValueError
    removed_spaces = re.sub(r"\s", "", input_str)
    removed_simbols = re.sub(r"[()\[\]:/.-]+", "", removed_spaces)
    final = unidecode(removed_simbols.upper())
    if search_fragment:
        if re.match(r"^[A-Z\d]+$", final) is None:
            return ValueError
        return final
    if re.fullmatch(CURP_REGEXP, final) is None:
        return ValueError
    return final


def safe_email(input_str, search_fragment=False):
    """Safe email"""
    if not isinstance(input_str, str) or input_str.strip() == "":
        raise ValueError
    final = input_str.strip().lower()
    if search_fragment:
        if re.match(r"^[\w.-]*@*[\w.-]*\.*\w*$", final) is None:
            return ValueError
        return final
    regexp = re.compile(EMAIL_REGEXP)
    if regexp.match(final) is None:
        raise ValueError
    return final


def safe_expediente(input_str):
    """Safe expediente"""
    if not isinstance(input_str, str) or input_str.strip() == "":
        raise ValueError
    elementos = re.sub(r"[^a-zA-Z0-9]+", "|", unidecode(input_str)).split("|")
    try:
        numero = int(elementos[0])
        ano = int(elementos[1])
    except (IndexError, ValueError) as error:
        raise error
    if ano < 1950 or ano > date.today().year:
        raise ValueError
    extra_1 = ""
    if len(elementos) >= 3:
        extra_1 = "-" + elementos[2].upper()
    extra_2 = ""
    if len(elementos) >= 4:
        extra_2 = "-" + elementos[3].upper()
    limpio = f"{str(numero)}/{str(ano)}{extra_1}{extra_2}"
    if len(limpio) > 16:
        raise ValueError
    return limpio


def safe_string(input_str, max_len=250, to_uppercase=True, do_unidecode=True):
    """Safe string"""
    if not isinstance(input_str, str):
        return None
    input_str = input_str.strip()
    if input_str == "":
        return None
    if do_unidecode:
        new_string = re.sub(r"[^a-zA-Z0-9.(),/-]+", " ", unidecode(input_str))
    else:
        new_string = re.sub(r"[^a-záéíóúüñA-ZÁÉÍÓÚÜÑ0-9.(),/-]+", " ", input_str)
    removed_multiple_spaces = re.sub(r"\s+", " ", new_string)
    final = removed_multiple_spaces.strip()
    if to_uppercase:
        final = final.upper()
    if max_len == 0:
        return final
    return (final[:max_len] + "...") if len(final) > max_len else final


def safe_telefono(input_str):
    """Safe telefono"""
    if not isinstance(input_str, str):
        raise ValueError
    input_str = input_str.strip()
    if input_str == "":
        return ValueError
    solo_numeros = re.sub(r"[^0-9]+", "", unidecode(input_str))
    if re.match(TELEFONO_REGEXP, solo_numeros) is None:
        return ValueError
    return solo_numeros
