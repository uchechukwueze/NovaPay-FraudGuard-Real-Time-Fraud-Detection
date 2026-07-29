
<p align="center">
  <img src="image.png"
       alt="Fraudulent Transaction Detection"
       width="100%">
</p>
# NovaPay FraudGuard: Real-Time Fraud Detection
The purpose of this project is to develop a machine learning-based fraud detection system for NovaPay, replacing its existing static, rules-based approach

### Business Context
NovaPay, a rapidly growing digital money transfer company, faces significant challenges in maintaining the security of its transactions amidst the increasing sophistication of fraud. As the company expands globally, it is essential to protect its customers and maintain operational efficiency. Fraudulent activities such as identity theft, unauthorized payments, and account takeovers threaten the company’s financial integrity and customer trust. Given the company's reliance on real-time transactions, the need for a more robust, scalable, and adaptable fraud detection system is critical.

### Purpose of Project
The purpose of this project is to develop a machine learning-based fraud detection system for NovaPay, replacing its existing static, rules-based approach. The solution will aim to enhance the accuracy of detecting fraudulent transactions while minimizing the rate of false positives (legitimate transactions wrongly flagged as fraudulent). This will ensure that customers have a smoother experience and trust in the service while also reducing the operational and financial impact of fraud. The machine learning model will be capable of evolving as fraud tactics change, providing long-term adaptability and scalability.

### Expected Outcome
The expected outcomes of this project are:

Increased Accuracy in Fraud Detection: A significant improvement in identifying fraudulent transactions compared to the previous rules-based system, with at least a 15% increase in recall (ability to catch fraudulent transactions).

Reduced False Positives: A decrease in the number of legitimate transactions wrongly flagged as fraud, improving the customer experience.

Scalable and Adaptable System: A machine learning system that can scale with NovaPay’s growth and quickly adapt to new fraud tactics.

Regulatory Compliance: An explainable model that provides transparent reasons for fraud predictions, ensuring that regulatory requirements are met.

Operational Efficiency: A model deployed as a microservice, integrated seamlessly into NovaPay’s transaction system, enabling real-time fraud detection without the need for manual reviews.

### Business Overview
NovaPay is a digital-first cross-border money transfer company based in Toronto, Canada. Operating in the United Kingdom, Canada, and United States, NovaPay empowers users to seamlessly send, receive, and hold multiple currencies across international borders.

### Key highlights:

Processes millions of monthly transactions across international borders

Prioritizes three key pillars: affordability, lightning-fast speed, and exceptional digital experiences

Serves diverse customer segments from expatriates supporting families abroad to businesses managing international payroll and freelancers receiving global payments

Mission-driven to make international money movement accessible and transparent

The company's strong customer satisfaction strategy depends heavily on secure transaction processing — making accurate early detection of fraudulent transactions a strategic priority.


### Busines Challenge
Digital payment platforms face a number of operational, financial, and regulatory challenges when handling fraud detection:

### Operational Challenges
Real-time processing requirements limit manual review capacity

Current static rules combined with manual review processes struggle to scale effectively and adapt to rapidly evolving fraudster tactics

Identity theft, account takeover, transaction laundering, and unauthorized payments pose constant threats

### Financial Challenges
Mounting costs from refunds, chargebacks, and compliance penalties erode profitability

False positives frustrate legitimate users and can drive customer attrition

Missed fraud damages revenue and increases operational costs

### Regulatory Challenges
Financial regulations require transparent and auditable fraud detection systems

Anti-money laundering (AML) and Know Your Customer (KYC) compliance frameworks demand explainable decision-making

Failure to maintain adequate fraud controls results in penalties or increased regulatory scrutiny

### Key Pain Points
Identity theft, account takeover, transaction laundering, and unauthorized payments

Highly imbalanced dataset (fraud represents less than 1% of all transactions)

Insufficient adaptive detection tools in current workflow

False positives that frustrate legitimate users

Regulatory pressure for transparency and explainable fraud decisions

These issues collectively justify the need for a machine learning–driven solution.


### Project Rationale
The project is relevant because the digital payments industry is undergoing a transformation toward automated and intelligence-driven fraud prevention.

### Why this project is important:

