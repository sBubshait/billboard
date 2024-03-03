# Database

The database is up and running. You can access the PHPMyAdmin at:

```
https://db.c4s.lol
```

The actual database:
```
https://db.c4s.lol:3306
username: root
```

# Schema

## Users
- id: Int
- bluetooth_code: String
- device_name: String
- created_at: DateTime

## billboards
This is for the billboard locations.

- billboardId: Int
- description: String
- latitude: Float
- longitude: Float
- created_at: DateTime

## ads
These are the actual ads.

- adId: Int
- adType: Int (1: Image, 2: Video)
- url: String
- bid: Int
- genre: Int


## Current Genres
- 1: Food
- 2: Clothing
- 3: Electronics
- 4: Entertainment
- 5: Health
- 6: Beauty
- 7: Automotive
- 8: Home
- 9: Other