## Test - github API datetime statitics

### Running Server and Tests


**Step_1**<br>
- Open a terminal window and run the command **<$ python -m uvicorn main:app --reload >**: Server will automatically run.

**Step_2**<br>
- Open another terminal window and run the command **<$ python test.py >**: Tests will automatically run.


**This is the api response format**<br>
```dif
api_response_dict = {
    'repository': None,
    'url': None,
    'timestamps': [],
    'success': True,
    'reponse_code_not_200': False,
    'repository_not_found': False
  }
```