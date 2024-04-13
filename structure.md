# App Structure Outline

## Client: HTML, CSS, JavaScript

## Server: Flask
Non-communication functionality:
- `generate_plant_image(Plant p)`
- `grow_plant(Plant p)`
- `water_plant(Plant p)`
- `sunlight_plant(Plant p)`

## Database: MongoDB Atlas

## Data
- User
    - Username: str
    - Password: str
    - Plant: Plant

- Plant
    - Growth Stage: int
    - Sunlight: int
    - Water: int
    - Image: str (url)
    - Aesthetic description

- Garden
    - Plants: Plant[]

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
