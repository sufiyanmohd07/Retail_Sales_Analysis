# Python Data Analysis

## 1. Overview

Python was used to inspect, validate and analyse the retail sales dataset using Pandas.

## 2. Libraries Used

- **Pandas:** Data manipulation, validation and analysis.
- **Pathlib:** File and folder path management.

## 3. Data Inspection

The dataset was loaded from the Excel file using Pandas.

The following checks were performed:

- Displayed the first five records.
- Checked the number of rows and columns.
- Reviewed column names and data types.
- Examined numerical data using descriptive statistics.
- Checked the date range.

## 4. Data Quality Checks

The following validation checks were performed:

- Missing values.
- Completely duplicated records.
- Duplicate Order IDs.
- Zero or negative values in numerical columns.
- Discount value distribution.
- Zero-profit orders.

## 5. Sales Validation

Expected sales were calculated using:

`Quantity × Unit Price × (1 − Discount Percentage / 100)`

The calculated sales were compared with the recorded sales to identify mismatches.

## 6. Business KPI Calculations

The following KPIs were calculated:

- Total Revenue
- Total Profit
- Total Units Sold
- Total Orders
- Average Order Value
- Profit Margin

## 7. Business Analysis

The dataset was analysed across four main areas:

### Monthly Sales Analysis
- Monthly revenue
- Monthly profit
- Monthly order count
- Monthly profit margin
- Highest and lowest revenue months

### Regional Sales Analysis
- Revenue by region
- Profit by region
- Number of orders
- Units sold
- Regional profit margins

### Category Analysis
- Revenue by product category
- Profit by category
- Number of orders
- Units sold
- Category profit margins

### Product Analysis
- Product-wise revenue
- Product-wise profit
- Number of orders
- Units sold
- Product profit margins
- Highest-performing products

## 8. Exported Files

The analysis results were exported as CSV files into the `outputs` folder:

1. `retail_sales_analysis_data.csv`
2. `monthly_sales_analysis.csv`
3. `regional_sales_analysis.csv`
4. `category_sales_analysis.csv`
5. `product_sales_analysis.csv`

## 9. Outcome

Python and Pandas were used to validate the dataset, calculate business KPIs and generate summary datasets for further analysis and visualisation in Power BI.