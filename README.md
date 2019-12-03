# Sportsball Cards by OKzoomers

**Roster/Roles**
- Saad Bhuiyan - `Frontend` (BOOTSTRAP)
  - Handle the frontend
  - Create templates
  - Routing
  - Styling with Bootstrap
- Matthew Chan - `Database Management`
  - Create a package for interacting with the database from backend
  - Continuously modify and update the package along the dev cycle
- Hannah Fried - `Project Manager`
  - Project manager
  - Make changes to repository when necessary
- Jacob Olin - `Backend Development`
  - Handle the backend
  - Handle caching to/from database
  - Search through database
  - send render-able information for Jinja/generally support front-end

**PROJECT PITCH**

Sportsball cards is a platform for:
- Testing your knowledge of your favorite basketball teams, and new ones via trivia quizzes!
- Upon winning said quizzes, winning prize virtual cards!
- Building a collection by card rarity, player stats, and more!
- And once you get that far, trading your cards with your friends!

*Won't you come join your friends and test your knowledge?*

**Nitty-Gritty**

Data retrieved from: [OpenTrivia API](https://docs.google.com/document/d/18dMPylFMGCljqjTa-GZnk-ZDE68HLR9Rvz8rShwlp-4/), [balldontlie API](https://docs.google.com/document/d/1zaKf7H-yUcP3lcyAzFsDjLqgZVdpKYNGoZqIcsZoFV0/edit), and the [NBA Player API](https://docs.google.com/document/d/18BfMVVlyTPref1yHHpnwolscon-3mLV2MCagVRoAWU8/).

THis website should be able to offer users the ability to create accounts and then play trivia games for basketball. The games are run through the trivia API providing things like verification for correct/incorrect answers. The user should be able to win virtual trading cards based on their trivia success, for which the images on the cards come from our images API and the stats come from the basketball API.

Each new quiz generates a new request from the quiz API - then for each new card, the image API and Basketball API provide information to be rendered in a card division within bootstrap.

**LAUNCH CODES**

- Clone the project from [here](https://github.com/IanHF/OKzoomers_bhuiyanS-chanM-friedH-olinJ). No key generation needed.
- Within the OKzoomers_bhuiyanS-chanM-friedH-olinJ directory, run in your terminal `pip install -r doc/requirements.txt`
- Run App.py to run the project.
- Play games! WIn cards! Have fun!
