import requests


class CrossrefProvider:

    BASE_URL = "https://api.crossref.org/works"

    def get_paper(self, doi):

        if not doi:
            return None

        url = f"{self.BASE_URL}/{doi}"

        response = requests.get(
            url,
            timeout=30
        )

        if response.status_code != 200:
            return None

        message = response.json()["message"]

        return {

            "doi": message.get("DOI"),

            "publisher": message.get("publisher"),

            "journal": (
                message.get(
                    "container-title",
                    ["Unknown"]
                )[0]
            ),

            "volume": message.get("volume"),

            "issue": message.get("issue"),

            "page": message.get("page"),

            "publication_date":

                message.get(
                    "created",
                    {}
                ).get(
                    "date-time"
                ),

            "license":

                message.get(
                    "license",
                    []
                )
        }