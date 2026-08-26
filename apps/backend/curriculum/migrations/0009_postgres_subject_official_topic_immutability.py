from django.db import migrations

TABLE = "curriculum_subjectofficialtopic"
TRIGGER = f"{TABLE}_no_mutation"


def install_postgres_trigger(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute(
        f"""
        CREATE TRIGGER {TRIGGER}
        BEFORE UPDATE OR DELETE ON {TABLE}
        FOR EACH ROW EXECUTE FUNCTION curriculum_reject_immutable_mutation();
        """
    )


def remove_postgres_trigger(apps, schema_editor):
    if schema_editor.connection.vendor != "postgresql":
        return
    schema_editor.execute(f"DROP TRIGGER IF EXISTS {TRIGGER} ON {TABLE};")


class Migration(migrations.Migration):
    dependencies = [
        ("curriculum", "0008_requirementauthorityplan_condition_expression_and_more"),
    ]

    operations = [
        migrations.RunPython(install_postgres_trigger, remove_postgres_trigger),
    ]
