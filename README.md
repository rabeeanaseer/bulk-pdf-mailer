<div align="center">

# 📄 Bulk PDF Report Generator & Email Dispatcher

### Automate report generation and delivery, end to end. Upload a spreadsheet, preview the data, generate personalized PDFs, and send them by email, all from one local app.

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![ReportLab](https://img.shields.io/badge/ReportLab-PDF%20Engine-2E7D32?style=for-the-badge)](https://www.reportlab.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-150458?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](#license)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)](#)

</div>


## 📽️ Overview

<!-- 🎥 Demo video goes here. Add a link, GIF, or embedded clip below. -->



This project takes a common, tedious business task, turning spreadsheet rows into individual PDF reports and emailing each one to its recipient, and automates the whole pipeline. It pairs a Python backend (pandas, ReportLab, smtplib) with a Streamlit interface so anyone on a team, not just a developer, can drop in a spreadsheet, review the data, and trigger a bulk send with confidence.

It was built to demonstrate practical skills in:

* Data processing with **pandas** (reading, validating, and iterating over spreadsheet data)
* Programmatic **PDF generation** with ReportLab (dynamic, styled documents from structured data)
* **Email automation** with smtplib (SMTP integration, attachments, templated content)
* **Front end tooling** with Streamlit (file upload, live preview, forms, progress feedback)
* Thoughtful **UX for risky operations** (dry run mode, row limits, per row success/failure reporting)


## 📑 Table of Contents

* [Overview](#️-overview)
* [Features](#-features)
* [Tech Stack](#-tech-stack)
* [Project Structure](#-project-structure)
* [Getting Started](#-getting-started)
* [Usage Guide](#-usage-guide)
* [Sample Data](#-sample-data)
* [SMTP Setup](#-smtp-setup)
* [Customization](#-customization)
* [Safety Notes](#-safety-notes)
* [Roadmap](#-roadmap)
* [License](#-license)
* [Contact](#-contact)


## ✨ Features

| Feature | Description |
|---|---|
| 🖱️ Drag and drop upload | Upload any `.xlsx` sheet directly in the browser |
| 👀 Live data preview | Review every row before anything is generated or sent |
| 🧩 Column mapping | Pick which columns map to recipient name and email |
| 🧾 Dynamic PDF generation | One styled PDF per row, built on the fly with ReportLab |
| ✉️ Templated emails | Subject and body support `{ColumnName}` placeholders |
| 🧪 Dry run mode | Generate PDFs without sending a single email |
| 🎯 Row limiting | Test on the first N rows before running a full batch |
| 📊 Per row results | Clear success/failure feedback for every recipient |
| 📦 Bulk download | Export all generated PDFs as a single zip |
| 🔒 Session only credentials | SMTP login details are never written to disk |


## 🛠 Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.10+ |
| UI | Streamlit |
| Data handling | pandas, openpyxl |
| PDF generation | ReportLab |
| Email delivery | smtplib (standard library) |


## 📁 Project Structure

```
bulk_pdf_mailer/
├── app.py               Streamlit UI and orchestration logic
├── pdf_generator.py      ReportLab based PDF builder
├── email_sender.py       smtplib email dispatch module
├── sample_data.xlsx      Example spreadsheet for quick testing
├── requirements.txt       Python dependencies
└── README.md
```


## 🚀 Getting Started

### Prerequisites

* Python 3.10 or newer
* An SMTP account (Gmail, Outlook, Yahoo, or any custom mail server)

### Installation

```bash
git clone https://github.com/your-username/bulk-pdf-mailer.git
cd bulk-pdf-mailer
pip install -r requirements.txt
```

### Run the app

```bash
streamlit run app.py
```

The app opens automatically in your browser, typically at `http://localhost:8501`.


## 📘 Usage Guide

1. **Upload** your spreadsheet, or try the included `sample_data.xlsx`.
2. **Preview** the full table to confirm the data looks right.
3. **Map columns**, choosing which one holds the recipient's name and which holds their email.
4. **Write the email template**, using placeholders like `{Name}` or `{InvoiceNumber}` that pull from any column.
5. **Configure SMTP**, selecting a provider preset or entering custom server details.
6. **Dry run first.** Generate PDFs only, then check the output before sending anything.
7. **Send.** Uncheck dry run and run the batch for real. A results table shows the outcome for every row.


## 🧪 Sample Data

`sample_data.xlsx` includes three example rows so you can test the full flow immediately, no setup required beyond installing dependencies.

| Name | Email | InvoiceNumber | Amount | DueDate | Notes |
|---|---|---|---|---|---|
| Ayesha Khan | ayesha.khan@example.com | INV 1001 | 4500 | 2026 07 15 | Q2 consulting services |

Every column in the sheet becomes both a row in the generated PDF and an available placeholder in the email template.


## 📧 SMTP Setup

Most providers require an **app password** rather than your normal login, especially with two factor authentication enabled.

* **Gmail:** Google Account → Security → 2 Step Verification → App passwords
* **Outlook / Office365:** Account security settings → App passwords
* **Yahoo:** Account security → Generate app password

Enter the generated password into the app's SMTP password field. It is kept only in memory for that session.


## 🎨 Customization

The PDF layout lives entirely in `build_pdf()` inside `pdf_generator.py`, built with ReportLab's Platypus layer. You're free to add a logo, adjust colors and fonts, add new sections, or introduce multi page layouts.


## ⚠️ Safety Notes

* Emails send one at a time with a short delay to respect provider rate limits.
* Always test with dry run enabled and a small row limit before a full send.
* SMTP credentials exist only in the running session's memory, never on disk.


## 🗺 Roadmap

* [ ] CC / BCC support per row
* [ ] Retry queue for failed sends
* [ ] PDF theming presets (light, dark, branded)
* [ ] Scheduled sending
* [ ] CSV support alongside Excel


## 📄 License

Distributed under the MIT License. See `LICENSE` for details.


## 👤 Contact

**Your Name**
📧 your.email@example.com
🔗 [LinkedIn](https://linkedin.com/in/your-profile) • [GitHub](https://github.com/your-username) • [Portfolio](https://your-portfolio.com)

<div align="center">

If this project was useful or interesting, consider giving it a ⭐ on GitHub.

</div>
