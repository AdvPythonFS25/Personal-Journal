# Unit Testing in the Journal Project

## Function Tested
`count_entries_with_keyword(entries, keyword)` - Counts how many entries contain a specific keyword.

## Why 
- The keyword could be the wrong type.
- Keyword case might cause false negatives.
- Entries might contain edge cases.

## Test Cases Implemented
Basic Match - Checks if the function finds keyword matches.

Case Insensitivity - Confirms matching works regardless of case.

No Match - Tests behavior when there are no matches.

Invalid Input - Verifies ValueError is raised for non string input.

## Future Improvements
Use entry.title or entry.content if entries have fields like title or content.
