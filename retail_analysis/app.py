from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Load dataset
df = pd.read_csv(r"C:\Users\saisr\Desktop\retail_analysis\data\transactions.csv")

@app.route('/')
def dashboard():
    # Summary KPIs
    unique_customers = df["CustomerID"].nunique()
    unique_products = df["ProductID"].nunique()
    df["TotalAmount"] = df["Quantity"] * df["Price"]
    total_revenue = df["TotalAmount"].sum()
    avg_transaction_value = df["TotalAmount"].mean()

    # Top 5 products by quantity
    top_products = (
    df.groupby(['ProductID', 'ProductCategory'])['Quantity']
      .sum()
      .reset_index()
      .sort_values(by='Quantity', ascending=False)
      .head(5)
)



    # Top 5 customers by spending
    top_customers = (
    df.groupby(['CustomerID','ProductCategory'])['TotalAmount']
      .sum()
      .reset_index()  # convert Series to DataFrame
      .sort_values(by='TotalAmount', ascending=False)
      .head(5)        # top 5
)


    # Customer purchase frequency
    customer_frequency = df.groupby("CustomerID")["TotalAmount"].count().reset_index().sort_values(by="TotalAmount", ascending=False)
    # Revenue by category
    category_revenue = df.groupby("ProductCategory")["TotalAmount"].sum().reset_index().sort_values(by="TotalAmount", ascending=False)

    return render_template(
        "index.html"
        unique_customers=unique_customers,
        unique_products=unique_products,
        total_revenue=total_revenue,
        avg_transaction_value=avg_transaction_value,
        top_products=top_products.to_dict(orient="records"),
        top_customers=top_customers.to_dict(orient="records"),
        customer_frequency=customer_frequency.to_dict(orient="records"),
        category_revenue=category_revenue.to_dict(orient="records")
    )

if __name__ == "__main__":
    app.run(debug=True)
