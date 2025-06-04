$raspberryPiIP = "192.168.1.5"  
$password = "raspberry"
$command = "sudo bash -c 'cd /home/speed/Desktop/speed/RobotCar && source nemoenv/bin/activate && python flask/twoCam.py'"
echo $password | plink.exe -ssh $speed@$raspberryPiIP -pw $password "echo $password | sudo -S bash -c 'cd /home/speed/Desktop/speed/RobotCar && source nemoenv/bin/activate && python flask/pictures.py'"