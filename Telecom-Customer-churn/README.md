# Telecom Customer Churn Prediction

## Project Overview
This project aims to predict customer churn for a telecommunications company using demographic and usage data. By identifying at-risk customers, the business can implement targeted retention campaigns to reduce churn rates.

## Dataset
The dataset used is the **Telco Customer Churn** dataset from Kaggle.
- Source: [Kaggle Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- File: `WA_Fn-UseC_-Telco-Customer-Churn.csv`
- Target: `Churn` (Yes/No)

##Key Insights & Business Recommendations
- Contract Type: Customers with month-to-month contracts are significantly more likely to churn compared to those with one or two-year contracts. *Recommendation: Offer incentives for customers to switch to longer-term contracts.*
- Tenure & Monthly Charges: New customers with high monthly charges are at high risk. *Recommendation: Implement a loyalty program or first-year discounts to increase tenure.*
- Internet Service: Fiber optic customers show higher churn rates, possibly due to pricing or service issues. Recommendation: Investigate service quality and competitive pricing for fiber optic plans.*
- Payment Method: Electronic check users churn more often. *Recommendation: Encourage automatic payment methods.*

## Model Performance Summary
- **Best Model**: Gradient Boosting Classifier
- **Metrics**: 
  - F1-Score: (~calculated during run)
  - Accuracy: (~calculated during run)
  - ROC-AUC: (~calculated during run)

## How to Run (Step-by-Step)

## 1. Prerequisites
- Python 3.8+
- Active internet connection (for Google Fonts & Icons)

### 2. Setup & Installation
```bash
# Install dependencies
pip install -r requirements.txt
pip install fastapi uvicorn pydantic python-multipart
```

### 3. Prepare AI Assets
Run the script to train the final model and save the scaler/features:
```bash
python prepare_api_assets.py
```

### 4. Start the Backend API
```bash
# Run the FastAPI server
python main.py
```
The API will be available at `http://localhost:8000`.

### 5. Launch the Web App
Simply open `index.html` in your web browser. Fill in the customer details and click **Analyze Risk** to see the prediction.

## Project Structure
- `churn_prediction.ipynb`: Original analysis and model development.
- `main.py`: FastAPI backend implementation.
- `index.html`, `style.css`, `script.js`: Premium frontend application.
- `models/`: Trained model, scaler, and feature set.
- `eda_plots/`: Visualizations from the EDA phase.
