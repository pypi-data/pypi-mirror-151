# py-test-api

## About
This project is a base for API-related test frameworks.

## Tools chain
* [python](https://www.python.org/doc/) to code
* [prospector](http://prospector.landscape.io/en/master/) to analyze code
* [pytest](https://docs.pytest.org/en/6.2.x/) to run tests
* [requests](https://docs.python-requests.org/en/latest/) to work with HTTP
* [wiremock](http://wiremock.org/) to mock HTTP-based APIs

## Features
* Comprehensive but easy to write/read tests
  * structured design
  * in-built HTTP client
  * in-built requests intercepting
  * in-built logging
  * configuration handling
* Kept cleaned codebase 
  * usage of tools for static code analysis
* Test management based on app versions
  * run only those tests which correspond to the right app version
* No flaky tests & impediments due to not-ready functionality
  * put JSON stubs into the special directory & enjoy
* Human-readable HTML reports
* Integration with Jira Xray 
* Ability to run tests in parallel

## How to
1. run a WireMock server
`java -jar "...\\py-test-api\\data\\wiremock\\wiremock-jre8-standalone-2.32.0.jar" --port 18389 --root-dir "...\\py-test-api\\data\\wiremock"`
2. make a static code analysis
`prospector`
3. execute particular tests + HTML-report
- sequentially 
`pytest test/spec/http_spec.py --html=pytest_report.html --self-contained-html --junitxml=report.xml`
- in parallel 
`pytest --html=pytest_report.html --self-contained-html --junitxml=report.xml -n auto --dist loadscope`
4. push a release to PiPy
- `python setup.py check -rs`
- `python setup.py sdist bdist_wheel`
- `twine upload dist/*`