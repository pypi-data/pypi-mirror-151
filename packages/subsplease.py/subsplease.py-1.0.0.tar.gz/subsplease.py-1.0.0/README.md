# subsplease.py 
A simple and asynchronous wrapper for SubsPlease.

# Installation
```
pip install subsplease.py
```

# Usage
```python
from subsplease import SubsPlease

subsplease = SubsPlease()
```

From magnet:
```python
releases_magnet = await subsplease.get_latest_magnet()
```

From torrent:
```python
releases_torrent = await subsplease.get_latest_torrent()
```