from django.db import connection
from django.db import migrations


def create_extension(ext_name):
    """Checking if Postgres extension is installed"""
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * FROM pg_catalog.pg_extension WHERE extname='{ext_name}'")
        res = cursor.fetchone()
        if res is None:
            cursor.execute(f"CREATE EXTENSION {ext_name}")


def enable_extensions(apps, schema_editor):
    create_extension('pg_trgm')
    create_extension('unaccent')


def create_imm_unaccent_stored_proc(apps, schema_editor):
    """
    This stored procedure is needed to build GIN index on unaccented words,
    to allow searching without regards for accents (a=ą)
    """

    with connection.cursor() as cursor:
        cursor.execute("""
            CREATE OR REPLACE FUNCTION imm_unaccent(text) RETURNS text AS
            $$
            SELECT public.unaccent('public.unaccent', $1)
            $$ LANGUAGE sql IMMUTABLE;
        """)


class Migration(migrations.Migration):
    dependencies = []
    operations = [
        migrations.RunPython(enable_extensions),
        migrations.RunPython(create_imm_unaccent_stored_proc),
    ]
