
from typing import TypedDict, Optional
from langgraph.graph import StateGraph, END

from database import (
    initialize_database,
    get_customer_details,
    create_ticket
)

from agents import investigate_complaint


class InsuranceState(TypedDict):
    customer_id: str
    query: str
    customer: Optional[dict]
    investigation: str
    category: str
    priority: str
    ticket_id: Optional[int]


def customer_lookup(state: InsuranceState):
    print("Step 1: Looking up customer...")

    customer = get_customer_details(
        state["customer_id"]
    )

    if customer is None:
        raise ValueError(
            f"Customer {state['customer_id']} not found."
        )

    return {"customer": customer}


def investigation_agent(state: InsuranceState):
    print("Step 2: Investigating complaint using Gemini...")

    result = investigate_complaint(
        state["query"],
        state["customer"]
    )

    return {
        "investigation": result["investigation"]
    }


def ticket_agent(state: InsuranceState):
    print("Step 3: Creating support ticket...")

    query = state["query"].lower()
    report = state["investigation"].lower()

    if any(word in query for word in [
        "premium", "renewal", "price", "payment"
    ]):
        category = "Premium Renewal"

    elif any(word in query for word in [
        "claim", "reimbursement", "hospital"
    ]):
        category = "Claims"

    elif any(word in query for word in [
        "coverage", "covered", "benefit"
    ]):
        category = "Coverage"

    else:
        category = "General Insurance"

    if (
        "human escalation: yes" in report
        or "human escalation:\nyes" in report
    ):
        priority = "High"
    else:
        priority = "Medium"

    ticket_id = create_ticket(
        state["customer_id"],
        state["query"],
        category,
        priority,
        state["investigation"]
    )

    return {
        "category": category,
        "priority": priority,
        "ticket_id": ticket_id
    }


def build_workflow():
    graph = StateGraph(InsuranceState)

    graph.add_node("customer_lookup", customer_lookup)
    graph.add_node("investigation", investigation_agent)
    graph.add_node("ticket_creation", ticket_agent)

    graph.set_entry_point("customer_lookup")

    graph.add_edge("customer_lookup", "investigation")
    graph.add_edge("investigation", "ticket_creation")
    graph.add_edge("ticket_creation", END)

    return graph.compile()


def run_insuredesk(customer_id, query):
    if not customer_id or not query or not query.strip():
        raise ValueError(
            "Customer ID and complaint are required."
        )

    initialize_database()

    workflow = build_workflow()

    initial_state = {
        "customer_id": customer_id,
        "query": query.strip(),
        "customer": None,
        "investigation": "",
        "category": "",
        "priority": "Medium",
        "ticket_id": None
    }

    return workflow.invoke(initial_state)


if __name__ == "__main__":
    try:
        result = run_insuredesk(
            "CUST001",
            "My health insurance premium increased "
            "from 12000 to 16000. Please investigate."
        )

        print("\n========== INSUREDESK REPORT ==========")
        print("\nCustomer:", result["customer"])
        print("\nInvestigation:\n", result["investigation"])
        print("\nCategory:", result["category"])
        print("\nPriority:", result["priority"])
        print("\nTicket ID:", result["ticket_id"])
        print("\n=======================================")

    except Exception as error:
        print("\nWorkflow failed:", error)
