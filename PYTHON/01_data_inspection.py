import pandas as pd
from pathlib import Path

# Step 1: Locate the main project folder
project_folder = Path(__file__).resolve().parent.parent

# Step 2: Locate the Excel dataset
file_path = (
    project_folder
    / "data"
    / "Project1_Retail_Sales_Dataset.xlsx"
)

# Step 3: Read the Excel worksheet
df = pd.read_excel(file_path, sheet_name="Raw_Data")

# Step 4: Display the first five rows
print("FIRST FIVE ROWS")
print(df.head())

# Step 5: Display the number of rows and columns
print("\nDATASET SHAPE")
print(df.shape)

# Step 6: Display all column names
print("\nCOLUMN NAMES")
print(df.columns.tolist())

# Step 7: Display dataset information
print("\nDATASET INFORMATION")
df.info()

# STEP 8: DATA QUALITY CHECKS

print("\n" + "=" * 40)
print("DATA QUALITY CHECKS")
print("=" * 40)

# 1. Check missing values
print("\n1. MISSING VALUES")
print(df.isnull().sum())

# 2. Check completely duplicated rows
print("\n2. DUPLICATE ROWS")
print("Total duplicate rows:", df.duplicated().sum())

# 3. Check duplicate Order IDs
print("\n3. DUPLICATE ORDER IDs")
print("Duplicate Order IDs:", df["Order_ID"].duplicated().sum())
print("Unique Order IDs:", df["Order_ID"].nunique())

# 4. Check the date range
print("\n4. DATE RANGE")
print("First date:", df["Order_Date"].min())
print("Last date:", df["Order_Date"].max())

# 5. Examine numerical columns
print("\n5. NUMERICAL SUMMARY")
print(
    df[
        [
            "Quantity",
            "Unit_Price_INR",
            "Discount_Pct",
            "Sales_INR",
            "Profit_INR",
        ]
    ].describe()
)

# 6. Examine discount values
print("\n6. DISCOUNT VALUES")
print(df["Discount_Pct"].value_counts().sort_index())

# 7. Check for zero or negative values
print("\n7. ZERO OR NEGATIVE VALUES")

for column in [
    "Quantity",
    "Unit_Price_INR",
    "Sales_INR",
    "Profit_INR",
]:
    print(
        f"{column}:",
        (df[column] <= 0).sum(),
        "values less than or equal to zero",
    )

# STEP 9: INVESTIGATE ZERO-PROFIT RECORDS

print("\n" + "=" * 40)
print("ZERO-PROFIT RECORDS")
print("=" * 40)

zero_profit = df[df["Profit_INR"] <= 0]

print(zero_profit.to_string(index=False))


# STEP 10: VALIDATE SALES CALCULATIONS

# Calculate expected sales using quantity, price, and discount
df["Expected_Sales_INR"] = (
    df["Quantity"]
    * df["Unit_Price_INR"]
    * (1 - df["Discount_Pct"] / 100)
)

# Calculate the difference between recorded and expected sales
df["Sales_Difference_INR"] = (
    df["Sales_INR"] - df["Expected_Sales_INR"]
).round(2)

# Identify records where the difference exceeds 1 paisa
mismatches = df[
    df["Sales_Difference_INR"].abs() > 0.01
]

print("\n" + "=" * 40)
print("SALES VALIDATION")
print("=" * 40)

print("Records checked:", len(df))
print("Sales mismatches:", len(mismatches))

if not mismatches.empty:
    print("\nRecords requiring investigation:")
    print(
        mismatches[
            [
                "Order_ID",
                "Quantity",
                "Unit_Price_INR",
                "Discount_Pct",
                "Sales_INR",
                "Expected_Sales_INR",
                "Sales_Difference_INR",
            ]
        ].to_string(index=False)
    )
else:
    print("All recorded sales match the expected formula.")



# STEP 11: INVESTIGATE ZERO-PROFIT ORDERS

zero_profit_orders = df[df["Profit_INR"] == 0]

print("\n" + "=" * 40)
print("ZERO-PROFIT ORDER INVESTIGATION")
print("=" * 40)

print("Number of zero-profit orders:", len(zero_profit_orders))

