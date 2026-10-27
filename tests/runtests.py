#!/usr/bin/env python
import argparse
import os
import subprocess
import sys
import warnings
from pathlib import Path

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

warnings.simplefilter("error", DeprecationWarning)


def parse_arguments():
    parser = argparse.ArgumentParser(description="django-experimental test runner")
    parser.add_argument(
        "-s",
        "--settings",
        dest="settings_module",
        default=None,
        help="Python path to settings module (e.g. auth_tests.settings).",
    )
    parser.add_argument(
        "test_labels",
        nargs="*",
        help="Optional test labels to run (e.g. admin_views or auth_tests).",
    )
    return parser.parse_known_args()


def discover_suite_types():
    """
    Categorizes test folders inside tests/ into:
    - isolated_suites: directories containing their own settings.py
    - standard_suites: directories running under the baseline tests.settings
    """
    isolated_suites = {}
    standard_suites = []

    for item in TESTS_DIR.iterdir():
        if (
            item.is_dir()
            and (item / "__init__.py").exists()
            and not item.name.startswith((".", "_"))
        ):
            if (item / "settings.py").exists():
                isolated_suites[item.name] = f"{item.name}.settings"
            else:
                standard_suites.append(item.name)

    return standard_suites, isolated_suites


def run_all_suites():
    standard_suites, isolated_suites = discover_suite_types()

    # Run all standard apps together under baseline settings
    if standard_suites:
        print(f"[django-experimental] Running baseline suites: {', '.join(standard_suites)}")
        cmd = [sys.executable, str(TESTS_DIR / "runtests.py")] + standard_suites
        result = subprocess.run(cmd)
        if result.returncode != 0:
            sys.exit(result.returncode)

    # Run each isolated app in its own dedicated process
    for app_name, app_settings in isolated_suites.items():
        print(f"\n[django-experimental] Running isolated suite '{app_name}' with {app_settings}...")
        cmd = [
            sys.executable,
            str(TESTS_DIR / "runtests.py"),
            f"--settings={app_settings}",
            app_name,
        ]
        result = subprocess.run(cmd)
        if result.returncode != 0:
            sys.exit(result.returncode)

    sys.exit(0)


def run_tests():
    args, test_runner_args = parse_arguments()

    test_labels = args.test_labels
    settings_module = args.settings_module

    # If no arguments provided, run all suites with automatic isolation
    if not test_labels and not settings_module:
        run_all_suites()
        return

    # If a test label was passed without --settings, check if it has a local settings.py
    if settings_module is None and test_labels:
        first_label = test_labels[0].split(".")[0]
        local_settings = TESTS_DIR / first_label / "settings.py"
        if local_settings.exists():
            settings_module = f"{first_label}.settings"

    if settings_module is None:
        settings_module = "tests.settings"

    os.environ["DJANGO_SETTINGS_MODULE"] = settings_module
    django.setup()

    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False)

    failures = test_runner.run_tests(test_labels)
    sys.exit(bool(failures))


if __name__ == "__main__":
    run_tests()