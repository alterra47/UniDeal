***

# UniDeal: Campus Marketplace & Auction 

**UniDeal** is a web-based marketplace designed for students to buy, sell, and auction items within the campus ecosystem. Built with a focus on clean architecture and scalable software design.

## Tech Stack

* **Backend:** Django (Python)
* **Frontend:** Bootstrap 5, jQuery
* **Database:** SQLite (Development) / PostgreSQL (Production)

---

## Software Design Principles

To keep the codebase maintainable as we add the auction feature, we follow these rules:

1. **Service Layer Pattern:** Keep logic out of `views.py`. Complex operations (like processing a bid) should live in `services.py`.
2. **Thin Views, Fat Models/Services:** Views should only handle request parsing and response returning.
3. **DRY (Don't Repeat Yourself):** Use Django template inheritance and custom mixins for repetitive logic.
4. **TDD (Test Driven Development):** Write unit tests for core business logic before implementing the UI.

---

##  Getting Started

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
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install bcrypt
```

### 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser  # Create an admin account
python manage.py runserver
```

---

##  Endpoints

### Auth & API Routes
| Endpoint | Method | Role | Description |
| :--- | :--- | :--- | :--- |
| `/api/signup/` | `POST` | Any | Register user (JWT) |
| `/api/signin/` | `POST` | Any | Login user (JWT) |
| `/register/` | `GET`, `POST` | Any | Template-based registration |
| `/login/` | `GET`, `POST` | Any | Template-based login |
| `/logout/` | `GET` | Authenticated | Destroy session and logout |

### Marketplace (General & Buyer)
| Endpoint | Method | Role | Description |
| :--- | :--- | :--- | :--- |
| `/` | `GET` | Any | Browse approved products |
| `/product/<id>/` | `GET` | Any | View product details |
| `/product/<id>/interest/` | `POST` | Buyer | Express interest in buying |
| `/product/<id>/comment/` | `POST` | Authenticated | Add a public comment |
| `/product/<id>/report/` | `POST` | Authenticated | Report product to admin |
| `/buyer/interests/` | `GET` | Buyer | View expressed interests |
| `/buyer/history/` | `GET` | Buyer | View past transactions |

### Seller Panel
| Endpoint | Method | Role | Description |
| :--- | :--- | :--- | :--- |
| `/seller/dashboard/` | `GET` | Seller | View product stats & status |
| `/seller/product/add/` | `GET`, `POST` | Seller | Add a new product |
| `/seller/product/<id>/edit/` | `GET`, `POST` | Seller | Update an existing product |
| `/seller/product/<id>/delete/`| `POST` | Seller | Delete a product |
| `/seller/interests/` | `GET` | Seller | View incoming buyer interests |
| `/seller/interest/<id>/respond/`| `POST` | Seller | Accept or reject an interest |
| `/seller/interest/<id>/complete/`| `POST` | Seller | Mark item as sold |
| `/seller/history/` | `GET` | Seller | View past sales |

### Admin Panel
| Endpoint | Method | Role | Description |
| :--- | :--- | :--- | :--- |
| `/admin-panel/login/` | `GET`, `POST` | Any | Admin login portal |
| `/admin-panel/logout/` | `GET` | Admin | Admin logout |
| `/admin-panel/dashboard/` | `GET` | Admin | View platform stats |
| `/admin-panel/products/pending/`| `GET` | Admin | View products awaiting approval |
| `/admin-panel/products/` | `GET` | Admin | View all platform products |
| `/admin-panel/product/<id>/approve/`| `POST` | Admin | Approve a product listing |
| `/admin-panel/product/<id>/reject/` | `POST` | Admin | Reject a product listing |
| `/admin-panel/product/<id>/remove/` | `POST` | Admin | Delete a product from site |
| `/admin-panel/users/` | `GET` | Admin | View all registered users |
| `/admin-panel/seller/<id>/ban/` | `POST` | Admin | Ban a seller & remove products |
| `/admin-panel/reports/` | `GET` | Admin | View unresolved user reports |
| `/admin-panel/report/<id>/resolve/` | `POST` | Admin | Mark a report as resolved |

---

##  Project Structure

```text
unideal/
├── core/               # Business Logic
├── templates/          # Global Bootstrap base and shared components
├── marketplace/        # Main app for listings and user profiles
│   ├── services.py     # (Design Principle: SRP)
│   ├── tests/          # Unit and Integration tests
│   └── static/         # jQuery scripts and custom CSS
├── manage.py
└── .gitignore
├── docs/               # Add diagrams for signup, login here; Files that explain the working of this project and its components
```

---

##  Testing

We use Django’s built-in testing framework. Ensure all tests pass before pushing to the main branch.

```bash
python manage.py test
```

---

## 🤝 Contribution Guidelines

1. **Branching:** Create a new branch for every feature (`git checkout -b feature/auction-logic`).
2. **Commits:** Use descriptive commit messages (e.g., "Add: Service logic for high-bid validation").
3. **Pull Requests:** All PRs must be reviewed by at least one other team member.
