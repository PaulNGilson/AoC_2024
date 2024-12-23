# Advent of Code 2024

My attempt at the 25*2 challenges from the [2024 Advent of
Code](https://adventofcode.com/2024) challenge.

I'd like to continue where I left off last year, so here are essentially the same
aims I had last time:

* No help from friends/colleagues/Reddit/etc. - I need to work out a solution on
  my own to all the challenges.
* I can do any _non-Advent of Code_ research I like, from looking up potential
  algorithms, studying bits of mathematics, snippets from Stack Overflow, etc.
* No AI.
* Final solutions should run in sub-15s and I'll rework where I can to make that
  happen, but accept it probably won't be possible for all 25 days.

| Days | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
| Stars | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: |
| Time | 61 | 73 | 57 | 75 | 80 | 1920 | 2815 | 42 | 2106 | 51 | 294 | 1988 | 1241 |

| Days | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
|-|-|-|-|-|-|-|-|-|-|-|-|-|
| Stars | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: |  |  |  |
| Time | 769 | 142 | 304 | 53 | 774 | 480 | 2133 | 49 | 3883 |  |  |  |

:star: means just the first star, :star2: means both stars, and :custard: (just
because "custard" showed up while searching for emojis with "star" in the name)
means no stars and the day is in the past. I suspect I'll be very behind the
daily-rate, as the days get busier through December...

Times to run are just one example run, in milliseconds (unless specified
otherwise).

## Updates

While completing the challenges, I was trying to keep performance to a "good"
level - not just sub-15s, but as optimal as I could manage, on my own. Notes on
this are below:

* Day 19: my initial solution started at 5.5s - good but the slowest for the
  year so far. New idea upon new idea, for once, just kept improving the time
  which felt unusual for me - next was 3.5s, then 813ms, then finally 480ms.
  I've put all three (I never kept one of the intermediate ones) significantly
  different implementations in the repo.
