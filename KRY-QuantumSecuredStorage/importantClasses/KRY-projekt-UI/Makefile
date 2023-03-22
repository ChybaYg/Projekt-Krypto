env:
	@echo "CREATING VIRTUAL ENVIRONMENT..."
	python3 -m venv env
	source ./env/bin/activate

install:
	mkdir out
	mkdir out/ntru_key
	mkdir out/ntru_log
	@echo "INSTALLING REQUIREMENTS..."
	pip3 install numpy
	pip3 install -r requirements.txt

help:
	python3 kry.py -h 

sign_multivariate:
	@echo "Example of signing a file using multivariate algorithm."
	python3 kry.py --onedir sign_multivariate loremipsum.txt

test_multivariate:
	@echo "TEST START"
	@echo "In this test we sign a document, change and verify it successfully, then we changed the file and verified again with unsuccessfull result."
	@echo "@@@@@@ Signing @@@@@@"
	python3 kry.py --onedir sign_multivariate loremipsum.txt
	@echo "@@@@@@ Verification should SUCCEED: @@@@@@"
	python3 kry.py --onedir verify_multivariate out/cvPub.pub out/loremipsum.txt.signature loremipsum.txt 
	@echo "Modifying original file"
	@echo "loremipsum" >> loremipsum.txt
	@echo "@@@@@@ Verification should FAIL: @@@@@@"
	python3 kry.py --onedir verify_multivariate out/cvPub.pub out/loremipsum.txt.signature loremipsum.txt 
	make loremipsum

save: 
	python3 kry.py --save

sign_sphinx:
	@echo "Example of signing a file using SPHINX+ algorithm."
	python3 kry.py --onedir sphinx_sign loremipsum.txt

test_sphinx:
	@echo "TEST START"
	@echo "In this test we sign a document, change and verify it successfully, then we changed the file and verified again with unsuccessfull result."
	@echo "@@@@@@ Signing @@@@@@"
	python3 kry.py --onedir sphinx_sign loremipsum.txt
	@echo "@@@@@@ Verification should SUCCEED: @@@@@@"
	python3 kry.py --onedir sphinx_verify out/loremipsum.txt.pbkey out/loremipsum.txt.signature loremipsum.txt 
	@echo "Modifying original file"
	@echo "loremipsum" >> loremipsum.txt
	@echo "@@@@@@ Verification should FAIL: @@@@@@"
	python3 kry.py --onedir sphinx_verify out/loremipsum.txt.pbkey out/loremipsum.txt.signature loremipsum.txt 
	make loremipsum

ntru_test:
	@echo "TEST START"
	@echo "In this test, we create a pair of keys and then encrypt/ decrypt the zprava.txt file with them"
	@echo "Key generation with parameter N = 167, p = 3, q = 128. The generated keys will be saved in ./out/ntru_key"
	python kry.py ntru_g -p 167 3 128 private public
	@echo "Enrcyption. The encrypted file will be saved in the ./ntru_file directory. The log will be saved in ./out/ntru_log"
	python kry.py ntru_e public.npz ntru_encrypted.txt zprava.txt
	@echo "Decryption. The decrypted file will be saved in the ./ntru_file directory. The log will be saved in ./out/ntru_log"
	python kry.py ntru_d private.npz ntru_encrypted.txt ntru_decrypted.txt

mceliece_H84:
	@echo "Generating key and encryption"
	python3 kry.py encrypt_mceliece loremipsum.txt
	@echo "Decryption"
	python3 kry.py decrypt_mceliece loremipsum.txt.priv loremipsum.txt.ctxt

remove_out:
	rm -rf out/*

clear_log:
	rm kry_log.log
	touch kry_log.log

pylint:
	pylint kry.py ./src

loremipsum:
	@echo "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum." > loremipsum.txt

documentation:
	mkdocs serve

gh_publish:
	mkdocs gh-deploy
