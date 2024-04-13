# App Structure Outline

## Client: HTML, CSS, JavaScript

## Server: Flask
Non-communication functionality:
- Generate plant image
- Grow plant
- Water plant
- Sunlight plant
- Add user task (for client)
- Delete user task
- Add task template (for db)
- Delete task template

## Database: MongoDB Atlas
- Can store potentially everything!
- Mongodb has collections, can have multiple collections in a database: EX: 
    - Collection for plants
        - this could make viewing all the plants easier so we don't have to iterate through users
        - might be easier for the community garden
    - Collection for Users 


## Data
- Garden
    - Users: User[]

- User
    - Username: str
    - Password: str
    - Plant: Plant
    - Tasks: Task[]

- Plant
    - Growth Stage: int
    - Sunlight: int
        - based on daily login
    - Water: int
        - based on good deeds
    - Image: str (url)
    - Aesthetic description

- Task
    - Description: str

## Functionality
- User Registration
- User Authentication
- Create Plant
    - define plant aesthetics
- Water Plant (homepage button)
    - Water gained through "good deeds"
- Sunlight (homepage button)
    - Sunlight gained through app interaction
- Grow Plant (event)
    - Once threshold is reached, increment growth stage
    - Growth stage determines plant image
- View Garden (separate tab/page)
- View Plant (homepage)

## ChatGPT Output 
### Tier 1: Simple Acts of Kindness
- Compliment someone genuinely.
- Hold the door open for someone.
- Smile at a stranger.
- Leave a positive note for someone to find.
- Send an encouraging text to a friend.
- Share your umbrella with someone during rain.
- Let someone go ahead of you in line.
- Share a book you've enjoyed with a friend.
- Plant a tree or a flower in a community space.
- Pick up litter in your neighborhood.

### Tier 2: Community Engagement
- Volunteer at a local shelter.
- Donate blood.
- Help a neighbor with yard work or groceries.
- Organize a community cleanup day.
- Cook a meal for someone who is ill or a new parent.
- Tutor a student in your area of expertise.
- Volunteer at a local library or community center.
- Create a little free library in your neighborhood.
- Help an elderly neighbor with technology.
- Carpool to reduce carbon emissions.

### Tier 3: Larger Commitments
- Start a community garden.
- Organize a fundraiser for a local cause.
- Adopt a pet from a shelter.
- Foster animals in need.
- Volunteer regularly at a hospital.
- Mentor a young person or a peer.
- Start a recycling program at work or school.
- Organize a charity run or walk.
- Build a habitat for wildlife.
- Volunteer for habitat restoration projects.

### Special Occasions
- Participate in or organize holiday-specific charity drives (e.g., toys for children during the holidays).
- Organize or participate in a meal drive during Thanksgiving.
- Make and distribute care packages for the homeless.
- Volunteer at special olympics or similar events.
- Organize a visit to a nursing home or hospice.

This list should give you a solid foundation for integrating various levels of good deeds into your app. Each tier encourages users to engage at their comfort level, promoting a culture of kindness and active community participation.
