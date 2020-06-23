# Saltiest Hacker API

## Primary URL
- `https://saltiest-hacker-json.herokuapp.com/`

### API Details

#### `/`
- API home page
    - Project Title
    - Developer Bylines

#### `/docs`
- API Index
    - List of endpoints

#### `/comments-by-author/<author>` :: The three saltiest comments of a given hacker
- id
- comment
- saltiness

#### `/score-by-author/<author>`
- Salty score by author's name
    - score

#### `/comment-by-id/<comment_id>` :: 
- Comment text by id
    - author
    - comment
    - saltiness

#### `/recent`
- List of most recent comments in order from most salty to least.
    - author
    - headline
    - comment
    - saltiness

#### `/sentiment/<text>`
- Live sentiment analysis
    - score
    - text


### ToDo
#### `/top-hackers/<optional number>`
- List of the top saltiest hackers of all time. Three by default.
    - rank
    - name
    - score

#### `/random-comment`
- Random hacker comment
    - author
    - comment
    - saltiness

#### `/random-author`
- Random hacker
    - author
    - score
