from django.db import migrations

TABLES = (
    "curriculum_subjectcoveragepolicy",
    "curriculum_subjectcurriculummanifest",
    "curriculum_subjectmanifestleaf",
    "curriculum_scopecoveragerequirement",
    "curriculum_coveragerequirementslot",
    "curriculum_subjectauthorityplan",
    "curriculum_requirementauthorityplan",
    "curriculum_caseauthorityrequirement",
    "curriculum_coveragerequirementsatisfaction",
    "curriculum_subjectcertifiedsubset",
    "curriculum_subjectplanhumanreview",
)


def install_postgres_triggers(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    for table in TABLES:
        trigger = f"{table}_no_mutation"
        schema_editor.execute(
            f"""
            CREATE TRIGGER {trigger}
            BEFORE UPDATE OR DELETE ON {table}
            FOR EACH ROW EXECUTE FUNCTION curriculum_reject_immutable_mutation();
            """
        )


def remove_postgres_triggers(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    for table in TABLES:
        trigger = f"{table}_no_mutation"
        schema_editor.execute(f"DROP TRIGGER IF EXISTS {trigger} ON {table};")


class Migration(migrations.Migration):
    dependencies = [
        ("curriculum", "0006_scopecoveragerequirement_coveragerequirementslot_and_more")
    ]

    operations = [
        migrations.RunPython(install_postgres_triggers, remove_postgres_triggers),
    ]
