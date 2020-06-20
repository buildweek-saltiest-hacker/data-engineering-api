# Saltiest Hacker API


### Primary API URL
- https://saltiest-hacker-json.herokuapp.com/

### Endpoints:
- /comment-by-id/<comment_id>
    - json object
        - comment: string
        - saltiness: string
```
https://saltiest-hacker-json.herokuapp.com/comment-by-id/256

{"comment":"That seems like a pretty easy fix.  Just ensure that you have a 
.something somewhere in the address, before the first slash.",
"saltiness":"-8442"}
```
- /comments-by-author/<author>
    - json object
        - comments: list of strings (max number of strings?)

- /score-by-author/<author>
    - json object
        - hacker_score: string (-10000, 10000) higher == more salty, zero == neutral
