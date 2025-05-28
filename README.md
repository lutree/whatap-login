# Whatap Login Automation

와탭 모니터링 서비스 자동 로그인 도구입니다.

## 기능
- 와탭 서비스 자동 로그인
- 액티브 트랜잭션 페이지 자동 접속
- 전체화면 모드 지원
- 종료 버튼 제공

## 설치 방법

1. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

2. 환경 변수 설정:
- `.env` 파일을 생성하고 다음 내용을 추가하세요:
```
WHATAP_EMAIL=your_email@example.com
WHATAP_PASSWORD=your_password
```

## 실행 방법

```bash
python whatap_login.py
```

## 시스템 요구사항
- Python 3.6 이상
- Chrome 브라우저
- Chrome WebDriver

## 주의사항
- `.env` 파일에는 민감한 로그인 정보가 포함되어 있으므로 절대로 Git에 커밋하지 마세요.
- 이 도구는 개인적인 자동화 목적으로만 사용해주세요. 