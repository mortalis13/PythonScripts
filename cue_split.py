import argparse
import datetime
import enum
import math
import os.path
import shlex
import shutil
import subprocess
import sys
import tempfile

import pprint

# -- Working edited version
# $ python cue-split.py [OPTIONS] "file.cue"
# -d -f
# (target dir, format)


class Context(enum.Enum):
  ALBUM = 0
  TRACK = 1

# -- Utils

def normalize_filename(val):
  remove_symbols = [':', '\"', '?', '*', '¿', '¡']
  dash_symbols = ['<', '>', '/', '\\', '|']
  
  for sym in remove_symbols:
    val = val.replace(sym, '')
  for sym in dash_symbols:
    val = val.replace(sym, '-')
    
  return val
  
  

def parse_cue_context(lines, context=Context.ALBUM, **defaults):
  result = {'genre': None, 'date': None, 'input_file': None, 'title': None, 'performer': None}
  if context == Context.ALBUM:
    result['tracks'] = []
  result.update(defaults)

  while lines:
    line = lines.pop(0)
    if line.startswith('REM GENRE '):
      result['genre'] = shlex.split(line[10:])[0]
    elif line.startswith('REM DATE '):
      result['date'] = shlex.split(line[9:])[0]
    elif line.startswith('PERFORMER '):
      result['performer'] = shlex.split(line[10:])[0]
    elif line.startswith('TITLE '):
      result['title'] = shlex.split(line[6:])[0]
    elif line.startswith('FILE '):
      result['input_file'] = shlex.split(line[5:])[0]
    elif line.startswith('POSTGAP '):
      result['postgap'] = parse_time(shlex.split(line[8:])[0])
    elif line.startswith('PREGAP '):
      result['pregap'] = parse_time(shlex.split(line[7:])[0])
    elif line.startswith('INDEX '):
      result['index_type'], result['start_time'] = shlex.split(line[6:])
      result['index_type'] = int(result['index_type'])
      result['start_time'] = parse_time(result['start_time'])
    elif line.startswith('  TRACK '):
      track_number, track_type = shlex.split(line[8:])
      if track_type == 'AUDIO':
        track_lines = []
        while lines:
          if not lines[0].startswith('  ') or lines[0].startswith('TRACK') or lines[0].startswith('  TRACK'):
            break
          track_lines.append(lines.pop(0)[4:])
        result['tracks'].append(parse_cue_context(track_lines, context=Context.TRACK, genre=result['genre'], date=result['date'], performer=result.get('performer', 'Unknown Artist'), title='Unknown Track', input_file=result['input_file']))
  return result


def parse_time(time):
  minutes, seconds, frames = tuple(map(int, time.split(':')))
  return datetime.timedelta(minutes=minutes, seconds=seconds, milliseconds=frames / 75 * 1000)


def split_cue(cue_data, no_gap):
  filename = None
  start_time = datetime.timedelta()
  end_time = None
  tracks = cue_data['tracks']
  for i in range(len(tracks)):
    is_first_track = i == 0
    is_last_track = i == (len(tracks) - 1)
    track = tracks[i]
    start_time = track['start_time']
    if not is_first_track:
      tracks[i - 1]['end_time'] = start_time
      if track['input_file'] != filename:
        tracks[i - 1]['end_time'] = None
    if is_last_track:
      track['end_time'] = None
    filename = track['input_file']

  track_number = 1
  output_track = {'track_number': track_number}
  for track in tracks:
    if track['index_type'] == 0 and not no_gap:
      output_track.setdefault('start_time', track['start_time'])
    elif track['index_type'] >= 1:
      for k, v in track.items():
        output_track.setdefault(k, v)
      yield output_track
      track_number += 1
      output_track = {'track_number': track_number}


