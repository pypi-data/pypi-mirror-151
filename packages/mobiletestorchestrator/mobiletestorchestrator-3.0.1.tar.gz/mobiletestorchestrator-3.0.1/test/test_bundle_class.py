import os
import zipfile
from pathlib import Path

from mobiletestorchestrator.tooling.bundle import Bundle


class TestBundle:

    def test_bundle_create(self, tmp_path: Path, support_app, support_test_app):
        mp_tmp_dir = tmp_path / "bundle"
        mp_tmp_dir.mkdir(exist_ok=True)
        shiv_path = mp_tmp_dir.joinpath("test.pyz")
        Bundle.create(shiv_path=shiv_path, test_apk=support_test_app, app_apk=support_app)
        assert os.path.isfile(str(mp_tmp_dir.joinpath("test.pyz")))
        with zipfile.ZipFile(shiv_path) as zfile:
            filelist = [item.filename for item in zfile.filelist]
            assert "site-packages/mobiletestorchestrator/resources/apks/app-debug.apk" in filelist
            assert "site-packages/mobiletestorchestrator/resources/apks/app-debug-androidTest.apk" in filelist
