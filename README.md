# 🛍️ Customer Shopping Behavior Analysis

> An end-to-end data analytics project covering data cleaning, feature engineering, SQL analysis, and Power BI visualization — built on a dataset of 3,900 customer transactions.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14+-336791?logo=postgresql&logoColor=white)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?logo=powerbi&logoColor=black)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458?logo=pandas&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 📌 Project Overview

This project analyzes customer shopping behavior to uncover revenue patterns, customer segments, product performance, and discount effectiveness. It follows a real-world analytics pipeline from raw data to business insights.

**Pipeline:**
```
Raw CSV  →  Python (EDA + Cleaning)  →  PostgreSQL  →  SQL Analysis  →  Power BI Dashboard
```

---

## 📁 Repository Structure

```
customer-shopping-behavior-analysis/
│
├── data/
│   └── customer_shopping_behavior.csv      # Raw dataset (3,900 records)
│
├── notebooks/
│   └── customer_behavior.ipynb             # Data cleaning & feature engineering
│
├── sql/
│   └── customer_behavior_sql_queries.sql   # 10 business SQL queries
│
├── db/
│   └── db_connection.py                    # SQLAlchemy PostgreSQL connection
│
├── dashboard/
│   └── customer_behavior.pbix              # Power BI dashboard file
│
├── report/
│   └── Customer_Shopping_Behavior_Analysis_Report.pdf
│
└── README.md
```

---

## 📊 Dataset

| Property      | Detail                              |
|---------------|-------------------------------------|
| Records       | 3,900 customer transactions         |
| Features      | 18 original → 19 after engineering  |
| Source        | Customer Shopping Behavior Dataset  |
| Format        | CSV                                 |

**Key Columns:**

| Column | Description |
|--------|-------------|
| `customer_id` | Unique customer identifier |
| `age` | Customer age (18–70) |
| `gender` | Male / Female |
| `item_purchased` | Product name (25 unique items) |
| `category` | Clothing, Footwear, Beauty, Accessories |
| `purchase_amount` | Transaction value in USD ($20–$100) |
| `season` | Spring, Summer, Fall, Winter |
| `review_rating` | 1–5 star product rating |
| `subscription_status` | Active subscription (Yes/No) |
| `discount_applied` | Discount used on purchase (Yes/No) |
| `previous_purchases` | Historical purchase count (1–50) |
| `frequency_of_purchases` | Self-reported buying cadence |

---

## 🔧 Tech Stack

| Layer | Technology |
|-------|------------|
| Language | Python 3.11 |
| Data Manipulation | Pandas, NumPy |
| Visualization (EDA) | Matplotlib, Seaborn |
| Database | PostgreSQL 14+ |
| ORM / Connector | SQLAlchemy, psycopg2 |
| BI Dashboard | Power BI Desktop |
| Notebook | Jupyter Notebook |

---