Ensures platform integrity
Accurate fraud detection helps prevent financial losses and maintains trust with customers and regulators.

Improves operational performance
Fraud teams can prioritize high-risk transactions more effectively while reducing manual review burden.

Increases customer satisfaction
Reduced false positives mean fewer legitimate transactions are incorrectly blocked, improving user experience.

Supports competitive advantage
ML-driven fraud detection is becoming standard among modern fintech leaders and digital payment platforms.

Enhances regulatory compliance
Transparent, explainable fraud decisions meet compliance standards and build institutional trust.

This makes real-time fraud detection a strategic asset for modern digital payment providers.

### Project Objective
The project focuses on achieving the following:

Build supervised classifiers capable of accurately distinguishing fraudulent transactions from legitimate ones across diverse transaction patterns.

Handle severe class imbalance (fraud <1% of transactions) through sophisticated re-sampling techniques and class-weighted ensemble methods.

Integrate SHAP explainability to provide transaction-level transparency for analysts and regulatory stakeholders.

Achieve at least 15% improvement in recall compared to rules-based baseline while maintaining acceptable precision levels to minimize false positives.

Deploy as a FastAPI microservice capable of real-time scoring for immediate transaction evaluation in production environments.

### Data Description
The dataset covers multiple categories of information. Click here to download dataset

1. Transaction Data
Captures core transaction details:

Transaction IDs

Amounts

Currency pairs

Timestamps

Channel indicators (mobile/web/ATM)

Device fingerprints

IP addresses

Geographic country codes

2. Customer Data
Includes customer profile information:

Account age

KYC verification tier

Typical transaction amounts

Historical behavior patterns

Internal risk scores

3. Fraud Labels
Binary labels (0/1) derived from:

Completed fraud investigations

Confirmed chargebacks

Verified customer disputes

Provides ground truth for model training.

Data Model Structure
Transaction → Customer data (many-to-one)

Transaction → Fraud labels (one-to-one)


### Project Work Flow
Step 1: Data Collection & Profiling
Analyze distributions, identify missingness patterns, and establish baseline fraud prevalence across the dataset.

Step 2: Data Preparation
Clean and standardize data; engineer features including velocity metrics, mismatch indicators, device fingerprints, and temporal patterns.

Step 3: Exploratory Data Analysis
Uncover patterns by channel, geography, and time; identify anomalies distinguishing fraudulent from legitimate behavior.

Step 4: Model Development
Progress from Logistic Regression and Random Forest baselines to advanced XGBoost and LightGBM models; tune hyperparameters and compare performance using recall, precision, F1-score, and ROC-AUC metrics.

Step 5: Validation & Explainability
Conduct rigorous holdout evaluation; generate SHAP values to provide transaction-level reasoning and build trust in model decisions.

Step 6: Deployment
Build FastAPI /score service endpoint; containerize with Docker for seamless portability across environments.

Step 7: Monitoring & Improvement
Implement Evidently-based drift detection; establish quarterly retraining playbook to maintain model accuracy as fraud patterns evolve.

### Learning Opportunities & Skilled Developed

Technical Skills
Real-world fraud detection modeling with severely imbalanced datasets

Building robust supervised classifiers with ensemble methods

Handling class imbalance through SMOTE and re-sampling techniques

Using SHAP for model interpretability and regulatory compliance

API-based model deployment with FastAPI and Docker

Implementing drift detection and model monitoring frameworks

Financial Services & Fintech Concepts

Understanding digital payment transaction flows

Cross-border money transfer operations

Fraud detection lifecycle from transaction to investigation

Regulatory frameworks (AML, KYC compliance)

Balance between security and customer experience

Professional Skills

Translating business problems into ML solutions

Working with cross-functional teams (fraud operations, compliance, engineering)

Communicating results to non-technical stakeholders

Building production-ready ML systems with monitoring

### Job Related
This project aligns strongly with several industry positions:

Data Scientist / Machine Learning Engineer

Fraud Analytics Specialist

Risk Analyst (Fintech & Payment Services)

Compliance Analyst / AML Specialist

Payment Operations Analyst

Business Intelligence or Reporting Analyst

Product Analyst (Fintech)

Completing this project showcases the practical and technical skills required in these roles.