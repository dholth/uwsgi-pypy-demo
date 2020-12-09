# Simple uwsgi demo application

import png
import urllib
import mandelbrot


from bottle import Bottle, request


app = Bottle()


def imagedata():
    # expects flattened R, G, B, R, ...
    for y in range(HEIGHT):
        yield [255, 0, 0] * WIDTH


@app.route("/<cx>/<cy>/<scale>")
def zoom(cx, cy, scale):
    # parse manually; bottle doesn't like e notation
    cx = float(cx)
    cy = float(cy)
    scale = float(scale)
    return f"""
    <html style="height: 100%">
    <head>
    <title>Mandelbrot</title>
    <script>
    let cornerx={cx},cornery={cy},scale={scale},factor=0.5;

    function coords(event) {{
        let x = (event.x - event.target.offsetLeft) / event.target.width;
        let y = (event.y - event.target.offsetTop) / event.target.height;
        let newscale = scale * factor;
        let centerx = cornerx + x * scale;
        let centery = cornery + y * scale;
        console.log(x, y, centerx, centery, centerx-newscale, centery-newscale);

        return {{ cx : centerx, cy : centery, scale: newscale }};
    }}

    function zoom(event) {{
        let c = coords(event)
        window.location = "/" + (c.cx - c.scale * 0.5) + "/" + (c.cy - c.scale * 0.5) + "/" + c.scale;
    }}
    </script>
    </head>
    <body style="display: flex; width: 100%; height: 100%; align-items: center; justify-content: center; margin: 0;">
    <div style="display: flex; align-items: center; justify-content: center;">
    <img src="mandelbrot.png?cx={cx}&cy={cy}&scale={scale}" srcset="mandelbrot.png?cx={cx}&cy={cy}&scale={scale} 2x" onclick="zoom(event)">
    </div>
    </body>
    </html>
    """


@app.route("/")
def home():
    return zoom(-1.5, -2.25, 3.0)


def application(env, start_response):
    if not ".png" in env["PATH_INFO"]:
        yield from app(env, start_response)
        return

    writer = start_response("200 Ok", [("Content-type", "image/png")])

    # use deprecated WSGI writer() object for file-like streaming response
    class outfile:
        write = writer

    params = urllib.parse.parse_qs(env["QUERY_STRING"])
    cx = float(params["cx"][0])
    cy = float(params["cy"][0])
    scale = float(params["scale"][0])

    pngWriter = png.Writer(
        size=(mandelbrot.SIZE, mandelbrot.SIZE), bitdepth=8, greyscale=False
    )
    pngWriter.write(outfile, mandelbrot.mandelbrot_parallel(cy, cx, scale))

    yield []
