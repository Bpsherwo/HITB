# HITB

## Welcome

- Hello! This repository is for the **H**alo **I**nfinite **T**eam **B**alancer tool. If you are a Host for Competitive Custom Games in Halo Infinite, this tool will massively help avoid matches that are landslide victories due to too many good players (and/or too many bad players) being on one team. Even for playtests, matches are more fun when they are fair.

## Why should I use this?

- In Custom Games lobbies that play minigames or party modes, this is not necessary (unless it is?). But if you are a host/organizer that runs Competitive Custom Games or Competitive Tournaments with no pre-set or pre-organized teams, this tool is perfect. Whether you are playing, watching, or commentating, doing so with ideally balanced teams is more fun and enjoyable for everyone involved.

## How do I download this?

- Scroll up and look for the green 'Code' button, and click "Download ZIP". Once it is done downloading, extract the files wherever you want, and you are good to go. You do not need to have Python installed or use any pip commands to get this running. Just download and go.

## How do I use this?

- Easy. Follow the steps in ["How do I download this?"](https://github.com/Bpsherwo/HITB#how-do-i-download-this), run the HITB.exe (if you are prompted with a Windows Security alert, click "More Info" -> "Run anyway"), enter in the Gamertags of the participants in the left column, enter each players' CSR rating in the corresponding right column, and click Generate Teams. The program will find the most ideal balanced team combination it can find, and print the teams at the bottom of the window along with the average CSR of each team. Tell the players to divide themselves (or if you can, do it manually) into their teams, and go. [Here is a video demonstration.](https://www.youtube.com/watch?v=Ip0-3L2hEtw)

## How do I know this executable is safe to run on my computer?

- The code is 100% open source and readable on this repository. Everything you see in the 'src' folder is the entire program from top to bottom.
- To be even more transparent, the executable is simply the 'balancer.py' script run through pyinstaller via the following CLI prompt:

*pyinstaller --onefile -w --add-data "src;src" --icon=C:\HITB_v1.0\HITB\src\observerteamico.ico src\HITB.py*

## How do I contribute?

- Feel free to make a fork and do whatever you wish. You do not need to credit me, but I do suggest crediting **[Taucari](https://github.com/Taucari)** unless you make substantial/tranformative changes to how the team balancing is computed.

## I have an issue with the program.

- Please submit a bug report to this Github Repo's [Issues](https://github.com/Bpsherwo/HITB/issues) page, and be sure to use the proper label corresponding to the issue you are having.

## I have a suggestion for a feature and/or functionality to this tool.

- Please submit a suggestion to this Github Repo's [Issue](https://github.com/Bpsherwo/HITB/issues) page, but be sure to use the proper label such as "Enhancement".

### Notes

- Trying to generate teams with any less or more than 8 players is not officially support at this time, but you may well try. Don't take the output as gospel.
- All gamertags **MUST** be unique. This should not be a problem with how Xbox Gamertags work, but it is worth mentioning.
- I suggest creating a Shortcut to HITB.exe in the src folder, and putting that Shortcut on your Desktop or wherever you want to be able to run HITB from. If you move the .exe out of the src folder, it will complain (and probably not run)!
- Do not delete k.py. k.py is what the .exe reads to see what color theme you were last using so it will reopen to the same theme you were using when you closed it. If k.py is deleted or invalidated, make a file named k.py in the src folder and copy/paste this into the k.py file:
```
page_color = '#313338'
text_color = '#FFFCF9'
button_color = '#404249'
field_color = '#3C3D42'
```
- If for some reason you need to contact me for something related to this program, reach me at **bsherwood1183@hotmail.com** and put "HITB" somewhere in the subject line.

### Credits

- This program is a revised version of **[Taucari](https://github.com/Taucari)**'s ELO Team Balancer, reworking all of the scripts to be in a single script, made specifically for Halo Infinite, and with a GUI for ease of use. (The original code is a CLI script.)
- The math and logic for this program is written entirely by **[Taucari](https://github.com/Taucari)**'s ELO Team Balancer found here: **[nTeamEloBalancer](https://github.com/Taucari/nTeamEloBalancer)**
- The GUI for this program is written entirely by **[me](https://github.com/Bpsherwo)**.
