![python](https://img.shields.io/badge/Python-3.8-blue)
![python](https://img.shields.io/badge/Python-3.9-blue)
![python](https://img.shields.io/badge/Python-3.10-blue)
![main](https://github.com/phewera/videoembed/actions/workflows/main.yml/badge.svg)

# videoembed

Videoembed is a tool to create embed codes from video URLs by using [oembed](https://oembed.com). You are also able to get thumbnail data.

**Supported platforms:**
* YouTube
* Vimeo


## Installation

Use the package manager [pip](https://pypi.org/project/pip/) to install videoembed.

```bash
pip install videoembed
```

## Usage

Basic usage:

```python
from videoembed import Embedder

embedder = Embedder()
video = embedder('https://www.youtube.com/watch?v=VIDEOID')

# get embed code
embed_code = video.embed_code

# get thumbnail data
thumbnail = video.thumbnail
```

You can also pass some configuration data to the embedder:

```python
from videoembed import Embedder

config = {
    'width': 600,
    'height': 360,
    'autoplay': True
}
embedder = Embedder(**config)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
