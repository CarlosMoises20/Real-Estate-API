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
    
    ```
    # Released under MIT License

    Copyright (c) 2013 Mark Otto.

    Copyright (c) 2017 Andrew Fong.

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
    ```