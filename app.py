import streamlit as st
import pandas as pd
from cart import (
    initialize_cart, add_to_cart, remove_from_cart,
    increase_quantity, decrease_quantity, cart_count
)
from utils import calculate_total, money

st.set_page_config(
    page_title="NovaCart | Modern Shopping",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background: #f7f8fc;
}

.block-container {
    padding-top: 1rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

.hero {
    background: linear-gradient(135deg, #111827 0%, #312e81 55%, #7c3aed 100%);
    border-radius: 28px;
    padding: 55px 50px;
    color: white;
    margin: 10px 0 30px 0;
}

.hero h1 {
    font-size: 52px;
    line-height: 1.05;
    margin-bottom: 15px;
    font-weight: 800;
}

.hero p {
    font-size: 18px;
    color: #e5e7eb;
    max-width: 650px;
    line-height: 1.6;
}

.badge {
    display: inline-block;
    background: rgba(255,255,255,.14);
    border: 1px solid rgba(255,255,255,.25);
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 13px;
    margin-bottom: 18px;
}

.section-title {
    font-size: 30px;
    font-weight: 800;
    color: #111827;
    margin: 25px 0 15px 0;
}

.card {
    background: white;
    border-radius: 20px;
    padding: 14px;
    margin-bottom: 18px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 6px 22px rgba(15,23,42,.06);
}

.card img {
    border-radius: 16px;
}

.product-name {
    font-size: 18px;
    font-weight: 700;
    margin-top: 8px;
    color: #111827;
}

.price {
    font-size: 21px;
    font-weight: 800;
    color: #111827;
}

.rating {
    color: #f59e0b;
    font-size: 14px;
}

.category-chip {
    background: #ede9fe;
    color: #5b21b6;
    padding: 6px 10px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
}

.feature {
    background: white;
    border-radius: 18px;
    padding: 20px;
    border: 1px solid #e5e7eb;
    text-align: center;
    min-height: 145px;
}

.feature-icon {
    font-size: 30px;
}

.cart-box {
    background: white;
    border-radius: 20px;
    padding: 22px;
    border: 1px solid #e5e7eb;
    margin-bottom: 15px;
}

.footer {
    text-align: center;
    color: #6b7280;
    padding: 30px 0 10px 0;
}

@media (max-width: 768px) {
    .hero {
        padding: 35px 25px;
    }
    .hero h1 {
        font-size: 36px;
    }
    .hero p {
        font-size: 16px;
    }
}
</style>
""", unsafe_allow_html=True)


# ---------- Data ----------
products = pd.read_csv("data/products.csv")
initialize_cart()

# ---------- Header ----------
top1, top2 = st.columns([5, 1])
with top1:
    st.markdown("## 🛍️ NovaCart")
    st.caption("Modern shopping, simple experience.")
with top2:
    st.markdown(f"### 🛒 {cart_count()}")

page = st.radio(
    "Navigation",
    ["Home", "Shop", "Cart", "Checkout"],
    horizontal=True,
    label_visibility="collapsed"
)

# ---------- Home ----------
if page == "Home":
    st.markdown("""
    <div class="hero">
        <div class="badge">✨ New season collection</div>
        <h1>Shop smarter.<br>Live better.</h1>
        <p>
            Discover hand-picked fashion, electronics, accessories and everyday
            essentials — all in one modern shopping experience.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if st.button("🛍️ Explore Products", type="primary"):
        st.session_state["go_shop"] = True
        st.rerun()

    st.markdown('<div class="section-title">Why shop with NovaCart?</div>', unsafe_allow_html=True)
    f1, f2, f3, f4 = st.columns(4)
    features = [
        ("🚚", "Fast Delivery", "Quick and reliable delivery."),
        ("🔒", "Secure Checkout", "Simple and protected checkout."),
        ("⭐", "Top Rated", "Quality products customers love."),
        ("💬", "Easy Support", "Friendly help when you need it.")
    ]
    for col, (icon, title, desc) in zip([f1,f2,f3,f4], features):
        with col:
            st.markdown(f"""
            <div class="feature">
                <div class="feature-icon">{icon}</div>
                <h4>{title}</h4>
                <p>{desc}</p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="section-title">🔥 Trending now</div>', unsafe_allow_html=True)

    featured = products.sort_values("rating", ascending=False).head(4)
    cols = st.columns(4)

    for col, (_, p) in zip(cols, featured.iterrows()):
        with col:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.image(p["image"], use_container_width=True)
            st.markdown(f'<div class="product-name">{p["name"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="category-chip">{p["category"]}</span>', unsafe_allow_html=True)
            st.markdown(f'<div class="rating">⭐ {p["rating"]}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="price">{money(p["price"])}</div>', unsafe_allow_html=True)
            if st.button("Add to cart", key=f"home_add_{p['id']}", use_container_width=True):
                add_to_cart(int(p["id"]))
                st.success("Added!")
            st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Shop by category</div>', unsafe_allow_html=True)
    cats = products["category"].unique().tolist()
    cat_cols = st.columns(len(cats))
    for col, cat in zip(cat_cols, cats):
        with col:
            count = len(products[products["category"] == cat])
            st.markdown(f"""
            <div class="feature">
                <div class="feature-icon">🛍️</div>
                <h4>{cat}</h4>
                <p>{count} products</p>
            </div>
            """, unsafe_allow_html=True)

# ---------- Shop ----------
elif page == "Shop":
    st.markdown('<div class="section-title">🛍️ Shop all products</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        search = st.text_input("🔎 Search", placeholder="Search products...")
    with c2:
        category = st.selectbox("Category", ["All"] + sorted(products["category"].unique()))
    with c3:
        max_price = int(products["price"].max())
        price = st.slider("Max price", 0, max_price, max_price)

    filtered = products.copy()
    if search:
        filtered = filtered[
            filtered["name"].str.contains(search, case=False, na=False) |
            filtered["description"].str.contains(search, case=False, na=False)
        ]
    if category != "All":
        filtered = filtered[filtered["category"] == category]
    filtered = filtered[filtered["price"] <= price]

    st.caption(f"{len(filtered)} product(s) found")

    for start in range(0, len(filtered), 4):
        row = filtered.iloc[start:start+4]
        cols = st.columns(4)
        for col, (_, p) in zip(cols, row.iterrows()):
            with col:
                st.markdown('<div class="card">', unsafe_allow_html=True)
                st.image(p["image"], use_container_width=True)
                st.markdown(f'<div class="product-name">{p["name"]}</div>', unsafe_allow_html=True)
                st.caption(p["description"])
                st.markdown(f'<div class="rating">⭐ {p["rating"]}</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="price">{money(p["price"])}</div>', unsafe_allow_html=True)
                if st.button("🛒 Add to cart", key=f"shop_add_{p['id']}", use_container_width=True):
                    add_to_cart(int(p["id"]))
                    st.success("Added!")
                st.markdown('</div>', unsafe_allow_html=True)

# ---------- Cart ----------
elif page == "Cart":
    st.markdown('<div class="section-title">🛒 Your shopping cart</div>', unsafe_allow_html=True)
    cart = st.session_state.cart

    if not cart:
        st.info("Your cart is empty. Visit Shop to add products.")
    else:
        for product_id, quantity in list(cart.items()):
            match = products[products["id"] == product_id]
            if match.empty:
                continue
            p = match.iloc[0]

            st.markdown('<div class="cart-box">', unsafe_allow_html=True)
            c1, c2, c3, c4 = st.columns([1, 3, 2, 1])
            with c1:
                st.image(p["image"], width=100)
            with c2:
                st.write(f"**{p['name']}**")
                st.caption(p["category"])
                st.write(money(p["price"]))
            with c3:
                a, b, c = st.columns(3)
                with a:
                    if st.button("➖", key=f"dec_{product_id}"):
                        decrease_quantity(product_id)
                        st.rerun()
                with b:
                    st.write(f"**{quantity}**")
                with c:
                    if st.button("➕", key=f"inc_{product_id}"):
                        increase_quantity(product_id)
                        st.rerun()
            with c4:
                if st.button("🗑️", key=f"rm_{product_id}"):
                    remove_from_cart(product_id)
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        total = calculate_total(cart, products)
        st.markdown(f"## Total: {money(total)}")
        if st.button("💳 Proceed to Checkout", type="primary"):
            st.session_state["checkout"] = True
            st.rerun()

# ---------- Checkout ----------
elif page == "Checkout":
    st.markdown('<div class="section-title">💳 Secure checkout</div>', unsafe_allow_html=True)
    cart = st.session_state.cart

    if not cart:
        st.info("Your cart is empty.")
    else:
        total = calculate_total(cart, products)

        left, right = st.columns([2, 1])

        with left:
            st.subheader("Delivery details")
            name = st.text_input("Full name *")
            email = st.text_input("Email *")
            phone = st.text_input("Phone number *")
            address = st.text_area("Delivery address *")
            payment = st.selectbox("Payment method", ["Cash on Delivery", "UPI", "Card"])

        with right:
            st.subheader("Order summary")
            for product_id, quantity in cart.items():
                match = products[products["id"] == product_id]
                if not match.empty:
                    p = match.iloc[0]
                    st.write(f"{p['name']} × {quantity}")
                    st.write(money(p["price"] * quantity))
            st.divider()
            st.markdown(f"### Total: {money(total)}")

        if st.button("✅ Place Order", type="primary", use_container_width=True):
            if not all([name.strip(), email.strip(), phone.strip(), address.strip()]):
                st.error("Please complete all required fields.")
            else:
                st.success("🎉 Order placed successfully!")
                st.balloons()
                st.write(f"**Customer:** {name}")
                st.write(f"**Payment:** {payment}")
                st.write(f"**Order total:** {money(total)}")
                st.session_state.cart = {}

st.markdown("""
<div class="footer">
    NovaCart • Built with Python + Streamlit • Portfolio Project
</div>
""", unsafe_allow_html=True)
