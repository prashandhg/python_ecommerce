# 🛍️ NovaCart — Modern Streamlit E-Commerce Website

A responsive e-commerce portfolio project built with Python and Streamlit.

## Features

- Modern homepage
- Hero section
- Featured/trending products
- Category section
- Product search
- Category filtering
- Price filtering
- Shopping cart
- Increase/decrease quantity
- Remove products
- Checkout form
- Order confirmation
- Responsive Streamlit layout
- GitHub + Streamlit Community Cloud ready

## Project structure

```text
ecommerce_streamlit/
├── app.py
├── cart.py
├── utils.py
├── requirements.txt
├── README.md
├── data/
│   └── products.csv
└── .streamlit/
    └── config.toml
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL shown by Streamlit, normally:

```text
http://localhost:8501
```

## Deployment

Push this folder to GitHub and deploy `app.py` through Streamlit Community Cloud.

## Important

This is a portfolio/demo store. The checkout does not process real payments. For a production store, add authentication, a database, secure secrets, server-side order handling, and a real payment provider.
