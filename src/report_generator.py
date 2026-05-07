import pandas as pd
import os

if not os.path.exists("outputs"):
    os.makedirs("outputs")

def generate_report(results):

    df = pd.DataFrame(results)

    df.to_csv("outputs/report.csv", index=False)