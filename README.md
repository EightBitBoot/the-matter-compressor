# The Matter Compressor

<p align="center">
    <!-- width and height are image_[width|height] * 0.6-->
    <img src="https://github.com/EightBitBoot/the-matter-compressor/blob/master/img/matter_compressor.png?raw=true" width=384 height=640/>
</p>

<br />

This is an art piece I implemented for a friend with the theme "collaborative change over time".  
It serves a webpage with a video and a single button below it. Users can click the button to send the video through a compressor (re-encoder) and iteratively degrade its fidelity.  
  
Internally, it uses:
- [flask](https://flask.palletsprojects.com/) for business logic
- [gunicorn](https://gunicorn.org/) as a dynamic http server (non-static content and http endpoints)
- [nginx](https://nginx.org/) to serve static files
- [redis](https://redis.io/) to store user data (in order to prevent multiple compressions from the same user)
- [ffmpeg](https://www.ffmpeg.org/) as a re-encoder to "compress" video files
- post requests to an http endpoint when notifying the server the client has initiated a compression
- websockets from the server to the client when the current compression has finished and a refresh is required

