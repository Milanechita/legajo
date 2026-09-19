"""Normalizacion de paises a codigo ISO 3166-1 alfa-2.

Las tres fuentes que usamos nombran a los mismos paises de forma distinta:

    GAFI         "Democratic Republic of the Congo"
    ARCA         "Republica Democratica del Congo"
    el padron    "CONGO", "RD CONGO", "CD", "Congo (Kinshasa)"

Comparar esos strings entre si es garantia de falso negativo silencioso, que
es justo el error que no se puede permitir en screening. La solucion es
normalizar una sola vez en el borde: todo entra como texto y sale como codigo
de dos letras, y de ahi en adelante las listas comparan codigos.

La tabla es explicita a proposito. Se puede intentar deducir el pais sacando
prefijos ("Republica Islamica de Iran" -> "Iran"), pero eso se rompe con
"Republica Kirguisa" y "Republica Gabonesa", donde lo que queda es un
adjetivo. Escribir los alias a mano es mas largo y es correcto.

Un pais que no esta en la tabla devuelve None, y eso es informacion: significa
que hay que agregarlo, no que el cliente sea de bajo riesgo.
"""

from __future__ import annotations

import re
import unicodedata

# (codigo ISO, alias). El primer alias es el nombre de referencia.
_TABLA: tuple[tuple[str, tuple[str, ...]], ...] = (
    # --- GAFI: alto riesgo ---
    ("KP", ("Corea del Norte", "Republica Popular Democratica de Corea", "RPDC",
            "Democratic Peoples Republic of Korea", "DPRK", "North Korea",
            "Democratic Republic of Korea")),
    ("IR", ("Iran", "Republica Islamica de Iran", "Islamic Republic of Iran")),
    ("MM", ("Myanmar", "Birmania", "Republica de la Union de Myanmar", "Burma")),

    # --- GAFI: monitoreo intensificado ---
    ("AO", ("Angola", "Republica de Angola")),
    ("BO", ("Bolivia", "Estado Plurinacional de Bolivia")),
    ("BA", ("Bosnia y Herzegovina", "Bosnia and Herzegovina", "Bosnia")),
    ("BG", ("Bulgaria",)),
    ("CM", ("Camerun", "Cameroon", "Republica de Camerun")),
    ("CI", ("Costa de Marfil", "Republica de Costa de Marfil", "Cote dIvoire",
            "Cote d Ivoire", "Ivory Coast")),
    ("CD", ("Republica Democratica del Congo", "RD Congo", "Congo Kinshasa",
            "Democratic Republic of the Congo", "DRC")),
    ("HT", ("Haiti", "Republica de Haiti")),
    ("IQ", ("Irak", "Iraq", "Republica de Irak")),
    ("KE", ("Kenia", "Kenya")),
    ("KW", ("Kuwait",)),
    ("LA", ("Laos", "Republica Democratica Popular Lao", "Lao PDR",
            "Lao Peoples Democratic Republic")),
    ("LB", ("Libano", "Lebanon", "Republica Libanesa")),
    ("MC", ("Monaco", "Principado de Monaco")),
    ("NP", ("Nepal", "Republica Federal Democratica de Nepal")),
    ("PG", ("Papua Nueva Guinea", "Papua New Guinea",
            "Estado Independiente de Papua Nueva Guinea")),
    ("SS", ("Sudan del Sur", "Republica de Sudan del Sur", "South Sudan")),
    ("SY", ("Siria", "Republica Arabe Siria", "Syria", "Syrian Arab Republic")),
    ("VE", ("Venezuela", "Republica Bolivariana de Venezuela")),
    ("VN", ("Vietnam", "Viet Nam", "Republica Socialista de Vietnam")),
    ("VG", ("Islas Virgenes Britanicas", "Virgin Islands UK", "British Virgin Islands",
            "BVI", "Islas Virgenes UK")),
    ("YE", ("Yemen", "Republica de Yemen")),

    # --- ARCA no cooperantes, resto ---
    ("AF", ("Afganistan", "Republica Islamica de Afganistan", "Afghanistan")),
    ("BD", ("Bangladesh", "Banglades", "Republica Popular de Banglades")),
    ("BI", ("Burundi", "Republica de Burundi")),
    ("BT", ("Butan", "Bhutan", "Reino de Butan")),
    ("BY", ("Bielorrusia", "Belarus", "Republica de Bielorrusia")),
    ("CF", ("Republica Centroafricana", "Central African Republic")),
    ("CG", ("Congo", "Republica del Congo", "Congo Brazzaville")),
    ("CU", ("Cuba", "Republica de Cuba")),
    ("DJ", ("Yibuti", "Djibouti", "Republica de Yibuti")),
    ("DZ", ("Argelia", "Algeria", "Republica Argelina Democratica y Popular")),
    ("EG", ("Egipto", "Egypt", "Republica Arabe de Egipto")),
    ("ER", ("Eritrea", "Estado de Eritrea")),
    ("ET", ("Etiopia", "Ethiopia", "Republica Democratica Federal de Etiopia")),
    ("FJ", ("Fiyi", "Fiji", "Republica de Fiyi")),
    ("FM", ("Micronesia", "Los Estados Federados de Micronesia")),
    ("GA", ("Gabon", "Republica Gabonesa")),
    ("GG", ("Guernsey", "Brecqhou", "Isla de Sark", "Sark")),
    ("GM", ("Gambia", "Republica de Gambia")),
    ("GN", ("Guinea", "Republica de Guinea")),
    ("GQ", ("Guinea Ecuatorial", "Republica de Guinea Ecuatorial")),
    ("GW", ("Guinea Bisau", "Guinea-Bisau", "Republica de Guinea-Bisau",
            "Guinea Bissau")),
    ("GY", ("Guyana", "Republica Cooperativa de Guyana")),
    ("HN", ("Honduras", "Republica de Honduras")),
    ("KG", ("Kirguistan", "Republica Kirguisa", "Kyrgyzstan")),
    ("KH", ("Camboya", "Reino de Camboya", "Cambodia")),
    ("KI", ("Kiribati", "Republica de Kiribati")),
    ("KM", ("Comoras", "Union de las Comoras", "Comoros")),
    ("LK", ("Sri Lanka", "Republica Democratica Socialista de Sri Lanka")),
    ("LS", ("Lesoto", "Reino de Lesoto", "Lesotho")),
    ("LY", ("Libia", "Estado de Libia", "Libya")),
    ("ML", ("Mali", "Republica de Mali")),
    ("MW", ("Malaui", "Malawi", "Republica de Malaui")),
    ("MZ", ("Mozambique", "Republica de Mozambique")),
    ("NE", ("Niger", "Republica del Niger")),
    ("NI", ("Nicaragua", "Republica de Nicaragua")),
    ("PN", ("Islas Pitcairn", "Pitcairn",
            "Territorio Britanico de Ultramar Islas Pitcairn Henderson Ducie y Oeno")),
    ("PW", ("Palaos", "Palau", "Republica de Palaos")),
    ("SB", ("Islas Salomon", "Solomon Islands")),
    ("SD", ("Sudan", "Republica del Sudan")),
    ("SH", ("Santa Elena", "Isla Santa Elena", "Isla Ascension", "Ascension",
            "Tristan da Cunha", "Saint Helena")),
    ("SL", ("Sierra Leona", "Republica de Sierra Leona", "Sierra Leone")),
    ("SO", ("Somalia", "Republica Federal de Somalia")),
    ("SR", ("Surinam", "Suriname", "Republica de Surinam")),
    ("ST", ("Santo Tome y Principe", "Republica Democratica de Santo Tome y Principe")),
    ("TD", ("Chad", "Republica del Chad")),
    ("TG", ("Togo", "Republica Togolesa")),
    ("TJ", ("Tayikistan", "Republica de Tayikistan", "Tajikistan")),
    ("TL", ("Timor Leste", "Timor Oriental", "Republica Democratica de Timor-Leste",
            "Republica Democratica de Timor Oriental", "East Timor")),
    ("TO", ("Tonga", "Reino de Tonga")),
    ("TV", ("Tuvalu",)),
    ("TZ", ("Tanzania", "Republica Unida de Tanzania")),
    ("UZ", ("Uzbekistan", "Republica de Uzbekistan")),
    ("VA", ("Vaticano", "Ciudad del Vaticano", "Estado de la Ciudad del Vaticano",
            "Santa Sede", "Holy See")),
    ("ZM", ("Zambia", "Republica de Zambia")),
    ("ZW", ("Zimbabue", "Zimbabwe", "Republica de Zimbabue")),

    # --- America Latina y socios habituales ---
    ("AR", ("Argentina", "Republica Argentina")),
    ("BR", ("Brasil", "Brazil", "Republica Federativa del Brasil")),
    ("CL", ("Chile", "Republica de Chile")),
    ("CO", ("Colombia", "Republica de Colombia")),
    ("CR", ("Costa Rica",)),
    ("DO", ("Republica Dominicana", "Dominican Republic")),
    ("EC", ("Ecuador",)),
    ("GT", ("Guatemala",)),
    ("MX", ("Mexico", "Estados Unidos Mexicanos")),
    ("PA", ("Panama", "Republica de Panama")),
    ("PE", ("Peru",)),
    ("PY", ("Paraguay", "Republica del Paraguay")),
    ("SV", ("El Salvador",)),
    ("UY", ("Uruguay", "Republica Oriental del Uruguay")),

    # --- Resto del mundo y centros offshore frecuentes ---
    ("AE", ("Emiratos Arabes Unidos", "United Arab Emirates", "EAU", "UAE", "Dubai")),
    ("AT", ("Austria",)),
    ("AU", ("Australia",)),
    ("BE", ("Belgica", "Belgium")),
    ("BM", ("Bermudas", "Bermuda")),
    ("BS", ("Bahamas",)),
    ("BZ", ("Belice", "Belize")),
    ("CA", ("Canada",)),
    ("CH", ("Suiza", "Switzerland", "Confederacion Suiza")),
    ("CN", ("China", "Republica Popular China")),
    ("CW", ("Curazao", "Curacao")),
    ("CY", ("Chipre", "Cyprus")),
    ("DE", ("Alemania", "Germany")),
    ("DK", ("Dinamarca", "Denmark")),
    ("ES", ("Espana", "Spain", "Reino de Espana")),
    ("FR", ("Francia", "France")),
    ("GB", ("Reino Unido", "United Kingdom", "Gran Bretana", "Inglaterra", "UK")),
    ("GI", ("Gibraltar",)),
    ("HK", ("Hong Kong",)),
    ("IE", ("Irlanda", "Ireland")),
    ("IL", ("Israel",)),
    ("IN", ("India",)),
    ("IT", ("Italia", "Italy")),
    ("JE", ("Jersey",)),
    ("JP", ("Japon", "Japan")),
    ("KY", ("Islas Caiman", "Cayman Islands", "Caiman")),
    ("LI", ("Liechtenstein",)),
    ("LU", ("Luxemburgo", "Luxembourg")),
    ("MT", ("Malta",)),
    ("MU", ("Mauricio", "Mauritius")),
    ("NL", ("Paises Bajos", "Holanda", "Netherlands")),
    ("NO", ("Noruega", "Norway")),
    ("NZ", ("Nueva Zelanda", "New Zealand")),
    ("PK", ("Pakistan",)),
    ("PT", ("Portugal",)),
    ("RU", ("Rusia", "Russia", "Federacion Rusa")),
    ("SA", ("Arabia Saudita", "Saudi Arabia")),
    ("SC", ("Seychelles",)),
    ("SE", ("Suecia", "Sweden")),
    ("SG", ("Singapur", "Singapore")),
    ("TR", ("Turquia", "Turkey", "Turkiye")),
    ("TW", ("Taiwan",)),
    ("US", ("Estados Unidos", "United States", "EEUU", "EE UU", "USA",
            "Estados Unidos de America")),
    ("ZA", ("Sudafrica", "South Africa")),
)

