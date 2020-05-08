echo "install start"
echo ""

sudo apt-get update
sudo apt-get -y upgrade

pip3 install --upgrade pip
pip3 install nltk
pip3 install flask
pip3 install plotly
pip3 install scikit-learn==22.1

echo ""
echo "install done"