if not zero_profit_orders.empty:
    print("\nZero-profit order details:")

    print(
        zero_profit_orders[
            [
                "Order_ID",
                "Order_Date",
                "Region",
                "Category",
                "Product",
                "Quantity",
                "Unit_Price_INR",
                "Discount_Pct",
                "Sales_INR",
                "Profit_INR",
            ]
        ].to_string(index=False)
    )

print("\nProfit summary:")
print(df["Profit_INR"].describe())



# STEP 12: CALCULATE BUSINESS KPIs

# KPI 1: Total Revenue
total_revenue = df["Sales_INR"].sum()

# KPI 2: Total Profit
total_profit = df["Profit_INR"].sum()

# KPI 3: Total Units Sold
total_units = df["Quantity"].sum()

# KPI 4: Average Order Value
total_orders = df["Order_ID"].nunique()
average_order_value = total_revenue / total_orders

# KPI 5: Profit Margin
profit_margin = (total_profit / total_revenue) * 100

# Display the results
print("\n" + "=" * 40)
print("RETAIL SALES BUSINESS KPIs")
print("=" * 40)

print(f"Total Revenue: ₹{total_revenue:,.2f}")
print(f"Total Profit: ₹{total_profit:,.2f}")
print(f"Total Units Sold: {total_units:,}")
print(f"Total Orders: {total_orders:,}")
print(f"Average Order Value: ₹{average_order_value:,.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")


# STEP 13: MONTHLY SALES ANALYSIS

# Extract the month from each order date
df["Month"] = df["Order_Date"].dt.to_period("M")

# Group data by month and calculate sales, profit, and orders
monthly_sales = df.groupby("Month").agg(
    Total_Sales=("Sales_INR", "sum"),
    Total_Profit=("Profit_INR", "sum"),
    Total_Orders=("Order_ID", "nunique")
).reset_index()

# Calculate monthly profit margin
monthly_sales["Profit_Margin_Pct"] = (
    monthly_sales["Total_Profit"]
    / monthly_sales["Total_Sales"]
    * 100
).round(2)

# Display results
print("\n" + "=" * 60)
print("MONTHLY SALES ANALYSIS")
print("=" * 60)

print(monthly_sales.to_string(index=False))

# Find the best month by revenue
best_month = monthly_sales.loc[
    monthly_sales["Total_Sales"].idxmax()
]

print("\nBest Month by Revenue:")
print("Month:", best_month["Month"])
print(f"Revenue: ₹{best_month['Total_Sales']:,.2f}")

# Find the lowest month by revenue
lowest_month = monthly_sales.loc[
    monthly_sales["Total_Sales"].idxmin()
]

print("\nLowest Month by Revenue:")
print("Month:", lowest_month["Month"])
print(f"Revenue: ₹{lowest_month['Total_Sales']:,.2f}")


# STEP 14: REGIONAL SALES ANALYSIS

regional_sales = df.groupby("Region").agg(
    Total_Sales=("Sales_INR", "sum"),
    Total_Profit=("Profit_INR", "sum"),
    Total_Orders=("Order_ID", "nunique"),
    Units_Sold=("Quantity", "sum")
).reset_index()

# Calculate profit margin for each region
regional_sales["Profit_Margin_Pct"] = (
    regional_sales["Total_Profit"]
    / regional_sales["Total_Sales"]
    * 100
).round(2)

# Sort regions by revenue, highest first
regional_sales = regional_sales.sort_values(
    by="Total_Sales",
    ascending=False
)

print("\n" + "=" * 60)
print("REGIONAL SALES ANALYSIS")
print("=" * 60)

print(regional_sales.to_string(index=False))

# Identify the best-performing region by revenue
best_region = regional_sales.loc[
    regional_sales["Total_Sales"].idxmax()
]

print("\nBest Region by Revenue:")
print("Region:", best_region["Region"])
print(f"Revenue: ₹{best_region['Total_Sales']:,.2f}")
print(f"Profit: ₹{best_region['Total_Profit']:,.2f}")
print(f"Profit Margin: {best_region['Profit_Margin_Pct']:.2f}%")



# STEP 15: PRODUCT CATEGORY ANALYSIS

category_sales = df.groupby("Category").agg(
    Total_Sales=("Sales_INR", "sum"),
    Total_Profit=("Profit_INR", "sum"),
    Total_Orders=("Order_ID", "nunique"),
    Units_Sold=("Quantity", "sum")
).reset_index()

