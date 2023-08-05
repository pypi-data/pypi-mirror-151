#!/usr/bin/env python
"""Linting policy for nf-core pipeline projects.

Tests Nextflow-based pipelines to check that they adhere to
the nf-core community guidelines.
"""

from rich.markdown import Markdown
from rich.table import Table
from rich.panel import Panel
from rich.console import group
import datetime
import git
import json
import logging
import re
import rich
import rich.progress

import nf_core.utils
import nf_core.lint_utils
import nf_core.modules.lint
from nf_core import __version__
from nf_core.lint_utils import console

log = logging.getLogger(__name__)


def run_linting(
    pipeline_dir, release_mode=False, fix=(), key=(), show_passed=False, fail_ignored=False, md_fn=None, json_fn=None
):
    """Runs all nf-core linting checks on a given Nextflow pipeline project
    in either `release` mode or `normal` mode (default). Returns an object
    of type :class:`PipelineLint` after finished.

    Args:
        pipeline_dir (str): The path to the Nextflow pipeline root directory
        release_mode (bool): Set this to `True`, if the linting should be run in the `release` mode.
                             See :class:`PipelineLint` for more information.

    Returns:
        An object of type :class:`PipelineLint` that contains all the linting results.
    """

    # Verify that the requested tests exist
    if key:
        all_tests = set(PipelineLint._get_all_lint_tests(release_mode)).union(
            set(nf_core.modules.lint.ModuleLint._get_all_lint_tests())
        )
        bad_keys = [k for k in key if k not in all_tests]
        if len(bad_keys) > 0:
            raise AssertionError(
                "Test name{} not recognised: '{}'".format(
                    "s" if len(bad_keys) > 1 else "",
                    "', '".join(bad_keys),
                )
            )
        log.info("Only running tests: '{}'".format("', '".join(key)))

    # Create the lint object
    pipeline_keys = list(set(key).intersection(set(PipelineLint._get_all_lint_tests(release_mode)))) if key else []

    lint_obj = PipelineLint(pipeline_dir, release_mode, fix, pipeline_keys, fail_ignored)

    # Load the various pipeline configs
    lint_obj._load_lint_config()
    lint_obj._load_pipeline_config()
    lint_obj._list_files()

    # Create the modules lint object
    module_lint_obj = nf_core.modules.lint.ModuleLint(pipeline_dir)

    # Verify that the pipeline is correctly configured
    try:
        module_lint_obj.has_valid_directory()
    except UserWarning:
        raise

    # Run only the tests we want
    if key:
        # Select only the module lint tests
        module_lint_tests = list(set(key).intersection(set(nf_core.modules.lint.ModuleLint._get_all_lint_tests())))
    else:
        # If no key is supplied, run the default modules tests
        module_lint_tests = ("module_changes", "module_version")
    module_lint_obj.filter_tests_by_key(module_lint_tests)

    # Set up files for modules linting test
    module_lint_obj.set_up_pipeline_files()

    # Run the pipeline linting tests
    try:
        lint_obj._lint_pipeline()
    except AssertionError as e:
        log.critical("Critical error: {}".format(e))
        log.info("Stopping tests...")
        return lint_obj, module_lint_obj

    # Run the module lint tests
    if len(module_lint_obj.all_local_modules) > 0:
        module_lint_obj.lint_modules(module_lint_obj.all_local_modules, local=True)
    if len(module_lint_obj.all_nfcore_modules) > 0:
        module_lint_obj.lint_modules(module_lint_obj.all_nfcore_modules, local=False)

    # Print the results
    lint_obj._print_results(show_passed)
    module_lint_obj._print_results(show_passed)
    nf_core.lint_utils.print_joint_summary(lint_obj, module_lint_obj)
    nf_core.lint_utils.print_fixes(lint_obj, module_lint_obj)

    # Save results to Markdown file
    if md_fn is not None:
        log.info("Writing lint results to {}".format(md_fn))
        markdown = lint_obj._get_results_md()
        with open(md_fn, "w") as fh:
            fh.write(markdown)

    # Save results to JSON file
    if json_fn is not None:
        lint_obj._save_json_results(json_fn)

    # Reminder about --release mode flag if we had failures
    if len(lint_obj.failed) > 0:
        if release_mode:
            log.info("Reminder: Lint tests were run in --release mode.")

    return lint_obj, module_lint_obj


