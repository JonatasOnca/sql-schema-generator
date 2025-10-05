# Copyright 2025 TecOnca Data Solutions.

from datetime import datetime, date

def convert_datetimes_to_strings(row: dict) -> dict:
    """
    Finds any datetime or date objects in a dictionary
    and converts them to ISO 8601 formatted strings.
    """
    for key, value in row.items():
        if isinstance(value, (datetime, date)):
            row[key] = value.isoformat()
    return row


{% for table in database['tables'] -%}

def map_{{ table['table'] }}_to_dict(row):
    """Mapeia uma linha da tabela '{{ table['table'] }}' para um dicionário."""
    return {
        {% for fields in table['fields_details'] %}
        {%- if fields[1] == 'time' -%}
        "{{ fields[0] }}": row.{{ fields[0] }},
        {%- else -%}
        "{{ fields[0] }}": row.{{ fields[0] }},
        {% endif %}
        {%- endfor -%}
    }


{% endfor -%}


MAP_FUNCTIONS = {
    {% for table in database['tables'] -%}
    "map_{{ table['table'] }}_to_dict": map_{{ table['table'] }}_to_dict,
    {% endfor -%}
}