def extract_track_ffmpeg(source_format, track_data, total_tracks, source_dir, target_dir, no_gap, dry_run):
  ext = '.' + source_format
  input_file = source_dir + '/' + track_data['input_file']
  
  add_params = []
  if source_format == 'ape':
    ext = '.mp3'
    add_params = ['-c:a', 'libmp3lame', '-b:a', '320k']
  
  # output_file = '{:02d} - {} - {}{}'.format(track_data['track_number'], track_data['performer'], track_data['title'], ext)
  output_file = '{:02d} - {}{}'.format(track_data['track_number'], track_data['title'], ext)
  output_file = normalize_filename(output_file)
  output_file = target_dir + '/' + output_file
  
  if os.path.exists(output_file):
    print('File exists:', output_file)
    return
  
  from_time = str(track_data['start_time'].total_seconds())
  
  cmd = ['ffmpeg', '-hide_banner', '-y', '-i', input_file]
  cmd.extend(['-ss', from_time])
  if track_data['end_time'] is not None:
    to_time = str(track_data['end_time'].total_seconds())
    cmd.extend(['-to', to_time])
  cmd.extend(add_params)
  cmd.append(output_file)
  print('== cmd: "' + ' '.join(cmd) + '"\n')
  
  # return
  if not dry_run:
    proc = subprocess.Popen(cmd)
    stdout, stderr = proc.communicate()
    if proc.returncode:
      raise RuntimeError(stderr)
  else:
    print(' '.join(map(shlex.quote, cmd)))


def extract_track_avconv(source_format, track_data, total_tracks, source_dir, target_dir, no_gap, dry_run):
  ext = '.' + source_format
  input_file = source_dir + '/' + track_data['input_file'] + ext
  
  output_file = '{:02d} - {} - {}{}'.format(track_data['track_number'], track_data['performer'], track_data['title'], ext)
  output_file = normalize_filename(output_file)
  output_file = target_dir + '/' + output_file
  
  from_time = str(track_data['start_time'].total_seconds())
  
  cmd = ['avconv', '-i', input_file]
  cmd.extend(['-c:a', 'copy',])
  
  cmd.extend(['-ss', from_time])
  if track_data['end_time'] is not None:
    duration = track_data['end_time'] - track_data['start_time']
    cmd.extend(['-t', str(duration.total_seconds())])
  
  cmd.append(output_file)
  
  # return
  if not dry_run:
    proc = subprocess.Popen(cmd)
    stdout, stderr = proc.communicate()
    if proc.returncode:
      raise RuntimeError(stderr)
  else:
    print(' '.join(map(shlex.quote, cmd)))


def main(argv=None):
  if argv is None:
    argv = sys.argv[1:]

  parser = argparse.ArgumentParser()
  parser.add_argument('cuefile')
  parser.add_argument('-G, --no-gap', default=False, action='store_true', help='Ignore audio gaps', dest='no_gap')
  parser.add_argument('-E, --encoding', default='UTF8', help='The text encoding of the CUE file', dest='encoding')
  parser.add_argument('--dry-run', default=False, action='store_true', dest='dry_run')
  parser.add_argument('-t', default=[], action='append', dest='track_numbers')
  parser.add_argument('-d', default='', action='append', dest='target_dir')
  # parser.add_argument('-f', default='flac', action='append', dest='source_format')
  parser.add_argument('-f', default='flac', dest='source_format')
  args = parser.parse_args(argv)
  
  source_dir = os.path.dirname(args.cuefile)
  if not args.target_dir:
    args.target_dir = source_dir
  
  with open(args.cuefile, encoding=args.encoding) as cuefile:
    cue = parse_cue_context(list(cuefile))
  
  tracks = list(split_cue(cue, args.no_gap))
  total_tracks = len(tracks)
  track_numbers = list(map(int, args.track_numbers))
  
  for track in tracks:
    if track_numbers and track['track_number'] not in track_numbers:
      continue
    
    extract_track_ffmpeg(args.source_format, track, total_tracks, source_dir, args.target_dir, args.no_gap, args.dry_run)
    # extract_track_avconv(args.source_format, track, total_tracks, source_dir, args.target_dir, args.no_gap, args.dry_run)


if __name__ == '__main__':
  main()
