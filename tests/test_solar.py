import subprocess
import sys

import energydatamodel as edm
import pytest


def test_import_energydatamodel_does_not_import_pvlib():
    result = subprocess.run(
        [sys.executable, "-c", "import energydatamodel, sys; assert 'pvlib' not in sys.modules"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr


def test_to_pvlib_missing_dep(monkeypatch):
    import builtins

    real_import = builtins.__import__

    def mock_import(name, *args, **kwargs):
        if name == "pvlib":
            raise ImportError
        return real_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", mock_import)
    pv = edm.solar.PVSystem(name="PV-1", capacity=2400, surface_azimuth=180, surface_tilt=25)
    with pytest.raises(ImportError, match="energydatamodel\\[solar\\]"):
        pv.to_pvlib()


def test_to_pvlib_with_pvlib_installed():
    pytest.importorskip("pvlib")
    pv = edm.solar.PVSystem(name="PV-1", capacity=2400, surface_azimuth=180, surface_tilt=25)
    pv_pvlib = pv.to_pvlib()
    assert pv_pvlib.name == "PV-1"
