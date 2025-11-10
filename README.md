# MWE Blog Site by Maya Berchin, Ashley Li, Evan Khosh and Robert Chen

### Project 00 Roles:
Project Manager: Maya

Dev1: Ashley

Dev2: Evan

Dev3: Robert

### Description of Blog Site:
Users must register and log in to use the blog site to publish articles, journals, and class notes. Logged in users have access to view other people's written blogs, and have the choice to create their own as well. You can add entries to your blogs and edit past entries written by you. Each user has a profile page and can customize their profiles. EVERYTHING IS PUBLIC!!! DON'T PUT THINGS ON BLOGS YOU DON'T WANT OTHERS TO SEE!!!

### Install Guides:
- Go to the top of the GitHub repo and click on the green "Code" button
- Click on the "SSH" tab and copy the text that is returned
- or copy
```
git@github.com:procrastinAFK/MWE-Wiki.git
```
- Go into your terminal and navigate to where you want this repo to be installed
- Clone the app using
```
 git clone <SSH link>
```
- Enter your password if necessary
- Navigate to the repository by typing
```
cd MWE-Wiki
```
- Create a virtual environment
```
python -m venv .venv
```
- Activate the virtual environment
  - Linux, macOS:
    ```. .venv/bin/activate```
  - Windows:
    ```. .venv\Scripts\activate```
 
(To deactivate when you no longer want to use your virtual environment, just type ```deactivate```)

- Install the required modules using
```
pip install -r requirements.txt
```
- You're done!

### Launch Codes
- Open your terminal and navigate to this repo on your machine.
- Activate your virtual environment if you haven't already (guide above)
- Then cd into the "app" repo:
```
cd app
```
- Run these commands:
```
python data.py
python __init__.py
```
- Go to
```
http://127.0.0.1:5000
```
or whatever link your terminal tells the app is running on on your preferred browser
- Have fun on the website!
