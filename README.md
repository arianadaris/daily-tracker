<h5 align="center">Python / Notion API / Tkinter / chron</h5>
<h1 align="center">Daily Tracker<br>
</h1>

![Screenshot 2023-05-12 at 3 40 34 PM](https://github.com/arianadaris/daily-tracker/assets/73635827/2c638bce-2b03-4af5-a580-6c51ac1cf07f)

<h3>A Python script that helps me keep track of daily habits and sleep schedules.</h3>

<h4>Overview</h4>
<p>I use a database in Notion to keep track of my sleep schedule, my habits and my gym routines. However, adding to this database daily is a slow process simply due to how many entries are shown on Notion's interface. Additionally, a few fields could be automated to make it easier to log habits. Therefore, I created the above Python scripts.</p>

<ul>
  <li> Interface.py - A visual interface built with Tkinter that allows me to enter daily habits without loading extra information from the database</li>
  <li> Daily.py - A script that creates a new entry in the Notion database daily using Notion API and chron (MacOS)</li>
  <li> Update.py - The helper script that interacts with NotionAPI to get data from the database and update the current day's entry</li>
</ul>
