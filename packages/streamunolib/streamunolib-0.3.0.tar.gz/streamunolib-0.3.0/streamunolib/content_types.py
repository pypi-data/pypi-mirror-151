"""This package contains tools to annotate transform outputs with a content type."""
from __future__ import annotations

import mimetypes
from dataclasses import dataclass
from typing import Literal, Mapping


@dataclass(frozen=True)
class ContentType:
    """The Content Type class."""

    mimetype: str

    @classmethod
    def from_ext(cls, ext: str) -> ContentType:
        """Content factory from file extension.

        Parameters:
            extension: The file extension for which the MIME type is requested.

        Returns:
            The ContentType instance associated with the extension.

        Examples:
            >>> ContentType.from_ext('wav')
            ContentType(mimetype='audio/wav')
        """
        ext = ext.lower()
        mimetype, _ = mimetypes.guess_type(f'http://file.{ext}')
        if mimetype is None:
            raise ValueError(f'No MIME type known for extension {ext!r}')
        return ContentType(mimetype)


def content_type(ext: str) -> Mapping[Literal['content_type'], str]:
    """Returns a mapping to annotate a content type.

    Parameters:
        extension: The file extension for which the MIME type is requested.

    Returns:
        The mapping {'content_type': mimetype} where mimetype is inferred from
        the extension.

    Examples:
        >>> content_type('wav')
        {'content_type': 'audio/wav'}
    """
    return {'content_type': ContentType.from_ext(ext).mimetype}
