import os
import stat
import subprocess
import sys
import tempfile


THIS_PATH = os.path.abspath(os.path.dirname(__file__))
ROOT_PATH = os.path.join(THIS_PATH, "..")
PULUMILOCAL_BIN = os.path.join(ROOT_PATH, "bin", "pulumilocal")


def test_missing_pulumi_exits_with_error():
    env = os.environ.copy()
    env["PULUMI_CMD"] = "nonexistent-pulumi-binary-xyz"

    proc = subprocess.run(
        [sys.executable, PULUMILOCAL_BIN, "version"],
        env=env,
        capture_output=True,
        timeout=5,
    )

    assert proc.returncode == 1
    stderr = proc.stderr.decode("utf-8")
    assert "Error: Unable to find 'nonexistent-pulumi-binary-xyz' executable in PATH." in stderr
    assert "Please ensure Pulumi is installed" in stderr


def test_pulumi_cmd_pulumilocal_self_reference_error():
    env = os.environ.copy()
    env["PULUMI_CMD"] = PULUMILOCAL_BIN

    proc = subprocess.run(
        [sys.executable, PULUMILOCAL_BIN, "version"],
        env=env,
        capture_output=True,
        timeout=5,
    )

    assert proc.returncode == 1
    stderr = proc.stderr.decode("utf-8")
    assert "Error" in stderr
    assert ("Unable to find 'pulumi'" in stderr or "points to pulumilocal itself" in stderr)


def test_custom_pulumi_cmd_execution():
    with tempfile.TemporaryDirectory() as tmpdir:
        mock_pulumi = os.path.join(tmpdir, "mock_pulumi")
        with open(mock_pulumi, "w") as f:
            f.write("#!/bin/sh\necho 'mock pulumi 3.0.0'\n")
        os.chmod(mock_pulumi, os.stat(mock_pulumi).st_mode | stat.S_IEXEC)

        env = os.environ.copy()
        env["PULUMI_CMD"] = mock_pulumi

        proc = subprocess.run(
            [sys.executable, PULUMILOCAL_BIN, "version"],
            env=env,
            capture_output=True,
            timeout=5,
        )

        assert proc.returncode == 0
        assert "mock pulumi 3.0.0" in proc.stdout.decode("utf-8")
