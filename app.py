import streamlit as st
import pickle
import pandas as pd

# ----------------------------------------------------------------
# page config - must be first streamlit command
# ----------------------------------------------------------------
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)

# ----------------------------------------------------------------
# custom CSS - makes it look professional not default streamlit
# ----------------------------------------------------------------
st.markdown("""
    <style>
    /* main background */
    .stApp {
        background-color: #0f0f0f;
        color: #f0f0f0;
    }

    /* header strip */
    .header-box {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
        border-radius: 16px;
        padding: 2.5rem 2rem;
        margin-bottom: 2rem;
        border: 1px solid #e94560;
        text-align: center;
    }
    .header-box h1 {
        font-size: 2.4rem;
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -1px;
    }
    .header-box p {
        color: #a0a0b0;
        font-size: 1rem;
        margin-top: 0.5rem;
    }

    /* input card */
    .input-card {
        background-color: #1a1a2e;
        border-radius: 12px;
        padding: 2rem;
        border: 1px solid #2a2a4a;
        margin-bottom: 1.5rem;
    }

    /* result box */
    .result-box {
        background: linear-gradient(135deg, #0f3460, #e94560);
        border-radius: 16px;
        padding: 2rem;
        text-align: center;
        margin-top: 1.5rem;
    }
    .result-box .label {
        font-size: 0.95rem;
        color: #ffffff99;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-bottom: 0.5rem;
    }
    .result-box .price {
        font-size: 3rem;
        font-weight: 900;
        color: #ffffff;
        letter-spacing: -1px;
    }
    .result-box .sub {
        font-size: 0.85rem;
        color: #ffffff88;
        margin-top: 0.5rem;
    }

    /* selectbox and input labels */
    .stSelectbox label, .stNumberInput label {
        color: #a0a0b0 !important;
        font-size: 0.9rem !important;
        font-weight: 500 !important;
    }

    /* predict button */
    .stButton > button {
        background: #e94560;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.75rem 2rem;
        font-size: 1rem;
        font-weight: 700;
        width: 100%;
        letter-spacing: 0.5px;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        background: #c73652;
        color: white;
        border: none;
    }

    /* hide streamlit default elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# load model
# ----------------------------------------------------------------
model = pickle.load(open('LinearRegressionModel.pkl', 'rb'))

# ----------------------------------------------------------------
# load cleaned data to get dropdown options
# same values model was trained on
# ----------------------------------------------------------------
car = pd.read_csv('Cleaned_Car.csv')

companies   = sorted(car['company'].unique())
car_names   = sorted(car['name'].unique())
fuel_types  = car['fuel_type'].unique()
years       = sorted(car['year'].unique(), reverse=True)

# ----------------------------------------------------------------
# header
# ----------------------------------------------------------------
st.markdown("""
    <div class="header-box">
        <h1>🚗 Car Price Predictor</h1>
        <p>Tell us about the car — we'll tell you what it's worth</p>
    </div>
""", unsafe_allow_html=True)

# ----------------------------------------------------------------
# input form
# ----------------------------------------------------------------
st.markdown('<div class="input-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    company = st.selectbox("Company", companies)

with col2:
    # filter car names by selected company so dropdown is cleaner
    # only show names that belong to selected company
    filtered_names = sorted(car[car['company'] == company]['name'].unique())
    name = st.selectbox("Model", filtered_names)

col3, col4 = st.columns(2)

with col3:
    year = st.selectbox("Year", years)

with col4:
    fuel_type = st.selectbox("Fuel Type", fuel_types)

kms_driven = st.number_input(
    "Kilometres Driven",
    min_value=0,
    max_value=500000,
    value=30000,
    step=1000,
    help="How many kilometres has this car been driven?"
)

st.markdown('</div>', unsafe_allow_html=True)

# ----------------------------------------------------------------
# predict button
# ----------------------------------------------------------------
if st.button("Predict Price"):

    # build input dataframe - same columns model was trained on
    input_data = pd.DataFrame(
        [[name, company, year, kms_driven, fuel_type]],
        columns=['name', 'company', 'year', 'kms_driven', 'fuel_type']
    )

    # predict
    prediction = model.predict(input_data)
    price = int(prediction[0])

    # format price nicely
    # convert to lakhs if above 1 lac
    if price >= 100000:
        price_display = f"₹ {price/100000:.2f} Lac"
    else:
        price_display = f"₹ {price:,}"

    # show result
    st.markdown(f"""
        <div class="result-box">
            <div class="label">Estimated Market Price</div>
            <div class="price">{price_display}</div>
            <div class="sub">
                {name} · {year} · {fuel_type} · {kms_driven:,} kms
            </div>
        </div>
    """, unsafe_allow_html=True)

    # extra context below result
    st.markdown("<br>", unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.metric("Year", year)
    with col_b:
        st.metric("Kms Driven", f"{kms_driven:,}")
    with col_c:
        st.metric("Fuel", fuel_type)