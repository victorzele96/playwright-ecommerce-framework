# Playwright & Python Robust E-Commerce Scraping Framework

This repository provides an enterprise-ready, robust Automation Framework designed to scrape e-commerce data, dynamically add items to a cart based on isolated runtime variables, and strictly enforce business budget logic constraints.

---

## 🛠️ Architecture Overview
The framework is built from the ground up utilizing pure **Object-Oriented Programming (OOP)** and strict design guidelines:
* **Page Object Model (POM):** Complete decoupling between raw UI element selectors (`Locators`) and higher-level test scripts.
* **Single Responsibility Principle (SRP):** Each page object is only responsible for its dedicated DOM view slice (`EcommercePage` handles mutations/queries, `CartPage` handles validations).
* **Data-Driven Design:** Test execution profiles, configurations, targets, and environment constants are loaded dynamically via `data/config.json`.
* **Robust Dynamic Locators:** Pure XPath/CSS queries optimized to extract nested prices and parse unstructured text accurately using sanitization filters.

---

## 🚀 Pre-requisites & How to Run

### 1. Initialize Virtual Environment & Dependencies
Ensure your python runtime is activated inside your local isolated `.venv`:
```bash
source .venv/bin/activate
pip install -r requirements.txt