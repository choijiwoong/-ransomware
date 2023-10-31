echo "테스트 디렉토리 생성중.."

mkdir test

cd test
echo "Hello test_target1!" >> target1.txt
echo "Hello test_target2!" >> target2.txt

mkdir test_test1
cd test_test1
echo "Hello test_test1_target1!" >> target1.txt
echo "Hello test_test1_target2!" >> target2.txt
cd ..

mkdir test_test2
cd test_test2
echo "Hello test_test2_target1!" >> target1.txt
echo "Hello test_test2_target2!" >> target2.txt

cd ..
cd ..
copy test.mp4 test
copy test.mp4 test\test_test1
copy test.mp4 test\test_test2
echo "테스트 디렉토리 생성완료"