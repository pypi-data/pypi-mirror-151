# Teko CLI Tools

```
pip install teko-cli
```
This is a Python package that contains some classes and CLI tools to be used during development 
process at Teko Vietnam (https://teko.vn).

List of tools:

- Teko Jira Tools: for pushing test case/ test cycle
- Teko Jira Export Test: for pytest export jira test case/test cycle
- Teko Oas Tools: for validate auto doc match with defined doc


## 1 Installation

To use this tools, Python 3.6+ should be instaled. 

Install or upgrade to the latest version:

```shell
$ pip install -r requirements.txt
$ pip install --editable .
```

After successful installation, you should be able to use `teko` command in your 
console terminal:

```
$ teko
```

You should see this kind of help message:

```
Usage: teko [OPTIONS] COMMAND [ARGS]...

Options:
  --install-completion [bash|zsh|fish|powershell|pwsh]
                                  Install completion for the specified shell.
  --show-completion [bash|zsh|fish|powershell|pwsh]
                                  Show completion for the specified shell, to
                                  copy it or customize the installation.

  --help                          Show this message and exit.

Commands:
  cs
  jira
  oas
```

## Using Teko Jira tool

### 2.1 Configure Jira credential

This tool use username/password authentication to Jira server, Confluence documentation and working with one Jira project 
at the same time. Jira server authentication uses 4 environment variables below. 
You can set these variables to the your environment, or save it to `.env` file in working
directory:

Sample content of `.env` file:

```
JIRA_SERVER=jira.teko.vn
JIRA_PROJECT_KEY=<project-key>
JIRA_USERNAME=<jira-username>
JIRA_PASSWORD=<jira-password>
CONFLUENCE_USERNAME=<confluence-username>
CONFLUENCE_PASSWORD=<confluence-password>
```

### 2.2 Submit (create) list of testcases to a Jira Project

To push testcases to a Jira Project, you should prepare a `.yaml` 
or a `.json` file, containing list of testcases to be created in Jira, 
then use following command:

```
$ teko jira create-tests {testcase_file}
```

To see help message, use `--help` option: `teko jira create-tests --help`:

```
Usage: teko jira create-tests [OPTIONS] FILE



Arguments:
  FILE  The name of a testcase definition file  [required]

Options:
  --help  Show this message and exit.
```

**Note:** This tool uses test case `name` as identification, so existing tests with same `name` 
will be updated with the latest information. 

#### Sample testcases file

- `.yaml` file

```yaml
- name: Testcase 01
  issueLinks: [TESTING-4]
  objective: Test 01 Objective
  precondition: Test 01 Precondition
  testScript:
    type: PLAIN_TEXT
    text: >
      - init x and y <br/>
      - call func add(x, y)
  labels: [ABC, XYZ]
- name: Testcase 02
  issueLinks: [TESTING-4, TESTING-5]
  objective: Test 02 Objective
  precondition: Test 02 Precondition
  priority: Normal
  status: Draft
  testScript:
    type: STEP_BY_STEP
    steps:
    - description: <i>Step 1</i>
      testData: (x,y) = (1,3)
      expectedResult: <strong>4</strong>
    - description: Step 2
      testData: <code>(x,y) = (4,5)</code>
      expectedResult: 9
```

- Equivalent `.json` file:

```json
[
  {
    "name": "Testcase 01",
    "issueLinks": [
      "TESTING-4"
    ],
    "objective": "Test 01 Objective",
    "precondition": "Test 01 Precondition",
    "testScript": {
      "type": "PLAIN_TEXT",
      "text": "- init x and y <br/> - call func add(x, y)\n"
    },
    "labels": ["ABC", "XYZ"]
  },
  {
    "name": "Testcase 02",
    "issueLinks": [
      "TESTING-4",
      "TESTING-5"
    ],
    "objective": "Test 02 Objective",
    "precondition": "Test 02 Precondition",
    "priority": "Normal",
    "status": "Draft",
    "testScript": {
      "type": "STEP_BY_STEP",
      "steps": [
        {
          "description": "<i>Step 1</i>",
          "testData": "(x,y) = (1,3)",
          "expectedResult": "<strong>4</strong>"
        },
        {
          "description": "Step 2",
          "testData": "<code>(x,y) = (4,5)</code>",
          "expectedResult": "9"
        }
      ]
    }
  }
]
```

### 2.3 Create test cycle (testrun result) in a Jira Project

To create a testrun report (cycle) to a Jira Project, you should prepare a `.yaml` 
or a `.json` file, containing list of testcases and **their result** to be created 
in Jira, then use following command:

```
$ teko jira create-cycle {testcase_file}
```

#### Sample testrun (cycle) file

- `.yaml` file

```yaml
- name: Testcase 01
  testrun_folder: /Sprint 1
  testrun_status: Pass
  testrun_environment: Dev
  testrun_comment: The test has passed successfully
  testrun_duration: 300000
  testrun_date: "2020-12-31T23:59:59Z"  
- name: Testcase 02
  testrun_folder: /Sprint 2
  testrun_status: Fail
  testrun_environment: test1
  testrun_comment: The test has failed on some automation tool procedure
  testrun_duration: 30000
  testrun_date: "2020-12-31T23:59:59Z" 
```

- Equivalent `.json` file

```json
[
  {
    "name": "Testcase 01",
    "testrun_folder": "/Sprint 1",
    "testrun_status": "Pass",
    "testrun_environment": "Dev",
    "testrun_comment": "The test has passed successfully",
    "testrun_duration": 300000,
    "testrun_date": "2020-12-31T23:59:59Z"
  },
  {
    "name": "Testcase 02",
    "testrun_folder": "/Sprint 2",
    "testrun_status": "Fail",
    "testrun_environment": "test1",
    "testrun_comment": "The test has failed on some automation tool procedure",
    "testrun_duration": 30000,
    "testrun_date": "2020-12-31T23:59:59Z"
  }
]
```
**Note:**
-  Test run results are grouped into multiple cycles based on their common `testrun_folder`.
- `testrun_duration` is measured in milliseconds.
- `testrun_environment` is chosen from available environments that defined by users in the project. Do this by accessing **Configuration** in Tests Board on Jira.  

### Sample combined testcase file with test results
Both test case and test run use the **same structure**. 
So you can you a single combined the information and the result of a test into one wrapper for both operation: create tests and create cycles. 
This file can be **generated automatically** from *docstrings* and/or 
*annotation*/*decorator* in auto test code.

### 2.4 Sample combined testcase file with test results

- `.yaml` file

```yaml
- name: Testcase 01
  issueLinks: [TESTING-4]
  objective: Test 01 Objective
  precondition: Test 01 Precondition
  testScript:
    type: PLAIN_TEXT
    text: >
      - init x and y <br/>
      - call func add(x, y)
  labels: ABC, XYZ
  testrun_status: Pass
  testrun_environment: Dev
  testrun_comment: The test has passed successfully
  testrun_duration: 300000
  testrun_date: "2020-12-31T23:59:59Z" 
- name: Testcase 02
  issueLinks: [TESTING-4, TESTING-5]
  objective: Test 02 Objective
  precondition: Test 02 Precondition
  priority: Normal
  status: Draft
  testScript:
    type: STEP_BY_STEP
    steps:
    - description: <i>Step 1</i>
      testData: (x,y) = (1,3)
      expectedResult: <strong>4</strong>
    - description: Step 2
      testData: <code>(x,y) = (4,5)</code>
      expectedResult: 9
  testrun_status: Fail
  testrun_environment: test1
  testrun_comment: The test has failed on some automation tool procedure
  testrun_duration: 30000
  testrun_date: "2020-12-31T23:59:59Z"
```   

- Equivalent `.json` file

```json
[
  {
    "name": "Testcase 01",
    "issueLinks": [
      "TESTING-4"
    ],
    "objective": "Test 01 Objective",
    "precondition": "Test 01 Precondition",
    "testScript": {
      "type": "PLAIN_TEXT",
      "text": "- init x and y <br/> - call func add(x, y)\n"
    },
    "labels": ["ABC", "XYZ"],
    "testrun_status": "Pass",
    "testrun_environment": "Dev",
    "testrun_comment": "The test has passed successfully",
    "testrun_duration": 300000,
    "testrun_date": "2020-12-31T23:59:59Z"
  },
  {
    "name": "Testcase 02",
    "issueLinks": [
      "TESTING-4",
      "TESTING-5"
    ],
    "objective": "Test 02 Objective",
    "precondition": "Test 02 Precondition",
    "priority": "Normal",
    "status": "Draft",
    "testScript": {
      "type": "STEP_BY_STEP",
      "steps": [
        {
          "description": "<i>Step 1</i>",
          "testData": "(x,y) = (1,3)",
          "expectedResult": "<strong>4</strong>"
        },
        {
          "description": "Step 2",
          "testData": "<code>(x,y) = (4,5)</code>",
          "expectedResult": "9"
        }
      ]
    },
    "testrun_status": "Fail",
    "testrun_environment": "Test1",
    "testrun_comment": "The test has failed on some automation tool procedure",
    "testrun_duration": 30000,
    "testrun_date": "2020-12-31T23:59:59Z"
  }
]
```
## 3 Using export test
### 3.1 Configure
- Add to test setting `pytest_plugins = ["teko.utils.jira_export_test"]` . Example, add to `conftest.py`
- To use decorator: `from teko.utils.jira_export_test.wraper import jira_test`
- To use test script type STEP_BY_STEP: `from teko.models.jira_export_test.test_step import TestStep`
#### Env
- `$JIRA_TEST_CASE_ARTIFACT`: test_case file path, default is test_case.json
- `$JIRA_TEST_CYCLE_ARTIFACT`: test_cycle file path, default is test_cycle.json
- Optional: `$ENV` or `$ENVIRONMENT` for test cycle env. Default, detect env from `$CI_COMMIT_BRANCH`
### 3.2 Write test function
- example in `/sample/jira_export_test/`

Maybe you need push test to Jira with teko-tool, this is example gitlab-ci.yml
```
test:unittest:
  stage: test
  ...
  variables:
    JIRA_TEST_CASE_ARTIFACT: test_case.json
    JIRA_TEST_CYCLE_ARTIFACT: test_cycle.json
  artifacts:
    paths:
      - $JIRA_TEST_CASE_ARTIFACT
      - $JIRA_TEST_CYCLE_ARTIFACT
    expire_in: 1 week
  allow_failure: false


report:push-test:
  stage: report
  image: python:3.7-slim
  variables:
    JIRA_TEST_CASE_ARTIFACT: test_case.json
    JIRA_TEST_CYCLE_ARTIFACT: test_cycle.json
    JIRA_PROJECT_KEY: TESTING
    JIRA_SERVER: jira.teko.vn
    JIRA_USERNAME: changeme
    JIRA_PASSWORD: changeme
    CONFLUENCE_USERNAME: changeme
    CONFLUENCE_PASSWORD: changeme
  script:
    - pip install --upgrade --cache-dir=.pip teko-cli
    - teko jira create-tests $JIRA_TEST_CASE_ARTIFACT
    - teko jira create-cycle $JIRA_TEST_CYCLE_ARTIFACT
  cache:
    key: pip-cache
    paths: [ .pip ]
  allow_failure: true
  when: always
```

- Enviroment:
 - `$JIRA_TEST_CASE_ARTIFACT`: test_case file path, default is test_case.json
 - `$JIRA_TEST_CYCLE_ARTIFACT`: test_cycle file path, default is test_cycle.json
 - `$JIRA_SERVER`: jira.teko.vn
 - `$JIRA_PROJECT_KEY`: TESTING
 - `$JIRA_USERNAME`: tekobot
 - `$JIRA_PASSWORD`: *****
 - `$CONFLUENCE_USERNAME`: tekobot
 - `$CONFLUENCE_PASSWORD`: *****

## 4. Teko OAS tool

Open Api Specification tool
- OpenAPI spec parser and validator
- OpenAPI spec comparator
- OpenAPI gen html/pdf (coming soon)
```
$ teko oas
```

```
Usage: teko oas [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  diff
  parse
```
### 4.1 Parse and validate Openapi spec

This tool parse and validate Openapi spec with input is path to file json/yaml or link to file yaml (json: coming soon) openapi file.
```
$ teko oas parse <Path/Link to openapi file>
```
You can see errors if file's format is wrong:
```
$ teko oas parse sample/oas_tool/sample-doc-false-format.yaml
```

```
...
paths./api/v1/rule/{id}.get.parameters.0: Parameter paths./api/v1/rule/{id}.get.parameters.0 must be required since it is in the path
paths./api/v1/rule/{id}.get.parameters.3.schema: Expected paths./api/v1/rule/{id}.get.parameters.3.schema.default to be one of [<class 'int'>], got <class 'str'>

2 errors

```

### 4.2 Compare spec

This tool compare between generated spec (from code) and designed spec.

Input is two paths to file json/yaml or link to file yaml (json: coming soon) openapi files.
```
$ teko oas diff <Path/Link to designed spec> <Path/Link to generated spec> 
```

* Example result:
```
$ teko oas diff sample/oas_tool/sample-doc.yaml sample/oas_tool/sample-param-change.json
```
```commandline
[TEKO TOOL][INFO]:        OAS compare spec!
 difference
   paths
     /api/v1/rule/{id} GET
       parameters
         miss_param1
-         Class object
+         None
         miss_param2
-         Class object
+         None
         diff_param_type1
           schema
             type
-             boolean
+             string
             default
-             False
+             None
         diff_param_default_and_in_2
           in
-           header
+           query
           required
-           False
+           True
           schema
             default
-             False
+             True
 miss
 redundancy
[TEKO TOOL][INFO]:        Error: 7
[TEKO TOOL][INFO]:        Warning: 0

```

### 4.3 Unit test
Run pytest file "sample/oas_tool_test/test_compare.py" 
to check compare tool with specific cases and results.
```commandline
teko-tools $ pytest sample/oas_tool_test/test_compare.py
```
