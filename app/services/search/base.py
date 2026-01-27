class SearchProviderError(Exception):
    pass
class SearchAuthError(SearchProviderError):
    pass
class SearchRateLimitError(SearchProviderError):
    pass
class SearchUpstreamError(SearchProviderError):
    pass