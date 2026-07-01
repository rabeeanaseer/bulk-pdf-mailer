"""
app.py
------
Streamlit front-end for the Bulk PDF Report Generator & Email Dispatcher.

Run with:
    streamlit run app.py

Workflow:
    1. Drag & drop (or browse to) an Excel file.
    2. Preview the rows that will be turned into PDFs / emails.
    3. Map which columns are the recipient Name and Email.
    4. Enter SMTP credentials (kept only in memory for this session).
    5. Generate PDFs locally, optionally send them by email.
"""

import io
import time
import zipfile
from pathlib import Path

import pandas as pd
import streamlit as st

from email_sender import SMTPConfig, send_email_with_attachment
from pdf_generator import build_pdf

OUTPUT_DIR = Path("generated_reports")

st.set_page_config(page_title="Bulk PDF Report Generator", page_icon="📄", layout="wide")

st.title("📄 Bulk PDF Report Generator & Email Dispatcher")
st.caption("Upload an Excel sheet → preview rows → generate a PDF per row → email it out.")

# ---------------------------------------------------------------------------
# 1. Upload & Preview
# ---------------------------------------------------------------------------
st.header("1. Upload Excel Sheet")

uploaded_file = st.file_uploader(
    "Drag and drop your .xlsx file here",
    type=["xlsx", "xls"],
    help="Each row will become one PDF report and (optionally) one email.",
)

if "df" not in st.session_state:
    st.session_state.df = None

if uploaded_file is not None:
    try:
        st.session_state.df = pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Could not read that Excel file: {e}")
        st.session_state.df = None

df = st.session_state.df

if df is not None:
    st.success(f"Loaded {len(df)} rows, {len(df.columns)} columns.")
    st.dataframe(df, use_container_width=True, height=280)
else:
    st.info("Waiting for a file. Expected shape: one row per recipient, one column per data field "
            "(e.g. Name, Email, InvoiceNumber, Amount, DueDate, ...).")
    st.stop()

# ---------------------------------------------------------------------------
# 2. Column mapping
# ---------------------------------------------------------------------------
st.header("2. Map Columns")

col1, col2 = st.columns(2)
columns = list(df.columns)

# Best-effort auto-detect of Name/Email columns
guess_name = next((c for c in columns if c.lower() in ("name", "full name", "recipient")), columns[0])
guess_email = next((c for c in columns if "email" in c.lower()), columns[0])

with col1:
    name_col = st.selectbox("Which column is the recipient's Name?", columns,
                             index=columns.index(guess_name))
with col2:
    email_col = st.selectbox("Which column is the recipient's Email address?", columns,
                              index=columns.index(guess_email))

report_heading = st.text_input("PDF report heading", value="Monthly Report")

# ---------------------------------------------------------------------------
# 3. Email template
# ---------------------------------------------------------------------------
st.header("3. Email Template")
st.caption("Use {ColumnName} placeholders — they'll be filled in per row, e.g. {Name}, {Amount}.")

default_subject = "Your Report is Ready, {" + name_col + "}"
default_body = (
    "Hi {" + name_col + "},\n\n"
    "Please find your report attached.\n\n"
    "Best regards,\nThe Team"
)

subject_template = st.text_input("Subject", value=default_subject)
body_template = st.text_area("Body", value=default_body, height=140)

# ---------------------------------------------------------------------------
# 4. SMTP settings
# ---------------------------------------------------------------------------
st.header("4. Email Server (SMTP) Settings")
st.caption("Credentials are kept only in this browser session's memory — never written to disk.")

