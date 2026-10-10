# Bear Totem Companion: An MTG Commander Tool

## Motivation

This project sprung from my local game store in Spokane (Bear Totem is a great place, you should definitely check it out if you get the chance). I go there most weeks to play Magic: The Gathering, and I noticed the owner always writing out lists of players grouped together to play on paper. After talking with him about his process, particularly about how it seemed pretty tiring to do every week, he agreed that the process was a drag, but he hadn't found a solution to fit some of his house rules. See, Seth is a nice guy and wants all of his players to have fun, but since it's an open event, there's no way of knowing how many people will show up or who will want to play more competitively versus casually. Combine that with having to send some people to the cafe downstairs to play when his main seating area got too full, and I could see why he struggled with a simple randomizer.

So I had a few more conversations with him about it, and I decided to try my hand at making a custom bot in Discord for him to use instead. With his input throughout the development process, I was able to make something that does roughly what he needs it to do, and we're currently in the live testing phase of development to see what needs to be improved upon in the future.

## Current Implementation

Currently, the program functions off a session that splits players into 3 pools (or brackets) of play: one for competitive players, one for people looking for a more casual game, and another one for any themes or events that may be going on. Once a session is started, players can be sorted into any of the 3 brackets, moved between them, removed from the pool, or even grouped together for players that want to be sat with their friends or partners.

After the player pools are filled, the user can use the !startRound command to randomize each bracket into play groups of 3-4 players using the tables available. Once the tables in the main area are full, the remaining groups are filtered downstairs into the cafe. This process follows special rules Seth layed out, such as making sure no player is randomized into a group of 3 or to a table downstairs multiple times over the course of the session.

## Future Plans

While the main functionality of the bot is there, there is still more to do. In the future, I plan to implement a system to autofill some commands that have predictable inputs to reduce the number of possible errors and/or typos made. Seth has also mentioned adding a rule to ensure no player is sat with another person they had played a game with previously that night, so that will be an upcoming feature as well.

### [GitHub Link](https://github.com/MageOf4Names/BearTotemCompanion)