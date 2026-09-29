import re
from typing import Tuple, Dict, Any, Optional
from backend.models.domain import Jurisdiction


COUNTRY_KNOWLEDGE_BASE: Dict[str, Dict[str, Any]] = {
    "canada": {
        "name": "Canada",
        "currency": "CAD",
        "language": "en",
        "locale": "en-CA",
        "timezone": "America/Toronto",
        "measurement": "metric",
        "postal_label": "Postal Code",
        "regions": ["Ontario", "Quebec", "British Columbia", "Alberta", "Manitoba", "Nova Scotia"],
        "cities": {"toronto": "Ontario", "vancouver": "British Columbia", "montreal": "Quebec", "calgary": "Alberta", "ottawa": "Ontario"}
    },
    "united kingdom": {
        "name": "United Kingdom",
        "currency": "GBP",
        "language": "en",
        "locale": "en-GB",
        "timezone": "Europe/London",
        "measurement": "metric",
        "postal_label": "Postcode",
        "regions": ["England", "Scotland", "Wales", "Northern Ireland"],
        "cities": {"london": "England", "manchester": "England", "edinburgh": "Scotland", "birmingham": "England", "glasgow": "Scotland"}
    },
    "uk": {"alias_for": "united kingdom"},
    "united states": {
        "name": "United States",
        "currency": "USD",
        "language": "en",
        "locale": "en-US",
        "timezone": "America/New_York",
        "measurement": "imperial",
        "postal_label": "ZIP Code",
        "regions": ["New York", "California", "Texas", "Florida", "Illinois", "Washington", "Massachusetts"],
        "cities": {"new york": "New York", "nyc": "New York", "san francisco": "California", "los angeles": "California", "chicago": "Illinois", "seattle": "Washington", "austin": "Texas", "boston": "Massachusetts"}
    },
    "usa": {"alias_for": "united states"},
    "us": {"alias_for": "united states"},
    "japan": {
        "name": "Japan",
        "currency": "JPY",
        "language": "ja",
        "locale": "ja-JP",
        "timezone": "Asia/Tokyo",
        "measurement": "metric",
        "postal_label": "Postal Code",
        "regions": ["Tokyo", "Osaka", "Kyoto", "Hokkaido", "Fukuoka"],
        "cities": {"tokyo": "Tokyo", "osaka": "Osaka", "kyoto": "Kyoto"}
    },
    "singapore": {
        "name": "Singapore",
        "currency": "SGD",
        "language": "en",
        "locale": "en-SG",
        "timezone": "Asia/Singapore",
        "measurement": "metric",
        "postal_label": "Postal Code",
        "regions": ["Central Region", "East Region", "West Region"],
        "cities": {"singapore": "Central Region"}
    },
    "brazil": {
        "name": "Brazil",
        "currency": "BRL",
        "language": "pt",
        "locale": "pt-BR",
        "timezone": "America/Sao_Paulo",
        "measurement": "metric",
        "postal_label": "CEP",
        "regions": ["São Paulo", "Rio de Janeiro", "Bahia", "Minas Gerais"],
        "cities": {"são paulo": "São Paulo", "sao paulo": "São Paulo", "rio de janeiro": "Rio de Janeiro"}
    },
    "portugal": {
        "name": "Portugal",
        "currency": "EUR",
        "language": "pt",
        "locale": "pt-PT",
        "timezone": "Europe/Lisbon",
        "measurement": "metric",
        "postal_label": "Código Postal",
        "regions": ["Lisbon", "Porto", "Faro"],
        "cities": {"lisbon": "Lisbon", "porto": "Porto"}
    },
    "uae": {"alias_for": "united arab emirates"},
    "united arab emirates": {
        "name": "United Arab Emirates",
        "currency": "AED",
        "language": "ar",
        "locale": "ar-AE",
        "timezone": "Asia/Dubai",
        "measurement": "metric",
        "postal_label": "Makani / PO Box",
        "regions": ["Dubai", "Abu Dhabi", "Sharjah"],
        "cities": {"dubai": "Dubai", "abu dhabi": "Abu Dhabi"}
    },
    "australia": {
        "name": "Australia",
        "currency": "AUD",
        "language": "en",
        "locale": "en-AU",
        "timezone": "Australia/Sydney",
        "measurement": "metric",
        "postal_label": "Postcode",
        "regions": ["New South Wales", "Victoria", "Queensland", "Western Australia"],
        "cities": {"sydney": "New South Wales", "melbourne": "Victoria", "brisbane": "Queensland"}
    },
    "india": {
        "name": "India",
        "currency": "INR",
        "language": "hi",
        "locale": "hi-IN",
        "timezone": "Asia/Kolkata",
        "measurement": "metric",
        "postal_label": "PIN Code",
        "regions": ["Maharashtra", "Karnataka", "Delhi", "Tamil Nadu", "Telangana"],
        "cities": {"mumbai": "Maharashtra", "bengaluru": "Karnataka", "delhi": "Delhi", "hyderabad": "Telangana"}
    },
    "germany": {
        "name": "Germany",
        "currency": "EUR",
        "language": "de",
        "locale": "de-DE",
        "timezone": "Europe/Berlin",
        "measurement": "metric",
        "postal_label": "Postleitzahl",
        "regions": ["Bavaria", "Berlin", "North Rhine-Westphalia", "Hesse"],
        "cities": {"berlin": "Berlin", "munich": "Bavaria", "frankfurt": "Hesse"}
    },
    "france": {
        "name": "France",
        "currency": "EUR",
        "language": "fr",
        "locale": "fr-FR",
        "timezone": "Europe/Paris",
        "measurement": "metric",
        "postal_label": "Code Postal",
        "regions": ["Île-de-France", "Provence-Alpes-Côte d'Azur"],
        "cities": {"paris": "Île-de-France", "lyon": "Auvergne-Rhône-Alpes", "marseille": "Provence-Alpes-Côte d'Azur"}
    },
    "spain": {
        "name": "Spain",
        "currency": "EUR",
        "language": "es",
        "locale": "es-ES",
        "timezone": "Europe/Madrid",
        "measurement": "metric",
        "postal_label": "Código Postal",
        "regions": ["Madrid", "Catalonia", "Andalusia"],
        "cities": {"madrid": "Madrid", "barcelona": "Catalonia"}
    },
    "italy": {
        "name": "Italy",
        "currency": "EUR",
        "language": "it",
        "locale": "it-IT",
        "timezone": "Europe/Rome",
        "measurement": "metric",
        "postal_label": "CAP",
        "regions": ["Lazio", "Lombardy"],
        "cities": {"rome": "Lazio", "milan": "Lombardy"}
    },
    "switzerland": {
        "name": "Switzerland",
        "currency": "CHF",
        "language": "de",
        "locale": "de-CH",
        "timezone": "Europe/Zurich",
        "measurement": "metric",
        "postal_label": "PLZ",
        "regions": ["Zurich", "Geneva"],
        "cities": {"zurich": "Zurich", "geneva": "Geneva"}
    },
    "netherlands": {
        "name": "Netherlands",
        "currency": "EUR",
        "language": "nl",
        "locale": "nl-NL",
        "timezone": "Europe/Amsterdam",
        "measurement": "metric",
        "postal_label": "Postcode",
        "regions": ["North Holland"],
        "cities": {"amsterdam": "North Holland"}
    },
    "new zealand": {
        "name": "New Zealand",
        "currency": "NZD",
        "language": "en",
        "locale": "en-NZ",
        "timezone": "Pacific/Auckland",
        "measurement": "metric",
        "postal_label": "Postcode",
        "regions": ["Auckland Region"],
        "cities": {"auckland": "Auckland Region"}
    },
    "south africa": {
        "name": "South Africa",
        "currency": "ZAR",
        "language": "en",
        "locale": "en-ZA",
        "timezone": "Africa/Johannesburg",
        "measurement": "metric",
        "postal_label": "Postal Code",
        "regions": ["Western Cape"],
        "cities": {"cape town": "Western Cape"}
    },
    "nigeria": {
        "name": "Nigeria",
        "currency": "NGN",
        "language": "en",
        "locale": "en-NG",
        "timezone": "Africa/Lagos",
        "measurement": "metric",
        "postal_label": "Postcode",
        "regions": ["Lagos State"],
        "cities": {"lagos": "Lagos State"}
    },
    "kenya": {
        "name": "Kenya",
        "currency": "KES",
        "language": "en",
        "locale": "en-KE",
        "timezone": "Africa/Nairobi",
        "measurement": "metric",
        "postal_label": "Postal Code",
        "regions": ["Nairobi County"],
        "cities": {"nairobi": "Nairobi County"}
    },
    "argentina": {
        "name": "Argentina",
        "currency": "ARS",
        "language": "es",
        "locale": "es-AR",
        "timezone": "America/Buenos_Aires",
        "measurement": "metric",
        "postal_label": "CPA",
        "regions": ["Buenos Aires"],
        "cities": {"buenos aires": "Buenos Aires"}
    },
    "mexico": {
        "name": "Mexico",
        "currency": "MXN",
        "language": "es",
        "locale": "es-MX",
        "timezone": "America/Mexico_City",
        "measurement": "metric",
        "postal_label": "Código Postal",
        "regions": ["CDMX"],
        "cities": {"mexico city": "CDMX"}
    },
    "saudi arabia": {
        "name": "Saudi Arabia",
        "currency": "SAR",
        "language": "ar",
        "locale": "ar-SA",
        "timezone": "Asia/Riyadh",
        "measurement": "metric",
        "postal_label": "Postal Code",
        "regions": ["Riyadh Region"],
        "cities": {"riyadh": "Riyadh Region"}
    },
    "thailand": {
        "name": "Thailand",
        "currency": "THB",
        "language": "th",
        "locale": "th-TH",
        "timezone": "Asia/Bangkok",
        "measurement": "metric",
        "postal_label": "Postal Code",
        "regions": ["Bangkok Metropolis"],
        "cities": {"bangkok": "Bangkok Metropolis"}
    },
    "malaysia": {
        "name": "Malaysia",
        "currency": "MYR",
        "language": "ms",
        "locale": "ms-MY",
        "timezone": "Asia/Kuala_Lumpur",
        "measurement": "metric",
        "postal_label": "Poskod",
        "regions": ["Kuala Lumpur"],
        "cities": {"kuala lumpur": "Kuala Lumpur"}
    },
    "sweden": {
        "name": "Sweden",
        "currency": "SEK",
        "language": "sv",
        "locale": "sv-SE",
        "timezone": "Europe/Stockholm",
        "measurement": "metric",
        "postal_label": "Postnummer",
        "regions": ["Stockholm County"],
        "cities": {"stockholm": "Stockholm County"}
    },
    "norway": {
        "name": "Norway",
        "currency": "NOK",
        "language": "no",
        "locale": "no-NO",
        "timezone": "Europe/Oslo",
        "measurement": "metric",
        "postal_label": "Postnummer",
        "regions": ["Oslo"],
        "cities": {"oslo": "Oslo"}
    },
    "denmark": {
        "name": "Denmark",
        "currency": "DKK",
        "language": "da",
        "locale": "da-DK",
        "timezone": "Europe/Copenhagen",
        "measurement": "metric",
        "postal_label": "Postnummer",
        "regions": ["Capital Region"],
        "cities": {"copenhagen": "Capital Region"}
    },
    "finland": {
        "name": "Finland",
        "currency": "EUR",
        "language": "fi",
        "locale": "fi-FI",
        "timezone": "Europe/Helsinki",
        "measurement": "metric",
        "postal_label": "Postinumero",
        "regions": ["Uusimaa"],
        "cities": {"helsinki": "Uusimaa"}
    },
    "china": {
        "name": "China",
        "currency": "CNY",
        "language": "zh",
        "locale": "zh-CN",
        "timezone": "Asia/Shanghai",
        "measurement": "metric",
        "postal_label": "Postal Code",
        "regions": ["Shanghai", "Hong Kong"],
        "cities": {"shanghai": "Shanghai", "hong kong": "Hong Kong"}
    },
    "south korea": {
        "name": "South Korea",
        "currency": "KRW",
        "language": "ko",
        "locale": "ko-KR",
        "timezone": "Asia/Seoul",
        "measurement": "metric",
        "postal_label": "Postal Code",
        "regions": ["Seoul Capital Area"],
        "cities": {"seoul": "Seoul Capital Area"}
    }
}