# Calculate profit margin
category_sales["Profit_Margin_Pct"] = (
    category_sales["Total_Profit"]
    / category_sales["Total_Sales"]
    * 100
).round(2)

# Sort by revenue from highest to lowest
category_sales = category_sales.sort_values(
    by="Total_Sales",
    ascending=False
)

print("\n" + "=" * 60)
print("PRODUCT CATEGORY ANALYSIS")
print("=" * 60)

print(category_sales.to_string(index=False))

# Identify the highest-revenue category
best_category = category_sales.loc[
    category_sales["Total_Sales"].idxmax()
]

print("\nBest Category by Revenue:")
print("Category:", best_category["Category"])
print(f"Revenue: ₹{best_category['Total_Sales']:,.2f}")
print(f"Profit: ₹{best_category['Total_Profit']:,.2f}")
print(f"Profit Margin: {best_category['Profit_Margin_Pct']:.2f}%")


# STEP 16: INDIVIDUAL PRODUCT ANALYSIS

product_sales = df.groupby("Product").agg(
    Total_Sales=("Sales_INR", "sum"),
    Total_Profit=("Profit_INR", "sum"),
    Total_Orders=("Order_ID", "nunique"),
    Units_Sold=("Quantity", "sum")
).reset_index()

# Calculate profit margin for each product
product_sales["Profit_Margin_Pct"] = (
    product_sales["Total_Profit"]
    / product_sales["Total_Sales"]
    * 100
).round(2)

# Rank products by revenue
product_sales = product_sales.sort_values(
    by="Total_Sales",
    ascending=False
)

print("\n" + "=" * 70)
print("INDIVIDUAL PRODUCT ANALYSIS")
print("=" * 70)

print(product_sales.to_string(index=False))

# Highest-revenue product
best_revenue_product = product_sales.loc[
    product_sales["Total_Sales"].idxmax()
]

print("\nHighest-Revenue Product:")
print("Product:", best_revenue_product["Product"])
print(f"Revenue: ₹{best_revenue_product['Total_Sales']:,.2f}")

# Highest-profit product
best_profit_product = product_sales.loc[
    product_sales["Total_Profit"].idxmax()
]

print("\nHighest-Profit Product:")
print("Product:", best_profit_product["Product"])
print(f"Profit: ₹{best_profit_product['Total_Profit']:,.2f}")

# Most-sold product by units
best_quantity_product = product_sales.loc[
    product_sales["Units_Sold"].idxmax()
]

print("\nMost-Sold Product by Units:")
print("Product:", best_quantity_product["Product"])
print(f"Units Sold: {best_quantity_product['Units_Sold']:,}")

# Highest profit margin
best_margin_product = product_sales.loc[
    product_sales["Profit_Margin_Pct"].idxmax()
]

print("\nHighest-Profit-Margin Product:")
print("Product:", best_margin_product["Product"])
print(f"Profit Margin: {best_margin_product['Profit_Margin_Pct']:.2f}%")



# STEP 17: EXPORT ANALYSIS RESULTS

from pathlib import Path

# Create the outputs folder automatically if it doesn't exist
output_folder = Path(__file__).resolve().parent.parent / "outputs"
output_folder.mkdir(parents=True, exist_ok=True)

# Export the cleaned/analysed order data
df.to_csv(
    output_folder / "retail_sales_analysis_data.csv",
    index=False
)

# Export monthly analysis
monthly_sales.to_csv(
    output_folder / "monthly_sales_analysis.csv",
    index=False
)

# Export regional analysis
regional_sales.to_csv(
    output_folder / "regional_sales_analysis.csv",
    index=False
)

# Export category analysis
category_sales.to_csv(
    output_folder / "category_sales_analysis.csv",
    index=False
)

# Export product analysis
product_sales.to_csv(
    output_folder / "product_sales_analysis.csv",
    index=False
)

print("\n" + "=" * 50)
print("ANALYSIS FILES EXPORTED SUCCESSFULLY")
print("=" * 50)

print("Output folder:", output_folder)
print("1. retail_sales_analysis_data.csv")
print("2. monthly_sales_analysis.csv")
print("3. regional_sales_analysis.csv")
print("4. category_sales_analysis.csv")
print("5. product_sales_analysis.csv")
