from flask import Blueprint, jsonify, request

from services.search_service import SearchService

search_bp = Blueprint(
    "search",
    __name__
)

search_service = SearchService()


@search_bp.route("/api/search", methods=["GET"])
def search():

    query = request.args.get("query", "").strip()

    if not query:

        return jsonify({

            "success": False,

            "message": "Query is required."

        }), 400

    try:

        papers = search_service.search(

            query=query,

            limit=20

        )

        response = []

        for paper in papers:

            response.append({

                "id": paper.id,

                "title": paper.title,

                "authors": paper.authors,

                "abstract": paper.abstract,

                "publication_year": paper.publication_year,

                "pdf_url": paper.pdf_url,

                "source": paper.source

            })

        return jsonify({

            "success": True,

            "count": len(response),

            "papers": response

        })

    except Exception as e:

        return jsonify({

            "success": False,

            "message": str(e)

        }), 500