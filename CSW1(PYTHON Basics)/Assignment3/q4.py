def sales_summary(*args, **kwargs):
    print("Total Sales Amount:", sum(args))
    print("Number of Extra Info:", len(kwargs))
    print("\nExtra Information Provided:")
    for k, v in kwargs.items():
        print(f"{k}: {v}")

sales_summary(4000, 4500, 4000, Name="John Doe", Date="2025-11-01", Location="Bhubaneswar")
