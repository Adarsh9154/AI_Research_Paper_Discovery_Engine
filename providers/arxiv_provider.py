import arxiv

from providers.base_provider import BaseProvider
from models.paper import Paper


class ArxivProvider(BaseProvider):

    def __init__(self):
        self.client = arxiv.Client()

    def search(self, query: str, limit: int = 10):

        search = arxiv.Search(
            query=query,
            max_results=limit,
            sort_by=arxiv.SortCriterion.Relevance
        )

        papers = []

        for result in self.client.results(search):

            paper = Paper(
                id=result.get_short_id(),
                title=result.title,
                authors=", ".join(
                    author.name for author in result.authors
                ),
                abstract=result.summary,
                pdf_url=result.pdf_url,
                publication_year=result.published.year,
                source="arXiv",
                doi=None
            )

            papers.append(paper)

        return papers