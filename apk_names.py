# Gets app names and package names from .apk files in a folder
# using aapt tool from Android SDK build tools

import os
import subprocess
from dataclasses import dataclass

os.environ['PATH'] = '/android-sdk/build-tools/35.0.0'


@dataclass
class ApkInfo:
  app_name: str
  package_name: str


def get_apk_data(apk_path: str) -> ApkInfo | None:
  try:
    result = subprocess.run(['aapt', 'dump', 'badging', apk_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8')
    if result.returncode != 0:
      raise Exception(f'aapt error: ```{result.stderr}```')
    
    app_name = None
    package_name = None
    
    for line in result.stdout.splitlines():
      if line.startswith('application-label:'):
        app_name = line.split(':', 1)[1].strip().strip("'")
      
      if line.startswith('package:'):
        package_name = line.split(' ')[1].split('=')[1].strip().strip("'")
    
    if app_name and package_name:
      return ApkInfo(app_name=app_name, package_name=package_name)
    
    raise Exception('App name or package name not found in APK')
  except Exception as e:
    print(f'Error: {e}')
    return None


def main(folder_path: str) -> None:
  data = {}
  for file_name in os.listdir(folder_path):
    if file_name.endswith('.apk'):
      print(f'{file_name}...')
      
      apk_path = os.path.join(os.path.normpath(folder_path), file_name)
      apk_info = get_apk_data(apk_path)
  
      if apk_info:
        data[file_name] = apk_info
  print()
  
  for file_name, apk_info in data.items():
    print(f'{apk_info.app_name} :: [{apk_info.package_name}] => ({file_name})')


folder_path = '/apk-files'
main(folder_path)
