# Copyright 2025 TecOnca Data Solutions.

{% for table in database['tables'] -%}
def map_{{ table['table'] }}_to_dict(row):
    """Mapeia uma linha da tabela '{{ table['table'] }}' para um dicionário."""
    return {
        {% for fields in table['fields'] -%}
        "{{ fields[0] }}": row.{{ fields[0] }},
        {% endfor -%}
    }
{% endfor -%}

MAP_FUNCTIONS = {
    {% for table in database['tables'] -%}
    "map_{{ table['table'] }}_to_dict": map_{{ table['table'] }}_to_dict,
    {% endfor -%}
}