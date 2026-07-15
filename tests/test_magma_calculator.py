from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT))

from scripts.utility.magma_calculator import (
    MAX_INPUT_BYTES,
    calculator_url,
    parse_calculator_xml,
    validate_source,
)


def test_parse_success_response() -> None:
    result = parse_calculator_xml(
        b"""<?xml version='1.0'?>
        <calculator><headers><max_time>60</max_time><max_input>50000</max_input>
        <seed>7</seed><version>2.29-8</version><time>0.02</time>
        <memory>32.09MB</memory></headers><results><line>CAP_OK</line>
        <line /></results></calculator>"""
    )

    assert result.status == "ok"
    assert result.version == "2.29-8"
    assert result.max_time == 60
    assert result.lines == ["CAP_OK", ""]


def test_parse_timeout_warning_as_magma_error() -> None:
    result = parse_calculator_xml(
        b"""<calculator><headers><warning>The computation exceeded the time limit.</warning>
        </headers><results><line>START</line></results></calculator>"""
    )

    assert result.status == "magma_error"
    assert result.warnings == ["The computation exceeded the time limit."]
    assert result.lines == ["START"]


def test_validate_source_enforces_public_limit() -> None:
    assert validate_source("x" * MAX_INPUT_BYTES) == MAX_INPUT_BYTES
    with pytest.raises(ValueError, match="calculator limit"):
        validate_source("x" * (MAX_INPUT_BYTES + 1))


def test_calculator_url_contains_encoded_source() -> None:
    url = calculator_url('print "CAP OK";')
    assert url.startswith("http://magma.maths.usyd.edu.au/calc/?input=")
    assert "%22CAP+OK%22" in url
