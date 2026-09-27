#!/usr/bin/env python
from pathlib import Path
import os
import sys

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

SRC_DIR = REPO_ROOT / "src"
if SRC_DIR.exists():
    sys.path.insert(0, str(SRC_DIR))

TESTS_DIR = REPO_ROOT / "tests"
if TESTS_DIR.exists():
    sys.path.insert(0, str(TESTS_DIR))

import django
from django.conf import settings
from django.test.utils import get_runner
import warnings

# Catch deprecated APIs 
warnings.simplefilter("error", DeprecationWarning)


def run_tests():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tests.settings")
    django.setup()
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False)

    test_labels = sys.argv[1:] if len(sys.argv) > 1 else None

    failures = test_runner.run_tests(test_labels)
    sys.exit(bool(failures))


if __name__ == "__main__":
    run_tests()