_APOSTROFO = re.compile(r"['\u2019\u02bc]")
_SIN_ALFANUM = re.compile(r"[^A-Z0-9 ]")
_ESPACIOS = re.compile(r"\s+")


def _clave(texto: str) -> str:
    """Forma canonica de un nombre de pais para buscar en la tabla."""
    descompuesto = unicodedata.normalize("NFKD", texto)
    sin_acentos = "".join(c for c in descompuesto if not unicodedata.combining(c))
    # El apostrofo se borra, no se convierte en espacio: "People's" y "Peoples"
    # tienen que dar la misma clave, igual que "d'Ivoire" y "dIvoire".
    sin_apostrofo = _APOSTROFO.sub("", sin_acentos.upper())
    limpio = _SIN_ALFANUM.sub(" ", sin_apostrofo)
    return _ESPACIOS.sub(" ", limpio).strip()


_INDICE: dict[str, str] = {}
_NOMBRE: dict[str, str] = {}
for _iso, _alias in _TABLA:
    _NOMBRE[_iso] = _alias[0]
    _INDICE[_iso] = _iso
    for _a in _alias:
        _INDICE.setdefault(_clave(_a), _iso)


def iso(pais: str | None) -> str | None:
    """Devuelve el codigo ISO alfa-2, o None si el pais no esta en la tabla.

    None no significa bajo riesgo: significa que falta el pais en la tabla y
    hay que agregarlo. Ver `desconocidos()`.
    """
    if not pais:
        return None
    return _INDICE.get(_clave(pais))


def nombre(codigo: str) -> str:
    """Nombre de referencia de un codigo ISO."""
    return _NOMBRE.get(codigo.upper(), codigo.upper())


def codigos(nombres) -> frozenset[str]:
    """Convierte una lista de nombres a un conjunto de codigos ISO.

    Falla ruidosamente si algun nombre no se reconoce. Una lista de riesgo
    cargada a medias es peor que ninguna, porque da una falsa sensacion de
    cobertura.
    """
    resultado, faltantes = set(), []
    for n in nombres:
        c = iso(n)
        if c is None:
            faltantes.append(n)
        else:
            resultado.add(c)
    if faltantes:
        raise ValueError(
            f"paises no reconocidos, hay que agregarlos a paises.py: {faltantes}"
        )
    return frozenset(resultado)


def desconocidos(nombres) -> list[str]:
    """Los nombres que la tabla no reconoce. Para diagnostico."""
    return [n for n in nombres if iso(n) is None]
