"""Implements Metadata discovery documents, as specified in [RFC8615](https://datatracker.ietf.org/doc/html/rfc8615) and [OpenID Connect Discovery 1.0](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderMetadata)."""

from furl import Path, furl  # type: ignore[import]


def well_known_uri(origin: str, name: str, at_root: bool = True) -> str:
    """
    Return the location of a well-known document on an origin, according to [RFC8615](https://datatracker.ietf.org/doc/html/rfc8615).

    :param origin: origin to use to build the well-known uri.
    :param name: document name to use to build the well-known uri.
    :param at_root: if `True`, assume the well-known document is at root level (as defined in [RFC8615](https://datatracker.ietf.org/doc/html/rfc8615)).
            If `False`, assume the well-known location is per-directory, as defined in [OpenID Connect Discovery 1.0](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderMetadata).
    :return: the well-know uri, relative to origin, where the well-known document named `name` should be found.
    """
    url = furl(origin)
    if at_root:
        url.path = Path(".well-known") / url.path / name
    else:
        url.path.add(Path(".well-known") / name)
    return str(url)


def oidc_discovery_document_url(issuer: str) -> str:
    """
    Given an `issuer` identifier, return the standardised URL where the OIDC discovery document can be retrieved.

    The returned URL is biuilt as specified in [OpenID Connect Discovery 1.0](https://openid.net/specs/openid-connect-discovery-1_0.html#ProviderMetadata).
    :param issuer: an OIDC Authentication Server `issuer`
    :return: the standardised discovery document URL. Note that no attempt to fetch this document is made.
    """
    return well_known_uri(issuer, "openid-configuration", at_root=False)


def oauth2_discovery_document_url(issuer: str) -> str:
    """
    Given an `issuer` identifier, return the standardised URL where the OAuth20 server metadata can be retrieved.

    The returned URL is built as specified in [RFC8414](https://datatracker.ietf.org/doc/html/rfc8414).
    :param issuer: an OAuth20 Authentication Server `issuer`
    :return: the standardised discovery document URL. Note that no attempt to fetch this document is made.
    """
    return well_known_uri(issuer, "oauth-authorization-server", at_root=True)
