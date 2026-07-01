from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    flash
)
from markdown import markdown
from config import Config
from models import db
from api.search_controller import search_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    app.secret_key = Config.SECRET_KEY

    # ==========================================================
    # DATABASE
    # ==========================================================

    db.init_app(app)

    with app.app_context():
        db.create_all()

    # ==========================================================
    # BLUEPRINTS
    # ==========================================================

    app.register_blueprint(search_bp)

    # ==========================================================
    # HOME
    # ==========================================================

    @app.route("/")
    def index():

        return render_template(
            "index.html"
        )

    # ==========================================================
    # SEARCH
    #
    # Paper model (models/paper.py) fields:
    #   id, title, authors (str, comma-joined), abstract,
    #   pdf_url, publication_year (int), source, doi
    #
    # UI templates expect:
    #   paper.authors  → LIST   (template does authors[:3]|join)
    #   paper.summary  → model stores this as "abstract"
    #   paper.published → ISO string (template slices [:4] / [:10])
    #   paper.entry_id → same as id
    # ==========================================================

    @app.route("/search", methods=["GET"])
    def search():

        query = request.args.get(
            "query",
            ""
        ).strip()

        papers = []

        if query:

            from services.search_service import SearchService

            service = SearchService()

            raw_papers = service.search(
                query=query,
                limit=20
            )
            print("\n===== SEARCH RESULTS =====")

            for p in raw_papers:
                print(vars(p))

            # Adapt raw Paper objects → view objects for templates
            papers = [
                _adapt_paper(p)
                for p in raw_papers
            ]

        return render_template(
            "search.html",
            query=query,
            papers=papers
        )

    # ==========================================================
    # PAPER DETAILS
    # Route: GET /paper/<paper_id>
    # search.html links here via url_for('paper_details', paper_id=paper.id)
    #
    # FIX: Do NOT rely on session cache (Flask's 4 KB cookie limit
    # causes silent data loss when caching 20 papers with abstracts).
    # Instead, fetch the paper directly from arXiv by ID — fast,
    # reliable, and always works regardless of session state.
    # ==========================================================

    @app.route("/paper/<path:paper_id>", methods=["GET"])
    def paper_details(paper_id):

        import arxiv

        try:

            client = arxiv.Client()

            search = arxiv.Search(id_list=[paper_id])

            results = list(
                client.results(search)
            )

            if not results:

                flash(
                    "Paper not found on arXiv.",
                    "warning"
                )

                return redirect(
                    url_for("search")
                )

            result = results[0]

            # Build a plain dict and store in session for
            # process_paper / ask_question to use
            paper_data = {

                "id":        result.get_short_id(),

                "title":     result.title,

                "authors":   [
                    author.name
                    for author in result.authors
                ],

                "summary":   result.summary,

                "published": (
                    result.published.strftime("%Y-%m-%d")
                    if result.published
                    else None
                ),

                "pdf_url":   result.pdf_url,

            }

            session["paper"] = paper_data

            return render_template(
                "paper_details.html",
                paper=_make_view(paper_data)
            )

        except Exception as e:

            flash(
                f"Could not load paper: {str(e)}",
                "danger"
            )

            return redirect(
                url_for("search")
            )

    # ==========================================================
    # PROCESS PAPER
    # Route: POST /process/<paper_id>
    # paper_details.html POSTs here with hidden field "paper_title"
    # process_success.html expects variable: paper_title (str)
    # ==========================================================

    @app.route("/process/<path:paper_id>", methods=["POST"])
    def process_paper(paper_id):

        from services.paper_processing_service import (
            PaperProcessingService
        )

        # Hidden field sent by paper_details.html
        paper_title = request.form.get(
            "paper_title",
            ""
        ).strip()

        paper = session.get("paper", {})

        pdf_url = paper.get("pdf_url", "")

        if not pdf_url:

            flash(
                "Paper not found in session. Please view the paper details first.",
                "warning"
            )

            return redirect(
                url_for("search")
            )

        if not paper_title:

            paper_title = paper.get(
                "title",
                "Unknown paper"
            )

        processor = PaperProcessingService()

        processor.process(

            paper_id=paper_id,

            pdf_url=pdf_url

        )

        flash(
            "Paper processed successfully.",
            "success"
        )

        # process_success.html uses {{ paper_title }} — plain string, not object
        return render_template(

            "process_success.html",

            paper_title=paper_title

        )

    # ==========================================================
    # AI ASSISTANT
    # assistant.html uses only: conversation (list of dicts)
    # ==========================================================

    @app.route("/assistant", methods=["GET"])
    def assistant():

        paper = session.get("paper")

        conversation = session.get(
            "conversation",
            []
        )

        return render_template(

            "assistant.html",

            paper=paper,

            conversation=conversation

        )

    # ==========================================================
    # ASK QUESTION
    # FIX: original used url_for("home") which does not exist
    #      → corrected to url_for("assistant")
    # ==========================================================

    @app.route("/ask_question", methods=["POST"])
    def ask_question():

        paper = session.get("paper")

        if paper is None:

            flash(
                "Please process a paper first.",
                "warning"
            )

            return redirect(
                url_for("assistant")
            )

        question = request.form.get(
            "question",
            ""
        ).strip()

        if not question:

            flash(
                "Please enter a question.",
                "warning"
            )

            return redirect(
                url_for("assistant")
            )

        from services.rag_service import RAGService

        rag = RAGService()

        answer = rag.ask(question)
        answer = markdown(
    answer,
    extensions=[
        "fenced_code",
        "tables",
        "nl2br"
    ]
)

        conversation = session.get(
            "conversation",
            []
        )

        conversation.append({

            "question": question,

            "answer": answer

        })

        session["conversation"] = conversation

        return render_template(

            "assistant.html",

            paper=paper,

            conversation=conversation

        )

    # ==========================================================
    # CLEAR CHAT
    # ==========================================================

    @app.route("/clear_chat", methods=["POST"])
    def clear_chat():

        session.pop(
            "conversation",
            None
        )

        flash(
            "Conversation cleared.",
            "success"
        )

        return redirect(
            url_for("assistant")
        )

    return app


# ------------------------------------------------------------------
# _adapt_paper: convert a raw Paper dataclass → view object
# for search results (no arXiv re-fetch needed here).
# ------------------------------------------------------------------

def _adapt_paper(paper):

    authors_list = [
        a.strip()
        for a in paper.authors.split(",")
        if a.strip()
    ]

    published_str = (
        f"{paper.publication_year}-01-01"
        if paper.publication_year
        else None
    )

    data = {

        "id":        paper.id,

        "title":     paper.title,

        "authors":   authors_list,

        "summary":   paper.abstract,

        "published": published_str,

        "pdf_url":   paper.pdf_url,

    }

    return _make_view(data)


# ------------------------------------------------------------------
# _make_view: build a dot-notation view object from a paper dict
# so Jinja templates can use paper.title, paper.authors, etc.
# ------------------------------------------------------------------

def _make_view(data):

    class PaperView:
        pass

    view = PaperView()

    view.id        = data["id"]
    view.title     = data["title"]
    view.authors   = data["authors"]    # list
    view.summary   = data["summary"]
    view.published = data["published"]  # "YYYY-MM-DD" or None
    view.pdf_url   = data["pdf_url"]
    view.entry_id  = data["id"]         # paper_details.html checks entry_id

    return view


app = create_app()


if __name__ == "__main__":

    app.run(
        debug=True
    )