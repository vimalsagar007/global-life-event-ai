from backend.jurisdiction.resolver import JurisdictionResolver


def test_cross_border_relocation_toronto_london():
    prompt = "I am moving from Toronto, Canada to London, UK"
    orig, dest, is_cross = JurisdictionResolver.resolve_from_text(prompt)

    assert orig.country == "Canada"
    assert orig.city == "Toronto"
    assert dest.country == "United Kingdom"
    assert dest.city == "London"
    assert is_cross is True


def test_domestic_relocation_ny_sf():
    prompt = "I am moving from New York to San Francisco"
    orig, dest, is_cross = JurisdictionResolver.resolve_from_text(prompt)

    assert orig.country == "United States"
    assert orig.city == "New York"
    assert dest.country == "United States"
    assert dest.city == "San Francisco"
    assert is_cross is False


def test_tokyo_singapore():
    prompt = "Relocating from Tokyo, Japan to Singapore"
    orig, dest, is_cross = JurisdictionResolver.resolve_from_text(prompt)

    assert orig.country == "Japan"
    assert dest.country == "Singapore"
    assert is_cross is True
