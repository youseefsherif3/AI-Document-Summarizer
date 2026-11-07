import pytest

import app.database as database


@pytest.fixture(autouse=True)
def isolated_database(monkeypatch, tmp_path):
    monkeypatch.setattr(database, "DATABASE_NAME", str(tmp_path / "documents.db"))
