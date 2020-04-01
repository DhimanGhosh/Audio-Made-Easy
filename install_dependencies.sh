case "$OSTYPE" in
    linux*)
		sudo add-apt-repository -y ppa:kivy-team/kivy
		sudo apt-get -y update
		sudo apt-get -y install python3-kivy
		pip install -r requirements.txt ;;
    msys*)
		pip install --upgrade pip wheel setuptools virtualenv
		pip install kivy_deps.sdl2==0.1.*
		pip install kivy_deps.glew==0.1.*
		pip install kivy_deps.gstreamer==0.1.*
		pip install kivy_deps.angle==0.1.*
		pip install kivy==1.11.1
		pip install -r requirements.txt ;;
esac
