from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import os
import time
import platform
import sys

def get_command_key():
    return Keys.CONTROL if platform.system() == 'Windows' else Keys.COMMAND

def add_exit_button(driver):
    # 종료 버튼 스타일과 함수를 추가하는 JavaScript 코드
    script = """
        // 종료 버튼 컨테이너 생성
        var exitContainer = document.createElement('div');
        exitContainer.style.position = 'fixed';
        exitContainer.style.top = '10px';
        exitContainer.style.left = '50%';
        exitContainer.style.transform = 'translateX(-50%)';
        exitContainer.style.zIndex = '9999';
        
        // 종료 버튼 생성
        var exitButton = document.createElement('button');
        exitButton.innerHTML = '종료';
        exitButton.style.padding = '8px 15px';
        exitButton.style.backgroundColor = '#ff4444';
        exitButton.style.color = 'white';
        exitButton.style.border = 'none';
        exitButton.style.borderRadius = '5px';
        exitButton.style.cursor = 'pointer';
        exitButton.style.fontSize = '14px';
        exitButton.style.fontWeight = 'bold';
        
        // 호버 효과 추가
        exitButton.onmouseover = function() {
            this.style.backgroundColor = '#ff6666';
        };
        exitButton.onmouseout = function() {
            this.style.backgroundColor = '#ff4444';
        };
        
        // 클릭 효과 추가
        exitButton.onmousedown = function() {
            this.style.backgroundColor = '#cc0000';
        };
        exitButton.onmouseup = function() {
            this.style.backgroundColor = '#ff4444';
        };
        
        // 종료 함수 설정
        exitButton.onclick = function() {
            document.dispatchEvent(new CustomEvent('exitApplication'));
        };
        
        // 버튼을 컨테이너에 추가
        exitContainer.appendChild(exitButton);
        
        // 컨테이너를 페이지에 추가
        document.body.appendChild(exitContainer);
    """
    driver.execute_script(script)
    
    # Python에서 종료 이벤트 리스너 추가
    driver.execute_script("""
        document.addEventListener('exitApplication', function() {
            window.isExiting = true;
        });
    """)

