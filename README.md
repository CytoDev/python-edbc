# subreddit desktop wallpaper crawler
sdwc grabs the top 20 posts from /r/earthporn and saves them in the ./output directory.

I made this script because I ocasionally want another desktop wallpaper and grew tired of searching for something I like. This way, the reddit community decides what my wallpaper is and I can spend more time on actually doing my job.

## Usage:
```
 $ python3 sdwc.py
```

## Hacking:
This script can easily be modified to grab posts from other subreddits. See `sdwc.py --help` for more

## Dependencies
##### Default libraries
 - [argparse](https://docs.python.org/3/library/argparse.html)
 - [json](https://docs.python.org/3/library/json.html)
 - [os](https://docs.python.org/3/library/os.html)
 - [sys](https://docs.python.org/3/library/sys.html)
 - [urllib.error](https://docs.python.org/3/library/urllib.error.html)

##### Third party libraries
 - [requests](https://pypi.org/project/requests/)
 - [wget](https://pypi.org/project/wget/)

## Changelog:
The changelog for this project can be found [here](CHANGELOG.md).

## License:
This project is licensed under the MIT License. You can find a copy of the license [here](LICENSE.md).

## Contributions:
You are more than welcome to submit issues as well as feature requests or just a 'how-ya-doin' in the [issue tracker](https://github.com/CytoDev/python-sdwc/issues/new). Contributing to the project can be done by forking it and submitting a pull request once it's all tested and tidy.
