#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
YouTube 채널에서 동영상을 자동으로 가져와서 index.html을 업데이트하는 스크립트
일요일마다 실행되도록 설정
"""

import requests
import json
import re
from datetime import datetime
import os
import logging

# YouTube Data API v3 키 (필요시 설정)
API_KEY = ""  # YouTube Data API 키를 여기에 입력하세요

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('update_log.txt', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def get_channel_videos(channel_url):
    """
    YouTube 채널에서 동영상 목록을 가져옵니다.
    API 키가 없으면 웹 스크래핑을 사용합니다.
    """
    if API_KEY:
        return get_videos_with_api(channel_url)
    else:
        return get_videos_with_scraping(channel_url)

def get_videos_with_api(channel_url):
    """YouTube Data API를 사용하여 동영상을 가져옵니다."""
    # 채널 ID 추출
    channel_id = extract_channel_id(channel_url)
    if not channel_id:
        return []
    
    # 채널의 업로드 재생목록 ID 가져오기
    url = f"https://www.googleapis.com/youtube/v3/channels"
    params = {
        'part': 'contentDetails',
        'id': channel_id,
        'key': API_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []
    
    data = response.json()
    if not data.get('items'):
        return []
    
    uploads_playlist_id = data['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    
    # 업로드된 동영상 목록 가져오기
    url = f"https://www.googleapis.com/youtube/v3/playlistItems"
    params = {
        'part': 'snippet',
        'playlistId': uploads_playlist_id,
        'maxResults': 50,
        'key': API_KEY
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        return []
    
    data = response.json()
    videos = []
    
    for item in data.get('items', []):
        video_id = item['snippet']['resourceId']['videoId']
        title = item['snippet']['title']
        videos.append({
            'id': video_id,
            'title': title
        })
    
    return videos

def get_videos_with_scraping(channel_url):
    """웹 스크래핑을 사용하여 동영상을 가져옵니다."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(channel_url, headers=headers)
        if response.status_code != 200:
            return []
        
        # YouTube 페이지에서 동영상 정보 추출
        content = response.text
        
        # ytInitialData 패턴 찾기
        pattern = r'var ytInitialData = ({.*?});'
        match = re.search(pattern, content, re.DOTALL)
        
        if not match:
            return []
        
        data = json.loads(match.group(1))
        
        # 동영상 목록 추출
        videos = []
        
        # 탭 콘텐츠에서 동영상 찾기
        tabs = data.get('contents', {}).get('twoColumnBrowseResultsRenderer', {}).get('tabs', [])
        
        for tab in tabs:
            if tab.get('tabRenderer', {}).get('selected', False):
                tab_content = tab.get('tabRenderer', {}).get('content', {})
                section_list = tab_content.get('sectionListRenderer', {}).get('contents', [])
                
                for section in section_list:
                    items = section.get('itemSectionRenderer', {}).get('contents', [])
                    
                    for item in items:
                        grid = item.get('gridRenderer', {})
                        if grid:
                            grid_items = grid.get('items', [])
                            
                            for grid_item in grid_items:
                                video_renderer = grid_item.get('gridVideoRenderer', {})
                                if video_renderer:
                                    video_id = video_renderer.get('videoId', '')
                                    title = video_renderer.get('title', {}).get('runs', [{}])[0].get('text', '')
                                    
                                    if video_id and title:
                                        videos.append({
                                            'id': video_id,
                                            'title': title
                                        })
        
        return videos[:50]  # 최대 50개만 반환
        
    except Exception as e:
        print(f"스크래핑 중 오류 발생: {e}")
        return []

