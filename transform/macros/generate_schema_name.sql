{% macro generate_schema_name(custom_schema_name, node) -%}
    {# dbt-duckdb's default prefixes schemas with the database name (e.g. main_staging).
       Override it so the `+schema` config maps directly to a DuckDB schema name. #}
    {%- if custom_schema_name is none -%}
        {{ target.schema }}
    {%- else -%}
        {{ custom_schema_name | trim }}
    {%- endif -%}
{%- endmacro %}
