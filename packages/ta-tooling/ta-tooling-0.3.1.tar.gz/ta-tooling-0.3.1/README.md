# TA Tooling

Various tools for teaching assistant who is working with [Blackboard](https://www.blackboard.com/), a learning management system.

## Installation

```console
python -m pip install ta-tooling
```

## Usage

### Get list of students in the class

To get list of students in the class, run

```console
ta-tooling get-student-list
```

The program will ask for `course id`, `username`, and `password`. It will login with the username password you provided
and produce a CSV file of students in the course. The `course id` can be the actual course id or a URL to your course.

The CSV file will have the following header.

```plain
emailHandle,firstName,lastName,userId,courseMembershipId
```

### Group submission files

To group the submission files by email handle. Download and extract the ZIP file into a directory (call `source-dir` in the example).

```console
ta-tooling categorize source-dir dest-dir
```

In version 0.3.x the support for categorizing directly from a ZIP file is added.

### Download file submitted for a question in a quiz

Note: Currently, only Firefox is supported, and webdriver is needed.

To download file submitted as an answer to a question in a quiz, first get the links by injecting the extraction code. To get the extraction code (and start the server for the code to call back to).

``` console
ta-tooling serve-inject
```
and follow instruction show on the web page. Obtain the user list if have not done already.

``` console
ta-tooling get-student-list
```

Use the student list and the download links to download the files.

``` console
ta-tooling download-links users.json files.json
```

Some files will not be automatically downloaded, in that case, you need to confirm the download manually
(within certain time limit; otherwise, you will miss the window of file moving).

## TODO

- The `Accept-Origin` that the submission download for a question in a quiz is relying on is expected to be
  tighten. The plan is to switch to the correct iframe, and execute javascript directly through selenium.
- (serve-inject) The script injected to the page will get
