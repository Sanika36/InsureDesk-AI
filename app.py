
import streamlit as st

from database import (
    initialize_database,
    get_customer_details,
    get_all_tickets
)

from workflow import run_insuredesk


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="InsureDesk AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. CUSTOM CSS
# =====================================================

st.markdown("""
<style>

    .main {
        background-color: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .hero {
        background: linear-gradient(
            120deg,
            #102a43,
            #176b87
        );

        padding: 30px;
        border-radius: 16px;
        color: white;
        margin-bottom: 28px;
    }

    .hero h1 {
        color: white;
        font-size: 34px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .hero p {
        color: #dcecf5;
        font-size: 16px;
        margin-bottom: 0;
    }

    .section-title {
        color: #102a43;
        font-size: 23px;
        font-weight: 650;
        margin-top: 20px;
        margin-bottom: 15px;
    }

    .sidebar-footer {
        color: #64748b;
        font-size: 12px;
    }

    div[data-testid="stMetric"] {
        background-color: white;
        border: 1px solid #e2e8f0;
        padding: 17px;
        border-radius: 12px;
    }

    div[data-testid="stForm"] {
        background-color: white;
        padding: 18px;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        border-radius: 8px;
        font-weight: 600;
    }

</style>
""", unsafe_allow_html=True)


# =====================================================
# 3. DATABASE INITIALIZATION
# =====================================================

initialize_database()


# =====================================================
# 4. COMMON HEADER
# =====================================================



def display_header():

    st.markdown("""
    <div style="
        background: linear-gradient(120deg, #102a43, #176b87);
        padding: 30px;
        border-radius: 15px;
        margin-bottom: 25px;
        color: white;
    ">
        <h1 style="color: white; margin: 0;">
            🛡️ InsureDesk AI
        </h1>
        <p style="
            color: white;
            font-size: 17px;
            margin-top: 10px;
            margin-bottom: 0;
        ">
            Intelligent Insurance Complaint Investigation
            and Customer Support Platform
        </p>
    </div>
    """, unsafe_allow_html=True)


# =====================================================
# 5. SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    st.title("🛡️ InsureDesk AI")

    st.caption("Intelligent Insurance Operations")

    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "AI Investigation",
            "Support Tickets"
        ],
        label_visibility="visible"
    )

    st.divider()

    st.markdown(
        """
        **Technology Stack**

        - Python
        - Google Gemini
        - LangGraph
        - Streamlit
        - SQLite
        """
    )

    st.divider()

    st.markdown(
        """
        <div class="sidebar-footer">

        AI-powered insurance support

        <br><br>

        Demo Version | Synthetic Data Only

        </div>
        """,
        unsafe_allow_html=True
    )


# =====================================================
# 6. DASHBOARD PAGE
# =====================================================

def show_dashboard():

    st.subheader("📊 Operations Overview")

    tickets = get_all_tickets()

    total_tickets = len(tickets)

    high_priority = sum(
        1 for ticket in tickets
        if ticket["priority"] == "High"
    )

    open_tickets = sum(
        1 for ticket in tickets
        if ticket["status"] == "Open"
    )

    # Dashboard statistics

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Support Tickets",
            total_tickets
        )

    with col2:

        st.metric(
            "High Priority Cases",
            high_priority
        )

    with col3:

        st.metric(
            "Open Tickets",
            open_tickets
        )

    st.divider()

    # Recent complaints

    st.subheader("📋 Recent Customer Complaints")

    if tickets:

        recent_tickets = tickets[:10]

        display_columns = [
            "ticket_id",
            "customer_id",
            "query",
            "category",
            "priority",
            "status",
            "created_at"
        ]

        st.dataframe(
            [
                {
                    key: ticket[key]
                    for key in display_columns
                    if key in ticket
                }
                for ticket in recent_tickets
            ],
            width="stretch",
            hide_index=True
        )

    else:

        st.info(
            "No support tickets available. "
            "Start an AI investigation to create one."
        )

    st.divider()

    st.caption(
        "InsureDesk AI | Insurance Operations Dashboard"
    )


# =====================================================
# 7. CUSTOMER INFORMATION CARDS
# =====================================================

def show_customer_information(customer):

    st.subheader("👤 Customer Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Customer Name",
            customer["name"]
        )

    with col2:

        st.metric(
            "Policy ID",
            customer["policy_id"]
        )

    with col3:

        st.metric(
            "Policy Type",
            customer["policy_type"]
        )

    previous = float(customer["previous_premium"])

    current = float(customer["current_premium"])

    increase = current - previous

    percentage = (
        (increase / previous) * 100
        if previous > 0
        else 0
    )

    st.markdown("#### Premium Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Previous Premium",
            f"₹{previous:,.0f}"
        )

    with col2:

        st.metric(
            "Current Premium",
            f"₹{current:,.0f}",
            delta=f"₹{increase:,.0f}"
        )

    with col3:

        st.metric(
            "Premium Increase",
            f"{percentage:.2f}%",
            delta=f"{percentage:.2f}%"
        )


