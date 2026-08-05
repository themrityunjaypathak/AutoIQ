<h3 align="center" id="top">AutoIQ : Used Car Pricing System</h3>

<div align="center">

[![Live Demo](https://img.shields.io/badge/Live-Demo-FF6D00?style=flat&logo=html5&logoColor=white)](https://autoiqlabs.vercel.app)
[![API Docs](https://img.shields.io/badge/API-Docs-05998B?style=flat&logo=fastapi&logoColor=white)](https://autoiq.onrender.com/docs)
[![Docker Hub](https://img.shields.io/badge/Docker%20Hub-Image-1D63ED?style=flat&logo=docker&logoColor=white)](https://hub.docker.com/r/themrityunjaypathak/autoiq)
[![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-4420C7?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Scikit-Learn](https://img.shields.io/badge/scikit--learn-F89939?style=flat&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/stable/)
[![Selenium](https://img.shields.io/badge/Selenium-4EB436?style=flat&logo=selenium&logoColor=white)](https://www.selenium.dev/)
[![Git](https://img.shields.io/badge/Git-F05133?style=flat&logo=git&logoColor=white)](https://git-scm.com/)

</div>

<a href="https://autoiqlabs.vercel.app"><img title="AutoIQ" src="https://github.com/user-attachments/assets/b4437a20-df79-43a7-b70d-363d52de8b1e"></a>

## Table of Contents
- [Problem](#problem)
- [Solution](#solution)
- [Workflow](#workflow)
- [Impact](#impact)
- [Dataset](#dataset)
- [Setup](#setup)
- [Testing](#testing)
- [Dockerization](#dockerization)
- [Application](#application)
- [Model Training & Evaluation](#model-training--evaluation)
- [Challenges & Solutions](#challenges--solutions)
- [Folder Structure](#folder-structure)
- [License](#license)

<hr>

## Problem
- In the used-car market, buyers and sellers often struggle to determine a fair price for a vehicle.
- Incorrect pricing leads to revenue loss when undervalued and slow sales when overpriced.
- The goal is to provide accurate and transparent pricing by analyzing real-world market listings.

<hr>

## Solution
- Built and deployed an ML pipeline predicting used-car prices from 2,800+ real Cars24 listings.
- Benchmarked 6 models, then selected tuned XGBoost for the best accuracy-to-complexity tradeoff.
- Deployed the model through a Dockerized FastAPI service with a live frontend for real-time predictions.

<hr>

## Workflow

<details>
<summary>Click Here to view Workflow Diagram</summary>
<br>

<img title="Workflow Diagram" src="https://github.com/user-attachments/assets/203c82e4-69bf-4cff-ad9a-92ee6f943882">

</details>

<hr>

## Impact
- Cut MAE by 31% (₹1,23,193 → ₹85,281) and improved R² from 0.77 to 0.88 over a Linear Regression baseline.
- Reduced MAE variability by 62% (std ₹6,435 → ₹2,426) over baseline for more consistent predictions.
- Validated on a held-out test set, achieving ₹87,723 MAE, 0.87 R², and ~14% MAPE on completely unseen data.
- Delivered data-backed price ranges instead of a single point estimate, enabling confident negotiation.

<hr>

## Dataset
- To train the model, I collected real-world used car listings data directly from the [Cars24](https://www.cars24.com/) website.
- Since Cars24 uses dynamically loaded content, a static scraper would not capture all the data.
- Instead, I implemented an automated Selenium + BeautifulSoup Python Script.

### Web Scraping Script (`scrape_car_listing`)

<details>
<summary>Click Here to view more Details</summary>
<br>

**Input :** URL of a Cars24 listing page to scrape.

#### 1. Launch Chrome Automatically
- Script uses `ChromeDriverManager` to install and manage the drivers without manual setup.
  
#### 2. Open Cars24 Website
- Loads the given URL in a real browser session.

#### 3. Simulate Scrolling
- Scrolls down the page in increments, with short random pauses (2-4 seconds) between scrolls.
- This ensures all dynamically loaded listings are fetched.
  
#### 4. Check for End of Page
- Stops scrolling when the bottom of the page is reached or no new content loads.

#### 5. Capture Rendered HTML
- Once fully loaded, it retrieves the complete DOM (including dynamically injected elements).
  
#### 6. Parse HTML with BeautifulSoup
- Returns a BeautifulSoup object containing the entire page's HTML for later parsing and data extraction.

#### Note
- At this stage, no data is extracted, the output is just the complete HTML source.
- It will later be parsed by a separate script to extract features like price, model, year, transmission, etc.

</details>

---

### Data Extraction Script (`get_car_details`)

<details>
<summary>Click Here to view more Details</summary>
<br>

**Input :** BeautifulSoup object (`soup`) containing the fully-rendered HTML of a Cars24 listing page.

#### 1. Find Raw Model Name Texts
- Looks for `<span>` elements with class `sc-braxZu kjFjan`.
- Extracts the text using `.text` into a list called `model_name`.
- The code only keeps those car models that start with `2` and stores them in `clean_model_name`.

<details>
<summary>Click to view the HTML Element Snapshot</summary>
<br>
<img title="cars24" src="https://github.com/user-attachments/assets/66524e3d-4c26-4edc-8f8a-40b17016eda4">
</details>

#### Important
- Inspect the HTML Element : `<span id class="sc-braxZu kjFjan">2016 Maruti Wagon R 1.0</span>`
- Tag : `<span>` → id (empty) → class : `sc-braxZu kjFjan` (two classes, separated by space)
- However when you hover over it in the browser, it shows : `span.sc-braxZu.kjFjan`
- CSS uses a dot `.` to indicate classes. The dot is not a part of the class name itself.
- It just means "this is a class", it is not the part of the class name.
- This might look confusing for someone with little HTML/CSS knowledge, so it's better to clarify it.

#### 2. Collect Specification Text Blocks
- Looks for `<p>` elements with class `sc-braxZu kvfdZL` (each holds one specification value).
- These are appended to `specs` list.
   
```python
['69.95k km',
 'Petrol',
 'Manual',
 '1st owner',
 'DL-1C',
 '70.72k km',
 'Diesel',
 'Manual',
 '2nd owner',
 'UP-14',
 '15.96k km',
 'CNG',
 'Manual',
 '1st owner',
 'UP-16',...]
```

<details>
<summary>Click to view the HTML Element Snapshot</summary>
<br>
<img title="cars24" src="https://github.com/user-attachments/assets/5185f66b-3de6-4354-ae11-fcb0b8fbb793">
</details>

#### 3. Group Specifications
- The flat `specs` list is split into consecutive groups of 5 (`clean_specs.append(specs[i:i+5])`).
- Each group corresponds to a set of specification values for each listing.
   
```python
[['69.95k km', 'Petrol', 'Manual', '1st owner', 'DL-1C'],
 ['70.72k km', 'Diesel', 'Manual', '2nd owner', 'UP-14'],
 ['15.96k km', 'CNG', 'Manual', '1st owner', 'UP-16'],...]
```

#### 4. Map Groups into Fields
- From each 5-item group, the script extracts :
    - `clean_specs[0]` → `km_driven`
    - `clean_specs[1]` → `fuel_type`
    - `clean_specs[2]` → `transmission`
    - `clean_specs[3]` → `owner`
    - `clean_specs[4]` → `number_plate` exists but is not relevant.

#### 5. Extract Price Values
- `soup.find_all('p', 'sc-braxZu cyPhJl')` collects price elements into `price` list.
- The script then slices `price = price[2:]`, removing the first two entries (non-listing elements on the page).
- So the remaining prices align with the listings.

```python
['₹3.09 lakh',
 '₹5.71 lakh',
 '₹7.37 lakh',...]
```

<details>
<summary>Click to view the HTML Element Snapshot</summary>
<br>
<img title="cars24" src="https://github.com/user-attachments/assets/9a974eca-b39b-4e9a-bdc3-ff5abe6c9491">
</details>

#### 6. Extract Listing Links
- `soup.find_all('a', 'styles_carCardWrapper__sXLIp')` collects anchor tag for each card and extracts `href`.

```python
['https://www.cars24.com/buy-used-honda-amaze-2018-cars-noida-11068642783/',
 'https://www.cars24.com/buy-used-ford-ecosport-2020-cars-noida-11234948707/',
 'https://www.cars24.com/buy-used-tata-altroz-2024-cars-noida-10563348767/',...]
```

<details>
<summary>Click to view the HTML Element Snapshot</summary>
<br>
<img title="cars24" src="https://github.com/user-attachments/assets/fbac495f-6894-41dc-b469-2d23e90e3610">
</details>

#### 7. Combine into a DataFrame
- All lists are assembled into a `pandas.DataFrame`.
- The column names are `model_name`, `km_driven`, `fuel_type`, `transmission`, `owner`, `price`, `link`.

#### 8. Return the DataFrame
- Finally, function returns the above DataFrame for further cleaning, analysis, and modelling.

</details>

---

### Engine Capacity Script (`get_engine_capacity`)

<details>
<summary>Click Here to view more Details</summary>
<br>

**Input :** List of URLs for individual car listings (`link` from the previous DataFrame).

#### 1. Iterate through each Car Listing URL
- Loops over the list of individual car listing page URL.

#### 2. Send an HTTP Request
- Uses the `requests` library to retrieve each page's HTML content.
- Adds a User-Agent header to simulate a real browser and reduce blocking risk.
- Applies a random delay of (4-8 seconds) between requests to avoid overloading the server.

#### 3. Parse the HTML Content
- Converts the response into a BeautifulSoup object using the `lxml` parser for fast, reliable parsing.

#### 4. Locate Engine Capacity Label
- Searches for all `<p>` tags with the class `sc-braxZu jjIUAi`.
- Checks if the text exactly matches "Engine capacity".

<details>
<summary>Click to view the HTML Element Snapshot</summary>
<br>
<img title="cars24" src="https://github.com/user-attachments/assets/80a81a7e-ffd6-4413-ab74-650dbf63afc6">
</details>

#### 5. Extract the Value
- If the label is found, grab the value from the next sibling element (`1197 cc`).
- Marks the entry as successfully found.
- If no engine capacity value is found, store `None` to maintain positional consistency.

#### 6. Return the List
- Outputs a list of engine capacities in the same order as the input URLs.

</details>

---

### Combine Data from Multiple Cities

<details>
<summary>Click Here to view Example Function</summary>
<br>

```python
# Parsing HTML Content of Hyderabad City from Cars24 Website
soup = scrape_car_listing('https://www.cars24.com/buy-used-cars-hyderabad/')

# Extracting Car Details of Hyderabad City
hyderabad = get_car_details(soup)
```

```python
# Parsing HTML Content of Bangalore City from Cars24 Website
soup = scrape_car_listing('https://www.cars24.com/buy-used-cars-bangalore/')

# Extracting Car Details of Bangalore City
bangalore = get_car_details(soup)
```

```python
# Parsing HTML Content of Mumbai City from Cars24 Website
soup = scrape_car_listing('https://www.cars24.com/buy-used-cars-mumbai/')

# Extracting Car Details of Mumbai City
mumbai = get_car_details(soup)
```

```python
# Parsing HTML Content of Delhi City from Cars24 Website
soup = scrape_car_listing('https://www.cars24.com/buy-used-cars-delhi-ncr/')

# Extracting Car Details of Delhi City
delhi = get_car_details(soup)
```

```python
# Concatenating Car Details of Different Cities into Single DataFrame
df = pd.concat([hyderabad, bangalore, mumbai, delhi], ignore_index=True)
df.head()
```

```python
# Extracting engine capacity of each car using its car listing link from Cars24 Website
engine_capacity = get_engine_capacity(df['link'])

# Adding "engine_capacity" column in the DataFrame
df['engine_capacity'] = engine_capacity

# Final DataFrame after Web Scraping
df.head()
```
</details>

---

### Dataset Description

<details>
<summary>Click Here to view more Details</summary>
<br>

The final dataset consists of 2,800+ unique car listings, with each record containing :

| Column | Description |
|:---|:---|
| `model_name` | Model name of car (2014 Hyundai Grand i10, etc.) |
| `fuel_type` | Fuel type (Petrol, Diesel, CNG, Electric) |
| `transmission` | Transmission type (Automatic or Manual) |
| `owner` | Previous owners count (1st owner, 2nd owner, 3rd owner, etc.) |
| `engine_capacity` | Engine size (in cc) |
| `km_driven` | Total distance traveled (in km) |
| `price` | Selling price (target variable) |

</details>

<hr>

## Setup

Follow these steps carefully to setup and run the project on your local machine :

### 1. Clone the Repository
First, you need to clone the project from GitHub to your local system.
```bash
git clone https://github.com/themrityunjaypathak/AutoIQ.git
```

### 2. Build the Docker Image
Docker allows you to package the application with all its dependencies.
```bash
docker build -t your_image_name .
```

> [!TIP]
>
> Make sure Docker is installed and running on your machine before executing this command.

### 3. Setup Environment Variables
This project uses a `.env` file to store configuration settings like model paths, allowed origins, etc.

#### `.env` file
- Stores environment variables in plain text.
```bash
# .env
ENV=dev_or_prod
MODEL_FREQ_PATH=path/to/model_freq.pkl
PIPE_PATH=path/to/pipe.pkl
LOWER_PIPE_PATH=path/to/lower_pipe.pkl
UPPER_PIPE_PATH=path/to/upper_pipe.pkl
ALLOWED_ORIGINS=comma_separated_list_of_allowed_origins
```

> [!IMPORTANT]
> Never commit `.env` to GitHub / Docker.
> 
> Add `.env` to `.gitignore` and `.dockerignore` to keep it private.

### 4. Run the Docker Container
Start the application using Docker. This will run the FastAPI server and handle all the dependencies automatically.
```bash
docker run --env-file .env -p 8000:8000 --name your_container_name your_image_name
```

> [!NOTE]
> `api.main` : Refers to the main.py file inside the api folder.
> 
> `app` : The FastAPI instance defined in your code.

### 5. Access the FastAPI Server
Once the container is running, open your browser and navigate to :
```bash
http://127.0.0.1:8000/docs
```

This opens the Swagger UI for testing the API endpoints.

> [!IMPORTANT]
> 
> If running the API locally :
> 
> ```bash
> uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
> ```
> Use the same host (`127.0.0.1`/`localhost`) for both the frontend and `ALLOWED_ORIGINS` in `.env`.
> 
> A mismatch makes browsers treat them as different origins and CORS will fail.

Access the live API [here](https://autoiq.onrender.com/docs) or Click on the Image below.

<a href="https://autoiq.onrender.com/docs"><img title="swagger-ui" src="https://github.com/user-attachments/assets/920ea2c9-231e-47f2-a1cc-d6ea9541481e"></a>

### 6. Stop the Docker Container
When you're done using the application, stop the running container.
```bash
docker stop your_container_name
```

<hr>

## Testing
Once the FastAPI server is running, you can test the API endpoints in Postman or any similar software.

### 1. Launch Postman and Create a New HTTP Request
- Launch the Postman application on your computer.
- Click on the "New" button, then select "HTTP" requests.

<img title="postman-ui" src="https://github.com/user-attachments/assets/deccef9b-ab45-4b7c-80ad-ec5fe0844e81">

### 2. Using GET and POST Methods in Postman

<details>
<summary>Click Here for details about GET Method</summary>

### GET Method
- Retrieve information from the server without modifying any data.
### Steps
- Open Postman and create a new request.
- Set the HTTP method to "GET" from the dropdown menu.
- Enter the endpoint URL you want to query.
```
http://127.0.0.1:8000
```
- Click the "Send" button to submit the request.
### Expected Response
- **Status Code :** It indicates that the request was successful and the server responded with the requested data.
```
200 OK
```
- **Response Body (JSON) :** This confirms that the API is running and returns the result of your API call.
```json
{
    "message":"Pipeline is live"
}
```

<img title="postman-get" src="https://github.com/user-attachments/assets/aaadad27-2074-4009-beae-35d36c82378d">

</details>

<details>
<summary>Click Here for details about POST Method</summary>

### POST Method
- Send data to a server to create/update a resource.
### Steps
- Open Postman and create a new request.
- Set the HTTP method to "POST" from the dropdown menu.
- Enter the endpoint URL you want to query.
```
http://127.0.0.1:8000/predict
```
- Navigate to the "Headers" tab and add the following : Key as `Content-Type`, Value as `application/json`
- Go to the "Body" tab, Select "raw", then choose "JSON" from the format dropdown menu.
- Enter the request payload in JSON format.
```json
{
  "brand": "MG",
  "model": "HECTOR",
  "km_driven": 80000,
  "engine_capacity": 1498,
  "fuel_type": "Petrol",
  "transmission": "Manual",
  "year": 2022,
  "owner": "1st owner"
}
```
- Click the "Send" button to submit the request.
### Expected Response
- **Status Code :** It indicates that the server successfully processed the request and generated a prediction.
```
200 OK
```
- **Response Body (JSON) :** This confirms that the API is running and returns the result of your API call.
```json
{
  "output": "₹7,81,412 to ₹12,66,018"
}
```

<img title="postman-post" src="https://github.com/user-attachments/assets/dfece1cc-37a5-4079-a0a1-a84a0f074c02">

</details>

<hr>

## Dockerization

Follow these steps carefully to containerize your project with Docker :

### 1. Install Docker
- Before starting, make sure Docker is installed on your system.
- Visit [Docker](https://www.docker.com/) ➜ Click on Download Docker Desktop ➜ Choose Windows / Mac / Linux.

<img title="docker" src="https://github.com/user-attachments/assets/200fd0a3-68f1-40d7-b1a7-299f0d6aae8e">

### 2. Verify the Installation
- Open Docker Desktop ➜ Make sure Docker Engine is Running.

<img title="docker-desktop" src="https://github.com/user-attachments/assets/5599f2fb-f1c1-4f0e-bc21-15fd31845270">

### 3. Create the Dockerfile
- Create a `Dockerfile` and place it in the root folder of your Repository.

### 4. Create the `.dockerignore` File
- This file tells Docker which files and folders to exclude from the image.
- This keeps the image small and prevents unnecessary files from being copied.

### 5. Build the Docker Image
- A Docker image is essentially a read-only template that contains everything needed to run an application.
- You can think of a Docker image as a blueprint or snapshot of an environment. It doesn't run anything.

```bash
docker build -t your_image_name .
```

### 6. Create the Docker Container
- When you run a Docker image, it becomes a Docker container.
- It is a live instance of that image, running your application in an isolated environment.

```bash
docker run --env-file .env -p 8000:8000 your_image_name
```

After the container starts, you can access your API.

```bash
http://127.0.0.1:8000
```

### 7. Push to Docker Hub
- Once your Docker image is ready, you can push it to Docker Hub.
- It allows anyone to pull and run it without building it themselves.

<details>
<summary>Click Here for steps to Push to Docker Hub</summary>

#### Login to Docker Hub
- Prompts you to enter your Docker Hub username and password.
- This authenticates your local Docker client with your Docker Hub account.

```bash
docker login
```

#### Tag the Docker Image
- Tagging prepares the image for upload to Docker Hub.

```bash
docker tag your_image_name your_dockerhub_username/your_image_name:latest
```

#### Push the Image to Docker Hub
- Uploads your image to your Docker Hub Repository.
- Once pushed, your image is publicly available.
- Anyone can now pull and run the image without building it locally.

```bash
docker push your_dockerhub_username/your_image_name:latest
```

</details>

Access the Docker Hub [here](https://hub.docker.com/r/themrityunjaypathak/autoiq) or Click on the Image below.

<a href="https://hub.docker.com/r/themrityunjaypathak/autoiq"><img title="docker-hub" src="https://github.com/user-attachments/assets/c118694b-ff6e-43ee-b358-9cfddfdbf7d4"></a>

### 8. Pull and Run Anywhere
- Once pushed, anyone can pull your image from Docker Hub and run it.
- This ensures that the application behaves the same way across all systems.

```bash
docker pull your_dockerhub_username/your_image_name:latest
```

- After pulling the Docker image, you can run it to create a Docker container from it.

```bash
docker run --env-file .env -p 8000:8000 your_dockerhub_username/your_image_name:latest
```

### 9. Verify the Container is Running
- Lists all the running containers with `container_id`.

```bash
docker ps
```

### 10. Stop the Container
- Stops the running container safely.
- `container_id` can be obtained from `docker ps` output.

```bash
docker stop container_id
```

<hr>

## Application

The frontend application files are in the `frontend/` folder :
- `index.html` : This file defines the structure and layout of the web page.
- `style.css` : This file handles the visual appearance of the web page.
- `script.js` : This file communicates between the web page and the REST API.

> [!IMPORTANT]
> If you clone this repo and want `script.js` to hit your local API instead of the live one, update the fetch URL.  
>
> Change from :  
> ```js
> const fetchPromise = fetch("https://autoiq.onrender.com/predict", {
>      method: "POST",
>      headers: { "Content-Type": "application/json" },
>      body: JSON.stringify(data),
> });
> ```  
>   
> To :  
> ```js
> const fetchPromise = fetch("http://127.0.0.1:8000/predict", {
>     method: "POST",
>     headers: { "Content-Type": "application/json" },
>     body: JSON.stringify(data),
> });
> ```

> [!NOTE]
>
> The API for this project is deployed using the free tier on Render.
>
> As a result, it may go to sleep after periods of inactivity.
> 
> Please start the API first by visiting the API URL. Then, navigate to the website to make predictions.
> 
> If the API was inactive, the first prediction may take a few seconds while the server spins back up.

Access the live website [here](https://autoiqlabs.vercel.app) or Click on the Image below.

<a href="https://autoiqlabs.vercel.app"><img title="frontend-ui" src="https://github.com/user-attachments/assets/2e2b5c1e-252f-46bb-9eaa-7fe0e34b24ce"></a>

<hr>

## Model Training & Evaluation

### 1. Load the Data

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Importing load_parquet function from read_data module
from read_data import load_parquet
cars = load_parquet('clean_data', 'clean_data_after_eda.parquet')
cars.head()
```
</details>

<hr>

### 2. Split the Data

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Creating Features and Target Variable
X = cars.drop('price', axis=1)
y = cars['price']
```
```python
# Splitting Data into Training and Testing Set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)
```
</details>

<hr>

### 3. Build Preprocessing Pipeline

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Pipeline for Nominal Column
nominal_cols = ['fuel_type','transmission','brand']
nominal_trf = Pipeline(steps=[
    ('ohe', OneHotEncoder(sparse_output=False, handle_unknown='ignore'))
])
```
```python
# Pipeline for Ordinal Column
ordinal_cols = ['owner']
ordinal_categories = [['Others','3rd owner','2nd owner','1st owner']]
ordinal_trf = Pipeline(steps=[
    ('oe', OrdinalEncoder(categories=ordinal_categories))
])
```
```python
# Pipeline for Numerical Column
numerical_cols = ['km_driven','year','engine_capacity']
numerical_trf = Pipeline(steps=[
    ('scaler', RobustScaler())
])
```
```python
# Adding Everything into ColumnTransformer
ctf = ColumnTransformer(transformers=[
    ('nominal', nominal_trf, nominal_cols),
    ('ordinal', ordinal_trf, ordinal_cols),
    ('scaling', numerical_trf, numerical_cols)
], remainder='passthrough', n_jobs=-1)
```
</details>

<hr>

### 4. Evaluate Multiple Models

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Models Dictionary
models = {
    'LR' : LinearRegression(n_jobs=-1),
    'KNN' : KNeighborsRegressor(n_jobs=-1),
    'DT' : DecisionTreeRegressor(random_state=42),
    'RF' : RandomForestRegressor(random_state=42, n_jobs=-1),
    'GB' : GradientBoostingRegressor(random_state=42),
    'XGB' : XGBRegressor(random_state=42, n_jobs=-1)
}
```
```python
# Computing Metrics through Cross-Validation
results = {}

for name, model in models.items():
    
    pipe = Pipeline(steps=[
        ('preprocessor', ctf),
        ('model', model)
    ])

    k = KFold(n_splits=5, shuffle=True, random_state=42)

    cv_results = cross_validate(estimator=pipe, X=X_train, y=y_train, cv=k, scoring={'mae':'neg_mean_absolute_error','r2':'r2'}, n_jobs=-1, return_train_score=False)

    results[name] = {'avg_error': -cv_results['test_mae'].mean(),'avg_score': cv_results['test_r2'].mean()}

    print()
    print(f'Model : {name}')
    print('-'*40)
    print(f'Average Error : {-cv_results['test_mae'].mean():.2f}')
    print(f'Standard Deviation of Error : {cv_results['test_mae'].std():.2f}')
    print(f'Average R2-Score : {cv_results['test_r2'].mean():.2f}')
    print(f'Error Stability (CV of MAE) : {(cv_results['test_mae'].std() / -cv_results['test_mae'].mean()) * 100:.2f}%')
```
</details>

<details>
<summary>Click Here to view Analysis</summary>
<br>

```
Model : LR
----------------------------------------
Average Error : 123193.35
Standard Deviation of Error : 6435.48
Average R2-Score : 0.77
Error Stability (CV of MAE) : 5.22%

Model : KNN
----------------------------------------
Average Error : 115518.58
Standard Deviation of Error : 3843.92
Average R2-Score : 0.79
Error Stability (CV of MAE) : 3.33%

Model : DT
----------------------------------------
Average Error : 116187.61
Standard Deviation of Error : 4254.52
Average R2-Score : 0.76
Error Stability (CV of MAE) : 3.66%

Model : RF
----------------------------------------
Average Error : 90937.17
Standard Deviation of Error : 2666.87
Average R2-Score : 0.86
Error Stability (CV of MAE) : 2.93%

Model : GB
----------------------------------------
Average Error : 98130.73
Standard Deviation of Error : 3453.66
Average R2-Score : 0.85
Error Stability (CV of MAE) : 3.52%

Model : XGB
----------------------------------------
Average Error : 90899.92
Standard Deviation of Error : 1913.66
Average R2-Score : 0.86
Error Stability (CV of MAE) : 2.11%
```

<img title="model-comparison" src="https://github.com/user-attachments/assets/d7805ffa-692c-48cc-af79-9ac3915f30a1">

</details>

<hr>

### 5. Evaluate StackingRegressor Model

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Evaluating StackingRegressor (RF + XGB + GB -> ElasticNet meta-learner)
from sklearn.ensemble import StackingRegressor
from sklearn.linear_model import ElasticNet

stack_estimators = [
    ('rf', RandomForestRegressor(random_state=42, n_jobs=-1)),
    ('xgb', XGBRegressor(random_state=42, n_jobs=-1)),
    ('gb', GradientBoostingRegressor(random_state=42))
]

stack_model = StackingRegressor(
    estimators=stack_estimators,
    final_estimator=ElasticNet(random_state=42),
    n_jobs=-1
)

stack_pipe = Pipeline(steps=[
    ('preprocessor', ctf),
    ('model', stack_model)
])

k = KFold(n_splits=5, shuffle=True, random_state=42)

stack_cv_results = cross_validate(estimator=stack_pipe, X=X_train, y=y_train, cv=k, scoring={'mae':'neg_mean_absolute_error','r2':'r2'}, n_jobs=-1, return_train_score=False)

stack_mae = -stack_cv_results['test_mae'].mean()
stack_std = stack_cv_results['test_mae'].std()
stack_r2 = stack_cv_results['test_r2'].mean()

print(f'Model : StackingRegressor')
print('-'*40)
print(f'Average Error : {stack_mae:.2f}')
print(f'Standard Deviation of Error : {stack_std:.2f}')
print(f'Average R2-Score : {stack_r2:.2f}')
print(f'Error Stability (CV of MAE) : {(stack_std / stack_mae) * 100:.2f}%')
print('')
```

</details>

<details>
<summary>Click Here to view Analysis</summary>
<br>

```
Model : StackingRegressor
----------------------------------------
Average Error : 87884.49
Standard Deviation of Error : 1488.70
Average R2-Score : 0.87
Error Stability (CV of MAE) : 1.69%
```
</details>

<hr>

### 6. Choosing a Single Model

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Creating Object of the Model
xgb = XGBRegressor(random_state=42, n_jobs=-1)

# Final Pipeline with XGBRegressor
pipe = Pipeline(steps=[
    ('preprocessor', ctf),
    ('model', xgb)
])
```
```python
# Computing Metrics through Cross-Validation
cv_results = cross_validate(estimator=pipe, X=X_train, y=y_train, cv=k, scoring={'mae':'neg_mean_absolute_error','r2':'r2'}, n_jobs=-1)
print(f"Average Error : {-cv_results['test_mae'].mean():.2f}")
print(f"Standard Deviation of Error : {cv_results['test_mae'].std():.2f}")
print(f"Average R2-Score : {cv_results['test_r2'].mean():.2f}")
print(f"Error Stability (CV of MAE) : {(cv_results['test_mae'].std() / -cv_results['test_mae'].mean()) * 100:.2f}%")
```
</details>

<details>
<summary>Click Here to view Analysis</summary>
<br>

```
Average Error : 90899.92
Standard Deviation of Error : 1913.66
Average R2-Score : 0.86
Error Stability (CV of MAE) : 2.11%
```

- The graph shows model performance by average error (lower is better) and average R<sup>2</sup> (higher is better).
- RandomForestRegressor and XGBRegressor are the top performers (\~₹90,900 MAE & R<sup>2</sup> 0.86).
- A StackingRegressor was also tried, improving MAE by only \~3% for 3x the model complexity and inference time.
```md
  [StackingRegressor]
   RF     XGB     GB
    \      |      /
     \     |     /
      \    |    /
       ▼   ▼   ▼
      ElasticNet
    [meta-learner]
          │
          ▼
    Final Prediction
```
- Not worth the trade-off for this project's scope, so **XGBRegressor** is used directly :
    - It ties RF on error but has the lowest standard deviation of error (XGB's ₹1,913 vs RF's ₹2,667),
    - It means more consistent predictions across folds.
    - Being a single model, it's also simpler to tune, explain, and serve than a 3-model stack.
</details>

<hr>

### 6. Performance Evaluation Graphs

#### Actual vs Predicted Plot

<details>
<summary>Click Here to view Analysis</summary>
<br>

| <img title="ap-plot" src="https://github.com/user-attachments/assets/00280bf2-cea3-4444-8687-778ea0f44bb3"> | <img title="ap-plot" src="https://github.com/user-attachments/assets/5dff1bed-780c-40bc-9593-0c3602e0bc29"> |
|---|---|

</details>

#### Learning Curve

<details>
<summary>Click Here to view Analysis</summary>
<br>

| R<sup>2</sup>-Score Curve | Error Curve |
|---|---|
| <img title="lr-curve" src="https://github.com/user-attachments/assets/1fdfdc9f-d4f9-43fa-a344-a1e2a96a21bc"> | <img title="lr-curve" src="https://github.com/user-attachments/assets/36c735f2-bc31-4792-b495-aed22af51f25"> |

</details>

<hr>

### 7. Hyperparameter Tuning

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Parameter Distribution
param_dist = {
    'model__n_estimators': [200, 300, 400],
    'model__learning_rate': [0.03, 0.05, 0.1],
    'model__max_depth': [2, 3, 4],
    'model__subsample': [0.5, 0.75, 1.0],
    'model__colsample_bytree': [0.5, 0.75, 1.0],
    'model__min_child_weight': [1, 3, 5]
}
```
```python
# RandomizedSearchCV Object with Cross-Validation
rcv = RandomizedSearchCV(estimator=pipe, param_distributions=param_dist, cv=k, scoring='neg_mean_absolute_error', n_iter=30, n_jobs=-1, random_state=42)
```
```python
# Fitting the RandomizedSearchCV Object
rcv.fit(X_train, y_train)
```
```python
# Best Parameter
rcv.best_params_
```
```python
# Best Estimator
best_model = rcv.best_estimator_
```
```python
# Computing Metrics through Cross-Validation after Tuning
cv_results = cross_validate(estimator=best_model, X=X_train, y=y_train, cv=k, scoring={'mae':'neg_mean_absolute_error','r2':'r2'}, n_jobs=-1)
print(f"Average Error : {-cv_results['test_mae'].mean():.2f}")
print(f"Standard Deviation of Error : {cv_results['test_mae'].std():.2f}")
print(f"Average R2-Score : {cv_results['test_r2'].mean():.2f}")
print(f"Error Stability (CV of MAE) : {(cv_results['test_mae'].std() / -cv_results['test_mae'].mean()) * 100:.2f}%")
```
</details>

<details>
<summary>Click Here to view Analysis</summary>
<br>

```
Average Error : 85281.35
Standard Deviation of Error : 2426.39
Average R2-Score : 0.88
Error Stability (CV of MAE) : 2.85%
```
</details>

<hr>

### 8. Performance Evaluation Comparison

#### Actual vs Predicted Plot

<details>
<summary>Click Here to view Analysis</summary>
<br>

| Before Tuning | After Tuning |
|---|---|
| <img title="ap-plot" src="https://github.com/user-attachments/assets/00280bf2-cea3-4444-8687-778ea0f44bb3"> | <img title="ap-plot" src="https://github.com/user-attachments/assets/6af0289a-c1da-415f-b890-7caf5fec3399"> |

</details>

#### Learning Curves

<details>
<summary>Click Here to view Analysis</summary>
<br>

| R<sup>2</sup>-Score Curve (Before Tuning) | R<sup>2</sup>-Score Curve (After Tuning) |
|---|---|
| <img title="lr-curve" src="https://github.com/user-attachments/assets/1fdfdc9f-d4f9-43fa-a344-a1e2a96a21bc"> | <img title="lr-curve" src="https://github.com/user-attachments/assets/c16236ed-019d-44c5-b262-9dec67c7c240"> |

| Error Curve (Before Tuning) | Error Curve (After Tuning) |
|---|---|
| <img title="lr-curve" src="https://github.com/user-attachments/assets/36c735f2-bc31-4792-b495-aed22af51f25"> | <img title="lr-curve" src="https://github.com/user-attachments/assets/7013f64c-4ae7-4f24-94f9-9804dd74d947"> |

</details>

<hr>

### 9. Final Model Evaluation on Unseen Data

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Model Performance on Unseen Data
y_pred_test = best_model.predict(X_test)
```
```python
# Mean Absolute Error and R2-Score on Unseen Data
from sklearn.metrics import mean_absolute_error, r2_score
print(f'Mean Absolute Error on Unseen Data : {mean_absolute_error(y_test, y_pred_test):.2f}')
print(f'R2-Score on Unseen Data : {r2_score(y_test, y_pred_test):.2f}')
```
```python
# Mean Absolute Percentage Error on Unseen Data
from sklearn.metrics import mean_absolute_percentage_error
mape = mean_absolute_percentage_error(y_test, y_pred_test)
print(f'Mean Absolute Percentage Error on Unseen Data : {mape * 100:.2f}%')
```
</details>

<details>
<summary>Click Here to view Analysis</summary>
<br>

```
Mean Absolute Error on Unseen Data : 87723.02
R2-Score on Unseen Data : 0.87
Mean Absolute Percentage Error on Unseen Data : 13.93%
```
</details>

<hr>

### 10. Predicting a Price Range

<details>
<summary>Click Here to view Code Snippet</summary>
<br>

```python
# Importing GradientBoostingRegressor for Quantile Regression
from sklearn.ensemble import GradientBoostingRegressor

# Lower Bound Pipeline (10th Percentile)
lower_pipe = Pipeline(steps=[
    ('preprocessor', ctf),
    ('model', GradientBoostingRegressor(loss='quantile', alpha=0.1, random_state=42))
])

# Upper Bound Pipeline (90th Percentile)
upper_pipe = Pipeline(steps=[
    ('preprocessor', ctf),
    ('model', GradientBoostingRegressor(loss='quantile', alpha=0.9, random_state=42))
])

# Fitting Both Quantile Pipelines on Training Data
lower_pipe.fit(X_train, y_train)
upper_pipe.fit(X_train, y_train)

# Predicting Lower and Upper Bounds on Unseen Data
y_pred_lower = lower_pipe.predict(X_test)
y_pred_upper = upper_pipe.predict(X_test)

# Clamping Lower Bound at 0 as a Safety Net (Price can never be Negative)
y_pred_lower = np.clip(y_pred_lower, a_min=0, a_max=None)
```
</details>

<details>
<summary>Click Here to view Analysis</summary>
<br>

- A single point prediction is not very useful on its own, a **range** is more practical for buyers/sellers.
- The initial approach used a flat `prediction ± MAE` range, but this is flawed :
    - MAE is one global average error, it does not scale with the price of the car.
    - For cheap cars, `prediction - MAE` could go **negative**, which makes no sense for a price.
    - For expensive cars, the same flat range was unrealistically tight.
    - It also required the exact training-time MAE in `.env`, which anyone cloning the repo would not have.
- This was replaced with two `GradientBoostingRegressor` models trained directly on the P<sub>10</sub> and P<sub>90</sub> of price.
- Both are exported as `lower_pipe.pkl` and `upper_pipe.pkl` alongside the main model,
- So the API loads them like any other artifact, no manual `.env` value needed.
- The lower bound is additionally clipped at 0 in the API as a safety net.

</details>

<hr>

## Challenges & Solutions

### Challenge 1 : Getting Real-World Data

#### Problem
- I wanted to use real-world data instead of a toy dataset, as it better represents messy, real-life scenarios.
- However, Cars24 loads its content dynamically using JavaScript, meaning a simple HTTP request is not enough.

#### Solution
- I used [Selenium](https://www.selenium.dev/) to simulate a real browser, ensuring the page was fully loaded before scraping.
- Once the content was rendered, I used [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to efficiently parse the HTML.
- This approach allowed me to reliably capture complete car details.

### Challenge 2 : Handling Large Datasets Efficiently

#### Problem
- The raw scraped dataset was large and consumed unnecessary memory.
- Loading it repeatedly during experimentation became slow and inefficient.

#### Solution
- I optimized memory usage by downcasting data types.
- I stored the dataset in Parquet format, which compresses data without losing information.
- This enabled much faster read/write performance compared to CSV.

### Challenge 3 : Avoiding Data Leakage

#### Problem
- If preprocessing is applied to the entire dataset, test data can leak into the training process.
- This creates overly optimistic results and reduces the model's ability to generalize.

#### Solution
- I implemented Scikit-learn [Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) and [ColumnTransformer](https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html) to apply preprocessing only on training data.
- This kept the test data completely unseen during preprocessing, preventing leakage.

### Challenge 4 : Communicating Prediction Uncertainty

#### Problem
- A single point prediction doesn't tell a buyer/seller how confident the model actually is.
- Our initial `prediction ± MAE` range went negative for cheap cars and needed the training-time MAE in `.env`.

#### Solution
- I trained two `GradientBoostingRegressor` models on the 10th and 90th percentile of price (quantile loss).
- The range now scales naturally with the predicted price and can't go negative, with a clip at 0 as a safety net.
- Both models ship as `lower_pipe.pkl`/`upper_pipe.pkl`, so the range updates automatically on retraining.

### Challenge 5 : Deploying the Model as an API

#### Problem
- Even after building the ML pipeline, it remained offline and could only be used locally.
- There was no way to send inputs and get predictions over the web or from other applications.
- The model depended on the local system and could not serve predictions to external users or services.

#### Solution
- I deployed the ML model as an API using [FastAPI](https://fastapi.tiangolo.com/).
- This allowed users and applications to send inputs and receive predictions in real time.
- I added a `/predict` endpoint for predictions and a `/health` endpoint for monitoring API status.
- I implemented input validation and rate limiting to prevent misuse and ensure stability under load.
- These improvements made the API accessible, reliable, and production-ready.

### Challenge 6 : Accessibility for Non-Technical Users

#### Problem
- Even if the API works correctly, non-technical users may still find it difficult to test and use.
- This limits adoption and accessibility.

#### Solution
- I created an HTML/CSS/JS frontend that sends requests to the API and displays predictions instantly.
- I also included an example payload in Swagger UI so users can test the API with minimal effort.

### Challenge 7 : Consistent Deployment Across Environments

#### Problem
- Installing dependencies and setting up the environment manually is time-consuming and error-prone.
- This becomes worse across different machines and operating systems.
- Sharing the project also becomes difficult, since others must replicate the exact setup.

#### Solution
- I created a multi-stage Dockerfile.
- It builds the FastAPI application, installs dependencies, and copies only required files into the final image.
- I used a `.dockerignore` file to exclude unnecessary files and keep the image lightweight.
- This allows the project to run consistently on any system with [Docker](https://www.docker.com/) installed.
- It eliminates dependency mismatches and OS-specific issues.
- Same Docker image can be used to deploy on Render, Docker Hub or run locally with a single docker command.

<hr>

## Folder Structure

```
AutoIQ/
│
├── api/                        # FastAPI Code to deploy API on Render
│   ├── main.py                 # App instance, middleware, and endpoints
│   ├── models.py               # Lifespan loads pipe/model_freq/lower_pipe/upper_pipe
│   ├── schemas.py              # Pydantic request & response models
│   └── config.py               # Loads and validates environment variables
│
├── clean_data/                 # Cleaned Dataset (Parquet Format)
│   └── clean_data.parquet
│   └── ...
│
├── frontend/                   # Frontend Application
│   ├── fonts/                  # Self-hosted Satoshi font (woff2)
│   ├── images/                 # Frontend Assets
│   ├── index.html              # Frontend HTML File
│   ├── script.js               # Frontend JS File
│   └── style.css               # Frontend CSS File
│
├── models/                     # Serialized Components for Prediction
│   ├── pipe.pkl                # Tuned XGBRegressor pipeline (point estimate)
│   ├── model_freq.pkl          # Frequency-encoding dictionary for "model" column
│   ├── lower_pipe.pkl          # Quantile pipeline, 10th percentile (price range lower bound)
│   └── upper_pipe.pkl          # Quantile pipeline, 90th percentile (price range upper bound)
│
├── notebooks/                  # Jupyter Notebooks for Project Development
│   └── ...
│
├── scrape_code/                # Web Scraping Notebook
│   └── scrape_code.ipynb
│
├── scrape_data/                # Scraped Dataset (CSV Format)
│   └── scrape_data.csv
│
├── utils/                      # Reusable Python Functions (utils Package)
│   ├── __init__.py
│   ├── web_scraping.py
│   ├── export_data.py
│   └── ...
│
├── .dockerignore               # All files and folders ignored by Docker while building Docker Image
├── .env.example                # Template for required environment variables
├── .gitignore                  # All files and folders ignored by Git while pushing code to GitHub
├── Dockerfile                  # Instructions for building the Docker Image
├── LICENSE                     # License specifying permissions and usage rights
├── README.md                   # Detailed documentation of the Project
└── requirements.txt            # List of required libraries for the Project
```

<hr>

## License

This project is licensed under the [MIT License](LICENSE). You are free to use and modify the code as needed.

<div align='left'>
  
**[`^        Scroll to Top       ^`](#top)**

</div>
