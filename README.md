# vigor_handbox
## OS aufsetzen
### SD flashen
Imager Version 2.0.6 https://www.raspberrypi.com/software/
| Parameter | Wert |
|-----------|------|
| Hostname | eindeutig z.B: TESTBRETT001ZERO |
| OS | 32bit Raspi OS Lite / Trixie ohne Desktop|
| User | admin |
| PW | 5210 |
| SSID | VigorHo |
| PW |smartduengen |
### setup
1. ```
   sudo apt install git
   ```

## Services
## can.service
1. canutils intallieren
```
sudo apt-get install can-utils
```
2. spi1 einstellen
```
sudo nano /boot/firmware/config.txt
```
am Ende hinzufügen
```
dtparam=spi=on
dtoverlay=spi1-1cs,cs0_pin=16
dtoverlay=mcp2515,spi1-0,oscillator=16000000,interrupt=26
```
3. neu starten
```
sudo reboot
```
4. can verbindung testweise starten
```
sudo ip link set can0 up type can bitrate 125000 restart-ms 100
ip -details link show can0
```
5. service aufsetzen
```
sudo nano /etc/systemd/system/can.service
```
folgenden Text rein kopieren:
```
[Unit]
Description=setup can interface
After=network.target

[Service]
Type=oneshot
ExecStart=/sbin/ip link set can0 up type can bitrate 125000 restart-ms 100
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```
6. service enablen
```
sudo systemctl daemon-reload
sudo systemctl enable can.service
```
7. service testen
```
sudo ip link set can0 down
sudo systemctl start can.service
ip -details link show can0
```


### display.service
1. install bcm library
```
curl -O http://www.airspayce.com/mikem/bcm2835/bcm2835-1.75.tar.gz
```
```
tar zxvf bcm2835-1.75.tar.gz
cd bcm2835-1.xx
./configure
make
sudo make check
sudo make install
```
2. install redis-server
```
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```
3. install hiredis
```
git clone https://github.com/redis/hiredis.git
cd hiredis
make
sudo make install
```
4. fork github
  ```
  git clone https://github.com/danielfhnw/Vigor_TFT_Display
  ```
5. build library
  ```
  cd Vigor_TFT_Display
  make
  sudo make install
  ```
6. build example
  ```
  cd examples
  make
  echo "/usr/local/lib" | sudo tee /etc/ld.so.conf.d/local.conf
  sudo ldconfig
```
7. testen ob Programm läuft:
```
  make run
  ```
8. service aufsetzen
```
sudo nano /etc/systemd/system/display.service
```
folgenden Text rein kopieren:
```
[Unit]
Description=start display
After=can0.service

[Service]
Type=simple
User=admin
WorkingDirectory=/home/admin/Vigor_TFT_Display/examples
ExecStart=/usr/bin/make run
Restart=on-failure

[Install]
WantedBy=multi-user.target
```
10. service enablen
```
sudo systemctl daemon-reload
sudo systemctl enable display.service
```
10. service testen
```
sudo systemctl start display.service
```
