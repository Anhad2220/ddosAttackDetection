# DDoS Attack Detection Using Machine Learning

A Machine Learning-based cybersecurity project designed to detect Distributed Denial of Service (DDoS) attacks from network traffic data. The system analyzes network traffic features and predicts whether the traffic is benign or malicious. A Flask-based dashboard provides an interactive interface for making predictions and monitoring results.

---

## Project Overview

DDoS attacks are among the most common cyber threats, where attackers overwhelm a target system with massive amounts of traffic, making services unavailable to legitimate users.

This project leverages Machine Learning algorithms to automatically identify suspicious network traffic patterns and classify them as either normal or DDoS attacks. The solution includes model training, prediction, and a web-based dashboard for user interaction.

---

## Features

* DDoS Attack Detection using Machine Learning
* Network Traffic Classification
* Data Preprocessing and Feature Engineering
* Model Training and Evaluation
* Trained Model Deployment
* Flask-Based Web Application
* Interactive Dashboard
* Real-Time Predictions
* Prediction History Storage
* User-Friendly Interface

---

## Technologies Used

### Programming Languages

* Python

### Machine Learning

* Scikit-learn
* NumPy
* Pandas

### Web Development

* Flask
* HTML
* CSS
* Bootstrap

### Database

* SQLite

### Tools

* Jupyter Notebook
* Git
* GitHub

---

## Dataset

This project uses the DDoS Dataset available on Kaggle:

Dataset Link:

https://www.kaggle.com/datasets/devendra416/ddos-datasets

### Dataset Description

The dataset contains network traffic records consisting of multiple features extracted from network flows. These features are used to distinguish normal traffic from DDoS attack traffic.

Examples of attributes include:

* Destination Port
* Flow Duration
* Total Forward Packets
* Total Backward Packets
* Flow Bytes/s
* Flow Packets/s
* Packet Length Statistics
* Various Traffic Flow Metrics

The dataset is suitable for binary classification problems where traffic is classified as either:

* Benign Traffic
* DDoS Attack Traffic

---

## Machine Learning Models Used

The project evaluates multiple machine learning algorithms:

* Decision Tree Classifier
* Random Forest Classifier
* Gaussian Naive Bayes
* Multi-Layer Perceptron (MLP)

These models are trained and evaluated using standard classification metrics.

The best-performing model is saved and deployed for real-time predictions.

---

## Project Architecture

1. Dataset Collection
2. Data Preprocessing
3. Feature Selection
4. Model Training
5. Model Evaluation
6. Model Serialization
7. Flask Application Integration
8. Dashboard Deployment
9. User Prediction Interface

---

## Project Structure

```text
ddosAttackDetection/
│
├── saved_model/
│   └── model_data.sav
│
├── train.py
├── test.py
├── app.py
├── dashboard.py
├── requirements.txt
├── README.md
│
├── database/
│
└── templates/
```

---

## Installation

### Clone the Repository

```bash
git clone https://github.com/Anhad2220/ddosAttackDetection.git
cd ddosAttackDetection
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Application

### Start the Flask Application

```bash
python app.py
```

or

```bash
python dashboard.py
```

Open your browser and navigate to:

```text
http://localhost:5000
```

---

## Training the Model

To retrain the model using the dataset:

```bash
python train.py
```

This process:

* Loads the dataset
* Cleans and preprocesses the data
* Trains the machine learning model
* Evaluates model performance
* Saves the trained model

---

## Testing the Model

Run:

```bash
python test.py
```

The saved model is loaded and used to predict whether the supplied traffic data represents a DDoS attack.

---

## Evaluation Metrics

The model performance is evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix

These metrics help assess the effectiveness of the model in identifying malicious traffic while minimizing false positives.

---

## Dashboard

The project includes a web-based dashboard that enables users to:

* Enter network traffic parameters
* Generate attack predictions
* View prediction results instantly
* Store prediction records
* Analyze prediction history

The dashboard provides a simple and intuitive interface for interacting with the trained machine learning model.

---

## Future Enhancements

* Real-Time Network Monitoring
* Deep Learning-Based Detection Models
* Cloud Deployment
* REST API Integration
* Live Traffic Visualization
* Advanced Threat Analytics
* Automated Alert System

---

## Screenshots

Add screenshots of:

* Dashboard Home Page
* Prediction Form
* Prediction Results
* Database Records
* Analytics Dashboard

---

## Author

### Anhad Sabharwal

* BCA (Artificial Intelligence & Machine Learning), UPES Dehradun

---

## License

This project is developed for educational, academic, and research purposes.
