# Playwright & Python Robust E-Commerce Scraping Framework

This repository provides an enterprise-ready, robust Automation Framework designed to scrape e-commerce(EBAY web) data, dynamically add items to a cart based on isolated runtime variables, and strictly enforce business budget logic constraints.

---

## 🛠️ Architecture Overview
The framework is built from the ground up utilizing pure **Object-Oriented Programming (OOP)** and strict design guidelines:
* **Page Object Model (POM):** Complete decoupling between raw UI element selectors (`Locators`) and higher-level test scripts.
* **Single Responsibility Principle (SRP):** Each page object is only responsible for its dedicated DOM view slice (`EcommercePage` handles mutations/queries, `CartPage` handles validations).
* **Data-Driven Design:** Test execution profiles, configurations, targets, and environment constants are loaded dynamically via `data/config.json`.
* **Robust Dynamic Locators:** Pure XPath/CSS queries optimized to extract nested prices and parse unstructured text accurately using sanitization filters.

---

## 📁 Project Structure
├── data/
│   └── config.json          # Environment, target URLs, and budget limits
├── pages/
│   ├── base_page.py         # Shared browser interactions and utilities
│   ├── ecommerce_page.py    # Item hunting, pagination, and variant logic
│   └── cart_page.py         # Cart content validation and total cost checks
├── tests/
│   └── test_ecommerce.py     # End-to-end automated test suites
├── requirements.txt         # Project dependency manifest
└── README.md                # Framework documentation

## 🚀 Pre-requisites & How to Run
Ensure Python 3.10+ and the Allure CLI utility are installed. Run the following commands to set up the environment and execute the framework:

```bash
# 1. Setup Environment & Dependencies
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

# 2. Execute Tests (Pytest)
pytest --headed             # Run in UI-Headed mode for visual verification
pytest                      # Run in Headless mode (CI/CD optimized)

# 3. Generate & View Allure Reports
pytest --alluredir=allure-results
allure serve allure-results