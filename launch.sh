VPN_SERVER=10.10.80.71
VPN_PORT=7890
export https_proxy=$VPN_SERVER:$VPN_PORT
python app.py