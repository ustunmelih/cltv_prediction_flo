
# CLTV with BG-NBD and Gamma-Gamma Model in a FLO Dataset

![img](https://cdn.prod.website-files.com/6234f0956f77842876f6a4d5/64a6e6195504bebc190de7e1_Aret.%20CLV%20Alex.png)

## What is CLV?

Customer Lifetime Value (CLTV) is a crucial metric that predicts the total revenue a business can reasonably expect from an average customer throughout their relationship. It's essentially a forecast of the customer's worth to the company.

To accurately calculate CLTV, businesses typically analyze both average revenue per customer and average profit per customer. While revenue indicates the overall sales generated, profit provides a clearer picture of the actual value a customer brings to the bottom line. By understanding these figures, companies can assess the effectiveness of their marketing strategies and make data-driven decisions to improve customer retention and loyalty.

## Business Case

To create a robust and effective medium to long-term sales and marketing roadmap, FLO needs a clear understanding of its customers' potential value. This is where Customer Lifetime Value (CLTV) becomes indispensable.


## The story of the dataset

The dataset comprises historical shopping data from FLO customers who made their most recent purchase between 2020 and 2021, utilizing both online and physical stores.

- **master_id:** Unique customer number
- **order_channel:** Which channel of the shopping platform used (Android, iOS, desktop, mobile)
- **last_order_channel:** Channel where the last shopping was made
- **first_order_date:** Customer's first shopping date
- **last_order_date:** Customer's latest shopping date
- **last_order_date_online:** Customer's latest shopping date on the online platform
- **last_order_date_offline:** Customer's latest shopping date on offline platform
- **order_num_total_ever_online:** Customer's total number of shopping on the online platform
- **order_num_total_ever_offline:** Customer's total number of shopping on the offline platform
- **customer_value_total_ever_offline:** Total fee paid by the customer in offline shopping
- **customer_value_total_ever_online:** Total fee paid by the customer in online shopping
- **interested_in_categories_12:** List of categories where the customer shopping in the last 12 months
