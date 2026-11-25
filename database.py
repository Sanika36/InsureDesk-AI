
import sqlite3
from contextlib import closing
from pathlib import Path

DB_PATH = Path(__file__).parent / "insuredesk.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers (
                customer_id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS policies (
                policy_id TEXT PRIMARY KEY,
                customer_id TEXT,
                policy_type TEXT,
                previous_premium REAL,
                current_premium REAL,
                status TEXT,
                FOREIGN KEY(customer_id)
                REFERENCES customers(customer_id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT,
                query TEXT,
                category TEXT,
                priority TEXT,
                status TEXT,
                resolution TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        customers = [
            ("CUST001", "Rahul Sharma", "rahul@example.com"),
            ("CUST002", "Priya Patel", "priya@example.com"),
            ("CUST003", "Amit Verma", "amit@example.com")
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO customers
            VALUES (?, ?, ?)
        """, customers)

        policies = [
            ("HLTH1001", "CUST001", "Health Insurance",
             12000, 16000, "Active"),
            ("HLTH1002", "CUST002", "Health Insurance",
             10000, 10000, "Active"),
            ("LIFE1003", "CUST003", "Life Insurance",
             15000, 15000, "Active")
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO policies
            VALUES (?, ?, ?, ?, ?, ?)
        """, policies)

        conn.commit()


def get_customer_details(customer_id):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                c.customer_id,
                c.name,
                c.email,
                p.policy_id,
                p.policy_type,
                p.previous_premium,
                p.current_premium,
                p.status
            FROM customers c
            LEFT JOIN policies p
            ON c.customer_id = p.customer_id
            WHERE c.customer_id = ?
        """, (customer_id,))

        result = cursor.fetchone()
        return dict(result) if result else None


def get_all_customers():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM customers
            ORDER BY name
        """)

        return [dict(row) for row in cursor.fetchall()]


def create_ticket(customer_id, query, category,
                  priority, resolution):
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tickets
            (customer_id, query, category, priority,
             status, resolution)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            customer_id,
            query,
            category,
            priority,
            "Open",
            resolution
        ))

        ticket_id = cursor.lastrowid
        conn.commit()

        return ticket_id


def get_all_tickets():
    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM tickets
            ORDER BY created_at DESC
        """)

        return [dict(row) for row in cursor.fetchall()]


def update_ticket_status(ticket_id, status):
    allowed_statuses = ["Open", "In Progress", "Resolved"]

    if status not in allowed_statuses:
        raise ValueError("Invalid ticket status")

    with closing(get_connection()) as conn:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tickets
            SET status = ?
            WHERE ticket_id = ?
        """, (status, ticket_id))

        conn.commit()
        return cursor.rowcount > 0


if __name__ == "__main__":
    initialize_database()

    print("InsureDesk database initialized successfully!")

    print("\nSample customer:")
    print(get_customer_details("CUST001"))

    print("\nAll customers:")
    print(get_all_customers())

    print("\nExisting tickets:")
    print(get_all_tickets())
