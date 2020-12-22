# validateoutput Documentation

## How it works

This is a very simple script that checks for abnormal lines in the logs.

For each log, it checks every line, checking if there is either the word "Action" or "Entity". If that's not the case, it means that something in the parsing process went wrong.

## Is it Necessary?

We commented out every irrelevant printf call in the parser, so the only thing the parser should log are the features we expect. Still, testing is always a good practice.