## ⚙️ Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/customer-shopping-behavior-analysis.git
cd customer-shopping-behavior-analysis
```

### 2. Install Python Dependencies
```bash
pip install pandas numpy matplotlib seaborn sqlalchemy psycopg2-binary jupyter
```

### 3. Set Up PostgreSQL
```sql
-- Run in psql or pgAdmin
CREATE DATABASE customer_behavior;
```

### 4. Update Database Credentials
Edit `db/db_connection.py`:
```python
DATABASE_URL = "postgresql://YOUR_USERNAME:YOUR_PASSWORD@localhost:5432/customer_behavior"
```

### 5. Run the Notebook
```bash
jupyter notebook notebooks/customer_behavior.ipynb
```
This will clean the data and load it into PostgreSQL automatically.

### 6. Run SQL Queries
Open `sql/customer_behavior_sql_queries.sql` in pgAdmin, DBeaver, or any PostgreSQL client and execute the queries.

---

## 🧹 Data Cleaning Steps

| Step | Action | Detail |
|------|--------|--------|
| Null Handling | Category-wise median imputation | `review_rating` had 37 nulls (0.95%) |
| Column Rename | Lowercased + snake_case | Standardized for PostgreSQL compatibility |
| Duplicate Detection | Dropped `promo_code_used` | 100% identical to `discount_applied` |
| Feature Engineering | Created `age_group` | Quartile binning via `pd.qcut` |
| Feature Engineering | Created `purchase_frequency_days` | Mapped ordinal text to numeric values |

---

## 📐 Feature Engineering

**`age_group`** — Derived from `age` using quartile binning:
```python
labels = ['Young Adult', 'Adult', 'Middle-Aged', 'Senior']
df['age_group'] = pd.qcut(df['age'], q=4, labels=labels)
```

**`purchase_frequency_days`** — Numeric encoding of purchase frequency:
```python
frequency_mapping = {
    'Weekly': 7, 'Fortnightly': 14, 'Monthly': 30,
    'Quarterly': 90, 'Every 3 Months': 90, 'Annually': 365
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
```

---

## 🗄️ SQL Analysis

10 business questions answered using PostgreSQL, showcasing a range of SQL techniques:

| # | Question | SQL Concepts Used |
|---|----------|-------------------|
| Q1 | Revenue by gender | `GROUP BY`, `SUM` |
| Q2 | Discount users above avg spend | Correlated subquery, `WHERE` |
| Q3 | Top 5 products by avg review rating | `GROUP BY`, `ORDER BY`, `LIMIT` |
| Q4 | Standard vs Express shipping avg spend | Filtered `GROUP BY` |
| Q5 | Subscriber vs non-subscriber spend | Multi-metric `GROUP BY` |
| Q6 | Products with highest discount rate | `CASE WHEN`, conditional aggregation |
| Q7 | Customer loyalty segmentation | CTE + `CASE WHEN` |
| Q8 | Top 3 products per category | `ROW_NUMBER()` window function + CTE |
| Q9 | Repeat buyers and subscription correlation | Filtered aggregation |
| Q10 | Revenue by age group | `GROUP BY` on engineered column |

**Sample Query — Window Function (Q8):**
```sql
WITH item_counts AS (
    SELECT category,
           item_purchased,
           COUNT(customer_id) AS total_orders,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY COUNT(customer_id) DESC) AS item_rank
    FROM customer
    GROUP BY category, item_purchased
)
SELECT item_rank, category, item_purchased, total_orders
FROM item_counts
WHERE item_rank <= 3;
```

---

## 📈 Key Insights

- 👨 **Male customers** account for ~68% of transactions but spend comparably to female customers per order
- 💳 **Subscribers** (27.3% of base) generate disproportionately higher revenue — strong ROI for the subscription model
- 🌸 **Spring** is the highest-volume purchase season; inventory should be pre-positioned accordingly
- 🏷️ **Discount & promo code flags** are perfectly correlated — redundant data was eliminated
- 🔁 **~82% of customers** are in the Loyal segment (11+ previous purchases), showing strong retention
- 👟 Certain products (Coat, Jacket, Sneakers) show **60%+ discount rates** — margin review recommended
- 👴 **Middle-Aged and Senior** customers contribute the most revenue; Young Adults are an untapped growth opportunity

---

## 📊 Power BI Dashboard

The dashboard connects to PostgreSQL and provides interactive exploration across 5 pages:

| Page | Focus |
|------|-------|
| Executive Overview | Revenue KPIs, gender split, seasonal trends |
| Customer Segmentation | Age groups, loyalty tiers, subscription comparison |
| Product Performance | Category treemap, top products, rating heatmap |
| Discount Analysis | Discount rates by product, revenue impact |
| Shipping & Payments | Delivery method distribution, payment preferences |

---

## 📋 Project Rating

| Dimension | Score |
|-----------|-------|
| Data Cleaning & EDA | 8.2 / 10 |
| Feature Engineering | 7.5 / 10 |
| SQL Query Complexity | 8.5 / 10 |
| Business Question Coverage | 8.0 / 10 |
| Power BI / Visualization | 8.0 / 10 |
| Code Quality & Structure | 7.8 / 10 |
| **Overall** | **8.2 / 10 — Grade A** |

---

## 🚀 Future Improvements

- [ ] RFM (Recency-Frequency-Monetary) customer segmentation model
- [ ] Churn prediction using logistic regression or random forest
- [ ] Customer Lifetime Value (CLV) estimation
- [ ] A/B test framework for discount effectiveness
- [ ] Automated ETL pipeline using Airflow or dbt
- [ ] Additional SQL: LAG/LEAD for trend analysis, running totals

---

## 👤 Author

**Ayush Pawshe**

[![GitHub](https://img.shields.io/badge/GitHub-your--username-181717?logo=github)](https://github.com/your-username)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?logo=linkedin)](https://linkedin.com/in/your-profile)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

*Dataset used for educational and portfolio purposes.*
