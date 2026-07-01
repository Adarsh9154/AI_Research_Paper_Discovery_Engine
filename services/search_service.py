from providers.arxiv_provider import ArxivProvider


class SearchService:

    def __init__(self):

        self.provider = ArxivProvider()

    def search(
        self,
        query: str,
        limit: int = 10
    ):

        return self.provider.search(
            query=query,
            limit=limit
        )