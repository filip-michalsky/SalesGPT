---
sidebar_position: 2

---

# Product catalog
To ensure that SalesGPT can effectively understand and utilize your product catalog, it is important to set up the correct chunk size in the text splitter within the `tools.py` file. Proper chunking helps in maintaining the context and coherence of the product information.

Here are two examples of incorrect setups and one example of a correct setup:

### Incorrect Setup 1
![Incorrect Setup 1](/img/bad_1.png)

### Incorrect Setup 2
![Incorrect Setup 2](/img/bad_2.png)

### Correct Setup
![Correct Setup](/img/correct.png)

You can implement your product catalog into SalesGPT by loading it. 
To add a different product catalog, such as the `sample_product_catalog_2.txt` file, follow these steps:

1. **Update the product catalog file**: Replace the existing product catalog file with your new product catalog file. For example, you can use the `sample_product_catalog_2.txt` file.

2. **Update the `run_api` file**: Make sure to update the `product_catalog` variable in the `run_api` file to point to the new product catalog file. Alternatively, if you have set up the `PRODUCT_CATALOG` environment variable, update it to the path of your new product catalog file.

Here is an example of how to update the `setup_knowledge_base` function (product catalog function) in the `tools.py` file:
![Correct Product Catalog](/img/new_products.png)
