from app.pipeline.pipeline import ComparisonPipeline
pipeline = ComparisonPipeline()

print("=== Test 1: Apple iPhone 15 128GB ===")
res = pipeline.run("Apple iPhone 15 128GB")
amz = res["amazon"]
fpk = res["flipkart"]
print("Amazon:", amz["title"] if amz else "None")
print("Flipkart:", fpk["title"] if fpk else "None")
print("Amazon stock:", res["analysis"]["amazon_stock"])
print("Flipkart stock:", res["analysis"]["flipkart_stock"])
print("Deal:", res["analysis"]["deal_badge"])
print("Confidence:", res["match_confidence"])

print()
print("=== Test 2: OnePlus 12 256GB (OOS on Flipkart) ===")
res2 = pipeline.run("OnePlus 12 256GB")
print("Amazon stock:", res2["analysis"]["amazon_stock"])
print("Flipkart stock:", res2["analysis"]["flipkart_stock"])
print("Deal:", res2["analysis"]["deal_badge"])
print("Summary:", res2["analysis"]["stock_summary"])
