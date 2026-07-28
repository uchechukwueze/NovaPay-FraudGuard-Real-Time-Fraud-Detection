from pathlib import Path
from textwrap import dedent

import pandas as pd
import plotly.express as px
import requests
import streamlit as st
import os


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="NovaPay AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = PROJECT_ROOT / "data" / "data_cleaned.csv"

API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)


# =========================================================
# COLOUR PALETTE
# =========================================================

NAVY = "#071426"
GREEN = "#2CE0AE"
RED = "#FF5269"
YELLOW = "#FFCA6A"
WHITE = "#F8FAFC"
MUTED = "#9FB3C8"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background:
            radial-gradient(
                circle at top right,
                #17385f 0%,
                #071426 38%,
                #030914 100%
            );
        color: #f8fafc;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                #071426 0%,
                #030914 100%
            );
        border-right: 1px solid rgba(255, 255, 255, 0.08);
    }

    [data-testid="stSidebar"] * {
        color: #f8fafc;
    }

    .brand-name {
        font-size: 2rem;
        font-weight: 850;
        color: #ffffff;
        margin-bottom: 0;
    }

    .brand-subtitle {
        color: #9fb3c8;
        font-size: 0.9rem;
        margin-top: 0.2rem;
    }

    .hero-card {
        padding: 2.3rem;
        border-radius: 24px;
        background:
            linear-gradient(
                135deg,
                rgba(20, 65, 110, 0.96),
                rgba(6, 20, 38, 0.96)
            );
        border: 1px solid rgba(255, 255, 255, 0.10);
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.30);
        margin-bottom: 1.5rem;
    }

    .hero-title {
        font-size: 2.5rem;
        font-weight: 850;
        line-height: 1.15;
        color: #ffffff;
        margin-bottom: 0.7rem;
    }

    .hero-description {
        font-size: 1rem;
        color: #c2d2e4;
        max-width: 780px;
        line-height: 1.7;
    }

    .hero-badge {
        display: inline-block;
        padding: 0.45rem 0.9rem;
        border-radius: 999px;
        background: rgba(44, 224, 174, 0.12);
        color: #42e8b8;
        border: 1px solid rgba(66, 232, 184, 0.30);
        font-size: 0.8rem;
        font-weight: 750;
        margin-bottom: 1rem;
    }

    .section-title {
        color: #ffffff;
        font-size: 1.4rem;
        font-weight: 800;
        margin-top: 0.5rem;
        margin-bottom: 0.2rem;
    }

    .section-description {
        color: #94a9bf;
        font-size: 0.9rem;
        margin-bottom: 1.2rem;
    }

    div[data-testid="stMetric"] {
        background: rgba(10, 26, 47, 0.88);
        border: 1px solid rgba(255, 255, 255, 0.09);
        padding: 1.2rem;
        border-radius: 18px;
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.18);
    }

    div[data-testid="stMetricLabel"] {
        color: #9fb3c8;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff;
    }

    div[data-baseweb="select"] > div {
        background-color: rgba(10, 26, 47, 0.90);
    }

    div[data-testid="stNumberInput"] input {
        background-color: rgba(10, 26, 47, 0.90);
        color: #ffffff;
    }

    .stButton > button,
    [data-testid="stFormSubmitButton"] button {
        width: 100%;
        border-radius: 12px;
        border: none;
        padding: 0.8rem 1rem;
        font-weight: 750;
        font-size: 1rem;
        color: #04111f;
        background:
            linear-gradient(
                90deg,
                #2ce0ae,
                #49b7ff
            );
        transition: 0.25s ease;
    }

    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 24px rgba(44, 224, 174, 0.20);
    }

    .result-safe {
        padding: 1.4rem;
        border-radius: 18px;
        background: rgba(31, 211, 168, 0.10);
        border: 1px solid rgba(31, 211, 168, 0.35);
        color: #63efc6;
        font-size: 1.2rem;
        font-weight: 750;
    }

    .result-fraud {
        padding: 1.4rem;
        border-radius: 18px;
        background: rgba(255, 82, 105, 0.10);
        border: 1px solid rgba(255, 82, 105, 0.38);
        color: #ff7087;
        font-size: 1.2rem;
        font-weight: 750;
    }

    .risk-low {
        color: #55e6ba;
        font-weight: 750;
    }

    .risk-medium {
        color: #ffca6a;
        font-weight: 750;
    }

    .risk-high {
        color: #ff7087;
        font-weight: 750;
    }

    .footer-note {
        text-align: center;
        color: #71869d;
        font-size: 0.8rem;
        padding-top: 2rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# HERO SECTION
# =========================================================

def display_hero(
    badge: str,
    title: str,
    description: str
) -> None:

    # Keep the HTML continuous so Streamlit renders it
    # instead of displaying parts of it as a code block.
    hero_html = (
        f'<div class="hero-card">'
        f'<div class="hero-badge">{badge}</div>'
        f'<div class="hero-title">{title}</div>'
        f'<div class="hero-description">{description}</div>'
        f'</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True
    )


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data(file_path: Path) -> pd.DataFrame:

    data = pd.read_csv(file_path)

    # Create aliases using the actual cleaned column names.
    # These aliases are only created inside the dashboard.
    # The original CSV file is not changed.

    # Convert timestamps to timezone-naive UTC values so they
    # can be compared safely with the date filter selections.
    data["timestamp"] = (
        pd.to_datetime(
            data["timestamp_clean"],
            errors="coerce",
            utc=True
        )
        .dt.tz_convert(None)
    )

    data["amount_usd"] = pd.to_numeric(
        data["amount_usd_clean"],
        errors="coerce"
    )

    data["amount_src"] = pd.to_numeric(
        data["amount_src_clean"],
        errors="coerce"
    )

    data["fee"] = pd.to_numeric(
        data["fee_clean"],
        errors="coerce"
    )

    data["country"] = (
        data["home_country_clean"]
        .fillna("Unknown")
        .astype(str)
    )

    data["home_country"] = (
        data["home_country_clean"]
        .fillna("Unknown")
        .astype(str)
    )

    data["ip_country"] = (
        data["ip_country_clean"]
        .fillna("Unknown")
        .astype(str)
    )

    data["kyc_tier"] = (
        data["kyc_tier_clean"]
        .fillna("Unknown")
        .astype(str)
    )

    data["device_trust_score"] = pd.to_numeric(
        data["device_trust_score_clean"],
        errors="coerce"
    )

    # Make sure is_fraud is numeric.
    if data["is_fraud"].dtype == bool:

        data["is_fraud"] = (
            data["is_fraud"]
            .astype(int)
        )

    elif data["is_fraud"].dtype == object:

        fraud_mapping = {
            "fraud": 1,
            "legitimate": 0,
            "true": 1,
            "false": 0,
            "yes": 1,
            "no": 0,
            "1": 1,
            "0": 0
        }

        cleaned_target = (
            data["is_fraud"]
            .astype(str)
            .str.strip()
            .str.lower()
            .map(fraud_mapping)
        )

        data["is_fraud"] = (
            cleaned_target
            .fillna(0)
            .astype(int)
        )

    else:

        data["is_fraud"] = (
            pd.to_numeric(
                data["is_fraud"],
                errors="coerce"
            )
            .fillna(0)
            .astype(int)
        )

    return data


try:

    df = load_data(DATA_PATH)
    data_error = None

except Exception as error:

    df = pd.DataFrame()
    data_error = str(error)


# =========================================================
# API CONNECTION
# =========================================================

def check_api_connection() -> bool:

    try:

        response = requests.get(
            f"{API_URL}/health",
            timeout=4
        )

        return response.status_code == 200

    except requests.RequestException:

        return False


api_is_connected = check_api_connection()


# =========================================================
# PLOTLY CHART STYLE
# =========================================================

def style_chart(
    figure,
    height: int = 390
):

    figure.update_layout(
        height=height,
        paper_bgcolor="rgba(0, 0, 0, 0)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        font={
            "color": "#DCE8F5",
            "family": "Arial"
        },
        title={
            "font": {
                "size": 19,
                "color": "#FFFFFF"
            }
        },
        margin={
            "l": 20,
            "r": 20,
            "t": 65,
            "b": 30
        },
        legend={
            "bgcolor": "rgba(0, 0, 0, 0)"
        },
        hoverlabel={
            "bgcolor": "#0A1A2F",
            "font_color": "#FFFFFF"
        }
    )

    figure.update_xaxes(
        gridcolor="rgba(255, 255, 255, 0.06)",
        zerolinecolor="rgba(255, 255, 255, 0.08)"
    )

    figure.update_yaxes(
        gridcolor="rgba(255, 255, 255, 0.06)",
        zerolinecolor="rgba(255, 255, 255, 0.08)"
    )

    return figure


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown(
        """
        <div class="brand-name">
            NovaPay AI
        </div>

        <div class="brand-subtitle">
            Intelligent fraud prevention
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "Executive Overview",
            "Live Fraud Scoring",
            "Fraud Intelligence",
            "Model Performance",
            "About NovaPay"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")

    if api_is_connected:

        st.success("Fraud API connected")

    else:

        st.error("Fraud API disconnected")

    if data_error is None:

        st.success("Transaction data loaded")
        st.caption(f"Dataset: {DATA_PATH.name}")

        detected_fields = {
            "Fraud target": (
                "is_fraud"
                if "is_fraud" in df.columns
                else None
            ),
            "Amount": (
                "amount_usd_clean"
                if "amount_usd_clean" in df.columns
                else None
            ),
            "Date": (
                "timestamp_clean"
                if "timestamp_clean" in df.columns
                else None
            ),
            "Channel": (
                "channel"
                if "channel" in df.columns
                else None
            ),
            "Country": (
                "home_country_clean"
                if "home_country_clean" in df.columns
                else None
            )
        }

        with st.expander("Detected dataset fields"):
            st.json(detected_fields)

    else:

        st.error("Transaction data unavailable")

    st.markdown("---")

    st.caption(
        "Powered by LightGBM, FastAPI, Docker and Streamlit"
    )


# =========================================================
# EXECUTIVE OVERVIEW
# =========================================================

if page == "Executive Overview":

    display_hero(
        badge="FRAUD MONITORING COMMAND CENTRE",
        title=(
            "Understand fraud exposure across "
            "the NovaPay network."
        ),
        description=(
            "Monitor transaction activity, fraud rates, "
            "financial exposure and high-risk payment "
            "channels from one intelligent dashboard."
        )
    )

    if data_error is not None:

        st.error(
            f"NovaPay could not load the dataset: {data_error}"
        )

        st.info(
            "Confirm that data_cleaned.csv is inside the data folder."
        )

        st.stop()

    if "is_fraud" not in df.columns:

        st.error(
            "The dataset does not contain the is_fraud column."
        )

        st.stop()

    # -----------------------------------------------------
    # FILTERS
    # -----------------------------------------------------

    filtered_df = df.copy()

    filter_col_1, filter_col_2 = st.columns(
        [1, 2]
    )

    with filter_col_1:

        available_channels = sorted(
            filtered_df["channel"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )

        selected_channel = st.selectbox(
            "Filter by channel",
            options=["All Channels"] + available_channels
        )

        if selected_channel != "All Channels":

            filtered_df = filtered_df[
                filtered_df["channel"].astype(str)
                == selected_channel
            ]

    with filter_col_2:

        valid_dates = (
            filtered_df["timestamp"]
            .dropna()
        )

        if not valid_dates.empty:

            min_date = valid_dates.min().date()
            max_date = valid_dates.max().date()

            selected_dates = st.date_input(
                "Filter by transaction date",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )

            if (
                isinstance(selected_dates, (tuple, list))
                and len(selected_dates) == 2
            ):

                start_date = pd.Timestamp(
                    selected_dates[0]
                )

                end_date = (
                    pd.Timestamp(selected_dates[1])
                    + pd.Timedelta(days=1)
                )

                filtered_df = filtered_df[
                    (
                        filtered_df["timestamp"]
                        >= start_date
                    )
                    &
                    (
                        filtered_df["timestamp"]
                        < end_date
                    )
                ]

    if filtered_df.empty:

        st.warning(
            "No transactions match the selected filters."
        )

        st.stop()

    # -----------------------------------------------------
    # KPI CALCULATIONS
    # -----------------------------------------------------

    total_transactions = len(filtered_df)

    fraud_transactions = int(
        filtered_df["is_fraud"]
        .fillna(0)
        .sum()
    )

    fraud_rate = (
        fraud_transactions
        / total_transactions
        * 100
    )

    transaction_value = (
        filtered_df["amount_usd"]
        .fillna(0)
        .sum()
    )

    amount_lost_to_fraud = (
        filtered_df.loc[
            filtered_df["is_fraud"] == 1,
            "amount_usd"
        ]
        .fillna(0)
        .sum()
    )

    # -----------------------------------------------------
    # KPI CARDS
    # -----------------------------------------------------

    metric_1, metric_2, metric_3, metric_4, metric_5 = st.columns(5)

    with metric_1:

        st.metric(
            "Total Transactions",
            f"{total_transactions:,}"
        )

    with metric_2:

        st.metric(
            "Fraudulent Transactions",
            f"{fraud_transactions:,}"
        )

    with metric_3:

        st.metric(
            "Fraud Rate",
            f"{fraud_rate:.2f}%"
        )

    with metric_4:

        st.metric(
            "Transaction Value",
            f"${transaction_value:,.0f}"
        )

    with metric_5:

        st.metric(
            "Amount Lost to Fraud",
            f"${amount_lost_to_fraud:,.0f}"
        )

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    # -----------------------------------------------------
    # MONTHLY FRAUD TREND
    # -----------------------------------------------------

    trend_column, distribution_column = st.columns(
        [1.65, 0.85],
        gap="large"
    )

    with trend_column:

        monthly_data = (
            filtered_df
            .dropna(subset=["timestamp"])
            .assign(
                month=lambda data: (
                    data["timestamp"]
                    .dt.to_period("M")
                    .dt.to_timestamp()
                )
            )
            .groupby("month")
            .agg(
                transactions=("is_fraud", "size"),
                fraud_cases=("is_fraud", "sum")
            )
            .reset_index()
        )

        monthly_data["fraud_rate"] = (
            monthly_data["fraud_cases"]
            / monthly_data["transactions"]
            * 100
        )

        monthly_figure = px.line(
            monthly_data,
            x="month",
            y="fraud_rate",
            markers=True,
            title="Monthly Fraud Rate",
            labels={
                "month": "Month",
                "fraud_rate": "Fraud Rate (%)"
            },
            color_discrete_sequence=[RED]
        )

        monthly_figure.update_traces(
            line={
                "width": 3
            },
            marker={
                "size": 8,
                "line": {
                    "width": 1,
                    "color": WHITE
                }
            }
        )

        monthly_figure = style_chart(
            monthly_figure,
            height=410
        )

        st.plotly_chart(
            monthly_figure,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    # -----------------------------------------------------
    # FRAUD DISTRIBUTION
    # -----------------------------------------------------

    with distribution_column:

        fraud_distribution = (
            filtered_df["is_fraud"]
            .value_counts()
            .rename_axis("fraud_label")
            .reset_index(name="transactions")
        )

        fraud_distribution["status"] = (
            fraud_distribution["fraud_label"]
            .map({
                0: "Legitimate",
                1: "Fraud"
            })
            .fillna("Unknown")
        )

        distribution_figure = px.pie(
            fraud_distribution,
            names="status",
            values="transactions",
            hole=0.62,
            title="Transaction Distribution",
            color="status",
            color_discrete_map={
                "Legitimate": GREEN,
                "Fraud": RED,
                "Unknown": MUTED
            }
        )

        distribution_figure.update_traces(
            textinfo="percent+label",
            textfont={
                "color": WHITE
            },
            marker={
                "line": {
                    "color": NAVY,
                    "width": 2
                }
            }
        )

        distribution_figure = style_chart(
            distribution_figure,
            height=410
        )

        st.plotly_chart(
            distribution_figure,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    # -----------------------------------------------------
    # CHANNEL AND VALUE ANALYSIS
    # -----------------------------------------------------

    channel_column, amount_column = st.columns(
        2,
        gap="large"
    )

    with channel_column:

        channel_summary = (
            filtered_df
            .assign(
                channel=lambda data: (
                    data["channel"]
                    .fillna("Unknown")
                    .astype(str)
                )
            )
            .groupby("channel")
            .agg(
                transactions=("is_fraud", "size"),
                fraud_cases=("is_fraud", "sum")
            )
            .reset_index()
        )

        channel_summary["fraud_rate"] = (
            channel_summary["fraud_cases"]
            / channel_summary["transactions"]
            * 100
        )

        channel_summary = (
            channel_summary
            .sort_values(
                "fraud_rate",
                ascending=False
            )
        )

        channel_figure = px.bar(
            channel_summary,
            x="channel",
            y="fraud_rate",
            title="Fraud Rate by Transaction Channel",
            labels={
                "channel": "Channel",
                "fraud_rate": "Fraud Rate (%)"
            },
            color="fraud_rate",
            color_continuous_scale=[
                GREEN,
                YELLOW,
                RED
            ]
        )

        channel_figure.update_traces(
            texttemplate="%{y:.1f}%",
            textposition="outside"
        )

        channel_figure = style_chart(
            channel_figure
        )

        channel_figure.update_layout(
            coloraxis_showscale=False
        )

        st.plotly_chart(
            channel_figure,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    with amount_column:

        amount_summary = (
            filtered_df
            .assign(
                status=lambda data: (
                    data["is_fraud"]
                    .map({
                        0: "Legitimate",
                        1: "Fraud"
                    })
                )
            )
            .groupby("status")
            .agg(
                total_value=("amount_usd", "sum")
            )
            .reset_index()
        )

        amount_figure = px.bar(
            amount_summary,
            x="status",
            y="total_value",
            title="Transaction Value by Fraud Status",
            labels={
                "status": "Transaction Status",
                "total_value": "Transaction Value (USD)"
            },
            color="status",
            color_discrete_map={
                "Legitimate": GREEN,
                "Fraud": RED
            }
        )

        amount_figure.update_traces(
            texttemplate="$%{y:,.0f}",
            textposition="outside"
        )

        amount_figure = style_chart(
            amount_figure
        )

        amount_figure.update_layout(
            showlegend=False
        )

        st.plotly_chart(
            amount_figure,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    # -----------------------------------------------------
    # RECENT TRANSACTIONS
    # -----------------------------------------------------

    st.markdown(
        """
        <div class="section-title">
            Recent Transaction Activity
        </div>

        <div class="section-description">
            Latest transactions available in the cleaned dataset.
        </div>
        """,
        unsafe_allow_html=True
    )

    table_columns = [
        "timestamp",
        "amount_usd",
        "channel",
        "home_country",
        "kyc_tier",
        "device_trust_score",
        "ip_risk_score",
        "is_fraud"
    ]

    recent_transactions = (
        filtered_df
        .sort_values(
            "timestamp",
            ascending=False
        )
        [table_columns]
        .head(15)
    )

    recent_transactions = recent_transactions.rename(
        columns={
            "timestamp": "Timestamp",
            "amount_usd": "Amount USD",
            "channel": "Channel",
            "home_country": "Home Country",
            "kyc_tier": "KYC Tier",
            "device_trust_score": "Device Trust Score",
            "ip_risk_score": "IP Risk Score",
            "is_fraud": "Fraud"
        }
    )

    st.dataframe(
        recent_transactions,
        hide_index=True,
        use_container_width=True
    )


# =========================================================
# LIVE FRAUD SCORING
# =========================================================

elif page == "Live Fraud Scoring":

    display_hero(
        badge="REAL-TIME FRAUD INTELLIGENCE",
        title=(
            "Stop suspicious transactions before "
            "they become losses."
        ),
        description=(
            "NovaPay AI analyses transaction behaviour, "
            "device signals, customer activity and network "
            "risk to estimate the probability of fraud "
            "in real time."
        )
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)

    with metric_1:

        st.metric(
            "Detection Model",
            "LightGBM"
        )

    with metric_2:

        st.metric(
            "API Status",
            (
                "Connected"
                if api_is_connected
                else "Disconnected"
            )
        )

    with metric_3:

        st.metric(
            "Scoring Mode",
            "Real Time"
        )

    with metric_4:

        st.metric(
            "Decision Output",
            "Fraud Risk"
        )

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    form_column, result_column = st.columns(
        [1.35, 0.85],
        gap="large"
    )

    with form_column:

        st.markdown(
            """
            <div class="section-title">
                Transaction Risk Assessment
            </div>

            <div class="section-description">
                Enter the transaction details to generate a fraud score.
            </div>
            """,
            unsafe_allow_html=True
        )

        with st.form("fraud_prediction_form"):

            input_col_1, input_col_2 = st.columns(2)

            with input_col_1:

                amount_usd = st.number_input(
                    "Transaction amount (USD)",
                    min_value=0.0,
                    value=500.0,
                    step=50.0
                )

                txn_velocity_1h = st.number_input(
                    "Transactions in the last hour",
                    min_value=0,
                    value=3,
                    step=1
                )

                ip_risk_score = st.slider(
                    "IP risk score",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.40,
                    step=0.01
                )

                new_device = st.selectbox(
                    "New device?",
                    options=[
                        "No",
                        "Yes"
                    ]
                )

            with input_col_2:

                channel = st.selectbox(
                    "Transaction channel",
                    options=[
                        "mobile",
                        "web",
                        "ATM"
                    ]
                )

                txn_velocity_24h = st.number_input(
                    "Transactions in the last 24 hours",
                    min_value=0,
                    value=10,
                    step=1
                )

                device_trust_score = st.slider(
                    "Device trust score",
                    min_value=0.0,
                    max_value=1.0,
                    value=0.70,
                    step=0.01
                )

                location_mismatch = st.selectbox(
                    "Location mismatch?",
                    options=[
                        "No",
                        "Yes"
                    ]
                )

            submitted = st.form_submit_button(
                "Analyse Transaction"
            )

    with result_column:

        st.markdown(
            """
            <div class="section-title">
                Risk Decision
            </div>

            <div class="section-description">
                The fraud prediction will appear here.
            </div>
            """,
            unsafe_allow_html=True
        )

        if not submitted:

            st.info(
                "Complete the form and select Analyse Transaction."
            )

        elif not api_is_connected:

            st.error(
                "The fraud API is not connected. "
                "Confirm that Docker is running."
            )

        else:

            transaction = {
                "amount_usd": amount_usd,
                "txn_velocity_1h": txn_velocity_1h,
                "txn_velocity_24h": txn_velocity_24h,
                "ip_risk_score": ip_risk_score,
                "device_trust_score": device_trust_score,
                "new_device": (
                    1 if new_device == "Yes" else 0
                ),
                "location_mismatch": (
                    1 if location_mismatch == "Yes" else 0
                ),
                "channel": channel
            }

            try:

                prediction_response = requests.post(
                    f"{API_URL}/predict",
                    json=transaction,
                    timeout=10
                )

                if prediction_response.status_code == 200:

                    result = prediction_response.json()

                    prediction = result["prediction"]

                    probability = float(
                        result["fraud_probability"]
                    )

                    if probability < 0.30:

                        risk_level = "Low Risk"
                        risk_class = "risk-low"

                    elif probability < 0.70:

                        risk_level = "Medium Risk"
                        risk_class = "risk-medium"

                    else:

                        risk_level = "High Risk"
                        risk_class = "risk-high"

                    if prediction == "Fraud":

                        st.markdown(
                            """
                            <div class="result-fraud">
                                Suspicious Transaction Detected
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    else:

                        st.markdown(
                            """
                            <div class="result-safe">
                                Transaction Appears Legitimate
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                    st.markdown(
                        "<br>",
                        unsafe_allow_html=True
                    )

                    st.metric(
                        "Fraud Probability",
                        f"{probability:.1%}"
                    )

                    st.progress(
                        min(
                            max(probability, 0.0),
                            1.0
                        )
                    )

                    st.markdown(
                        f"""
                        <p class="{risk_class}">
                            Risk classification: {risk_level}
                        </p>
                        """,
                        unsafe_allow_html=True
                    )

                    if risk_level == "High Risk":

                        st.warning(
                            "Recommended action: Hold the "
                            "transaction for manual review."
                        )

                    elif risk_level == "Medium Risk":

                        st.info(
                            "Recommended action: Request "
                            "additional customer verification."
                        )

                    else:

                        st.success(
                            "Recommended action: Transaction may proceed."
                        )

                else:

                    st.error(
                        f"Prediction failed: "
                        f"{prediction_response.text}"
                    )

            except requests.RequestException:

                st.error(
                    "The fraud prediction API could not be reached."
                )


# =========================================================
# FRAUD INTELLIGENCE
# =========================================================

elif page == "Fraud Intelligence":

    display_hero(
        badge="BEHAVIOURAL FRAUD ANALYSIS",
        title="Discover where fraud is concentrated.",
        description=(
            "Compare fraud exposure across payment channels, "
            "home countries and transaction periods."
        )
    )

    if data_error is not None:

        st.error(
            f"Dataset loading failed: {data_error}"
        )

        st.stop()

    chart_column_1, chart_column_2 = st.columns(
        2,
        gap="large"
    )

    # -----------------------------------------------------
    # CHANNEL FRAUD RATE
    # -----------------------------------------------------

    with chart_column_1:

        channel_intelligence = (
            df
            .assign(
                channel=lambda data: (
                    data["channel"]
                    .fillna("Unknown")
                    .astype(str)
                )
            )
            .groupby("channel")
            .agg(
                transactions=("is_fraud", "size"),
                fraud_cases=("is_fraud", "sum")
            )
            .reset_index()
        )

        channel_intelligence["fraud_rate"] = (
            channel_intelligence["fraud_cases"]
            / channel_intelligence["transactions"]
            * 100
        )

        channel_intelligence = (
            channel_intelligence
            .sort_values(
                "fraud_rate",
                ascending=True
            )
        )

        channel_intelligence_figure = px.bar(
            channel_intelligence,
            x="fraud_rate",
            y="channel",
            orientation="h",
            title="Highest-Risk Transaction Channels",
            labels={
                "fraud_rate": "Fraud Rate (%)",
                "channel": "Channel"
            },
            color="fraud_rate",
            color_continuous_scale=[
                GREEN,
                YELLOW,
                RED
            ]
        )

        channel_intelligence_figure.update_traces(
            texttemplate="%{x:.1f}%",
            textposition="outside"
        )

        channel_intelligence_figure = style_chart(
            channel_intelligence_figure
        )

        channel_intelligence_figure.update_layout(
            coloraxis_showscale=False
        )

        st.plotly_chart(
            channel_intelligence_figure,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    # -----------------------------------------------------
    # HOME COUNTRY FRAUD RATE
    # -----------------------------------------------------

    with chart_column_2:

        country_intelligence = (
            df
            .assign(
                home_country=lambda data: (
                    data["home_country"]
                    .fillna("Unknown")
                    .astype(str)
                )
            )
            .groupby("home_country")
            .agg(
                transactions=("is_fraud", "size"),
                fraud_cases=("is_fraud", "sum")
            )
            .reset_index()
        )

        country_intelligence["fraud_rate"] = (
            country_intelligence["fraud_cases"]
            / country_intelligence["transactions"]
            * 100
        )

        country_intelligence = (
            country_intelligence
            .sort_values(
                "fraud_rate",
                ascending=False
            )
            .head(10)
        )

        country_figure = px.bar(
            country_intelligence,
            x="home_country",
            y="fraud_rate",
            title="Top Home Countries by Fraud Rate",
            labels={
                "home_country": "Home Country",
                "fraud_rate": "Fraud Rate (%)"
            },
            color="fraud_rate",
            color_continuous_scale=[
                GREEN,
                YELLOW,
                RED
            ]
        )

        country_figure.update_traces(
            texttemplate="%{y:.1f}%",
            textposition="outside"
        )

        country_figure = style_chart(
            country_figure
        )

        country_figure.update_layout(
            coloraxis_showscale=False
        )

        st.plotly_chart(
            country_figure,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    # -----------------------------------------------------
    # MONTHLY FRAUD CASES
    # -----------------------------------------------------

    monthly_fraud = (
        df
        .dropna(subset=["timestamp"])
        .assign(
            month=lambda data: (
                data["timestamp"]
                .dt.to_period("M")
                .dt.to_timestamp()
            )
        )
        .groupby("month")
        .agg(
            total_transactions=("is_fraud", "size"),
            fraud_cases=("is_fraud", "sum")
        )
        .reset_index()
    )

    monthly_fraud_figure = px.bar(
        monthly_fraud,
        x="month",
        y="fraud_cases",
        title="Monthly Fraud Cases",
        labels={
            "month": "Month",
            "fraud_cases": "Fraud Cases"
        },
        color_discrete_sequence=[RED]
    )

    monthly_fraud_figure.update_traces(
        texttemplate="%{y:,}",
        textposition="outside"
    )

    monthly_fraud_figure = style_chart(
        monthly_fraud_figure,
        height=430
    )

    st.plotly_chart(
        monthly_fraud_figure,
        use_container_width=True,
        config={
            "displayModeBar": False
        }
    )


# =========================================================
# MODEL PERFORMANCE
# =========================================================

elif page == "Model Performance":

    display_hero(
        badge="MODEL VALIDATION",
        title="Evaluate how well NovaPay identifies fraud.",
        description=(
            "Review the final LightGBM model's fraud-class "
            "precision, recall, F1 score and PR-AUC."
        )
    )

    model_metric_1, model_metric_2, model_metric_3, model_metric_4 = (
        st.columns(4)
    )

    with model_metric_1:

        st.metric(
            "PR-AUC",
            "0.962"
        )

    with model_metric_2:

        st.metric(
            "Fraud Precision",
            "1.00"
        )

    with model_metric_3:

        st.metric(
            "Fraud Recall",
            "0.92"
        )

    with model_metric_4:

        st.metric(
            "Fraud F1 Score",
            "0.95"
        )

    st.markdown(
        "<br>",
        unsafe_allow_html=True
    )

    performance_column, matrix_column = st.columns(
        [1, 1],
        gap="large"
    )

    with performance_column:

        performance_table = pd.DataFrame(
            {
                "Metric": [
                    "PR-AUC",
                    "Fraud Precision",
                    "Fraud Recall",
                    "Fraud F1 Score"
                ],
                "Score": [
                    0.9617,
                    1.0000,
                    0.9200,
                    0.9500
                ]
            }
        )

        performance_figure = px.bar(
            performance_table,
            x="Metric",
            y="Score",
            color="Metric",
            title="Model Performance Scores",
            text="Score",
            color_discrete_sequence=[
                "#3CC7D6",
                "#49B7FF",
                "#2CE0AE",
                "#40C9C3"
            ]
        )

        performance_figure.update_traces(
            texttemplate="%{y:.3f}",
            textposition="outside"
        )

        performance_figure = style_chart(
            performance_figure,
            height=430
        )

        performance_figure.update_layout(
            showlegend=False,
            yaxis_range=[0, 1.08],
            xaxis_title="Metric",
            yaxis_title="Score"
        )

        st.plotly_chart(
            performance_figure,
            use_container_width=True,
            config={
                "displayModeBar": False
            }
        )

    with matrix_column:

        st.markdown(
            """
            <div class="section-title">
                Confusion Matrix
            </div>
            """,
            unsafe_allow_html=True
        )

        confusion_matrix = pd.DataFrame(
            [
                [1918, 1],
                [26, 283]
            ],
            index=[
                "Actual Legitimate",
                "Actual Fraud"
            ],
            columns=[
                "Predicted Legitimate",
                "Predicted Fraud"
            ]
        )

        st.dataframe(
            confusion_matrix,
            use_container_width=True
        )

        st.caption(
            "These values come from the final "
            "time-based test evaluation."
        )


# =========================================================
# ABOUT NOVAPAY
# =========================================================

elif page == "About NovaPay":

    display_hero(
        badge="ABOUT THE PROJECT",
        title=(
            "An intelligent defence layer "
            "for digital payments."
        ),
        description=(
            "NovaPay AI is a machine-learning real-time "
            "fraud-detection system designed to identify "
            "suspicious financial transactions through "
            "behavioural, device, location and "
            "transaction-risk signals within milliseconds."
        )
    )

    about_column_1, about_column_2, about_column_3 = st.columns(3)

    with about_column_1:

        st.subheader("Machine Learning")

        st.write(
            """
            A tuned LightGBM model estimates the probability
            that a transaction is fraudulent.
            """
        )

    with about_column_2:

        st.subheader("Real-Time API")

        st.write(
            """
            FastAPI exposes the saved model through a prediction
            endpoint that receives transaction information.
            """
        )

    with about_column_3:

        st.subheader("Deployment")

        st.write(
            """
            Docker packages the FastAPI service, model files
            and required Python dependencies.
            """
        )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer-note">
        NovaPay AI · Intelligent Fraud Prevention Platform
    </div>
    """,
    unsafe_allow_html=True
)