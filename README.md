# DevOps Apprenticeship: Project Exercise

## Getting started

The project uses a virtual environment to isolate package dependencies. To create the virtual environment and install required packages, run the following from a bash shell terminal:

```bash
$ poetry install
$ cp -n .env.template .env
```

Once all packages have been installed, start the Flask app by running:
```bash
$ poetry run flask run
```

You should see output similar to the following:
```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: development
 * Debug mode: on
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
 * Restarting with fsevents reloader
 * Debugger is active!
 * Debugger PIN: 226-556-590
```
Now visit [`http://localhost:5000/`](http://localhost:5000/) in your web browser to view the app.

### Connecting with Azure Cosmos DB
To connect up the app with a Cosmos DB collection, copy the contents of `.env.template` into a `.env` file if not already done in setup. 
Paste the database connection string and collection name into the respective values.

### Running tests
To be able to run the e2e tests, Chrome must be installed and you must download `chromedriver.exe` and put it in the root folder of the project.

To run all tests, run `pytest`.
To run tests in a particular folder, run `pytest tests` or `pytest tests_e2e`.

### Running the app in a VM
In the root directory of this repo, run `vagrant up`.

### Running the app via docker-compose
To run the app in their respective environments, run the following commands:
Dev: `docker-compose up --build`
Prod: `docker-compose -f docker-compose.prod.yml up --build`

### Running tests via docker-compose
To run the tests in a docker container, run `docker-compose -f docker-compose.test.yml up --build`

### Architecture diagrams
These can be found in the `./documentation` folder.