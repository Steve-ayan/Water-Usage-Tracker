# 🌊 Water Usage Tracker

## Project Overview

This is a full-stack web application developed using the **Django** framework. Its purpose is to provide households with a robust tool for tracking, visualizing, and analyzing their daily water consumption. By offering clear analytics on usage trends and per-member consumption, the app encourages sustainable water management and provides valuable data for civil engineering and environmental analysis.

| Status | Details |
| :--- | :--- |
| **Live URL** | **[https://water-usage-tracker.onrender.com](https://water-usage-tracker.onrender.com)** |
| **Technology**| Django 5.x, PostgreSQL, Bootstrap 5 |
| **Source** | [https://github.com/Steve-ayan/Water-Usage-Tracker](https://github.com/Steve-ayan/Water-Usage-Tracker) |

---

## ✨ Key Features

* **Custom Authentication:** Secure registration and login using a customized Django User Model.
* **Household Management:** Users can create a household, invite other registered members to join, and manage affiliations.
* **Daily Data Logging:** Simple interface for recording daily water consumption in Liters, linked to the user's household.
* **Interactive Dashboard:** Displays charts (powered by **Chart.js**) illustrating historical usage trends.
* **Analytics & Metrics:** Calculates average daily usage per member, total household usage, and more.
* **Responsive Design:** Fully styled with **Bootstrap 5** for seamless use on desktop and mobile devices.

---

## 🛠️ Technology Stack

| Category | Technology | Role in Project |
| :--- | :--- | :--- |
| **Backend** | Python 3.x, Django | Core application logic, ORM, routing, and security. |
| **Database** | PostgreSQL | Robust production database hosted on Render. |
| **Server** | Gunicorn | WSGI HTTP Server to serve the application in production. |
| **Frontend/UI** | HTML, Bootstrap 5 | User interface styling and mobile responsiveness. |
| **Visualization**| Chart.js | Rendering interactive, dynamic usage graphs. |
| **Deployment** | Render, Whitenoise | Hosting the application and serving static files efficiently. |

---

## 💻 Local Installation

To run the application locally for development or testing:

### Prerequisites

* Python 3.10+
* Git

### Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/Steve-ayan/Water-Usage-Tracker.git](https://github.com/Steve-ayan/Water-Usage-Tracker.git)
    cd Water-Usage-Tracker
    ```

2.  **Set up the Virtual Environment:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use: .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Prepare Database (SQLite for local):**
    ```bash
    python manage.py migrate
    ```

5.  **Create an Admin Account (Optional):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the local server:**
    ```bash
    python manage.py runserver
    ```
    Access the application at: `http://127.0.0.1:8000/`

---

## 🚀 Deployment Notes (Render)

The application is hosted on **Render** using a PostgreSQL database.

* **Live Application URL:** `https://water-usage-tracker.onrender.com`
* **Gunicorn** is used as the application server via the `Procfile`.
* **Whitenoise** handles serving static files (CSS/JS).
* `ALLOWED_HOSTS` is explicitly configured to accept the Render live domain to prevent the 400 Bad Request error.

---

## 📝 Usage & Contribution

Feel free to report any issues or suggest features by opening a new issue in the repository.

---