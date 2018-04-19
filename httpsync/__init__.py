#!/usr/bin/env python
import os
import json
import time
import random
import argparse
import requests
from lxml import html
from functools import partial
from urllib.parse import urljoin
from urllib.parse import urlparse
from multiprocessing.dummy import Pool as ThreadPool 


parser = argparse.ArgumentParser(description='HTTP Based Mirroring Tool')
parser.add_argument('--url', '-u', dest="url", help='URL of site to mirror', required=True)
parser.add_argument('--mirrors', '-m', dest="mirrors", help='List of mirrors to attempt the download', nargs='*')
parser.add_argument('--directory', '-d', dest="directory", help='Directory to store files', required=True)
parser.add_argument('--max-depth', '-M', dest="max_depth", help='Maximum depth to traverse', default=10)
parser.add_argument('--delete', dest="delete", action='store_true', help='Delete files no longer in the server',
                    default=False)
parser.add_argument('--verbose', '-v', dest="verbose", action='store_true', help='Verbose output', default=False)
parser.add_argument('--daemon', '-D', dest="daemon", action='store_true', help='Run as a daemon', default=False)
parser.add_argument('--daemon-delay', dest="daemon_delay", help='Seconds of delay between each run', default=120)
parser.add_argument('--version', action='version', version='%(prog)s 1.0')
results = parser.parse_args()
url = results.url
data_dir = results.directory
enable_verbose = results.verbose
pool = ThreadPool(4) 

def info(string):
  print(str(string))


def verbose(string):
  if enable_verbose: print(str(string))


def resolve_links(url, max_depth=4, depth=0):
  if not url.endswith('/'): url+='/'
  if depth >= max_depth:
    raise StopIteration
  page = requests.get(url)
  dom = html.fromstring(page.content)
  for path in dom.xpath('//a/@href'):
    if not '..' in path:
      clean_path = path.lstrip('/')
      full_url = urljoin(url,clean_path)
      verbose('Discovered {}'.format(full_url))
      if full_url.endswith('/'):
        for link in resolve_links(url=full_url, depth=depth+1):
          yield link
      yield full_url


def map_files(links, data_dir):
  '''
  Traverse the list of links and determine which links are files and get basic info
  :param links: list of urls
  :param data_dir: directory to save files to
  :return: 
  '''
  if not data_dir.endswith('/'): data_dir+='/'
  for link in links:
    file_info = {}
    response = requests.head(link)
    if 'content-length' in response.headers:
      file_info['url']      = link
      file_info['size']     = response.headers['content-length']
      file_info['path']     = urlparse(link).path
      file_info['filepath'] = urljoin(data_dir,urlparse(link).path.lstrip('/'))
      file_info['filedir']  = os.path.dirname(
        file_info['filepath']
      )

      if results.mirrors:
        mirrors = results.mirrors
        random.shuffle(mirrors)
        for mirror in mirrors+[link]:
          mirror_link = '{}://{}{}'.format(
            urlparse(mirror).scheme,
            urlparse(mirror).netloc,
            urlparse(link).path
          )
          try:
            mirror_response = requests.head(mirror_link, timeout=10)
            if 'content-length' in mirror_response.headers and mirror_response.headers['content-length'] == file_info['size']:
              file_info['url'] = mirror_link
              break
          except:
            info('Could not reach {}, removing from mirrors from now on'.format(mirror))
            results.mirrors.remove(mirror)
    
      yield file_info


def list_local_paths(data_dir):
  '''
  Find the local files
  :param data_dir: path of the root of local files
  :return: Path to local file
  '''
  for root, subdirs, files in os.walk(data_dir):
    for file in files:
      yield urljoin(root+'/',file)


def download(args):
  '''
  Download a file
  :param url: full url of what to download
  :param dest: where to download the file to
  :return:
  '''
  url, dest = args
  info('Downloading {} to {}'.format(url,dest))
  temppath = dest+'.tmp'
  r = requests.get(url, stream=True)
  with open(temppath, 'wb') as f:
    for chunk in r.iter_content(chunk_size=1024):
      if chunk:
        f.write(chunk)
  os.rename(temppath,dest)


def fetch_files(files):
  '''
  Loop through a list of files and handles whether or not it needs to be fetched
  :param files: list of file info dicts
  '''
  jobs = []
  for file_info in files:
    verbose('Checking {}'.format(file_info['url']))
    if not os.path.isdir(file_info['filedir']):
      verbose('Creating directory {}'.format(file_info['filedir']))
      os.makedirs(file_info['filedir'])
    if os.path.isfile(file_info['filepath']):
      if int(os.path.getsize(file_info['filepath'])) == int(file_info['size']):
        verbose('Skipping {}, it already exists'.format(file_info['filepath']))
      else:
        info('File {} needs to be updated'.format(file_info['filepath']))
        jobs.append([file_info['url'], file_info['filepath']])
    else:
      jobs.append([file_info['url'], file_info['filepath']])
  print(jobs)
  pool.map(download, jobs)
  pool.close()
  pool.join()


def purge_old_files(url, data_dir):
  '''
  Gets a list of expected file paths and compares to the local store and deletes old files/
  :param url: url of the repo
  :param data_dir: path of the root of local files
  :return: local path of the deleted file
  '''
  expected_files = [
    remote_file['filepath'] for remote_file in list(
      map_files(
        resolve_links(url),
        data_dir
      )
    ) if 'filepath' in remote_file
  ]
  for local_path in list_local_paths(data_dir):
    if not local_path in expected_files:
      info('Deleting {}'.format(local_path))
      os.remove(local_path)
      yield local_path


def run():
  while True:
    fetch_files(
      map_files(
        resolve_links(url, max_depth=int(results.max_depth)),
        data_dir
      )
    )
    if results.delete:
      list(purge_old_files(url, data_dir))
    if not results.daemon: break
    info('Sleeping for {} seconds'.format(str(results.daemon_delay)))
    time.sleep(int(results.daemon_delay))
