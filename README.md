# real_estate_web_app

python -m venv .venv -> create a virtual environment to install all packages you will need for this project, in an isolated environment. This prevents any possible conflicts with packages previously installed on your local machine

.\.venv\Scripts\activate -> activate the created virtual enviromnent

pip install -r requirements.txt -> install all packages inside the file "requirements.txt"


Environment variables that you need to set on the .env file inside the "compose" folder

- GEOAPIFY_API_KEY
   The API Key of Geoapify. Create an account on Geoapify and generate an API Key that you will use to access your data


- FSQ_OS_PLACES_ACCESS_TOKEN

    The Access Token of FSQ OS Places. Create an account on FSQ OS Places and generate an API Key that you will use to access your data


- IDEALISTA_API_KEY

    The API Key of Idealista. Create an account on Idealista and generate an API Key that you will use to access your data


Datasets Source:

- Internal Dataset: https://www.kaggle.com/datasets/luvathoms/portugal-real-estate-2024 (portugal_listnigs.csv)

    - IMPORTANT NOTE: This dataset contains data of some properties from Brazil and Dubai


## Data sources & licenses

The license of this project's code does not apply to the data below. Each source keeps its own license, and its attribution must be shown wherever its data is displayed (API responses and web app). The API exposes this information at `/api/v1/sources`, built from `DATA_SOURCES` and `SERIES_SOURCES` in `backend/common/constants.py`.

| Source | Data | License / reuse conditions | Attribution | Can be exposed to third parties |
|---|---|---|---|---|
| [Statistics Portugal (INE)](https://www.ine.pt) | Inflation, average salary, unemployment, housing transactions, price per m² | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) | Source: Statistics Portugal (INE) | Yes |
| [DGPJ](https://estatisticas.justica.gov.pt) (via INE) | Crime rate | [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) (disseminated by INE) | Source: INE / Directorate-General for Justice Policy (DGPJ) | Yes |
| [Eurostat](https://ec.europa.eu/eurostat) | GDP, household consumption | [Eurostat copyright notice](https://ec.europa.eu/eurostat/help/copyright-notice) | Source: Eurostat | Yes |
| [European Central Bank](https://data.ecb.europa.eu) | Housing credit rate | [ECB reuse conditions](https://www.ecb.europa.eu/services/disclaimer/html/index.en.html) | Source: European Central Bank (ECB) | Yes |
| [Foursquare Open Source Places](https://docs.foursquare.com/data-products/docs/fsq-places-open-source) | Points of interest | [Apache-2.0](https://www.apache.org/licenses/LICENSE-2.0) (see [NOTICE](NOTICE)) | Contains data from Foursquare Open Source Places | Yes |
| [OpenStreetMap](https://www.openstreetmap.org) | Points of interest, maps | [ODbL 1.0](https://www.openstreetmap.org/copyright) | © OpenStreetMap contributors | Yes (derived databases must stay under ODbL) |
| [Geoapify](https://www.geoapify.com) | Points of interest | [Geoapify Terms](https://www.geoapify.com/terms-and-conditions/) (OSM data, ODbL 1.0) | Powered by Geoapify \| © OpenStreetMap contributors | Not confirmed |
| [CAOP 2024 - DGT](https://www.dgterritorio.gov.pt/cartografia/cartografia-tematica/caop) | Parish (freguesia) boundaries and areas | Free download from DGT (license to confirm) | Source: CAOP 2024, Direção-Geral do Território (DGT) | Yes (license to confirm) |
| [Kaggle - luvathoms](https://www.kaggle.com/datasets/luvathoms/portugal-real-estate-2024) | Property listings | MIT as declared by the uploader; origin of the listings unverified | Source: Portugal Real Estate dataset (luvathoms, Kaggle) | No (development and ML training only) |
| [idealista](https://www.idealista.pt) | Property listings | Pending API access request | Source: idealista | No (requires idealista's written authorization) |

Values transformed by this project (e.g. 12-month average salary, year-on-year growth of the last 4 quarters of housing transactions) are marked as `derived` in `SERIES_SOURCES`, with the transformation described, and must never be presented as official statistics.


## Disclaimers

These must be shown to the users of the API and web app, and included in the product's terms of use:

- Official statistics are revised by their producers over time; values reflect the date they were retrieved.
- Values marked as derived were calculated by this project and are not official statistics.
- INE, DGPJ, Eurostat and the ECB are not responsible for derived values or for the use made of the data.
- Property price estimates are produced by statistical models and are not official property valuations.