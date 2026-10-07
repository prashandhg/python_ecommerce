import streamlit as st

def initialize_cart():
    if "cart" not in st.session_state:
        st.session_state.cart = {}

def add_to_cart(product_id):
    st.session_state.cart[product_id] = st.session_state.cart.get(product_id, 0) + 1

def remove_from_cart(product_id):
    st.session_state.cart.pop(product_id, None)

def increase_quantity(product_id):
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id] += 1

def decrease_quantity(product_id):
    if product_id in st.session_state.cart:
        st.session_state.cart[product_id] -= 1
        if st.session_state.cart[product_id] <= 0:
            remove_from_cart(product_id)

def cart_count():
    return sum(st.session_state.cart.values())
