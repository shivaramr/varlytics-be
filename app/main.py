from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import stock, search, varlytics_special, simulations, portfolio, nifty, prophet_prediction

app = FastAPI(
    title="VaRLytics API",
    openapi_tags=[
        {
            "name": "General",
            "description": "General utilities like search.",
        },
        {
            "name": "Stock",
            "description": "Operations related to stock data.",
        },
        {
            "name": "VarLytics Special",
            "description": "Specialized financial analytics and simulations.",
        },
        {
            "name": "Simulations",
            "description": "22 different simulation models including GARCH, EGARCH, GJR-GARCH variants.",
        },
        {
            "name": "Portfolio Analysis",
            "description": "Comprehensive portfolio risk analysis with multiple VaR models and stress testing.",
        },
        {
            "name": "Nifty 50",
            "description": "Comprehensive Nifty 50 index analytics including summary, technical indicators, risk metrics, market overview, and sentiment analysis.",
        },
        {
            "name": "Stock Price Prediction",
            "description": "AI-powered stock price prediction using Meta's Prophet machine learning library with 3 years of historical data analysis.",
        },
    ],
)

# ✅ Add CORS Middleware
origins = [
    "http://localhost:5173",  # your frontend dev server
    "http://localhost:3000",  # your frontend dev server
    "https://your-frontend-domain.com",  # your production frontend
    # add other allowed origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # or ["*"] for public APIs (not recommended with credentials)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Include API routers
app.include_router(stock.router, prefix="/api")
app.include_router(search.router, prefix="/api")
app.include_router(varlytics_special.router, prefix="/api")
app.include_router(simulations.router, prefix="/api")
app.include_router(portfolio.router, prefix="/api")
app.include_router(nifty.router, prefix="/api")
app.include_router(prophet_prediction.router, prefix="/api")
