# recaptcha-scraper

This application will scrape sites protected by [reCAPTCHA](https://www.google.com/recaptcha/about/) 

## How to build it?

This project contains a Dockerfile, so the main requirement to be able to use this is to have 
[docker](https://www.docker.com/get-started/) installed in the system.

To build the docker image, being at the root of the project, run this command:

```shell
docker build -t my_fastapi_playwright_app .
```

Once this is done, you can start the app using this command:

```shell
docker run -d --name my_app_container -p 8000:8000 my_fastapi_playwright_app
```

This will expose the app using the port 8000, you can adjust the command if you have any other port available
by changing the part of the command
```shell
-p [ANY_AVAILABLE_PORT]:8000
```

## How to use it?

Assuming you are running the application on port 8000, you can access in the URL http://localhost:8000/, also
as the implementation of the API was done using FastAPI, it has native support for swagger, which can be accessed
in http://localhost:8000/docs

The endpoint to use is the POST handler for `/scrape` endpoint, it will receive a string of the URL to scrape.

## Possible errors

The implementation uses external libraries to transform speech to text, so this could sometimes fail. If that is the
case, an error will be thrown informing to the user that a timeout happened.

## Implementation specific details

The project structure contains two main parts:
- `scraper` Contains the source code of the implementation
- `tests` Contains the tests implemented for the solution

### scraper directory

- `router` Contains the routers needed for each use case. For now, only has `scraping.py` router
- `schemas` Contains the pydantic models used for data validation. I called schemas, so in case in a furhter
step we would like to add library to interact with databases, we can store the models in a directory called
`modles`
- `services` Contains the business logic to perform the scraping.

## Sample use cases:
https://www.google.com/recaptcha/api2/demo

https://recaptcha-demo.appspot.com/recaptcha-v2-checkbox.php