def extract_channel_id(url):
    """URL에서 채널 ID를 추출합니다."""
    patterns = [
        r'youtube\.com/@([^/?]+)',
        r'youtube\.com/channel/([^/?]+)',
        r'youtube\.com/c/([^/?]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    
    return None

def get_existing_videos():
    """현재 HTML 파일에서 기존 동영상 목록을 가져옵니다."""
    html_file = 'index.html'
    
    if not os.path.exists(html_file):
        return []
    
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # videos 배열 부분 찾기
    pattern = r'const videos = \[(.*?)\];'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        return []
    
    videos_text = match.group(1)
    
    # 각 동영상 항목 추출
    video_pattern = r'{\s*id:\s*[\'"]([^\'"]+)[\'"],\s*title:\s*[\'"]([^\'"]+)[\'"]\s*}'
    matches = re.findall(video_pattern, videos_text, re.DOTALL)
    
    existing_videos = []
    for video_id, title in matches:
        existing_videos.append({
            'id': video_id,
            'title': title
        })
    
    return existing_videos

def has_new_videos(new_videos, existing_videos):
    """새 동영상이 있는지 확인합니다."""
    if not existing_videos:
        return True  # 기존 동영상이 없으면 새 동영상이 있다고 간주
    
    existing_ids = {video['id'] for video in existing_videos}
    
    for video in new_videos:
        if video['id'] not in existing_ids:
            return True
    
    return False

def update_html_file(videos):
    """index.html 파일을 업데이트합니다."""
    html_file = 'index.html'
    
    if not os.path.exists(html_file):
        print(f"오류: {html_file} 파일을 찾을 수 없습니다.")
        return False
    
    # 기존 동영상 목록 가져오기
    existing_videos = get_existing_videos()
    print(f"기존 동영상 수: {len(existing_videos)}개")
    
    # 새 동영상이 있는지 확인
    if not has_new_videos(videos, existing_videos):
        print("새 동영상이 없습니다. 업데이트를 건너뜁니다.")
        return False
    
    # HTML 파일 읽기
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # videos 배열 부분 찾기
    pattern = r'const videos = \[(.*?)\];'
    match = re.search(pattern, content, re.DOTALL)
    
    if not match:
        print("오류: videos 배열을 찾을 수 없습니다.")
        return False
    
    # 새로운 videos 배열 생성
    videos_json = []
    for video in videos:
        videos_json.append({
            'id': video['id'],
            'title': video['title']
        })
    
    # HTML에서 사용할 형식으로 변환
    videos_html = []
    for video in videos_json:
        videos_html.append(f"        {{\n            id: '{video['id']}',\n            title: '{video['title']}'\n        }}")
    
    videos_content = ',\n'.join(videos_html)
    
    # HTML 파일 업데이트
    new_content = re.sub(pattern, f'const videos = [\n{videos_content}\n    ];', content, flags=re.DOTALL)
    
    # 백업 파일 생성
    backup_file = f'index_backup_{datetime.now().strftime("%Y%m%d_%H%M%S")}.html'
    with open(backup_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"백업 파일 생성: {backup_file}")
    
    # 새 파일 저장
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"동영상 {len(videos)}개로 업데이트 완료")
    return True

def main():
    """메인 함수"""
    channel_url = "https://www.youtube.com/@%EC%98%88%EC%82%B0%ED%99%94%ED%83%80"
    
    logger.info("YouTube 동영상 업데이트 시작")
    
    print("YouTube 채널에서 동영상을 가져오는 중...")
    videos = get_channel_videos(channel_url)
    
    if not videos:
        logger.warning("동영상을 가져올 수 없습니다.")
        print("동영상을 가져올 수 없습니다.")
        return
    
    logger.info(f"총 {len(videos)}개의 동영상을 찾았습니다.")
    print(f"총 {len(videos)}개의 동영상을 찾았습니다.")
    
    # 동영상 제목에서 카테고리 분류를 위한 숫자 확인
    for video in videos[:5]:  # 처음 5개만 확인
        print(f"- {video['title']}")
    
    # HTML 파일 업데이트
    updated = update_html_file(videos)
    
    if updated:
        logger.info("업데이트가 완료되었습니다!")
        print("업데이트가 완료되었습니다!")
    else:
        logger.info("새 동영상이 없어서 업데이트하지 않았습니다.")
        print("새 동영상이 없어서 업데이트하지 않았습니다.")

if __name__ == "__main__":
    main() 