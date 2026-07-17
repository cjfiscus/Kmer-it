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


def test_count_kmers(conda_prefix):

    with tempfile.TemporaryDirectory() as tmpdir:
        workdir = Path(tmpdir) / "workdir"
        config_path = Path(".tests/unit/count_kmers/config")
        data_path = Path(".tests/unit/count_kmers/data")
        expected_path = Path(".tests/unit/count_kmers/expected")

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
                "results/counts/b.jf",
                "results/counts/b.txt.gz",
                "--snakefile",
                "workflow/Snakefile",
                "-f",
                "--notemp",
                "--show-failed-logs",
                "-j1",
                "--target-files-omit-workdir-adjustment",
                "--allowed-rules",
                "count_kmers",
                "--configfile",
                ".tests/integration/config.yaml",
                "--directory",
                workdir,
            ]
            + conda_prefix
        )

        # Check the output byte by byte using cmp/zmp/bzcmp/xzcmp.
        # jellyfish's internal .jf hash-table file is not guaranteed to be
        # byte-identical across runs of identical input, so we only check
        # that it exists and skip the deep comparison for it; the dumped
        # results/counts/{id}.txt.gz is the meaningful output and is still
        # compared byte-for-byte.
        import common

        class CountKmersOutputChecker(common.OutputChecker):
            def compare_files(self, expected_file, generated_file, cmp_cmds):
                if expected_file.suffix == ".jf":
                    return
                super().compare_files(expected_file, generated_file, cmp_cmds)

        CountKmersOutputChecker(data_path, expected_path, workdir).check()
