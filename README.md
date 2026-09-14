# 🏠 Houseboat AI Recommendation System

An AI-powered houseboat discovery and recommendation platform built with **Django, MySQL, Machine Learning, and a database-driven chatbot**.

The system allows users to explore houseboats, search and filter available options, receive personalized recommendations, make bookings, manage wishlists, and interact with an AI-style chatbot for houseboat information.

---

## 🚀 Project Overview

**Houseboat AI Recommendation System** is a full-stack web application designed to make houseboat discovery and selection easier through intelligent recommendations and data-driven search.

The application combines:

* Full-stack web development
* Machine Learning
* Database management
* AI-based recommendation
* Chatbot interaction
* Data analytics

The project uses a dataset containing **500 houseboat records** with information such as location, price, bedrooms, capacity, facilities, ratings, bookings, and luxury status.

---

## ✨ Key Features

### 👤 User Features

* User registration and login
* Browse houseboats
* Search houseboats
* Filter houseboats based on preferences
* View detailed houseboat information
* AI-powered houseboat recommendations
* Add houseboats to wishlist
* Book houseboats
* View booking history
* Contact/message functionality

### 🤖 AI & Machine Learning

* K-Nearest Neighbors (KNN) based recommendation system
* User-preference-based houseboat recommendations
* Machine-learning-driven similarity matching
* Database-driven chatbot for houseboat queries

### 💬 Chatbot

The chatbot can answer queries such as:

* "Show me luxury houseboats"
* "Show me houseboats in Alleppey under ₹10,000"
* "Which houseboat has the highest rating?"
* "Show me houseboats with AC"
* "Show me houseboats with Wi-Fi"

### 👨‍💼 Admin Features

* Admin dashboard
* Houseboat management
* User management
* Booking management
* Wishlist management
* Contact message management
* Dataset monitoring

### 📊 Data Analytics

A separate **Power BI dashboard** was created to analyze:

* Total houseboats
* Luxury vs non-luxury houseboats
* Average rating
* Houseboat distribution by location
* Average price by location
* Rating distribution
* Most-booked houseboats

---

## 🧠 System Architecture

```text
                    ┌──────────────────────┐
                    │       User           │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │  Django Web Interface│
                    │   HTML/CSS/Bootstrap  │
                    └──────────┬───────────┘
                               │
                ┌──────────────┼──────────────┐
                │              │              │
                ▼              ▼              ▼
          Search & Filter   Booking       Wishlist
                │              │              │
                └──────────────┼──────────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      MySQL Database  │
                    └──────────┬───────────┘
                               │
                ┌──────────────┴──────────────┐
                │                             │
                ▼                             ▼
       ┌─────────────────┐          ┌─────────────────┐
       │ Recommendation  │          │    Chatbot      │
       │   System (KNN)  │          │ Database Query  │
       └─────────────────┘          └─────────────────┘
                │                             │
                └──────────────┬──────────────┘
                               ▼
                    Personalized Results
```

---

## 🛠️ Technologies Used

### Frontend

* HTML5
* CSS3
* Bootstrap

### Backend

* Python
* Django

### Database

* MySQL

### Machine Learning

* Scikit-learn
* K-Nearest Neighbors (KNN)
* Feature-based similarity

### Data Processing

* Pandas
* NumPy
* Exploratory Data Analysis (EDA)

### Analytics

* Microsoft Power BI

### Development Tools

* Visual Studio Code
* MySQL Workbench
* Git
* GitHub
* Google Colab

---

## 📂 Dataset

The project uses a **500-row professional houseboat dataset**.

Important attributes include:

| Feature       | Description                   |
| ------------- | ----------------------------- |
| HouseboatID   | Unique houseboat identifier   |
| HouseboatName | Name of the houseboat         |
| Location      | Houseboat location            |
| PriceINR      | Price in Indian Rupees        |
| Bedrooms      | Number of bedrooms            |
| Capacity      | Guest capacity                |
| AC            | Air-conditioning availability |
| Luxury        | Luxury classification         |
| Rating        | Customer rating               |
| ReviewCount   | Number of reviews             |
| BookingCount  | Number of bookings            |
| Food          | Food availability             |
| WiFi          | Wi-Fi availability            |
| Jacuzzi       | Jacuzzi availability          |
| Fishing       | Fishing facility              |
| Canoeing      | Canoeing facility             |

---

## 🤖 Recommendation System

The recommendation component uses **K-Nearest Neighbors (KNN)** to identify houseboats that are similar to the user's selected preferences.

Relevant features can include:

* Price
* Bedrooms
* Capacity
* Rating
* Location
* Facilities
* Luxury preference

The system compares the user's requirements with available houseboats and returns suitable recommendations.

---

## 💬 Chatbot

The chatbot provides database-driven responses to natural-language-style houseboat queries.

Example:

```text
User:
Show me luxury houseboats

System:
Returns houseboats where Luxury = Yes
```

Another example:

```text
User:
Show me houseboats in Alleppey under 10000

System:
Filters houseboats based on location and price
and returns matching results.
```

---

## 📊 Power BI Dashboard

The project also includes a Power BI analytics dashboard for exploring the houseboat dataset.

Dashboard insights include:

* Houseboat count
* Average rating
* Location-wise distribution
* Location-wise average price
* Luxury distribution
* Rating distribution
* Top 10 most-booked houseboats

---

## 📸 Project Screenshots

### 🏠 Home Page

![Home Page](screenshots/home.png)

### 🤖 AI Recommendation

![AI Recommendation](screenshots/recomendation_ai.png)

### 💬 Chatbot

![AI Chatbot](screenshots/ai_chatbot.png)

### 📅 Booking
![Booking](screenshots/bookings.png)


### 👨‍💼 Admin Dashboard

![Admin Dashboard](screenshots/admin-dashboard.png)



---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/24ubc226/HouseboatAI.git
```

### 2. Navigate to the project

```bash
cd HouseboatAI
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows

```bash
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

### 6. Configure the database

Create a MySQL database and update the Django database configuration using environment variables.

### 7. Apply migrations

```bash
python manage.py migrate
```

### 8. Run the development server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 🔐 Environment Variables

Sensitive information should be stored in environment variables rather than committed to GitHub.

Example:

```text
SECRET_KEY=your-secret-key
DB_NAME=your-database-name
DB_USER=your-database-user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=3306
```

---

## 📁 Project Structure

```text
HouseboatAI/
│
├── houseboat_ai/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── recommendation/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── templates/
│   └── ...
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
├── screenshots/
│
├── manage.py
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 🎯 Learning Outcomes

This project helped develop practical experience in:

* Full-stack web development
* Django application development
* MySQL database integration
* Machine Learning
* KNN recommendation systems
* Data preprocessing
* Exploratory Data Analysis
* Chatbot development
* Power BI data visualization
* Git and GitHub
* Debugging and deployment preparation

---

## 🔮 Future Improvements

Possible future enhancements include:

* Cloud deployment
* Real-time booking availability
* Payment gateway integration
* Advanced NLP chatbot
* Vector database-based RAG
* Deep-learning recommendation models
* Personalized user profiles
* Mobile application
* Real-time notifications

---

## 👨‍💻 Author

**Bijil Biju**

BCA (Honours) – Artificial Intelligence & Machine Learning

GitHub:
https://github.com/24ubc226

LinkedIn:
https://linkedin.com/in/bijil-biju-7a14b9320

---

## ⭐ Project Purpose

This project was developed as a **portfolio project** to demonstrate practical skills in **Artificial Intelligence, Machine Learning, Data Analytics, Web Development, and Database Management**.
