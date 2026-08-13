import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

from .models import ProfessionalHouseboatDataset500Rows


# =========================================================
# LOAD EMBEDDING MODEL
# =========================================================

MODEL_NAME = "all-MiniLM-L6-v2"

embedding_model = SentenceTransformer(
    MODEL_NAME
)


# =========================================================
# CREATE HOUSEBOAT TEXT
# =========================================================

def create_houseboat_text(boat):
    """
    Converts one houseboat database record
    into searchable text for the RAG system.
    """

    return f"""
Houseboat ID: {boat.houseboatid}
Houseboat Name: {boat.houseboatname}
Location: {boat.location}
Price: ₹{boat.priceinr}
Season: {boat.season}
Bedrooms: {boat.bedrooms}
Capacity: {boat.capacity} guests
AC: {boat.ac}
Luxury: {boat.luxury}
Rating: {boat.rating}
Reviews: {boat.reviewcount}
Bookings: {boat.bookingcount}
Food: {boat.food}
WiFi: {boat.wifi}
Latitude: {boat.latitude}
Longitude: {boat.longitude}
"""


# =========================================================
# LOAD 500-ROW HOUSEBOAT DATASET
# =========================================================

def load_houseboats():

    boats = list(
        ProfessionalHouseboatDataset500Rows.objects.all()
    )

    return boats


# =========================================================
# BUILD RAG KNOWLEDGE BASE
# =========================================================

def build_knowledge_base():

    boats = load_houseboats()

    if not boats:
        return [], None, None

    documents = []

    for boat in boats:

        text = create_houseboat_text(
            boat
        )

        documents.append(text)

    # Create embeddings
    embeddings = embedding_model.encode(
        documents,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    embeddings = np.asarray(
        embeddings,
        dtype="float32"
    )

    # Create FAISS index
    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(
        dimension
    )

    index.add(
        embeddings
    )

    return boats, documents, index


# =========================================================
# SEARCH HOUSEBOATS
# =========================================================

def search_houseboats(
    question,
    top_k=5
):

    boats, documents, index = (
        build_knowledge_base()
    )

    if not boats:

        return []

    # Convert question into embedding
    question_embedding = (
        embedding_model.encode(
            [question],
            convert_to_numpy=True,
            normalize_embeddings=True
        )
    )

    question_embedding = np.asarray(
        question_embedding,
        dtype="float32"
    )

    # Search FAISS
    scores, indices = index.search(
        question_embedding,
        min(top_k, len(documents))
    )

    results = []

    for score, idx in zip(
        scores[0],
        indices[0]
    ):

        if idx < 0:
            continue

        results.append(
            {
                "boat": boats[idx],
                "text": documents[idx],
                "score": float(score),
            }
        )

    return results


# =========================================================
# GENERATE RAG ANSWER
# =========================================================

def generate_answer(
    question,
    results
):

    if not results:

        return (
            "Sorry, I couldn't find any "
            "houseboat information matching "
            "your question."
        )

    # -----------------------------------------------------
    # Build answer from retrieved database records
    # -----------------------------------------------------

    question_lower = question.lower()

    # LOCATION QUESTIONS
    if (
        "location" in question_lower
        or "where" in question_lower
    ):

        answers = []

        for result in results:

            boat = result["boat"]

            answers.append(
                f"{boat.houseboatname} "
                f"is located in {boat.location}."
            )

        return " ".join(
            answers[:3]
        )


    # PRICE QUESTIONS
    if (
        "price" in question_lower
        or "cost" in question_lower
        or "budget" in question_lower
        or "₹" in question
    ):

        answers = []

        for result in results:

            boat = result["boat"]

            answers.append(
                f"{boat.houseboatname} "
                f"costs ₹{boat.priceinr}."
            )

        return " ".join(
            answers[:3]
        )


    # RATING QUESTIONS
    if (
        "rating" in question_lower
        or "rated" in question_lower
        or "review" in question_lower
    ):

        answers = []

        for result in results:

            boat = result["boat"]

            answers.append(
                f"{boat.houseboatname} "
                f"has a rating of "
                f"{boat.rating} with "
                f"{boat.reviewcount} reviews."
            )

        return " ".join(
            answers[:3]
        )


    # BEDROOM QUESTIONS
    if (
        "bedroom" in question_lower
        or "rooms" in question_lower
    ):

        answers = []

        for result in results:

            boat = result["boat"]

            answers.append(
                f"{boat.houseboatname} "
                f"has {boat.bedrooms} bedrooms."
            )

        return " ".join(
            answers[:3]
        )


    # CAPACITY / GUEST QUESTIONS
    if (
        "guest" in question_lower
        or "people" in question_lower
        or "capacity" in question_lower
    ):

        answers = []

        for result in results:

            boat = result["boat"]

            answers.append(
                f"{boat.houseboatname} "
                f"can accommodate "
                f"{boat.capacity} guests."
            )

        return " ".join(
            answers[:3]
        )


    # AC QUESTIONS
    if "ac" in question_lower:

        answers = []

        for result in results:

            boat = result["boat"]

            answers.append(
                f"{boat.houseboatname} "
                f"has AC: {boat.ac}."
            )

        return " ".join(
            answers[:3]
        )


    # WIFI QUESTIONS
    if (
        "wifi" in question_lower
        or "wi-fi" in question_lower
    ):

        answers = []

        for result in results:

            boat = result["boat"]

            answers.append(
                f"{boat.houseboatname} "
                f"has WiFi: {boat.wifi}."
            )

        return " ".join(
            answers[:3]
        )


    # LUXURY QUESTIONS
    if (
        "luxury" in question_lower
        or "premium" in question_lower
    ):

        answers = []

        for result in results:

            boat = result["boat"]

            answers.append(
                f"{boat.houseboatname} "
                f"is a luxury boat: "
                f"{boat.luxury}."
            )

        return " ".join(
            answers[:3]
        )


    # -----------------------------------------------------
    # GENERAL HOUSEBOAT QUESTION
    # -----------------------------------------------------

    answers = []

    for result in results[:3]:

        boat = result["boat"]

        answers.append(
            f"{boat.houseboatname} "
            f"in {boat.location} costs "
            f"₹{boat.priceinr}, has a rating "
            f"of {boat.rating}, and can "
            f"accommodate {boat.capacity} guests."
        )

    return " ".join(
        answers
    )


# =========================================================
# MAIN RAG FUNCTION
# =========================================================

def ask_rag(question):

    if not question:

        return (
            "Please ask me something about "
            "the houseboats."
        )

    # Retrieve relevant houseboats
    results = search_houseboats(
        question,
        top_k=5
    )

    # Generate answer from retrieved data
    answer = generate_answer(
        question,
        results
    )

    return answer