class PipelineLint(nf_core.utils.Pipeline):
    """Object to hold linting information and results.

    Inherits :class:`nf_core.utils.Pipeline` class.

    Use the :func:`PipelineLint._lint_pipeline` function to run lint tests.

    Args:
        path (str): The path to the nf-core pipeline directory.

    Attributes:
        failed (list): A list of tuples of the form: ``(<test-name>, <reason>)``
        ignored (list): A list of tuples of the form: ``(<test-name>, <reason>)``
        lint_config (dict): The parsed nf-core linting config for this pipeline
        passed (list): A list of tuples of the form: ``(<test-name>, <reason>)``
        release_mode (bool): `True`, if you the to linting was run in release mode, `False` else.
        warned (list): A list of tuples of the form: ``(<warned no>, <reason>)``
    """

    from .actions_awsfulltest import actions_awsfulltest
    from .actions_awstest import actions_awstest
    from .actions_ci import actions_ci
    from .actions_schema_validation import actions_schema_validation
    from .files_exist import files_exist
    from .files_unchanged import files_unchanged
    from .merge_markers import merge_markers
    from .modules_json import modules_json
    from .multiqc_config import multiqc_config
    from .nextflow_config import nextflow_config
    from .pipeline_name_conventions import pipeline_name_conventions
    from .pipeline_todos import pipeline_todos
    from .readme import readme
    from .schema_lint import schema_lint
    from .schema_params import schema_params
    from .schema_description import schema_description
    from .template_strings import template_strings
    from .version_consistency import version_consistency

    def __init__(self, wf_path, release_mode=False, fix=(), key=(), fail_ignored=False):
        """Initialise linting object"""

        # Initialise the parent object
        try:
            super().__init__(wf_path)
        except UserWarning:
            raise

        self.lint_config = {}
        self.release_mode = release_mode
        self.fail_ignored = fail_ignored
        self.failed = []
        self.ignored = []
        self.fixed = []
        self.passed = []
        self.warned = []
        self.could_fix = []
        self.lint_tests = self._get_all_lint_tests(self.release_mode)
        self.fix = fix
        self.key = key
        self.progress_bar = None

    @staticmethod
    def _get_all_lint_tests(release_mode):
        return [
            "files_exist",
            "nextflow_config",
            "files_unchanged",
            "actions_ci",
            "actions_awstest",
            "actions_awsfulltest",
            "readme",
            "pipeline_todos",
            "pipeline_name_conventions",
            "template_strings",
            "schema_lint",
            "schema_params",
            "schema_description",
            "actions_schema_validation",
            "merge_markers",
            "modules_json",
            "multiqc_config",
        ] + (["version_consistency"] if release_mode else [])

    def _load(self):
        """Load information about the pipeline into the PipelineLint object"""
        # Load everything using the parent object
        super()._load()

        # Load lint object specific stuff
        self._load_lint_config()

    def _load_lint_config(self):
        """Parse a pipeline lint config file.

        Load the '.nf-core.yml'  config file and extract
        the lint config from it

        Add parsed config to the `self.lint_config` class attribute.
        """
        tools_config = nf_core.utils.load_tools_config(self.wf_path)
        self.lint_config = tools_config.get("lint", {})

        # Check if we have any keys that don't match lint test names
        for k in self.lint_config:
            if k not in self.lint_tests:
                log.warning("Found unrecognised test name '{}' in pipeline lint config".format(k))

    def _lint_pipeline(self):
        """Main linting function.

        Takes the pipeline directory as the primary input and iterates through
        the different linting checks in order. Collects any warnings or errors
        into object attributes: ``passed``, ``ignored``, ``warned`` and ``failed``.
        """
        log.info(f"Testing pipeline: [magenta]{self.wf_path}")
        if self.release_mode:
            log.info("Including --release mode tests")

        # Check that we recognise all --fix arguments
        unrecognised_fixes = list(test for test in self.fix if test not in self.lint_tests)
        if len(unrecognised_fixes):
            raise AssertionError(
                "Unrecognised lint test{} for '--fix': '{}'".format(
                    "s" if len(unrecognised_fixes) > 1 else "", "', '".join(unrecognised_fixes)
                )
            )

        # Check that supplied test keys exist
        bad_keys = [k for k in self.key if k not in self.lint_tests]
        if len(bad_keys) > 0:
            raise AssertionError(
                "Test name{} not recognised: '{}'".format(
                    "s" if len(bad_keys) > 1 else "",
                    "', '".join(bad_keys),
                )
            )

        # If -k supplied, only run these tests
        if self.key:
            self.lint_tests = [k for k in self.lint_tests if k in self.key]

        # Check that the pipeline_dir is a clean git repo
        if len(self.fix):
            log.info("Attempting to automatically fix failing tests")
            try:
                repo = git.Repo(self.wf_path)
            except git.exc.InvalidGitRepositoryError as e:
                raise AssertionError(
                    f"'{self.wf_path}' does not appear to be a git repository, this is required when running with '--fix'"
                )
            # Check that we have no uncommitted changes
            if repo.is_dirty(untracked_files=True):
                raise AssertionError(
                    "Uncommitted changes found in pipeline directory!\nPlease commit these before running with '--fix'"
                )

        self.progress_bar = rich.progress.Progress(
            "[bold blue]{task.description}",
            rich.progress.BarColumn(bar_width=None),
            "[magenta]{task.completed} of {task.total}[reset] » [bold yellow]{task.fields[test_name]}",
            transient=True,
        )
        with self.progress_bar:
            lint_progress = self.progress_bar.add_task(
                "Running lint checks", total=len(self.lint_tests), test_name=self.lint_tests[0]
            )
            for test_name in self.lint_tests:
                if self.lint_config.get(test_name, {}) is False:
                    log.debug("Skipping lint test '{}'".format(test_name))
                    self.ignored.append((test_name, test_name))
                    continue
                self.progress_bar.update(lint_progress, advance=1, test_name=test_name)
                log.debug("Running lint test: {}".format(test_name))
                test_results = getattr(self, test_name)()
                for test in test_results.get("passed", []):
                    self.passed.append((test_name, test))
                for test in test_results.get("ignored", []):
                    if self.fail_ignored:
                        self.failed.append((test_name, test))
                    else:
                        self.ignored.append((test_name, test))
                for test in test_results.get("fixed", []):
                    self.fixed.append((test_name, test))
                for test in test_results.get("warned", []):
                    self.warned.append((test_name, test))
                for test in test_results.get("failed", []):
                    self.failed.append((test_name, test))
                if test_results.get("could_fix", False):
                    self.could_fix.append(test_name)

    def _print_results(self, show_passed):
        """Print linting results to the command line.

        Uses the ``rich`` library to print a set of formatted tables to the command line
        summarising the linting results.
        """

        # Spacing from log messages above
        console.print("")

        log.debug("Printing final results")

        # Helper function to format test links nicely
        @group()
        def format_result(test_results):
            """
            Given an list of error message IDs and the message texts, return a nicely formatted
            string for the terminal with appropriate ASCII colours.
            """
            for eid, msg in test_results:
                tools_version = __version__
                if "dev" in __version__:
                    tools_version = "latest"
                yield Markdown(
                    f"[{eid}](https://nf-co.re/tools/docs/{tools_version}/pipeline_lint_tests/{eid}.html): {msg}"
                )

        def _s(some_list):
            if len(some_list) != 1:
                return "s"
            return ""

        # Table of passed tests
        if len(self.passed) > 0 and show_passed:
            console.print(
                rich.panel.Panel(
                    format_result(self.passed),
                    title=r"[bold][✔] {} Pipeline Test{} Passed".format(len(self.passed), _s(self.passed)),
                    title_align="left",
                    style="green",
                    padding=1,
                )
            )

        # Table of fixed tests
        if len(self.fixed) > 0:
            console.print(
                rich.panel.Panel(
                    format_result(self.fixed),
                    title=r"[bold][?] {} Pipeline Test{} Fixed".format(len(self.fixed), _s(self.fixed)),
                    title_align="left",
                    style="bright_blue",
                    padding=1,
                )
            )

        # Table of ignored tests
        if len(self.ignored) > 0:
            console.print(
                rich.panel.Panel(
                    format_result(self.ignored),
                    title=r"[bold][?] {} Pipeline Test{} Ignored".format(len(self.ignored), _s(self.ignored)),
                    title_align="left",
                    style="grey58",
                    padding=1,
                )
            )

        # Table of warning tests
        if len(self.warned) > 0:
            console.print(
                rich.panel.Panel(
                    format_result(self.warned),
                    title=r"[bold][!] {} Pipeline Test Warning{}".format(len(self.warned), _s(self.warned)),
                    title_align="left",
                    style="yellow",
                    padding=1,
                )
            )

        # Table of failing tests
        if len(self.failed) > 0:
            console.print(
                rich.panel.Panel(
                    format_result(self.failed),
                    title=r"[bold][✗] {} Pipeline Test{} Failed".format(len(self.failed), _s(self.failed)),
                    title_align="left",
                    style="red",
                    padding=1,
                )
            )

    def _print_summary(self):
        def _s(some_list):
            if len(some_list) != 1:
                return "s"
            return ""

        # Summary table
        summary_colour = "red" if len(self.failed) > 0 else "green"
        table = Table(box=rich.box.ROUNDED, style=summary_colour)
        table.add_column(f"LINT RESULTS SUMMARY".format(len(self.passed)), no_wrap=True)
        table.add_row(r"[green][✔] {:>3} Test{} Passed".format(len(self.passed), _s(self.passed)))
        if len(self.fix):
            table.add_row(r"[bright blue][?] {:>3} Test{} Fixed".format(len(self.fixed), _s(self.fixed)))
        table.add_row(r"[grey58][?] {:>3} Test{} Ignored".format(len(self.ignored), _s(self.ignored)))
        table.add_row(r"[yellow][!] {:>3} Test Warning{}".format(len(self.warned), _s(self.warned)))
        table.add_row(r"[red][✗] {:>3} Test{} Failed".format(len(self.failed), _s(self.failed)))
        console.print(table)

    def _get_results_md(self):
        """
        Create a markdown file suitable for posting in a GitHub comment.

        Returns:
            markdown (str): Formatting markdown content
        """
        # Overall header
        overall_result = "Passed :white_check_mark:"
        if len(self.warned) > 0:
            overall_result += " :warning:"
        if len(self.failed) > 0:
            overall_result = "Failed :x:"

        # List of tests for details
        test_failure_count = ""
        test_failures = ""
        if len(self.failed) > 0:
            test_failure_count = "\n-| ❌ {:3d} tests failed       |-".format(len(self.failed))
            test_failures = "### :x: Test failures:\n\n{}\n\n".format(
                "\n".join(
                    [
                        "* [{0}](https://nf-co.re/tools-docs/lint_tests/{0}.html) - {1}".format(
                            eid, self._strip_ansi_codes(msg, "`")
                        )
                        for eid, msg in self.failed
                    ]
                )
            )

        test_ignored_count = ""
        test_ignored = ""
        if len(self.ignored) > 0:
            test_ignored_count = "\n#| ❔ {:3d} tests were ignored |#".format(len(self.ignored))
            test_ignored = "### :grey_question: Tests ignored:\n\n{}\n\n".format(
                "\n".join(
                    [
                        "* [{0}](https://nf-co.re/tools-docs/lint_tests/{0}.html) - {1}".format(
                            eid, self._strip_ansi_codes(msg, "`")
                        )
                        for eid, msg in self.ignored
                    ]
                )
            )

        test_fixed_count = ""
        test_fixed = ""
        if len(self.fixed) > 0:
            test_fixed_count = "\n#| ❔ {:3d} tests had warnings |#".format(len(self.fixed))
            test_fixed = "### :grey_question: Tests fixed:\n\n{}\n\n".format(
                "\n".join(
                    [
                        "* [{0}](https://nf-co.re/tools-docs/lint_tests/{0}.html) - {1}".format(
                            eid, self._strip_ansi_codes(msg, "`")
                        )
                        for eid, msg in self.fixed
                    ]
                )
            )

        test_warning_count = ""
        test_warnings = ""
        if len(self.warned) > 0:
            test_warning_count = "\n!| ❗ {:3d} tests had warnings |!".format(len(self.warned))
            test_warnings = "### :heavy_exclamation_mark: Test warnings:\n\n{}\n\n".format(
                "\n".join(
                    [
                        "* [{0}](https://nf-co.re/tools-docs/lint_tests/{0}.html) - {1}".format(
                            eid, self._strip_ansi_codes(msg, "`")
                        )
                        for eid, msg in self.warned
                    ]
                )
            )

        test_passed_count = ""
        test_passes = ""
        if len(self.passed) > 0:
            test_passed_count = "\n+| ✅ {:3d} tests passed       |+".format(len(self.passed))
            test_passes = "### :white_check_mark: Tests passed:\n\n{}\n\n".format(
                "\n".join(
                    [
                        "* [{0}](https://nf-co.re/tools-docs/lint_tests/{0}.html) - {1}".format(
                            eid, self._strip_ansi_codes(msg, "`")
                        )
                        for eid, msg in self.passed
                    ]
                )
            )

        now = datetime.datetime.now()

        comment_body_text = "Posted for pipeline commit {}".format(self.git_sha[:7]) if self.git_sha is not None else ""
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
        markdown = (
            f"## `nf-core lint` overall result: {overall_result}\n\n"
            f"{comment_body_text}\n\n"
            f"```diff{test_passed_count}{test_ignored_count}{test_fixed_count}{test_warning_count}{test_failure_count}\n"
            "```\n\n"
            "<details>\n\n"
            f"{test_failures}{test_warnings}{test_ignored}{test_fixed}{test_passes}### Run details\n\n"
            f"* nf-core/tools version {nf_core.__version__}\n"
            f"* Run at `{timestamp}`\n\n"
            "</details>\n"
        )

        return markdown

    def _save_json_results(self, json_fn):
        """
        Function to dump lint results to a JSON file for downstream use

        Arguments:
            json_fn (str): File path to write JSON to.
        """

        log.info("Writing lint results to {}".format(json_fn))
        now = datetime.datetime.now()
        results = {
            "nf_core_tools_version": nf_core.__version__,
            "date_run": now.strftime("%Y-%m-%d %H:%M:%S"),
            "tests_pass": [[idx, self._strip_ansi_codes(msg)] for idx, msg in self.passed],
            "tests_ignored": [[idx, self._strip_ansi_codes(msg)] for idx, msg in self.ignored],
            "tests_fixed": [[idx, self._strip_ansi_codes(msg)] for idx, msg in self.fixed],
            "tests_warned": [[idx, self._strip_ansi_codes(msg)] for idx, msg in self.warned],
            "tests_failed": [[idx, self._strip_ansi_codes(msg)] for idx, msg in self.failed],
            "num_tests_pass": len(self.passed),
            "num_tests_ignored": len(self.ignored),
            "num_tests_fixed": len(self.fixed),
            "num_tests_warned": len(self.warned),
            "num_tests_failed": len(self.failed),
            "has_tests_pass": len(self.passed) > 0,
            "has_tests_ignored": len(self.ignored) > 0,
            "has_tests_fixed": len(self.fixed) > 0,
            "has_tests_warned": len(self.warned) > 0,
            "has_tests_failed": len(self.failed) > 0,
            "markdown_result": self._get_results_md(),
        }
        with open(json_fn, "w") as fh:
            json.dump(results, fh, indent=4)

    def _wrap_quotes(self, files):
        """Helper function to take a list of filenames and format with markdown.

        Args:
            files (list): List of filenames, eg::

                ['foo', 'bar', 'baz']

        Returns:
            markdown (str): Formatted string of paths separated by word ``or``, eg::

                `foo` or bar` or `baz`
        """
        if not isinstance(files, list):
            files = [files]
        bfiles = ["`{}`".format(f) for f in files]
        return " or ".join(bfiles)

    def _strip_ansi_codes(self, string, replace_with=""):
        """Strip ANSI colouring codes from a string to return plain text.

        Solution found on Stack Overflow: https://stackoverflow.com/a/14693789/713980
        """
        ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        return ansi_escape.sub(replace_with, string)
