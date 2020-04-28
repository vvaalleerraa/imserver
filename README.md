# imserver
Tiny multihreaded python3 web server for quick previewing huge folders with images on headless GPU servers. 
# Usage
```cd /folder-with-million-images/```

```python3 /full/path/to/imserver.py [cusotom_port]```
* open browser http://your_ip:8080
* you can click on folder name to dive into
* images will have previews and will have BIGGER previews on mouse hover
* click 'view_all' or 'view_all_sorted' links if you dare to wait for processing all files in current folder

# Caution
Do not run this on public servers! It's DANGEROUS in terms of security.
