import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Jineau - Vertical Farm Calculator", layout="centered")

st.title("🌿 Jineau - Vertical Farm Financial & Risk Calculator")
st.markdown("This tool helps you estimate ROI, Levelized Cost, and Loan Risk for your vertical farming project.")

# --- Input Parameters ---
st.sidebar.header("🔧 Input Parameters")
CapEx = st.sidebar.number_input("Capital Expenditure (CapEx) [$]", value=400000)
OpEx = st.sidebar.number_input("Annual Operating Cost (OpEx) [$]", value=80000)
price_per_kg = st.sidebar.number_input("Price per kg [$]", value=4.99)
yield_annual = st.sidebar.number_input("Annual Yield [kg]", value=7000)
discount_rate = st.sidebar.slider("Discount Rate [%]", 0.0, 0.2, 0.07)
loan_amount = st.sidebar.number_input("Loan Amount [$]", value=300000)
interest_rate = st.sidebar.slider("Interest Rate [%]", 0.00, 0.2, 0.05)
loan_term = st.sidebar.slider("Loan Term [Years]", 1, 10, 5)
grace_period = st.sidebar.slider("Grace Period [Years]", 0, 5, 0)
stepwise = st.sidebar.checkbox("Stepwise (پلکانی) Repayment", value=False)

# --- Levelized Cost Calculation ---
def levelized_cost(capex, opex, yield_kg, r, n=5):
    discounted_opex = sum([opex / (1 + r) ** (k + 1) for k in range(n)])
    discounted_yield = sum([yield_kg / (1 + r) ** (k + 1) for k in range(n)])
    return (capex + discounted_opex) / discounted_yield

lc = levelized_cost(CapEx, OpEx, yield_annual, discount_rate)

# --- Loan Repayment Schedule ---
def loan_schedule(amount, rate, term, grace=0, stepwise=False):
    schedule = []
    for year in range(1, term + 1):
        if year <= grace:
            payment = 0
        elif stepwise:
            step = (year - grace) / (term - grace)
            payment = (amount / (term - grace)) * (1 + step * rate)
        else:
            payment = (amount * (1 + rate * (term - grace))) / (term - grace)
        schedule.append(payment)
    return schedule

repayments = loan_schedule(loan_amount, interest_rate, loan_term, grace_period, stepwise)
total_repay = sum(repayments)

# --- Outputs ---
revenue = yield_annual * price_per_kg
roi = (revenue - OpEx) / CapEx

st.subheader("📊 Financial Summary")
st.write(f"**Levelized Cost ($/kg):** ${lc:.2f}")
st.write(f"**Annual Revenue:** ${revenue:,.0f}")
st.write(f"**ROI:** {roi * 100:.1f}%")
st.write(f"**Total Loan Repayment:** ${total_repay:,.0f}")

# --- Chart ---
st.subheader("📈 Loan Repayment Schedule")
fig, ax = plt.subplots()
ax.plot(range(1, loan_term + 1), repayments, marker='o')
ax.set_xlabel("Year")
ax.set_ylabel("Annual Payment ($)")
ax.set_title("Loan Repayment Over Time")
st.pyplot(fig)
