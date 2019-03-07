# BETO SALES FLASK BOILERPLATE

### Coverage of tests
To run the coverage, run the commands below:
```bash
dotenv run coverage run --source project -m unittest discover -s project/server -v
coverage html
```
These commands will create a directory named `htmlcov`, you should open the `htmlcov/index.html` in your favorite browser to see which parts of your code have been covered or not.
