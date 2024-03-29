# Copyright 2023 neomadas-dev
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#   1. Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#   2. Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#   3. Neither the name of the copyright holder nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
# IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
# TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
# PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
# PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
# LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import subprocess
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError, CommandParser

try:
    import coverage
except ImportError as error:
    raise CommandError("coverage package not installed") from error


class Command(BaseCommand):
    help = "Validate coverage (ci)."

    def add_arguments(self, parser: CommandParser):
        parser.add_argument("test-module", help="Test module base")
        parser.add_argument("rate", help="At least rate coverage", type=float)

    def handle(self, *args, **options):
        basedir = Path(settings.BASE_DIR)

        if not basedir.is_dir():
            raise CommandError(f"Invalid project directory: {basedir}")

        if not (basedir / "manage.py").exists():
            raise CommandError(f"No project directory: {basedir}")

        testmodule = options["test-module"]
        try:
            subprocess.run(
                " ".join(
                    (
                        "coverage",
                        "run",
                        "--source=.",
                        "manage.py",
                        "test",
                        testmodule,
                    )
                ),
                shell=True,
                check=True,
            )
        except subprocess.CalledProcessError:
            raise CommandError(f"Coverage execution: {coverage.__version__}")
        report = subprocess.run(
            ["coverage", "report", "--skip-covered", "--skip-empty"],
            capture_output=True,
        )
        totalline = report.stdout.decode().split("\n")[-4].split()
        rate = float(totalline[-1][:-1])
        expectedRate = options["rate"]
        if rate < expectedRate:
            raise ValueError(f"Coverage rate failed: {rate} < {expectedRate}")
