# Software Engineering Principles
> Key changes we've made in our code while applying SE principles such as DRY, KISS, Encapsulation, Top Down Thinking

## Database (Encapsulation of Data)
- There is extensive use of database interface functions `database.py`, so that the API functions are not interacting with the database directly with `open()`
- We have been updating the database to suit the needs of the backend to optimise its use, throughout the project duration, and only minor changes to keys and naming were needed in this iteration.
- Some problems in this area is that we are returning whole dictionaries or lists in some of the database functions, which will poorly translate to API functions when changes are made to the database
  - Creating functions to access each of the elements proved to increases clutter in our code and also had this problem, so we did not change this

## Permissions
- To reduce clutter when checking for Slackr permissions, we apply DRY and KISS so that `if` statements are short and sweet
  - With the help of python functions and operators

```python
  # Before
  if user["permission"] == OWNER or
      user["permission"] == ADMIN:
      # Do something

  # After
  if user["permission"] in [OWNER, ADMIN]:
      # Do something
```
- This change allows the code to be easily changed, e.g. if more permissions are added, we only need to add an element into a list rather than a whole line

## Functionalising
- Functions with very long and complicated parts and nesting are broken down into functions
  - This process also encouraged careful analysis of the parts being made into functions, and weeded out many errors that had gone unnoticed until this stage
  - This was performed on `search.py`, `standup.py`
  - The change here causes the functions to be more easy to read and understand for others who will maintain our code
- Other repetitive tasks such as checking for valid token, valid name, translating time objects/strings/integers etc. were made into modules in `server_files/util` and `server_files/exceptions`
  - This was mainly done during iteration 2 when the API functions were being developed, however we continued to apply this during the refinement and changes in this iteration
  - This change greatly increases the maintainability of the code, since we can make changes that effect all our API modules

## Conditional Statements
- There were many complicated if statements and chaining of conditions in our code. This was broken down to _keep things simple_ and increase readability
  - A additional effect of this is a decrease in bugs, that stem from the complicated use of `and` and `or`
- Some `if` statements were wrapping large portions of a function, with small `else` exceptions. The abundance of this indented block reduces readability
  - This was reduced down to a check to induce the exception, and having a majority of the block outside the if statement
  - Some places where this is not changed is when the spec specifies "error when none of the following are true" where this type of structure is necessary
  - Notable changes: many functions in `channel.py`, `channels.py`, `message.py`

## Collecting error messages
- Due to the abundances of Exceptions the backend raises, and the general disconnect between messages, we refactored the structure of error messages by placing them in a module, `server_files/exceptions`
  - This act helps commonly used error messages to have consistent messages, and also for all messages to be easily changed and maintained
    - Since all messages are in one file, and no searches across multiple files are required to change the contents of one message
  - The change in messages were applied to all files in `server_files/api` where all error messages were replaced with global variables containing the message