with st.expander("SMTP configuration", expanded=True):
    preset = st.selectbox("Provider preset", ["Custom", "Gmail", "Outlook / Office365", "Yahoo"])
    presets = {
        "Gmail": ("smtp.gmail.com", 587, True, False),
        "Outlook / Office365": ("smtp.office365.com", 587, True, False),
        "Yahoo": ("smtp.mail.yahoo.com", 587, True, False),
        "Custom": ("", 587, True, False),
    }
    host_default, port_default, tls_default, ssl_default = presets[preset]

    c1, c2 = st.columns(2)
    with c1:
        smtp_host = st.text_input("SMTP host", value=host_default)
        smtp_username = st.text_input("SMTP username / email", value="")
        from_name = st.text_input("Sender display name (optional)", value="")
    with c2:
        smtp_port = st.number_input("SMTP port", value=port_default, step=1)
        smtp_password = st.text_input(
            "SMTP password / app password", value="", type="password",
            help="For Gmail/Outlook, generate an 'app password' — don't use your normal login password.",
        )
        use_ssl = st.checkbox("Use SSL (port 465) instead of STARTTLS", value=ssl_default)

# ---------------------------------------------------------------------------
# 5. Generate + send
# ---------------------------------------------------------------------------
st.header("5. Generate & Send")

dry_run = st.checkbox(
    "Dry run — generate PDFs only, do NOT send emails",
    value=True,
    help="Uncheck this only once you've verified everything looks right.",
)

max_rows = st.number_input(
    "Limit to first N rows (0 = all rows)", min_value=0, value=0, step=1,
    help="Useful for testing on a small batch before running the full sheet.",
)

run_button = st.button("🚀 Generate PDFs" + ("" if dry_run else " and Send Emails"), type="primary")

if run_button:
    rows = df.to_dict(orient="records")
    if max_rows > 0:
        rows = rows[:max_rows]

    OUTPUT_DIR.mkdir(exist_ok=True)

    progress = st.progress(0.0)
    status_placeholder = st.empty()
    results = []

    smtp_config = None
    if not dry_run:
        if not smtp_host or not smtp_username or not smtp_password:
            st.error("Please fill in all SMTP fields, or enable Dry Run.")
            st.stop()
        smtp_config = SMTPConfig(
            host=smtp_host,
            port=int(smtp_port),
            username=smtp_username,
            password=smtp_password,
            use_tls=not use_ssl,
            use_ssl=use_ssl,
        )

    for i, row in enumerate(rows):
        recipient_name = str(row.get(name_col, "")).strip() or f"row_{i+1}"
        recipient_email = str(row.get(email_col, "")).strip()
        safe_filename = "".join(c for c in recipient_name if c.isalnum() or c in (" ", "_", "-")).strip()
        pdf_path = OUTPUT_DIR / f"{safe_filename or f'report_{i+1}'}.pdf"

        row_result = {"Row": i + 1, "Name": recipient_name, "Email": recipient_email}

        try:
            build_pdf(row, str(pdf_path), name_field=name_col, report_heading=report_heading)
            row_result["PDF"] = "✅ Created"
        except Exception as e:
            row_result["PDF"] = f"❌ {e}"
            results.append(row_result)
            continue

        if not dry_run:
            try:
                subject = subject_template.format(**row)
                body = body_template.format(**row)
                send_email_with_attachment(
                    smtp_config, recipient_email, subject, body, str(pdf_path), from_name=from_name,
                )
                row_result["Email"] += " — ✅ Sent"
            except Exception as e:
                row_result["Email"] += f" — ❌ {e}"
        else:
            row_result["Email"] += " (not sent — dry run)"

        results.append(row_result)
        progress.progress((i + 1) / len(rows))
        status_placeholder.text(f"Processed {i + 1} / {len(rows)}")
        time.sleep(0.05)  # gentle pacing so you don't trip SMTP rate limits

    st.success("Done!")
    st.dataframe(pd.DataFrame(results), use_container_width=True)

    # Offer a zip download of all generated PDFs
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        for pdf_file in OUTPUT_DIR.glob("*.pdf"):
            zf.write(pdf_file, arcname=pdf_file.name)
    zip_buffer.seek(0)

    st.download_button(
        "⬇️ Download all generated PDFs (.zip)",
        data=zip_buffer,
        file_name="generated_reports.zip",
        mime="application/zip",
    )
