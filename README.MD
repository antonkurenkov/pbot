# True AI bot for blowing up website visitor metrics stats. 
### Rebellion comes, you meatfools!

![](.github/.README_images/google0.png)

Disclaimer: I'm not completely sure if this project does not violate any kind of rules, agreements or etc, and i would be really sorry for that because I did not meant in any way to disrespect anyone or have a wish to make unfair money on this stuff. It is been released just for fun and never been threated seriously. Usage of this shitcode for free or for money is on your own conscience and risk:)

This bot works together with my other project https://github.com/antonkurenkov/qr-coder (flask app for generating payment qr-codes on bank account requisites, i ran it for about a month on vps, collecting statistics and now it is archived). 

I start describing the system from the highest level going deeper to the core so you could understand it easier, 

There we have a systemd daemon config which infinitely reboots sh wrapper over the docker daemon with some schedule (which is hardcoded just to be sure it will rerun the scenario despite everything). Just add the config where it should be. 

Sh wraps docker daemon, rebuilds an image with random delays from half an hour to about two hours and wipes all docker cached data, layers, containers and etc then. It also spawns 5 containers with AI bots acting at the same time. If there are no containers (they have been overflowed with memory-greedy chrome-zombie processes, and banhammered by docker daemon then), the loop continues, the data wipes and the image rebuilds again. If your eyes are bleeding of that architectural soution, i say sorry, i've never cicded large highload enterprise projects, so that kind of knowledge was enough. Open PR and let's make it better haha

Inside each image there is a python bot build on Selenium which simulates human behaviour on a website. It generates fake names, surnames, and fills other fake bank data in a form, solves object-on-image detection hcaptcha and sometimes clicks on advertisement banner (that money, another metric i investigated, but i've never withdrawed a copper (haha because did not ever had enough for min payout:). 

There is also some lines to be said about what is the bot "personality" made of: The bot acts with random delays, personal random speed coeff for typing the data, scrolling the screen, and clicking the buttons on a page. The bot vitits the target website using free global proxies which are mined and tested asincronously. The true AI behaviour could be imagined as the tree, where nodes have their weights as coefficients of probability of following to the some next node representing the next action in default standard website visitor scenario. If the enter function "does not happen" on some node, the visitor stops, and the process sleeps for a random time (~1m-1h) thus we add moaar random to the bot. After each sleep session the bot creates new entity with all personality attributes (including also random device size dimentions, random useragent and  ok well enough random other related headers). 

Finally after about a month running this vicious golem on GCP cloud free trial I collected this statistics on Yandex and Google. It was funny (the feeling seems to be like the one you have raising plants on your country land) and i know what is "robocity" (or any kind of eng word for a metric describing real-person-looking-like behaviour), it was the target metric which could in some kind of way describe "efficiency" of all that randomizing. Unfortunately I did not find any relations and correlations between using different behavioral strategies and in/excluding some behavioral parameters. I also have no idea how this metric been calculated by yandex. Probably I didn't have enough resources to process more cases, feed a model with results and reverse-resolve the algorithm and what lies behind this percentage. Anyway, I've just got bored. 

![](.github/.README_images/yandex0.png)

***

Thanks for nothing! [33nXLAPXt3vQPbKjJhfdt7bmDfm7sbw9ih]:

