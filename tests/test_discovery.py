import json

from benchcalm.cli import main
from benchcalm.features.cpu import CpuFeature


def _write(path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def test_cpu_discovery_reports_policy_without_changing_sysfs(tmp_path) -> None:
    policy = tmp_path / "policy0"
    _write(policy / "scaling_available_governors", "powersave performance\n")
    _write(policy / "scaling_governor", "powersave\n")
    _write(policy / "scaling_min_freq", "800000\n")
    _write(policy / "scaling_max_freq", "3600000\n")
    before = {path: path.read_text(encoding="utf-8") for path in policy.iterdir()}

    report = CpuFeature(tmp_path).discover()

    assert report.id == "cpu"
    assert report.status == "supported"
    assert [control.current for control in report.controls] == [
        "powersave",
        "800000",
        "3600000",
    ]
    assert report.controls[0].available_values == ("powersave", "performance")
    assert {path: path.read_text(encoding="utf-8") for path in policy.iterdir()} == before


def test_cpu_discovery_reports_missing_cpufreq_as_unsupported(tmp_path) -> None:
    report = CpuFeature(tmp_path / "missing").discover()

    assert report.status == "unsupported"
    assert report.controls == ()


def test_discover_cli_outputs_json(capsys) -> None:
    result = main(["discover", "--json"])

    assert result == 0
    assert isinstance(json.loads(capsys.readouterr().out), list)