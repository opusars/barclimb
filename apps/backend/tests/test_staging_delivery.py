import json
import logging
from pathlib import Path

import pytest
from django.core.mail import EmailMessage
from django.test import override_settings

from config.email_backends import StagingAuthEmailSink


@override_settings(PUBLIC_BASE_URL="https://staging.example.test")
def test_staging_sink_validates_action_shape_without_logging_secret(caplog):
    caplog.set_level(logging.INFO, logger="barclimb.staging_email")
    secret = "credential-that-must-not-be-logged"
    backend = StagingAuthEmailSink()
    assert (
        backend.send_messages(
            [
                EmailMessage(
                    body=f"Complete this action:\nhttps://staging.example.test/reset-password#token={secret}"
                )
            ]
        )
        == 1
    )
    assert secret not in caplog.text
    assert "reset-password" in caplog.text


@override_settings(PUBLIC_BASE_URL="https://staging.example.test")
@pytest.mark.parametrize(
    "link",
    [
        "http://staging.example.test/reset-password#token=x",
        "https://other.example.test/reset-password#token=x",
        "https://staging.example.test/reset-password?token=x",
        "https://staging.example.test/unknown#token=x",
    ],
)
def test_staging_sink_rejects_unsafe_action_links(link):
    with pytest.raises(ValueError):
        StagingAuthEmailSink().send_messages([EmailMessage(body=link)])


def test_web_routes_support_direct_refresh(client, settings, tmp_path):
    settings.WEB_DIST_DIR = tmp_path
    (tmp_path / "index.html").write_text("<html>BarClimb shell</html>")
    assets = tmp_path / "assets"
    assets.mkdir()
    (assets / "app.js").write_text("console.log('barclimb')")
    routes = (
        "/",
        "/login",
        "/signup",
        "/verify-email",
        "/forgot-password",
        "/reset-password",
        "/app",
    )
    for path in routes:
        response = client.get(path)
        assert response.status_code == 200
        assert b"BarClimb shell" in b"".join(response.streaming_content)
    asset = client.get("/assets/app.js")
    assert asset.status_code == 200
    assert asset["Cache-Control"] == "public, max-age=31536000, immutable"


def test_mobile_associations_are_disabled_until_signing_is_verified(client):
    assert client.get("/.well-known/apple-app-site-association").status_code == 404
    assert client.get("/.well-known/assetlinks.json").status_code == 404


@override_settings(
    MOBILE_LINKS_ENABLED=True,
    APPLE_TEAM_ID="TEAMID",
    IOS_BUNDLE_IDENTIFIER="com.barclimb.app.staging",
    ANDROID_PACKAGE_NAME="com.barclimb.app.staging",
    ANDROID_SHA256_CERT_FINGERPRINTS=["AA:BB"],
)
def test_mobile_associations_exclude_web_only_auth_credentials(client):
    apple = client.get("/.well-known/apple-app-site-association").json()
    serialized = json.dumps(apple)
    assert "/app/*" in serialized
    assert "verify-email" not in serialized
    assert "reset-password" not in serialized
    android = client.get("/.well-known/assetlinks.json").json()
    assert android[0]["target"]["sha256_cert_fingerprints"] == ["AA:BB"]


def test_deploy_process_topology_and_root_python_manifest_exist():
    root = Path(__file__).resolve().parents[3]
    procfile = (root / "Procfile").read_text()
    assert all(f"{process}:" in procfile for process in ("web", "worker", "beat", "release"))
    assert (root / "requirements.txt").read_text().strip() == "-r apps/backend/requirements.txt"
