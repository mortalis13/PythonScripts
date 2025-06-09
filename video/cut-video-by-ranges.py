import subprocess
import os

def calculate_duration(start_time: str, end_time: str) -> str:
  """
  Calculates the duration between two time points.

  Args:
    start_time: Start time in 'HH:MM:SS' format.
    end_time: End time in 'HH:MM:SS' format.

  Returns:
    Duration in 'HH:MM:SS' format.
  """
  start_parts = list(map(int, start_time.split(':')))
  end_parts = list(map(int, end_time.split(':')))
  start_seconds = start_parts[0] * 3600 + start_parts[1] * 60 + start_parts[2]
  end_seconds = end_parts[0] * 3600 + end_parts[1] * 60 + end_parts[2]
  duration_seconds = end_seconds - start_seconds
  hours = duration_seconds // 3600
  minutes = (duration_seconds % 3600) // 60
  seconds = duration_seconds % 60
  return f'{hours:02}:{minutes:02}:{seconds:02}'


def add_durations(duration1: str, duration2: str) -> str:
  """
  Adds two durations given in 'HH:MM:SS' format.

  Args:
    duration1: First duration in 'HH:MM:SS' format.
    duration2: Second duration in 'HH:MM:SS' format.

  Returns:
    The sum of the two durations in 'HH:MM:SS' format.
  """
  parts1 = list(map(int, duration1.split(':')))
  parts2 = list(map(int, duration2.split(':')))
  total_seconds = (parts1[0] * 3600 + parts1[1] * 60 + parts1[2]) + (parts2[0] * 3600 + parts2[1] * 60 + parts2[2])
  hours = total_seconds // 3600
  minutes = (total_seconds % 3600) // 60
  seconds = total_seconds % 60
  return f'{hours:02}:{minutes:02}:{seconds:02}'


def log_chunks_adjusted_times(time_ranges):
  current_position = '00:00:00'
  for idx, (start_time, end_time) in enumerate(time_ranges):
    duration = calculate_duration(start_time, end_time)
    current_position = add_durations(current_position, duration)
    print(f'Chunk {idx + 1} ends at {current_position}')


def log_time_between_chunks(time_ranges: list[tuple[str, str]]) -> None:
  print()
  print(f'Gap 0: {time_ranges[0][0]}')
  for idx in range(len(time_ranges) - 1):
    end_time_current = time_ranges[idx][1]
    start_time_next = time_ranges[idx + 1][0]
    gap = calculate_duration(end_time_current, start_time_next)
    print(f'Gap {idx + 1}: {gap}')
  

def cut_video(input_file: str, time_ranges: list[tuple[str, str]], output_prefix: str) -> list[str]:
  """
  Cuts a video into chunks based on the provided time ranges.

  Args:
    input_file: Path to the input video file.
    time_ranges: List of tuples containing start and end times in 'HH:MM:SS' format.
    output_prefix: Prefix for the output chunk file names.

  Returns:
    List of output chunk file names.
  """
  
  if not os.path.exists('temp'):
    os.makedirs('temp')
  
  chunk_files = []
  for idx, (start_time, end_time) in enumerate(time_ranges):
    print(f'Processing chunk {idx + 1}/{len(time_ranges)}: {start_time} to {end_time}')
    duration = calculate_duration(start_time, end_time)
    output_file = f'{output_prefix}-{idx + 1}.mp4'
    
    command = ['ffmpeg', '-y', '-hide_banner', '-ss', start_time, '-t', duration, '-i', input_file, '-map', '0', '-c', 'copy', f'temp/{output_file}']
    subprocess.run(command, check=True)
    
    print(f'Chunk {idx + 1} saved as "{output_file}"')
    chunk_files.append(output_file)
  
  print('All chunks processed successfully.')
  return chunk_files


def merge_chunks(chunk_files: list[str], output_file: str, time_ranges: list[tuple[str, str]]) -> None:
  """
  Merges video chunks into a single video file.

  Args:
    chunk_files: List of chunk file names to merge.
    output_file: Path to the output merged video file.

  Returns:
    None
  """
  print('Merging chunks into final output...')
  list_file = 'temp/mylist.txt'
  with open(list_file, 'w') as f:
    for chunk in chunk_files:
      f.write(f"file '{chunk}'\n")
  
  command = ['ffmpeg', '-y', '-hide_banner', '-f', 'concat', '-i', list_file, '-map', '0', '-c:v', 'libx264', '-crf', '18', '-c:a', 'copy', output_file]
  subprocess.run(command, check=True)
  
  print(f'Final output saved as "{output_file}"')


# ----------------

prefix = 'output'

data = {
  'input': 'input.mp4',
  'output': 'output.mp4',
  'ranges': '''
  00:00:11:01 00:11:04:09
  00:18:05:02 00:37:00:00
  00:43:45:05 00:58:03:00
  '''
}

time_ranges = [tuple(line.split()) for line in data['ranges'].strip().split('\n')]
time_ranges = [(range[0][:8], range[1][:8]) for range in time_ranges]

chunks = cut_video(data['input'], time_ranges, prefix)
merge_chunks(chunks, data['output'], time_ranges)

log_chunks_adjusted_times(time_ranges)
log_time_between_chunks(time_ranges)
