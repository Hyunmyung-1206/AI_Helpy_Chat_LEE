from pathlib import Path

import conftest


class DummyDriver:
    def quit(self):
        pass


def test_start_webdriver_uses_remote_driver_when_selenium_url_is_set(monkeypatch, tmp_path):
    calls = {}

    def fake_remote(command_executor, options):
        calls["remote"] = {
            "command_executor": command_executor,
            "options": options,
        }
        return DummyDriver()

    def fake_chrome(options):
        calls["chrome"] = {"options": options}
        return DummyDriver()

    monkeypatch.setenv("SELENIUM_REMOTE_URL", "http://selenium:4444/wd/hub")
    monkeypatch.setattr(conftest.webdriver, "Remote", fake_remote)
    monkeypatch.setattr(conftest.webdriver, "Chrome", fake_chrome)

    driver = conftest._start_webdriver("chrome", Path(tmp_path))

    assert isinstance(driver, DummyDriver)
    assert calls["remote"]["command_executor"] == "http://selenium:4444/wd/hub"
    assert "chrome" not in calls
