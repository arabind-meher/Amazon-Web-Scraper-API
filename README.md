# 🛒 Amazon Web Scraper API

This project is a **FastAPI**-based web API that scrapes product data from Amazon using **Selenium** and stores it in a **MySQL** database. It allows users to add, update, retrieve, and delete product records via HTTP endpoints.

> ⚠️ **Note**: This project is for educational purposes only. Frequent scraping of Amazon may violate their Terms of Service.

---

## 🚀 Features

- Scrape Amazon product details using a provided product URL.
- Extracted fields include:
  - Product title
  - Price
  - Image URL
- Store product data in a MySQL database.
- Perform CRUD operations via RESTful endpoints:
  - Add new product
  - Fetch all or specific product
  - Update individual or all product prices
  - Delete product by ID

---

## 📁 Project Structure

```
Amazon-Web-Scraper-API/
│
├── amazon/
│   └── products.py          # Core logic for scraping product data using Selenium
│
├── app/
│   └── main.py              # FastAPI application with all API routes
│
├── database/
│   ├── models.py            # SQLAlchemy models for Products table
│   └── schemas.py           # Database connection and session logic
│
├── .gitignore
├── requirements.txt
├── README.md
└── credentials.env          # Environment variables (ignored in git)
```

---

## ⚙️ Requirements

Install dependencies using pip:

```bash
pip install -r requirements.txt
```

Ensure you have **MySQL** running and a database created. Store your credentials in a `credentials.env` file like this:

```dotenv
_USERNAME=your_username
_PASSWORD=your_password
_HOST=localhost
_PORT=3306
_DATABASE=your_database_name
```

---

## ▶️ How to Run

1. **Create the database schema:**

   ```python
   from database.models import create_all
   create_all()
   ```

2. **Start the FastAPI server:**

   ```bash
   uvicorn app.main:app --reload
   ```

3. **Use the API endpoints**:

   - Add product by scraping:
     ```
     POST /products/add?url={amazon_product_url}&target={target_price}
     ```
   - Fetch all products:
     ```
     GET /products
     ```
   - Fetch specific product:
     ```
     GET /products/{product_id}
     ```
   - Update all products:
     ```
     PUT /products/update
     ```
   - Update specific product:
     ```
     PUT /products/update/{product_id}
     ```
   - Delete a product:
     ```
     DELETE /products/delete/{product_id}
     ```

---

## 🛠 Technologies Used

- Python
- FastAPI
- Selenium
- SQLAlchemy
- MySQL
- Uvicorn
- Python-dotenv

---

## 👨‍💻 Author

**Arabind Meher**  
[GitHub](https://github.com/arabind-meher) • [LinkedIn](https://www.linkedin.com/in/arabind-meher)
