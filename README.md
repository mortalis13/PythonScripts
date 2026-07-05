A suite of **Python** scripts for various tasks:  
(files/text manipulation, HTTP requests, file downloads, web parsers etc.)

`/modules`  
- `file_system_functions` - Functions for retrieving of lists of filenames, paths, for removing files etc.
- `general_functions` - Functions for regex search, filenames normalization
- `torrent_parser` - Parses torrent files content

`/audio`  
- `audio_fft_calc` - Gets FFT data for an audio file, builds graphs for frequency distribution
- `audio_wave_plot` - Plots a graph for an audio wave in the time domain
- `create_sine_wav` - Writes sine wave data to a wav file
- `cue_split` - Splits FLAC, APE audio files by a CUE-file
- `extract_audio_pcm` - Writes audio data from a .wav file as text
- `fft_manual_calc` - Calculates FFT for an audio using the original algorithm
- `play_wave` - Plays a sine wave using `PyAudio`
- `wav_extractor` - Extracts WAV audio data from a binary file

`/scrapers`  
- `addons_downloader` - Downloader for Firefox addons by direct URLs
- `addons_parser` - Gets Firefox addons direct links from search pages
- `bankia_api` - Shows bank account balance and last operations
- `file_downloader` - Downloads files from a server by direct links
- `fuse_downloader` - Downloader for Fender FUSE presets by direct links
- `metaltabs_downloader` - Downloads tabs from metaltabs.org
- `parse_html` - Walks through HTML elements tree and extracts information
- `proxy_downloader` - Downloads a file through a proxy IP from a list
- `rapidgator_downloader` - Downloads a file from rapidgator.net by file ID
- `tabs_downloader` - Downloader for Guitar Pro tabs from ultimate-guitar.com
- `vimeo_downloader` - Downloads a mp4 video from vimeo.com
- `web_scraper` - Generic web scraper template

`/ai`  
- `copilot_rest` - Github Copilot REST tester

`/rsa` - Example of REST endpoint requiring RSA certificate  
- generate a certificate and key with `gen.py`
- run `server.py`
- test the endpoint with `client.py` or with a REST call to `GET https://localhost:5000/items`

---

`apk_names` - Gets app names from APK files in a folder  
`archive_process` - Scans ZIP files and gets their content  
`auto_sys_proxy` - Sets system proxy from a dynamically retrieved proxies list  
`convert_encoding` - Converts text encoding for all files in a folder  
`copy_files` - Batch copies files with a filter  
`covid_stat_csv` - Shows world statistics on COVID-19 spread  
`cut_video_by_ranges` - Extracts selected chunks from a video and merges them into a new video file  
`dump_directory` - Recursively scans a directory and writes its structure to a text file  
`dump_files` - Generates a flat files list for a directory  
`directory_structure_duplicate` - Makes a duplicate of a folder tree without copying files  
`dsl_find_largest_article` - Searches for a longest article body in a DSL dictionary  
`dsl_get_headwords` - Gets all headwords in a DSL dictionary  
`ftp_list` - Gets a list of files in FTP directories  
`generate_unicode_char_from_ranges` - Writes Unicode chars having a list of code ranges  
`get_java_imports` - Extracts Java imports from a directory  
`gmail_api_remove_unread` - Removes unread messages from a Gmail account using Gmail API  
`gmail_api_send` - Sends an email using Gmail API  
`google_keep_export` - Exports Google Keep notes to a text file  
`google_search` - Downloads a page with Google search results
`merge_files` - Combines multiple files into one  
`multi_rename` - Renames multiple files using a naming map  
`pdf_merge` - Combines multiple PDF or image files  
`pdf_process` - Extracts information from a PDF file  
`process_csv` - Gets info and combines CSV files  
`randomize_album` - Selects a random music album and copies it  
`replace_string_in_files` - Replaces a string in all text files in a folder  
`rss_service` - Retrieves information from a RSS feed and sends an email with the parsed data  
`torrent_parse` - Extracts a torrent file contents to a text file  
`tumblr_api` - Basic usage of Tumblr API  
`win_daily_uptime` - Prints total Windows uptime by day  
`youtube_api` - Gets information from YouTube channels  
