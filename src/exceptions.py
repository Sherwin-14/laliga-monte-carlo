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
