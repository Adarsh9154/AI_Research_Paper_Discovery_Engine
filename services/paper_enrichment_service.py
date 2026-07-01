from providers.openalex_provider import OpenAlexProvider
from providers.crossref_provider import CrossrefProvider


class PaperEnrichmentService:

    def __init__(self):

        self.openalex = OpenAlexProvider()

        self.crossref = CrossrefProvider()

    def enrich(self, paper):

        enriched = {

            "id": paper.id,

            "title": paper.title,

            "authors": paper.authors,

            "abstract": paper.abstract,

            "publication_year": paper.publication_year,

            "pdf_url": paper.pdf_url,

            "source": paper.source

        }

        # ------------------------
        # OpenAlex
        # ------------------------

        oa = self.openalex.search(
            paper.id
        )

        if oa:

            enriched.update(oa)

        # ------------------------
        # Crossref
        # ------------------------

        doi = enriched.get("doi")

        if doi:

            cr = self.crossref.get_paper(
                doi
            )

            if cr:

                enriched.update(cr)

        return enriched