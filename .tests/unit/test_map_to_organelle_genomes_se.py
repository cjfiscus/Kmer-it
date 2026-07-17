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


def test_map_to_organelle_genomes_se(conda_prefix):

    with tempfile.TemporaryDirectory() as tmpdir:
        workdir = Path(tmpdir) / "workdir"
        config_path = Path(".tests/unit/map_to_organelle_genomes_se/config")
        data_path = Path(".tests/unit/map_to_organelle_genomes_se/data")
        expected_path = Path(".tests/unit/map_to_organelle_genomes_se/expected")

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
                "results/alignments/c.sam",
                "--snakefile",
                "workflow/Snakefile",
                "-f",
                "--notemp",
                "--show-failed-logs",
                "-j1",
                "--target-files-omit-workdir-adjustment",
                "--allowed-rules",
                "map_to_organelle_genomes_se",
                "--configfile",
                ".tests/integration/config.yaml",
                "--directory",
                workdir,
            ]
            + conda_prefix
        )

        # Check the output byte by byte using cmp/zmp/bzcmp/xzcmp.
        # bwa embeds the invoked thread count (-t N) in the SAM @PG header,
        # which varies between the full multi-threaded run that produced the
        # "expected" snapshot and this isolated single-threaded test run;
        # compare everything except that line, since the alignment records
        # are the part that actually matters.
        import common

        class MapOutputChecker(common.OutputChecker):
            def compare_files(self, expected_file, generated_file, cmp_cmds):
                if expected_file.suffix == ".sam":
                    def without_pg(path):
                        with open(path) as fh:
                            return [line for line in fh if not line.startswith("@PG")]
                    assert without_pg(expected_file) == without_pg(
                        generated_file
                    ), f"{expected_file} and {generated_file} differ (ignoring @PG header)"
                    return
                super().compare_files(expected_file, generated_file, cmp_cmds)

        MapOutputChecker(data_path, expected_path, workdir).check()
