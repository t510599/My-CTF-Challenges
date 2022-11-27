# yeeclass
- Tags: `Web`
- Score: 215/500
- Solves: 52

## Description
Due to the security concerns, we are going to phase out the old LMS system.  
We have developed a new E-learning system called "yeeclass", please give it a try!

## Overview
[`uniqid()`](https://www.php.net/manual/en/function.uniqid.php) is based on timestamp, so one can recover the id when timestamp is provided.

## Solution
See [exploit/brute.py](exploit/brute.py)

First, the access control of submission list is broken.  
If the user does not login, its `userclass` in session would be NULL, which can bypass `userclass <= PERM_TA (0)`. By visiting `submission.php?homeworkid=1` without login, one can retrieve the timestamp of flag submission.  

With the knowledge of how `uniqid()` works ([php/php-src: ext/standard/uniqid.c](https://github.com/php/php-src/blob/master/ext/standard/uniqid.c)), we can transform the date string into timestamp, and derive the id from it.

Next, the timestamp of the submission is recorded by database with `CURRENT_TIMESTAMP(6)`, which is a little bit later than the id creation timestamp. One can observe this by comparing the id printed out while initialization and the timestamp stored in the database.  
The expected bruteforce range is less than 1000, since the delay between submission and insertion should be short.

In addition, if `datetime` module in python is used to convert the date string to timestamp, you need to check the timezone when conversion. Since UTC timezone is used in container by default, you have to add `.replace(tzinfo=UTC)` after calling `strptime()` or `fromisoformat()`.