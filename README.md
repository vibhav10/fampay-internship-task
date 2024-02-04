# fampay-internship-task

This is a Django Restframework project made for the Fampay Internship Task. The project is a simple API that fetches videos from the Youtube API and stores them in the database.



### Prerequisites

- Python 3.6 or higher
- pip package manager


## Setup Instructions

To set up and run this Django project locally, please refer to the [Setup Instructions](./SETUP.md).

## API Documentation
[Postman Collection](https://interstellar-crescent-487348.postman.co/workspace/TICC~f2c8121f-3c6e-4f37-8235-c8fdd6b5a5b4/collection/17375194-8b1d35a6-4b78-46ad-830b-378ede6bc8bb?action=share&creator=17375194) <br>


## User Flow
1. Create a new user by sending a POST request to the /users/auth/register/ endpoint with the following payload:
```json
{
    "email": "your_email",
    "password": "your_password",
    "full_name": "your_name"
}
2. Add search string to the database by sending a POST request to the /users/addsearchstring/ endpoint with the following payload:
```json
{
    "search":"football"
}

```
3. Add API key to the database by sending a POST request to the /users/addapikey/ endpoint
```json
{
    "key":"your_api_key"
}
```
4. Fetch videos from the Youtube API by sending a GET request to the /videos/videolist/ endpoint
