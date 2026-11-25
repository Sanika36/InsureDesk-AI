
import re

POLICY_DOCUMENTS = [
    {
        "section": "Premium Renewal",
        "content": """
        Health insurance policies may have renewal premiums
        that differ from previous years. The applicable
        renewal quotation and pricing terms must be checked
        before confirming the reason for an increase.
        """
    },
    {
        "section": "Hospitalization Coverage",
        "content": """
        Hospitalization coverage is subject to the policy's
        sum insured, waiting periods, exclusions and other
        applicable terms and conditions.
        """
    },
    {
        "section": "Claim Processing",
        "content": """
        Insurance claims require supporting documents.
        Claim processing depends on document verification,
        policy coverage and the insurer's assessment.
        """
    },
    {
        "section": "Policy Renewal",
        "content": """
        Customers should review their renewal notice and
        applicable policy terms before renewing their policy.
        """
    },
    {
        "section": "Complaint Resolution",
        "content": """
        Customer complaints should be recorded and reviewed.
        Complaints that cannot be resolved with available
        information should be escalated to human support.
        """
    }
]

STOP_WORDS = {
    "the", "is", "a", "an", "and", "or", "to", "of",
    "my", "me", "i", "has", "have", "been", "for",
    "in", "on", "with", "what", "why", "how", "can",
    "do", "does", "your", "this", "that", "it"
}


def tokenize(text):
    """Convert text into useful searchable words."""
    words = re.findall(r"[a-z0-9]+", text.lower())

    return {
        word for word in words
        if len(word) > 2 and word not in STOP_WORDS
    }


def search_policy_documents(query):
    """
    Search policy sections using keyword matching.
    Returns the three most relevant sections.
    """

    query_words = tokenize(query)
    results = []

    if not query_words:
        return results

    for document in POLICY_DOCUMENTS:
        section_words = tokenize(document["section"])
        content_words = tokenize(document["content"])

        section_matches = query_words & section_words
        content_matches = query_words & content_words

        score = (
            len(section_matches) * 3
            + len(content_matches)
        )

        if score > 0:
            results.append({
                "section": document["section"],
                "content": document["content"].strip(),
                "score": score
            })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:3]


if __name__ == "__main__":
    test_query = "Why has my health insurance premium increased?"

    print("POLICY SEARCH RESULTS")
    print("Query:", test_query)

    results = search_policy_documents(test_query)

    for result in results:
        print("\nSection:", result["section"])
        print("Score:", result["score"])
        print("Information:", result["content"])
