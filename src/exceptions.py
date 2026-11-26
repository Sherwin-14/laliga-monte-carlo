"""Custom exceptions for the La Liga pipeline.

One specific type per failure mode, so call sites can fail loudly with a
clear message. Raise sites should state what was wrong, what was expected,
and what was received — for example::

    raise ChecksumMismatchError(
        f"{path}: checksum mismatch — expected {expected_sha}, got {actual_sha}"
    )
"""


class PipelineError(Exception):
    """Base class for every error raised by the pipeline.

    Catch this when a caller wants to handle any pipeline failure uniformly,
    without knowing which specific step failed.
    """


class ConfigError(PipelineError):
    """Required configuration or secret is missing or invalid."""


class FetchError(PipelineError):
    """A historical source file could not be downloaded."""


class ChecksumMismatchError(PipelineError):
    """A downloaded file's SHA-256 did not match the manifest entry."""


class ValidationError(PipelineError):
    """A boundary value (API response or CSV row) failed validation."""