# =====================================================
# 8. AI INVESTIGATION PAGE
# =====================================================

def show_investigation():

    st.subheader("🔍 AI Insurance Investigation")

    st.write(
        """
        Submit a customer complaint and let InsureDesk AI
        investigate it using customer records, policy
        information and the insurance knowledge base.
        """
    )

    # Customer complaint form

    with st.form("investigation_form"):

        customer_id = st.selectbox(
            "Select Customer",
            [
                "CUST001",
                "CUST002",
                "CUST003"
            ]
        )

        customer = get_customer_details(customer_id)

        if customer:

            st.info(
                f"Customer: {customer['name']} | "
                f"Policy: {customer['policy_id']}"
            )

        else:

            st.warning(
                "Customer information is unavailable."
            )

        query = st.text_area(
            "Describe the Customer Complaint",

            placeholder=(
                "Example: My health insurance premium "
                "increased from 12000 to 16000. "
                "Please investigate the reason."
            ),

            height=130
        )

        submitted = st.form_submit_button(
            "🚀 Investigate Complaint",
            width="stretch"
        )

    # Execute workflow

    if submitted:

        if not query.strip():

            st.warning(
                "Please enter a customer complaint."
            )

        elif not customer:

            st.error(
                "Unable to retrieve customer information."
            )

        else:

            try:

                with st.spinner(
                    "InsureDesk AI agents are investigating..."
                ):

                    result = run_insuredesk(
                        customer_id,
                        query
                    )

                st.session_state["last_result"] = result

                st.session_state["last_query"] = query

                st.success(
                    "Investigation completed successfully!"
                )

            except Exception as error:

                st.error(
                    f"Investigation failed: {error}"
                )

    # Display previous investigation result

    result = st.session_state.get("last_result")

    if result:

        st.divider()

        st.subheader("📑 AI Investigation Report")

        # Ticket summary

        col1, col2, col3 = st.columns(3)

        with col1:

            st.metric(
                "Ticket ID",
                f"#{result['ticket_id']}"
            )

        with col2:

            st.metric(
                "Priority",
                result["priority"]
            )

        with col3:

            st.metric(
                "Category",
                result["category"]
            )

        st.divider()

        # Customer details

        customer = result["customer"]

        if customer:

            show_customer_information(customer)

        st.divider()

        # AI findings

        st.subheader("🤖 Investigation Findings")

        st.markdown(
            result["investigation"]
        )

        # Human escalation indicator

        report = result["investigation"].lower()

        if "human escalation" in report:

            st.warning(
                """
                **Human Review Recommended**

                This case requires review by the appropriate
                insurance support or underwriting team.
                """
            )

        else:

            st.info(
                "Review the AI findings before taking action."
            )

        st.success(
            f"Support Ticket #{result['ticket_id']} "
            "has been created successfully."
        )

        st.caption(
            "AI-generated findings are decision-support "
            "information and require human verification."
        )


# =====================================================
# 9. SUPPORT TICKET MANAGEMENT PAGE
# =====================================================

def show_support_tickets():

    st.subheader("📋 Support Ticket Management")

    tickets = get_all_tickets()

    if not tickets:

        st.info(
            "No support tickets have been created yet."
        )

        return

    st.write(
        f"Total registered support tickets: {len(tickets)}"
    )

    st.divider()

    # Display tickets

    for ticket in tickets:

        ticket_id = ticket["ticket_id"]

        category = ticket["category"]

        priority = ticket["priority"]

        status = ticket["status"]

        with st.expander(
            f"Ticket #{ticket_id} | "
            f"{category} | "
            f"{priority}"
        ):

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Ticket ID",
                    f"#{ticket_id}"
                )

            with col2:

                st.metric(
                    "Priority",
                    priority
                )

            with col3:

                st.metric(
                    "Status",
                    status
                )

            st.write(
                "**Customer ID:**",
                ticket["customer_id"]
            )

            st.write(
                "**Customer Complaint:**"
            )

            st.write(
                ticket["query"]
            )

            st.divider()

            st.write(
                "**AI Investigation Report:**"
            )

            st.markdown(
                ticket["resolution"]
            )

            if "human escalation" in ticket["resolution"].lower():

                st.warning(
                    "Human review recommended."
                )

            st.caption(
                f"Created At: {ticket['created_at']}"
            )


# =====================================================
# 10. APPLICATION ROUTING
# =====================================================

display_header()

if page == "Dashboard":

    show_dashboard()

elif page == "AI Investigation":

    show_investigation()

elif page == "Support Tickets":

    show_support_tickets()


# =====================================================
# END OF INSUREDESK AI
# =====================================================
