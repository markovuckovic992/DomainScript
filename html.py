import mammoth, base64, sys

def convert_image(image):
    with image.open() as image_bytes:
        encoded_src = base64.b64encode(image_bytes.read()).decode("ascii")

    return {
        "src": "data:{0};base64,{1}".format(image.content_type, encoded_src),
        "style": "margin-left: 15%;"
    }

def make_html(file, output):
	style_map = """
	p[style-name='Section Title'] => h1:fresh
	p[style-name='Subsection Title'] => h2:fresh
	"""
	with open("/home/marko/" + file, "rb") as docx_file:
	    result = mammoth.convert_to_html(docx_file, convert_image=mammoth.images.inline(convert_image))
	    html = result.value.encode('ascii', 'ignore')
	    file = open(output, 'w')
	    file.write(html)
	    file.close()

if __name__ == '__main__':
	make_html(sys.argv[1], sys.argv[2])