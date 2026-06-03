import pickle
import sys
import pandas as pd

def model_test(attributes):
    feature_names = ["Fwd Seg Size Avg", "Flow IAT Min", "Flow Duration", "Tot Fwd Pkts", "Pkt Size Avg", "Src Port", "Init Bwd Win Byts"]
    
    try:
        model = pickle.load(open('./saved_model/model_data.sav', 'rb'))
        if len(attributes) == len(feature_names):
            df = pd.DataFrame([attributes], columns=feature_names)
            print(model.predict(df))
        else:
            print(f"Error: Expected {len(feature_names)} features, but got {len(attributes)}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    attributes = list(map(float, sys.argv[1:])) if len(sys.argv) > 1 else None
    if attributes:
        model_test(attributes)
    else:
        print("Please provide the attributes for prediction.")