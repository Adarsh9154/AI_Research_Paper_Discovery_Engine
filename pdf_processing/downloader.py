import os
from pathlib import Path

import requests


class PDFDownloader:
    """
    Downloads research papers and stores them locally.
    """

    def __init__(self, download_dir: str = "data/pdfs"):

        self.download_dir = Path(download_dir)

        self.download_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def download(
        self,
        paper_id: str,
        pdf_url: str
    ) -> str:

        filename = f"{paper_id}.pdf"

        pdf_path = self.download_dir / filename

        # Skip if already downloaded
        if pdf_path.exists():

            print("✅ PDF already exists.")

            return str(pdf_path)

        print("⬇ Downloading PDF...")

        response = requests.get(
            pdf_url,
            timeout=60,
            stream=True
        )

        response.raise_for_status()

        with open(pdf_path, "wb") as file:

            for chunk in response.iter_content(
                chunk_size=8192
            ):

                if chunk:
                    file.write(chunk)

        print("✅ PDF Download Complete.")

        return str(pdf_path)