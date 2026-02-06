# UniDeal: Campus Marketplace & Auction 🎓

**UniDeal** is a web-based marketplace designed for students to buy, sell, and auction items within the campus ecosystem. Built with a focus on clean architecture and scalable software design.

## 🛠 Tech Stack

* **Backend:** Django (Python)
* **Frontend:** Bootstrap 5, jQuery
* **Database:** SQLite (Development) / PostgreSQL (Production)

---

## 🏗 Software Design Principles

To keep the codebase maintainable as we add the auction feature, we follow these rules:

1. **Service Layer Pattern:** Keep logic out of `views.py`. Complex operations (like processing a bid) should live in `services.py`.
2. **Thin Views, Fat Models/Services:** Views should only handle request parsing and response returning.
3. **DRY (Don't Repeat Yourself):** Use Django template inheritance and custom mixins for repetitive logic.
4. **TDD (Test Driven Development):** Write unit tests for core business logic before implementing the UI.

---

## 🚀 Getting Started

### 1. Prerequisites

* Python 3.10+
* `pip` (Python package manager)

### 2. Installation

```bash
# Clone the repository
git clone <repository-url>
cd unideal

# Create a virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install django

```

### 3. Database Setup

```bash
python manage.py migrate
python manage.py createsuperuser  # Create an admin account
python manage.py runserver

```

---

## 📂 Project Structure

```text
unideal/
├── core/               # Global settings and URL routing
├── templates/          # Global Bootstrap base and shared components
├── marketplace/        # Main app for listings and user profiles
│   ├── services.py     # Business logic (Design Principle: SRP)
│   ├── tests/          # Unit and Integration tests
│   └── static/         # jQuery scripts and custom CSS
├── manage.py
└── .gitignore
├── docs/               # Add diagrams for signup, login here; Files that explain the working of this project and its components

```

---

## 🧪 Testing

We use Django’s built-in testing framework. Ensure all tests pass before pushing to the main branch.

```bash
python manage.py test

```

---

## 🤝 Contribution Guidelines

1. **Branching:** Create a new branch for every feature (`git checkout -b feature/auction-logic`).
2. **Commits:** Use descriptive commit messages (e.g., "Add: Service logic for high-bid validation").
3. **Pull Requests:** All PRs must be reviewed by at least one other team member.
