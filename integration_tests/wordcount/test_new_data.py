#!/usr/bin/env python

import argparse
import pathlib

import pytest

from .base import (
    FS_STORAGE_NAME,
    S3_STORAGE_NAME,
    STATIC_MODE_NAME,
    STREAMING_MODE_NAME,
    do_test_persistent_wordcount,
)


@pytest.mark.parametrize("n_cpus", [1, 2, 4])
@pytest.mark.parametrize("pstorage_type", [S3_STORAGE_NAME, FS_STORAGE_NAME])
@pytest.mark.parametrize(
    "n_backfilling_runs,mode",
    [
        (3, STREAMING_MODE_NAME),
        (3, STATIC_MODE_NAME),
    ],
)
def test_integration_new_data(
    n_backfilling_runs, n_cpus, mode, pstorage_type, tmp_path: pathlib.Path
):
    do_test_persistent_wordcount(
        n_backfilling_runs, n_cpus, tmp_path, mode, pstorage_type
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simple persistence test")
    parser.add_argument("--n-backfilling-runs", type=int, default=0)
    parser.add_argument("--n-cpus", type=int, default=1, choices=[1, 2, 4])
    parser.add_argument(
        "--mode",
        type=str,
        choices=[STATIC_MODE_NAME, STREAMING_MODE_NAME],
        default=STREAMING_MODE_NAME,
    )
    parser.add_argument(
        "--pstorage-type",
        type=str,
        choices=["s3", "fs"],
        default="fs",
    )
    args = parser.parse_args()

    do_test_persistent_wordcount(
        args.n_backfilling_runs,
        args.n_cpus,
        pathlib.Path("./"),
        args.mode,
        args.pstorage_type,
    )
