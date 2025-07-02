import streamlit as st
import google.generativeai as genai

# Configure Gemini
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-2.5-flash")

st.title("💸 Dynamic Discount Analyzer for Shopkeepers")

st.markdown("""
Optimize discounts to boost sales while maintaining profit!  
Get AI-powered suggestions on pricing strategies.
""")

# Inputs
original_price = st.number_input("Original Price (₹)", min_value=1.0, value=500.0)
cost_price = st.number_input("Cost Price (₹)", min_value=1.0, value=300.0)
discount_percentage = st.slider("Discount (%)", 0, 90, 20)
expected_base_sales = st.number_input("Expected Base Sales Volume", min_value=1, value=100)

# Simple elasticity factor (simulate how sales increase with discount)
elasticity_factor = 1 + (discount_percentage / 50)  # Example formula

if st.button("Analyze Discount Impact"):
    # Calculate selling price
    discount_amount = (discount_percentage / 100) * original_price
    selling_price = original_price - discount_amount

    # Profit per unit
    profit_per_unit = selling_price - cost_price

    # Expected sales volume with discount
    expected_sales_volume = int(expected_base_sales * elasticity_factor)

    # Total profit
    total_profit = profit_per_unit * expected_sales_volume

    st.success("✅ Analysis Results")
    st.write(f"**Selling Price after Discount:** ₹{selling_price:.2f}")
    st.write(f"**Profit per Unit:** ₹{profit_per_unit:.2f}")
    st.write(f"**Expected Sales Volume:** {expected_sales_volume} units")
    st.write(f"**Estimated Total Profit:** ₹{total_profit:.2f}")

    # Gemini prompt
    prompt = f"""
    I am a shopkeeper. Here are my product details:
    - Original price: ₹{original_price}
    - Cost price: ₹{cost_price}
    - Discount offered: {discount_percentage}%
    - Profit per unit after discount: ₹{profit_per_unit:.2f}
    - Expected sales volume: {expected_sales_volume}
    - Estimated total profit: ₹{total_profit:.2f}

    Please give me:
    - Advice on whether this discount is reasonable.
    - Suggestions on how to further increase sales without hurting profit.
    - Ideas for marketing or bundling to support this discount.
    Present it as a friendly shop consultant.
    """

    response = model.generate_content(prompt)
    st.markdown("---")
    st.subheader("🤖 AI Recommendations")
    st.markdown(response.text)

st.caption("🛍️ Built with Python, Streamlit & Gemini API")
