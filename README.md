# real_estate_web_app

python -m venv .venv -> create a virtual environment to install all packages you will need for this project, in an isolated environment. This prevents any possible conflicts with packages previously installed on your local machine

.\.venv\Scripts\activate -> activate the created virtual enviromnent

pip install -r requirements.txt -> install all packages inside the file "requirements.txt"



Datasets Source:

- https://www.kaggle.com/datasets/luvathoms/portugal-real-estate-2024 (portugal_listings.csv)
- https://www.kaggle.com/datasets/paulexx/portugal-house-prices (House_prices_kag.csv)

real_estate_data_final_v0.csv -> dataset generated before applying most of the pre-processing steps

real_estate_data_final.csv -> dataset generated after applying every pre-processing steps, which was used to train and test the models