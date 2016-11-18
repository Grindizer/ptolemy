# -*- coding: utf-8 -*-

import glob
import json
import os
import subprocess

from behave import *  # noqa: F403


@when("I run ptolemy against some source files")  # noqa: F405
def step_impl(context):
    src_dir = os.path.abspath(os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "fixtures",
        "src"
    ))
    source_files = glob.glob(os.path.join(src_dir, "*.yaml"))

    context.generated_mappings = {
        get_basename_root(source_file):
            subprocess.check_output(["ptolemy", source_file])
        for source_file in source_files
    }


@then("the generated mappings match the expected mappings")  # noqa: F405, F811
def step_impl(context):
    mappings_dir = os.path.abspath(os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "fixtures",
        "mappings"
    ))
    mapping_files = glob.glob(os.path.join(mappings_dir, "*.json"))

    expected_mappings = {
        get_basename_root(mapping_file): json.load(open(mapping_file))
        for mapping_file in mapping_files
    }

    for name, expected_mapping in expected_mappings.items():
        generated_mapping = context.generated_mappings[name]
        assert expected_mapping == json.loads(generated_mapping)


def get_basename_root(path):
    """Return the extensionless basename of the file described by ``path``.

    Example:
        name = get_basename_root("/path/to/file.json")
        name == "file"  # true

    :param path: A file path.
    :type path: str
    :returns: str

    """
    name, _ = os.path.splitext(os.path.basename(path))
    return name
