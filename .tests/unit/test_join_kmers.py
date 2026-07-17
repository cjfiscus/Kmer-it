"""
Rule test code for unit testing of rules generated with Snakemake 9.23.1.
"""

import os
import sys
import shutil
import tempfile
from pathlib import Path
from subprocess import check_output

sys.path.insert(0, os.path.dirname(__file__))


def test_join_kmers(conda_prefix):

    with tempfile.TemporaryDirectory() as tmpdir:
        workdir = Path(tmpdir) / "workdir"
        config_path = Path(".tests/unit/join_kmers/config")
        data_path = Path(".tests/unit/join_kmers/data")
        expected_path = Path(".tests/unit/join_kmers/expected")

        # Copy config to the temporary workdir.
        shutil.copytree(config_path, workdir)

        # Copy data to the temporary workdir.
        shutil.copytree(data_path, workdir, dirs_exist_ok=True)

        # Copy the sample sheet referenced by the test config; the
        # Snakefile reads it directly at parse time (not via a
        # declared rule input), so it must be present unconditionally.
        (workdir / ".tests" / "integration").mkdir(parents=True, exist_ok=True)
        shutil.copy(
            ".tests/integration/samples.tsv",
            workdir / ".tests" / "integration" / "samples.tsv",
        )

        # Run the test job.
        check_output(
            [
                "python",
                "-m",
                "snakemake",
                "results/count_tbl.txt.gz",
                "--snakefile",
                "workflow/Snakefile",
                "-f",
                "--notemp",
                "--show-failed-logs",
                "-j1",
                "--target-files-omit-workdir-adjustment",
                "--allowed-rules",
                "join_kmers",
                "--configfile",
                ".tests/integration/config.yaml",
                "--directory",
                workdir,
            ]
            + conda_prefix
        )

        # Check the output byte by byte using cmp/zmp/bzcmp/xzcmp.
        # To modify this behavior, you can inherit from common.OutputChecker in here
        # and overwrite the method `compare_files(generated_file, expected_file),
        # also see common.py.
        import common
        common.OutputChecker(data_path, expected_path, workdir).check()
