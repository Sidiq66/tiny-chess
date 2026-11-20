# Pack engine_src.py into main.py: lzma + base85 one-line bootstrap.
# Same pack format as the current engine: the payload decompresses to the
# exact bytes of engine_src.py and the bootstrap is a single line, so
# main.py alone is the engine (it reads no other file at run time).
import base64
import hashlib
import lzma

SRC = "engine_src.py"
OUT = "main.py"

def pack(src):
	raw = lzma.compress(src, preset=6)
	b85 = base64.b85encode(raw).decode()
	return "import lzma,base64;exec(lzma.decompress(base64.b85decode('%s')))\n" % b85

def main():
	src = open(SRC, "rb").read()
	data = pack(src).encode()
	open(OUT, "wb").write(data)
	print("source bytes:", len(src))
	print("main.py bytes:", len(data))
	print("main.py sha256:", hashlib.sha256(data).hexdigest())

if __name__ == "__main__":
	main()
