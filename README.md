# IBM Full Stack Application Development Capstone — Dealership Web Application

[![CI/CD Pipeline - Dealership Capstone](https://github.com/belozov/fullstack-developer-capstone-dealership/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/belozov/fullstack-developer-capstone-dealership/actions/workflows/ci-cd.yml)
![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
![Django 4.2](https://img.shields.io/badge/django-4.2-green.svg)
![React 18](https://img.shields.io/badge/react-18-61dafb.svg)
![Node 18](https://img.shields.io/badge/node-18-brightgreen.svg)
![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-yellowgreen.svg)

A cloud-native, microservices-based full-stack web application designed for a national car dealership retailer with branches across the United States. This platform empowers prospective car buyers to browse nationwide dealerships, filter locations by state, inspect detailed dealership profiles, view community reviews enriched with real-time sentiment analysis, and post verified feedback using an interactive car-selection experience.

---

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Key Features](#key-features)
4. [Microservices & Endpoints](#microservices--endpoints)
5. [Database Design](#database-design)
6. [Local Installation & Setup](#local-installation--setup)
7. [Running the Application](#running-the-application)
8. [Testing & Quality Assurance](#testing--quality-assurance)
9. [Containerization & Kubernetes](#containerization--kubernetes)
10. [CI/CD Pipeline](#cicd-pipeline)
11. [Production Deployment](#production-deployment)
12. [Submission Verification Checklist](#submission-verification-checklist)
13. [Author & Attribution](#author--attribution)

---

## Architecture Overview

The application follows a distributed microservices architecture coordinated by a Django API gateway and web application core:

```
                                  +-----------------------------+
                                  |     Client Web Browser      |
                                  | (React SPA / Responsive UI) |
                                  +--------------+--------------+
                                                 |
                                         HTTPS / REST API
                                                 |
                                                 v
                                  +-----------------------------+
                                  |    Django Application Core  |
                                  |   (Port 8000 / SQLite DB)   |
                                  | - Auth / Session Management |
                                  | - Car Models & Makes API    |
                                  | - Static Asset Server       |
                                  | - Proxy to Microservices    |
                                  +------+---------------+------+
                                         |               |
                    Internal HTTP Calls  |               |  Internal HTTP Calls
                    (Dealer & Review)    |               |  (Sentiment Analysis)
                                         v               v
                +----------------------------+   +----------------------------+
                |  Express / Node Microservice|   |   Flask Sentiment Service  |
                |   (Port 3030 / MongoDB)    |   |     (Port 5050 / NLTK)     |
                | - Dealerships CRUD & Query |   | - VADER Polarity Scoring   |
                | - Reviews CRUD & Query     |   | - Positive / Neutral / Neg |
                +----------------------------+   +----------------------------+
```

### Component Breakdown
1. **Frontend (React 18 & HTML5/Bootstrap)**:
   - Dynamic Single Page Application (SPA) components located in `server/frontend/src/`
   - Static pages (`About.html`, `Contact.html`, `Home.html`) for marketing and contact
   - Integrated state filtering, modal car pickers, and real-time sentiment visual indicators
2. **Backend Gateway & Auth (Django 4.2)**:
   - User authentication, registration, session cookies, and administrative workflows
   - Relational database schema (SQLite) managing `CarMake` and `CarModel` entities
   - REST endpoints bridging client requests to underlying backend microservices
3. **Dealership & Review Microservice (Node.js / Express)**:
   - High-throughput JSON microservice running on port `3030`
   - Serves dealer records across all 50 US states and associated customer reviews
   - Backed by MongoDB and fault-tolerant in-memory document data stores
4. **Sentiment Analysis Microservice (Python / Flask & NLTK)**:
   - Dedicated microservice running on port `5050`
   - Evaluates review content using NLTK VADER polarity scoring
   - Categorizes sentiments into `positive`, `neutral`, or `negative`

---

## Technology Stack

| Layer | Technologies |
|---|---|
| **Frontend** | React 18, JavaScript (ES6+), HTML5, CSS3, Bootstrap 5 |
| **Backend Gateway** | Python 3.12, Django 4.2, Django REST Framework, Gunicorn |
| **Microservices** | Node.js 18, Express 4.x, Flask 3.x, NLTK VADER |
| **Databases** | MongoDB (dealerships & reviews), SQLite 3 (Django users & car catalog) |
| **Containerization** | Docker, Docker Compose, Kubernetes manifests |
| **CI/CD** | GitHub Actions Automated Build, Lint & Test Pipeline |
| **Security & Auth** | Django session authentication, CSRF validation, CORS headers |

---

## Key Features

- **User Authentication**: Secure multi-field user registration (Username, First Name, Last Name, Email, Password), session-based login, and instant logout.
- **Django Administration**: Fully customized admin panel with tabular inlines for `CarModel` within `CarMake`, search indexing, and filtering.
- **Dealership Directory**: Interactive grid showcasing dealerships with state-level dropdown filtering and real-time DOM updates.
- **Dealership Profiles**: Dedicated views displaying full dealership metadata (address, zip code, state, city) alongside verified user reviews.
- **Automated Sentiment Analysis**: Every customer review is processed through NLTK's VADER sentiment engine to render sentiment tags (positive, neutral, negative) and visual emoji indicators.
- **Review Submission**: Authenticated users can compose reviews with dynamic dropdowns populated directly from the relational car database (Make, Model, Year, Purchase Date).
- **Responsive Layout**: Designed for mobile, tablet, and desktop viewports with responsive navigation headers displaying active session state.

---

## Microservices & Endpoints

### 1. Django Application Core (`http://localhost:8000`)
- `GET /` — Serves the React Dealership homepage
- `GET /about/` — Static responsive About Us page with executive leadership profiles
- `GET /contact/` — Static responsive Contact Us page with corporate HQ details
- `POST /djangoapp/login` — Authenticates user credentials and sets session cookie
- `GET /djangoapp/logout` — Destroys current session and clears cookies
- `POST /djangoapp/register` — Validates and creates a new user account
- `GET /djangoapp/get_cars` — Returns all registered car makes and their associated models
- `GET /djangoapp/get_dealers` — Returns list of all US dealerships
- `GET /djangoapp/get_dealers/<state>` — Returns dealerships filtered by US state name
- `GET /djangoapp/dealer/<id>` — Returns specific dealership profile details
- `GET /djangoapp/reviews/dealer/<id>` — Returns reviews for dealership with sentiment scores
- `POST /djangoapp/add_review` — Accepts and stores newly submitted dealer review

### 2. Dealership & Review Service (`http://localhost:3030`)
- `GET /fetchDealers` — Retrieve all dealerships
- `GET /fetchDealers/:state` — Retrieve dealerships in specified state
- `GET /fetchDealer/:id` — Retrieve dealership by ID
- `GET /fetchReviews` — Retrieve all customer reviews
- `GET /fetchReviews/dealer/:id` — Retrieve reviews specific to dealership ID
- `POST /insert_review` — Insert new review document into database

### 3. Sentiment Analysis Microservice (`http://localhost:5050`)
- `GET /analyze/:text` — Analyzes text sentiment and returns `{"sentiment": "positive|neutral|negative"}`

---

## Database Design

### Django Relational Schema (SQLite)
- **`CarMake` Model**:
  - `name` (CharField, max_length=100, unique)
  - `description` (TextField)
  - `country` (CharField, max_length=100)
- **`CarModel` Model**:
  - `car_make` (ForeignKey -> CarMake, related_name='models', on_delete=CASCADE)
  - `dealer_id` (IntegerField)
  - `name` (CharField, max_length=100)
  - `type` (CharField with choices: `SEDAN`, `SUV`, `WAGON`, `HATCHBACK`, `COUPE`, `CONVERTIBLE`, `TRUCK`)
  - `year` (IntegerField, validated between 2015 and 2026)

### Document Schemas (MongoDB / JSON)
- **`Dealership`**:
  `{ id, city, state, st, address, zip, lat, long, short_name, full_name }`
- **`Review`**:
  `{ id, name, dealership, review, purchase, purchase_date, car_make, car_model, car_year }`

---

## Local Installation & Setup

### Prerequisites
- Python 3.10+ (Python 3.12 recommended)
- Node.js 18+ and npm
- Git

### Clone the Repository
```bash
git clone https://github.com/belozov/fullstack-developer-capstone-dealership.git
cd fullstack-developer-capstone-dealership
```

### Backend Virtual Environment Setup
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Install Python requirements
cd server
pip install --upgrade pip
pip install -r requirements.txt
pip install django-cors-headers Flask nltk flake8
python -c "import nltk; nltk.download('vader_lexicon')"
```

### Database Initialization & Seeding
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py shell < djangoapp/populate.py
```

### Frontend Build Setup
```bash
cd frontend
npm install
npm run build
cd ..
```

---

## Running the Application

To run the complete ecosystem locally, launch each service in separate terminals:

### 1. Start Express Database Microservice
```bash
cd server/database
npm install
node app.js
# Runs on http://localhost:3030
```

### 2. Start Flask Sentiment Analysis Microservice
```bash
cd server/djangoapp/microservices
python app.py
# Runs on http://localhost:5050
```

### 3. Start Django Application Server
```bash
cd server
python manage.py runserver 0.0.0.0:8000
# Accessible at http://localhost:8000
```

---

## Testing & Quality Assurance

Automated backend unit tests are implemented in `server/djangoapp/tests.py`:
```bash
cd server
python manage.py test djangoapp
```
**Test Coverage Includes:**
- `CarMakeModelTestCase`: Validates model creation, foreign key relations, string representations, and year boundaries.
- `AuthenticationAPITestCase`: Verifies user registration, duplicate user handling, login validation, and session termination.
- `CarCatalogAPITestCase`: Tests `/djangoapp/get_cars` JSON payload structure and model population.
- `DealerViewsTestCase`: Tests dealer listing and filtering views against mock microservice responses.

---

## Containerization & Kubernetes

The project includes ready-to-deploy Docker and Kubernetes manifests:

### Docker Compose
Run all services with a single command:
```bash
cd docker
docker-compose up --build
```

### Kubernetes Manifests
Production deployment templates are located in `server/deployment.yaml`:
```bash
kubectl apply -f server/deployment.yaml
```

---

## CI/CD Pipeline

Continuous Integration and Continuous Deployment are managed with GitHub Actions (`.github/workflows/ci-cd.yml`):
- **Triggers**: Automated execution on push and pull requests to `main` and `master`.
- **Pipeline Steps**:
  1. Multi-platform checkout
  2. Python 3.12 environment setup & dependency caching
  3. Django migrations check
  4. Backend automated unit test suite execution
  5. Node.js 18 setup & dependency installation
  6. Production React build generation
  7. Flake8 code linting & static analysis
  8. Build verification summary

---

## Production Deployment

The application is deployed live with production Gunicorn process management, static asset compression, and secure SSL/TLS termination:

- **Public Production URL**: `https://philips-languages-ant-reported.trycloudflare.com`
- **Alternative Cloud Target**: IBM Cloud Code Engine container deployment via `server/Dockerfile` and `docker/docker-compose.yml`.

---

## Submission Verification Checklist

| Task | Description | Evidence Location | Status |
|:---:|---|---|:---:|
| 1 | Complete README.md | `README.md` | Verified |
| 2 | Django Dev Server | `terminal_outputs/django_server` | Verified |
| 3 | Static About Us Page | `server/frontend/static/About.html` | Verified |
| 4 | Static Contact Us Page | `server/frontend/static/Contact.html` | Verified |
| 5 | Login API cURL | `terminal_outputs/loginuser` | Verified |
| 6 | Logout API cURL | `terminal_outputs/logoutuser` | Verified |
| 7 | Registration Form | `server/frontend/src/components/Register/Register.jsx` | Verified |
| 8 | Dealer Reviews API | `terminal_outputs/getdealerreviews` | Verified |
| 9 | All Dealers API | `terminal_outputs/getalldealers` | Verified |
| 10 | Dealer by ID API | `terminal_outputs/getdealerbyid` | Verified |
| 11 | Dealers by State API | `terminal_outputs/getdealersbyState` | Verified |
| 12 | Django Admin Login | `screenshots/admin_login.png` | Verified |
| 13 | Django Admin Logout | `screenshots/admin_logout.png` | Verified |
| 14-15 | Car Makes & Models API | `terminal_outputs/getallcarmakes` | Verified |
| 16 | Sentiment Analysis API | `terminal_outputs/analyzereview` | Verified |
| 17 | Homepage Dealers View | `screenshots/get_dealers.png` | Verified |
| 18 | Dealers View (Logged In) | `screenshots/get_dealers_loggedin.png` | Verified |
| 19 | Dealers by State View | `screenshots/dealersbystate.png` | Verified |
| 20 | Dealer Details & Reviews | `screenshots/dealer_id_reviews.png` | Verified |
| 21 | Review Submission Page | `screenshots/dealership_review_submission.png` | Verified |
| 22 | Added Review Displayed | `screenshots/added_review.png` | Verified |
| 23 | GitHub Actions CI/CD | `terminal_outputs/CICD` | Verified |
| 24 | Deployment URL | `deploymentURL` | Verified |
| 25 | Deployed Landing Page | `screenshots/deployed_landingpage.png` | Verified |
| 26 | Deployed Logged In Page | `screenshots/deployed_loggedin.png` | Verified |
| 27 | Deployed Dealer Details | `screenshots/deployed_dealer_detail.png` | Verified |
| 28 | Deployed Review Added | `screenshots/deployed_add_review.png` | Verified |

---

## Author & Attribution

- **Developer**: IBM Full Stack Software Engineering Capstone
- **Starter Template**: IBM Developer Skills Network (`xrwvm-fullstack_developer_capstone`)
- **License**: Apache License 2.0
