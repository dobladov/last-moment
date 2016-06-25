# Last Moment

Plugin for [Totem](https://wiki.gnome.org/Apps/Videos) that saves the last time position of your videos 

## Install

Clone the repository on `/home/username/.local/share/totem/plugins`

	cd ~/.local/share/totem/plugins
    git clone https://github.com/dobladov/last-moment.git

Or download the [files](https://github.com/dobladov/last-moment/archive/master.zip) and copy the folder inside `/home/username/.local/share/totem/plugins`

Enable the plugin on Edit --> Preferences --> Plugins

![Plugins](https://my.mixtape.moe/wrwpsy.png)

## How it works

Any time you open a video a small file tracks the progress with the inode number, so you can change the name, or directory of the file and this plugin still can track the progress.

Just play a previously opened video and it will continue where it was. 

The program deletes the track of files older than 30 days.

## Documentation

+ [Totem Reference Manual](https://developer.gnome.org/totem/stable/)
+ [Writing Plugins for Totem Movie Player](http://asanka-abeyweera.blogspot.com.es/2012/03/writing-plugins-for-totem-movie-player.html)
+ Based on this awesome plugin by [Yauhen-l](https://github.com/yauhen-l) [remember-last-position-totem-plugin
](https://github.com/yauhen-l/remember-last-position-totem-plugin)

---

![Remember](https://my.mixtape.moe/leoqnh.gif)