class JurisdictionResolver:
    """Parses text prompts to extract origin & destination jurisdictions and determine cross-border status."""

    @staticmethod
    def resolve_from_text(raw_text: str) -> Tuple[Jurisdiction, Optional[Jurisdiction], bool]:
        text_lower = raw_text.lower()

        # Check for relocation patterns like "from X to Y"
        move_match = re.search(r"from\s+([a-z0-9\s,\.-]+?)\s+to\s+([a-z0-9\s,\.-]+?)(?:\s+in|\s+with|\s+for|\.|$)", text_lower)
        
        if move_match:
            origin_str = move_match.group(1).strip()
            dest_str = move_match.group(2).strip()
            
            origin_juris = JurisdictionResolver.parse_location_string(origin_str)
            dest_juris = JurisdictionResolver.parse_location_string(dest_str)
            
            is_cross_border = (origin_juris.country.lower() != dest_juris.country.lower())
            return origin_juris, dest_juris, is_cross_border

        # Single location event
        origin_juris = JurisdictionResolver.parse_location_string(text_lower)
        return origin_juris, None, False

    @staticmethod
    def parse_location_string(location_str: str) -> Jurisdiction:
        location_lower = location_str.lower()
        found_country_key = None
        found_city = None
        found_region = None

        # Search for matched country or alias
        for key, meta in COUNTRY_KNOWLEDGE_BASE.items():
            if key in location_lower:
                target_key = meta.get("alias_for", key)
                found_country_key = target_key
                break

        # Search for matched city
        for c_key, meta in COUNTRY_KNOWLEDGE_BASE.items():
            if "alias_for" in meta:
                continue
            cities = meta.get("cities", {})
            for city_name, region_name in cities.items():
                if city_name in location_lower:
                    found_city = city_name.title()
                    found_region = region_name
                    if not found_country_key:
                        found_country_key = c_key
                    break

        if not found_country_key:
            # Fallback default if unspecified
            found_country_key = "united states"

        meta = COUNTRY_KNOWLEDGE_BASE.get(found_country_key, COUNTRY_KNOWLEDGE_BASE["united states"])
        
        return Jurisdiction(
            country=meta["name"],
            region=found_region or (meta["regions"][0] if meta["regions"] else None),
            city=found_city or (list(meta["cities"].keys())[0].title() if meta["cities"] else None),
            postal_code=None,
            timezone=meta["timezone"],
            currency=meta["currency"],
            language=meta["language"],
            locale=meta["locale"],
            measurement_system=meta["measurement"]
        )
