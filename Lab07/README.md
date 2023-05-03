# 2023 NYCU Software Testing - Lab7
0816044    黃則維

---

### poc: the file that can trigger the vulnerability
The file id/000000,sig/06,src/000000,op/flip1,pos/18 can trigger the vulnerability.

The line 41 of bmpgrayscale.c is memset(pixel, gray, 2 * padding - 3); which will send 2\*padding-3 as third parameter size_t n.

And the size_t n cannot be less than 0.

So **if padding of the file is equal or less than 1**, the size_t n will be equal or less than -1, error will occur.

---

### The commands (steps) that you used in this lab
#### install AFL
```
$ git clone https://github.com/google/AFL.git
$ cd AFL
$ make
$ sudo make install
```
#### install libtool
```
$ wget http://mirrors.kernel.org/gnu/libtool/libtool-2.4.7.tar.gz && tar -xzvf libtool-2.4.7.tar.gz
$ cd libtool-2.4.7
$ ./configure
$ sudo make
$ sudo make install 
```
#### install autoconf
```
$ wget http://mirrors.kernel.org/gnu/autoconf/autoconf-2.71.tar.gz && tar -xzvf autoconf-2.71.tar.gz
$ cd autoconf-2.71
$ ./configure
$ sudo make
$ sudo make install 
```
#### install automake
```
$ wget http://mirrors.kernel.org/gnu/automake/automake-1.16.5.tar.gz && tar -xzvf automake-1.16.5.tar.gz
$ cd automake-1.16.5
$ ./configure
$ sudo make
$ sudo make install 
```
#### install libxml2
```
$ git clone https://gitlab.gnome.org/GNOME/libxml2.git
$ cd libxml2
$ cp /usr/share/aclocal/*.m4 /usr/local/share/aclocal/
$ ./autogen.sh
$ export CC=~/AFL/afl-gcc
$ export CXX=~/AFL/afl-g++
$ export AFL_USE_ASAN=1
$ ./configure --enable-shared=no
$ make
```
#### Build & fuzz with AFL
```
$ cd Lab07
$ export CC=~/AFL/afl-gcc
$ export AFL_USE_ASAN=1
$ make
$ mkdir in
$ cp test.bmp in/
$ ~/AFL/afl-fuzz -i in -o out -m none -- ./bmpgrayscale @@ a.bmp
```
#### Check crash detail
```
$ ./bmpgrayscale out/crashes/id:000000* a.bmp
```
---

### Screenshot of AFL running (with triggered crash)
![](https://i.imgur.com/o5CPEJT.jpg)

---

### Screenshot of crash detail (with ASAN error report)
![](https://i.imgur.com/9Fq8uHv.jpg)
