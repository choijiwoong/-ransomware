Encryption
1. "folder_path" 변수에 암호화할 폴더 선택 (이하 폴더까지 전부 암호화)
(저의 경우 바탕화면/Test(폴더))
Test 폴더 내부 (hwp 파일, 새 폴더) -> 새 폴더 내부 (zip 파일, ppt 파일)

2. 'zip', 'hwp', 'hwpx', 'xlsx', 'docx', 'pptx', 'pdf' 확장자를 선별하여 byte_size 만큼 암호화 (AES-256)

3. 암호화 시 IV, Key Value는 난수 생성(IV, Key 출력 -> 복호화에 사용) -> 암호화 완료

4. 파일 실행 안됨 -> hwp. zip, ppt 3개의 파일이 모두 암호화되어 열리지 않음

---

Decryption
1. "folder_path" 변수에 복호화 할 폴더 선택 (이하 폴더까지 전부 복호화)
    (저의 경우 바탕화면/Test(폴더))
    Test 폴더 내부 (hwp 파일, 새 폴더) -> 새 폴더 내부 (zip 파일, ppt 파일)

2.  'zip', 'hwp', 'hwpx', 'xlsx', 'docx', 'pptx', 'pdf' 확장자를 선별하여 byte_size 만큼 복호화 (AES-256)

3. 이때 복호화를 위해 IV, Key Value 입력 -> 복호화 완료

4. 모든 파일 실행됨 -> hwp. zip, ppt 3개의 파일이 모두 복호화 되어 열림

##### +RSA
