import requests


class OpenAlexProvider:

    BASE_URL = "https://api.openalex.org/works"

    def search(self, arxiv_id: str):

        try:

            response = requests.get(

                self.BASE_URL,

                params={

                    "filter": f"locations.landing_page_url.search:arxiv.org/abs/{arxiv_id}"

                },

                timeout=30

            )

            if response.status_code != 200:

                print(response.text)

                return None

            results = response.json().get(
                "results",
                []
            )

            if not results:
                return None

            paper = results[0]

            doi = paper.get("doi")

            if doi:
                doi = doi.replace(
                    "https://doi.org/",
                    ""
                )

            return {

                "doi": doi,

                "openalex_id": paper.get("id"),

                "citation_count": paper.get("cited_by_count"),

                "publication_year": paper.get("publication_year"),

                "journal": (
                    paper.get("primary_location", {})
                    .get("source", {})
                    .get("display_name")
                ),

                "concepts": [

                    c["display_name"]

                    for c in paper.get(
                        "concepts",
                        []
                    )

                ],

                "referenced_works": paper.get(
                    "referenced_works",
                    []
                ),

                "related_works": paper.get(
                    "related_works",
                    []
                )

            }

        except Exception as e:

            print("OpenAlex Error:", e)

            return None