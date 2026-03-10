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
