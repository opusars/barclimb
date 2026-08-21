from django.db import migrations

TRIGGER_FUNCTION = """
CREATE OR REPLACE FUNCTION official_scope_reject_artifact_mutation()
RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'Official source artifacts are immutable; register a new version.';
END;
$$ LANGUAGE plpgsql;
"""

CREATE_TRIGGERS = """
CREATE TRIGGER official_scope_artifact_no_update
BEFORE UPDATE ON official_scope_officialsourceartifact
FOR EACH ROW EXECUTE FUNCTION official_scope_reject_artifact_mutation();
CREATE TRIGGER official_scope_artifact_no_delete
BEFORE DELETE ON official_scope_officialsourceartifact
FOR EACH ROW EXECUTE FUNCTION official_scope_reject_artifact_mutation();
"""

SCOPE_TRIGGER_FUNCTIONS = """
CREATE OR REPLACE FUNCTION official_scope_reject_frozen_scope_mutation()
RETURNS trigger AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        IF OLD.status IN ('ACTIVE', 'SUPERSEDED') THEN
            RAISE EXCEPTION 'Active and superseded scope versions are immutable.';
        END IF;
        RETURN OLD;
    END IF;
    IF OLD.status = 'SUPERSEDED' OR
       (OLD.status = 'ACTIVE' AND NOT (
           NEW.status = 'SUPERSEDED' AND
           (to_jsonb(NEW) - 'status') = (to_jsonb(OLD) - 'status')
       )) THEN
        RAISE EXCEPTION 'Active and superseded scope versions are immutable.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION official_scope_reject_frozen_child_mutation()
RETURNS trigger AS $$
DECLARE old_scope_status text;
DECLARE new_scope_status text;
BEGIN
    SELECT status INTO old_scope_status
    FROM official_scope_officialscopeversion
    WHERE id = OLD.scope_version_id;
    IF TG_OP = 'UPDATE' THEN
        SELECT status INTO new_scope_status
        FROM official_scope_officialscopeversion
        WHERE id = NEW.scope_version_id;
    END IF;
    IF old_scope_status IN ('ACTIVE', 'SUPERSEDED') OR
       new_scope_status IN ('ACTIVE', 'SUPERSEDED') THEN
        RAISE EXCEPTION 'Children of active and superseded scope versions are immutable.';
    END IF;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
"""

CREATE_SCOPE_TRIGGERS = """
CREATE TRIGGER official_scope_version_no_historical_update
BEFORE UPDATE OR DELETE ON official_scope_officialscopeversion
FOR EACH ROW EXECUTE FUNCTION official_scope_reject_frozen_scope_mutation();
CREATE TRIGGER official_scope_item_no_historical_mutation
BEFORE UPDATE OR DELETE ON official_scope_officialscopeitem
FOR EACH ROW EXECUTE FUNCTION official_scope_reject_frozen_child_mutation();
CREATE TRIGGER official_scope_source_no_historical_mutation
BEFORE UPDATE OR DELETE ON official_scope_officialscopesource
FOR EACH ROW EXECUTE FUNCTION official_scope_reject_frozen_child_mutation();
"""

DROP_TRIGGERS = """
DROP TRIGGER IF EXISTS official_scope_artifact_no_update
ON official_scope_officialsourceartifact;
DROP TRIGGER IF EXISTS official_scope_artifact_no_delete
ON official_scope_officialsourceartifact;
DROP FUNCTION IF EXISTS official_scope_reject_artifact_mutation();
DROP TRIGGER IF EXISTS official_scope_version_no_historical_update
ON official_scope_officialscopeversion;
DROP TRIGGER IF EXISTS official_scope_item_no_historical_mutation
ON official_scope_officialscopeitem;
DROP TRIGGER IF EXISTS official_scope_source_no_historical_mutation
ON official_scope_officialscopesource;
DROP FUNCTION IF EXISTS official_scope_reject_frozen_scope_mutation();
DROP FUNCTION IF EXISTS official_scope_reject_frozen_child_mutation();
"""


def install_postgres_triggers(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(TRIGGER_FUNCTION)
        schema_editor.execute(CREATE_TRIGGERS)
        schema_editor.execute(SCOPE_TRIGGER_FUNCTIONS)
        schema_editor.execute(CREATE_SCOPE_TRIGGERS)


def remove_postgres_triggers(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(DROP_TRIGGERS)


class Migration(migrations.Migration):
    dependencies = [("official_scope", "0001_initial")]
    operations = [migrations.RunPython(install_postgres_triggers, remove_postgres_triggers)]
