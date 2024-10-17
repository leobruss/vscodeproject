mkdir CercaStringa
cp cerca.py CercaStringa
cp requirements.txt CercaStringa
cd CercaStringa
sudo apt install virtualenv
virtualenv myenv
source myenv/bin/activate
pip3 install -r requirements.txt