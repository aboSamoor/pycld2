clean:
	rm -rf build/
	rm -rf dist/
	rm -rf pycld2.egg-info/
	rm -rf pycld2/__pycache__/
	rm -f pycld2/_pycld2*.so

build:
	python setup.py build
	python setup.py install

dist:
	make clean
	python setup.py sdist
	twine upload dist/*

dist-test:
	make clean
	python setup.py sdist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*
