#!/usr/bin/python
#coding:utf-8
"""
  royguo1988@gmail.com
"""
from auth import Course
import os
import re
import sys
import subprocess

class Downloader(object):
  """下载器,登陆后使用"""
  def __init__(self, course):
    self.course = course
    # {[id, name],[id, name]}
    self.links = []

  def parse_links(self):
    html = 'lectures.html'
    # 下载课程首页，根据页面html抽取页面链接，应该有更好的方式实现...
    cmd = 'curl https://class.coursera.org/neuralnets-2012-001/lecture/index -k -# -L -o ' + html + ' --cookie "csrf_token=%s; session=%s"' % (self.course.csrf_token, self.course.session)
    os.system(cmd)
    with open('lectures.html','r') as f:
      arr = re.findall(r'data-lecture-id="(\d+)"|class="lecture-link">\n(.*)</a>',f.read())
      i = 0
      while i < len(arr):
        lecture_id = arr[i][0]
        lecture_name = arr[i+1][1]
        self.links.append([lecture_id, lecture_name])
        i += 2
    print 'total lectures : ', len(self.links)
    os.remove(html)


  def download(self, url, target):
    if os.path.exists(target):
      print 'file already exist, skip.'
      return
    print 'downloading : ', target
    cmd = ['curl', url, '-k', '-#', '-L', '-o', target, '--cookie',
           "csrf_token=%s; session=%s" % (self.course.csrf_token, self.course.session)]
    subprocess.call(cmd)

def main():
  if len(sys.argv) != 5:
    # class name example "neuralnets-2012-001"
    print 'usage : ./downloader.py download_dir username password class_name'
    return
  path = sys.argv[1] + "/"
  if not os.path.exists(path):
    os.makedirs(path)
  print 'download dir : ', path

  # 账号和课程信息
  c = Course(sys.argv[2], sys.argv[3])
  c.open(sys.argv[4])
  d = Downloader(c)
  d.parse_links()
  # count作为文件名的前缀
  count = 1
  for link in d.links:
    srt = "https://class.coursera.org/neuralnets-2012-001/lecture/subtitles?q=%s_en&format=srt" %link[0]
    file_name = path + count + '.' +link[1]+'.srt'
    d.download(srt, file_name)
    count += 1

if __name__ == '__main__':
  main()
