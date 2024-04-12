# [new-dinker] API Server

**Role1. Scrapps Starbucks menu data from the official website.**\
**Role2. Stores data in mysql.**\
**Role3. Provides the data through API.**


## Getting Started
1. Clone the repository
   - ```git clone https://github.com/yunseoLee0343/new-dinker-api-server.git ```
2. Navigate to the project directory
    - ``` cd myApi ```
3. Install the dependencies
    - ``` pip install -r requirements.txt ```
4. Run the server
    - ``` python manage.py runserver 8000 ```


## API Endpoints
- /admin
- /fetch
  - /fetch/starbucks/all
  - /fetch/starbucks/{str:field_name}/{str:field_value}
    - Model Product consist of fields: 'product_name', 'image_url', 'calories', etc.
      - You can request any of fields.
        - '/fetch/starbucks/product_name/카푸치노' and '/fetch/starbucks/calories/100' both possible.
      - You can get multiple products.


## Notable Features
1. **Priority Queue as a whole**
   - The server uses a priority queue to manage all the requests.
   - Scrapping process and API response process are separated.
   - Especially, I intended scrapping to be done in the background.
2. **Priority Queue as Error Handling**
    - If the server fails to fetch the data from the official website, the server will retry the request.
    - The server will retry the request with a higher priority.


## Project Structure
- [WARNING] This project is not yet deployed on AWS EC2 instance.

![NewDinker_Diagram.jpg](myApi%2FNewDinker_Diagram.jpg)

