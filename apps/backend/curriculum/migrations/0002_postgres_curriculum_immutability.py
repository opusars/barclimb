from django.db import migrations

FUNCTIONS = """
CREATE OR REPLACE FUNCTION curriculum_reject_immutable_mutation()
RETURNS trigger AS $$
BEGIN
    RAISE EXCEPTION 'Immutable curriculum provenance cannot be changed or deleted.';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION curriculum_reject_frozen_compile_mutation()
RETURNS trigger AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        IF OLD.status IN ('CERTIFIED', 'SUPERSEDED') THEN
            RAISE EXCEPTION 'Certified curriculum history is immutable.';
        END IF;
        RETURN OLD;
    END IF;
    IF OLD.status = 'SUPERSEDED' OR
       (OLD.status = 'CERTIFIED' AND NOT (
           NEW.status = 'SUPERSEDED' AND
           (to_jsonb(NEW) - 'status') = (to_jsonb(OLD) - 'status')
       )) THEN
        RAISE EXCEPTION 'Certified curriculum history is immutable.';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION curriculum_reject_frozen_direct_child()
RETURNS trigger AS $$
DECLARE compile_status text;
BEGIN
    SELECT status INTO compile_status
    FROM curriculum_curriculumcompileversion
    WHERE id = OLD.compile_version_id;
    IF compile_status IN ('CERTIFIED', 'SUPERSEDED') THEN
        RAISE EXCEPTION 'Certified curriculum children are immutable.';
    END IF;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION curriculum_reject_frozen_obligation_child()
RETURNS trigger AS $$
DECLARE compile_status text;
DECLARE obligation_id uuid;
BEGIN
    IF TG_TABLE_NAME = 'curriculum_obligationrelationship' THEN
        obligation_id := OLD.source_id;
    ELSE
        obligation_id := OLD.obligation_id;
    END IF;
    SELECT compile.status INTO compile_status
    FROM curriculum_curriculumcompileversion compile
    JOIN curriculum_ruleobligation obligation
      ON obligation.compile_version_id = compile.id
    WHERE obligation.id = obligation_id;
    IF compile_status IN ('CERTIFIED', 'SUPERSEDED') THEN
        RAISE EXCEPTION 'Certified curriculum children are immutable.';
    END IF;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION curriculum_reject_frozen_review()
RETURNS trigger AS $$
DECLARE compile_status text;
BEGIN
    SELECT compile.status INTO compile_status
    FROM curriculum_curriculumcompileversion compile
    JOIN curriculum_reconciliationissue issue
      ON issue.compile_version_id = compile.id
    WHERE issue.id = OLD.issue_id;
    IF compile_status IN ('CERTIFIED', 'SUPERSEDED') THEN
        RAISE EXCEPTION 'Certified curriculum reviews are immutable.';
    END IF;
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;
"""


TRIGGERS = """
CREATE TRIGGER curriculum_authority_no_mutation
BEFORE UPDATE OR DELETE ON curriculum_authoritysource
FOR EACH ROW EXECUTE FUNCTION curriculum_reject_immutable_mutation();
CREATE TRIGGER curriculum_policy_no_mutation
BEFORE UPDATE OR DELETE ON curriculum_coveragepolicy
FOR EACH ROW EXECUTE FUNCTION curriculum_reject_immutable_mutation();
CREATE TRIGGER curriculum_snapshot_no_mutation
BEFORE UPDATE OR DELETE ON curriculum_coveragereleasesnapshot
FOR EACH ROW EXECUTE FUNCTION curriculum_reject_immutable_mutation();
CREATE TRIGGER curriculum_compile_no_historical_mutation
BEFORE UPDATE OR DELETE ON curriculum_curriculumcompileversion
FOR EACH ROW EXECUTE FUNCTION curriculum_reject_frozen_compile_mutation();
CREATE TRIGGER curriculum_obligation_no_historical_mutation
BEFORE UPDATE OR DELETE ON curriculum_ruleobligation
FOR EACH ROW EXECUTE FUNCTION curriculum_reject_frozen_direct_child();
CREATE TRIGGER curriculum_issue_no_historical_mutation
BEFORE UPDATE OR DELETE ON curriculum_reconciliationissue
FOR EACH ROW EXECUTE FUNCTION curriculum_reject_frozen_direct_child();
CREATE TRIGGER curriculum_mapping_no_historical_mutation
BEFORE UPDATE OR DELETE ON curriculum_obligationscopemapping
FOR EACH ROW EXECUTE FUNCTION curriculum_reject_frozen_obligation_child();
CREATE TRIGGER curriculum_relationship_no_historical_mutation
BEFORE UPDATE OR DELETE ON curriculum_obligationrelationship
FOR EACH ROW EXECUTE FUNCTION curriculum_reject_frozen_obligation_child();
CREATE TRIGGER curriculum_evidence_no_historical_mutation
BEFORE UPDATE OR DELETE ON curriculum_authorityevidence
FOR EACH ROW EXECUTE FUNCTION curriculum_reject_frozen_obligation_child();
CREATE TRIGGER curriculum_review_no_historical_mutation
BEFORE UPDATE OR DELETE ON curriculum_reviewresolution
FOR EACH ROW EXECUTE FUNCTION curriculum_reject_frozen_review();
"""


DROP = """
DROP TRIGGER IF EXISTS curriculum_review_no_historical_mutation
ON curriculum_reviewresolution;
DROP TRIGGER IF EXISTS curriculum_evidence_no_historical_mutation
ON curriculum_authorityevidence;
DROP TRIGGER IF EXISTS curriculum_relationship_no_historical_mutation
ON curriculum_obligationrelationship;
DROP TRIGGER IF EXISTS curriculum_mapping_no_historical_mutation
ON curriculum_obligationscopemapping;
DROP TRIGGER IF EXISTS curriculum_issue_no_historical_mutation
ON curriculum_reconciliationissue;
DROP TRIGGER IF EXISTS curriculum_obligation_no_historical_mutation
ON curriculum_ruleobligation;
DROP TRIGGER IF EXISTS curriculum_compile_no_historical_mutation
ON curriculum_curriculumcompileversion;
DROP TRIGGER IF EXISTS curriculum_snapshot_no_mutation
ON curriculum_coveragereleasesnapshot;
DROP TRIGGER IF EXISTS curriculum_policy_no_mutation
ON curriculum_coveragepolicy;
DROP TRIGGER IF EXISTS curriculum_authority_no_mutation
ON curriculum_authoritysource;
DROP FUNCTION IF EXISTS curriculum_reject_frozen_review();
DROP FUNCTION IF EXISTS curriculum_reject_frozen_obligation_child();
DROP FUNCTION IF EXISTS curriculum_reject_frozen_direct_child();
DROP FUNCTION IF EXISTS curriculum_reject_frozen_compile_mutation();
DROP FUNCTION IF EXISTS curriculum_reject_immutable_mutation();
"""


def install_postgres_triggers(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(FUNCTIONS)
        schema_editor.execute(TRIGGERS)


def remove_postgres_triggers(apps, schema_editor):
    if schema_editor.connection.vendor == "postgresql":
        schema_editor.execute(DROP)


class Migration(migrations.Migration):
    dependencies = [("curriculum", "0001_initial")]
    operations = [migrations.RunPython(install_postgres_triggers, remove_postgres_triggers)]