def resource_path(relative_path):
    """ PyInstaller에서 임시 폴더와 실제 파일 경로를 모두 처리할 수 있도록 하는 함수 """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def login_to_whatap():
    # 환경 변수 로드
    env_path = resource_path('.env')
    load_dotenv(env_path)
    
    # 환경 변수에서 로그인 정보 가져오기
    email = os.getenv('WHATAP_EMAIL')
    password = os.getenv('WHATAP_PASSWORD')
    
    if not email or not password:
        print("Error: 환경 변수가 설정되지 않았습니다.")
        print("1. .env 파일을 생성하세요.")
        print("2. 다음 내용을 .env 파일에 추가하세요:")
        print("WHATAP_EMAIL=your_email@example.com")
        print("WHATAP_PASSWORD=your_password")
        input("\nEnter 키를 눌러 종료하세요...")
        return
    
    # Chrome 옵션 설정
    chrome_options = Options()
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--kiosk')  # 전체 화면 모드
    chrome_options.add_argument('--app=https://service.whatap.io/account/login')  # 앱 모드로 실행
    
    # Mac M1/M2 환경 설정
    if platform.processor() == 'arm':
        chrome_options.add_argument('--remote-debugging-port=9222')
    
    try:
        # WebDriver 초기화
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Whatap 로그인 페이지로 이동
        driver.get('https://service.whatap.io/account/login')
        
        # 페이지가 완전히 로드될 때까지 대기
        wait = WebDriverWait(driver, 4)
        
        # 이메일 입력
        email_input = wait.until(EC.presence_of_element_located((By.ID, 'id_email')))
        email_input.send_keys(get_command_key() + 'a')
        email_input.send_keys(Keys.DELETE)
        email_input.send_keys(email)
        
        # 비밀번호 입력
        password_input = wait.until(EC.presence_of_element_located((By.ID, 'id_password')))
        password_input.send_keys(get_command_key() + 'a')
        password_input.send_keys(Keys.DELETE)
        password_input.send_keys(password)
        
        # 로그인 버튼 클릭
        login_button = wait.until(EC.element_to_be_clickable((By.ID, 'btn_login')))
        login_button.click()
        
        # 로그인 후 페이지 로드 대기
        time.sleep(2)
        
        # 로그인 실패 확인
        try:
            error_message = wait.until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '아이디나 패스워드가 잘못되었습니다')]")))
            if error_message:
                print("\n로그인 실패: 아이디나 비밀번호가 잘못되었습니다.")
                print("1. .env 파일의 내용을 확인해주세요.")
                print(f"2. 현재 입력된 이메일: {email}")
                print("3. 비밀번호가 올바른지 확인해주세요.")
                input("\nEnter 키를 눌러 종료하세요...")
                return
        except:
            # 에러 메시지가 없다면 로그인 성공
            print("로그인 성공!")
            
            # 페이지가 완전히 로드될 때까지 충분히 대기
            time.sleep(1)
            
            # 종료 버튼 추가
            add_exit_button(driver)
            
            # 액티브 트랜잭션 클릭
            try:
                print("액티브 트랜잭션 찾는 중...")
                
                # 더 구체적인 선택자 추가
                selectors = [
                    "//span[normalize-space(text())='액티브 트랜잭션']",
                    "//div[normalize-space(text())='액티브 트랜잭션']",
                    "//a[contains(.,'액티브 트랜잭션')]",
                    "//span[contains(text(),'액티브 트랜잭션')]",
                    "//div[contains(text(),'액티브 트랜잭션')]",
                    "//*[contains(text(),'액티브 트랜잭션')]"
                ]
                
                element_found = False
                for selector in selectors:
                    try:
                        print(f"선택자 시도 중: {selector}")
                        # 명시적 대기 시간 증가
                        wait = WebDriverWait(driver, 10)
                        active_transaction = wait.until(
                            EC.element_to_be_clickable((By.XPATH, selector))
                        )
                        # 요소가 화면에 보이도록 스크롤
                        driver.execute_script("arguments[0].scrollIntoView(true);", active_transaction)
                        time.sleep(1)  # 스크롤 후 잠시 대기
                        
                        # 클릭 시도
                        active_transaction.click()
                        element_found = True
                        print(f"액티브 트랜잭션 클릭 성공! (사용된 선택자: {selector})")
                        break
                    except Exception as e:
                        print(f"선택자 {selector} 실패: {str(e)}")
                        continue
                
                if not element_found:
                    print("\n액티브 트랜잭션 요소를 찾을 수 없습니다.")
                    print("현재 페이지의 모든 텍스트:")
                    print(driver.find_element(By.TAG_NAME, "body").text)
                    input("\nEnter 키를 눌러 종료하세요...")
                    
            except Exception as e:
                print(f"\n액티브 트랜잭션 클릭 실패: {str(e)}")
                print("현재 페이지에서 다음 작업을 진행할 수 없습니다.")
                print("페이지 소스:")
                print(driver.page_source)
                input("\nEnter 키를 눌러 종료하세요...")
        
        print("\n화면 상단 중앙의 '종료' 버튼을 클릭하여 프로그램을 종료할 수 있습니다.")
        
        # 브라우저가 닫힐 때까지 대기
        while True:
            try:
                # 종료 플래그 확인
                is_exiting = driver.execute_script("return window.isExiting === true;")
                if is_exiting:
                    driver.quit()
                    break
                time.sleep(0.5)
            except:
                break  # 브라우저가 이미 닫혔거나 오류가 발생한 경우
        
    except Exception as e:
        print(f"예상치 못한 오류 발생: {str(e)}")
        
        # 디버깅을 위한 페이지 소스 출력
        try:
            print("\n현재 페이지 정보:")
            print(f"URL: {driver.current_url}")
            print("\n페이지 텍스트:")
            print(driver.find_element(By.TAG_NAME, "body").text)
        except:
            pass
        input("\nEnter 키를 눌러 종료하세요...")
    
    finally:
        try:
            driver.quit()
        except:
            pass

if __name__ == "__main__":
    login_to_whatap() 