mkdir ~/Desktop/CC
cd `dirname $0`
cd CC4Wifi
python CC4Wifi.py ~/Desktop/CC/
osascript -e 'tell application "Terminal" to quit'
