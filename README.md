# 🗨️ WeChat

## A Proof of Concept for a Hackathon Fabricate23 conducted by [Christ University](https://christuniversity.in/)

What is WeChat? WeChat is web application developed over two days for a hackathon. Why WeChat? Social Media Apps have evolved over the years perfecting their algorithms to retain their users which has resulted in them getting addicted to it. When alcohol was banned in US in the [1920s](https://en.wikipedia.org/wiki/Prohibition_in_the_United_States), it had resulted in widespread unregulated use of alcohol over the country which ultimately resulted in government legalising alcohol again as alcohol would be much more regulated under the law. As is the case with screentime, haphazard when not being monitored. WeChat tries to implement a system of [stamina](https://genshin-impact.fandom.com/wiki/Original_Resin) most commonly used in video games to regulate the screentime of users. WeChat believes a healthy amount of screentime would be around thirty minutes a day, hence it has embraced a system that doesn't permit screentime of more than thirty minutes per day.

## Shards in WeChat

What is a Shard? As discussed in previous section, we try to embrace a stamina system most commonly used in video games. These Shards will allow poeple to buy screentime. How might you earn these Shards? You can earn Shards by logging out, Yes that's it, There are no other monetary options. The more time you spend in the real world, you get more screentime. Is there a cap to Shards? Yes, There's a barrier on how much of these Shards you can earn, it's 1440 Shards. What's the conversion rate?

- 1 minute spent in the real world earns you upto 1 shard.
- It costs 48 Shards to spend a minute on WeChat.
- Spending a day in the real world would buy you 30 minutes on WeChat.
- 30 minutes on WeChat costs you 1440 Shards.

## Getting started with Installations and Starting up WeChat

The backend of this web application is served by [flask](https://www.python.org/downloads/), it's frontend is handled by js and for databases, I've used [XAMPP](https://www.apachefriends.org/) and [phpmyadmin](http://localhost/phpmyadmin/). You can get started by installing the above requirements.

- Startup your terminal.
- Install the virtualenv module to create virtual environment for our web app.
```
pip install virtualenv
```
- Create a virtual environment in the terminal.
```
python -m virtualenv wechat
```
- Clone the  following requirements [requirements.txt](/requirement.txt), [main.py](/main.py), [static](/static), [templates](/templates) and [database](/wechat.sql) from my repo.
- Install additional requirements from the terminal.
```
pip install -r.\requirements.txt
```

Now that we're done with the installation part, we're only left with importing the database to your local computer and starting up the website. To import the database, first open your XAMPP and startup Apache and MySQL. Open your phpmyadmin and import the [database](/wechat.sql). Now, that we have everything ready for our website the only thing left is to run the [main.py](/main.py) file in the IDE of your choice. Visit WeChat on your [localhost](http://127.0.0.1:5000/).
