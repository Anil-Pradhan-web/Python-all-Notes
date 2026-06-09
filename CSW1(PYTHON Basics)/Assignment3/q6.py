def filter_high_sales(sales, threshold):
    for s in sales:
        if s >= threshold:
            yield s

sales = [250, 800, 450, 1200, 600]
for s in filter_high_sales(sales, 500):
    print(s)
