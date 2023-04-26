# 2023 NYCU Software Testing - Lab6
0816044    黃則維

### 編譯器種類及版本
gcc version 11.3.0 (Ubuntu 11.3.0-1ubuntu1~22.04)

## part1

### Heap out-of-bounds
##### source code
```
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *p = (int *)malloc(10 * sizeof(int));
    
    int num = p[15];

    p[12] = 7;

    free(p);
    return 0;
}
```
##### ASan report
```
$ gcc -fsanitize=address -g -o asan_t1 t1.c
$ ./asan_t1 
=================================================================
==79414==ERROR: AddressSanitizer: heap-buffer-overflow on address 0x60400000004c at pc 0x557d5e83c23e bp 0x7ffd299397d0 sp 0x7ffd299397c0
READ of size 4 at 0x60400000004c thread T0
    #0 0x557d5e83c23d in main /home/benny/st/lab6/t1.c:7
    #1 0x7fa8f8decd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7fa8f8dece3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x557d5e83c124 in _start (/home/benny/st/lab6/asan_t1+0x1124)

0x60400000004c is located 20 bytes to the right of 40-byte region [0x604000000010,0x604000000038)
allocated by thread T0 here:
    #0 0x7fa8f909f867 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x557d5e83c1fe in main /home/benny/st/lab6/t1.c:5
    #2 0x7fa8f8decd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

SUMMARY: AddressSanitizer: heap-buffer-overflow /home/benny/st/lab6/t1.c:7 in main
Shadow bytes around the buggy address:
  0x0c087fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c087fff8000: fa fa 00 00 00 00 00 fa fa[fa]fa fa fa fa fa fa
  0x0c087fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==79414==ABORTING
```
##### valgrind report
```
$ gcc -o val_t1 t1.c
$ valgrind ./val_t1 
==79421== Memcheck, a memory error detector
==79421== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==79421== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==79421== Command: ./val_t1
==79421== 
==79421== Invalid read of size 4
==79421==    at 0x109187: main (in /home/benny/st/lab6/val_t1)
==79421==  Address 0x4a8e07c is 20 bytes after a block of size 40 alloc'd
==79421==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==79421==    by 0x10917E: main (in /home/benny/st/lab6/val_t1)
==79421== 
==79421== Invalid write of size 4
==79421==    at 0x109195: main (in /home/benny/st/lab6/val_t1)
==79421==  Address 0x4a8e070 is 8 bytes after a block of size 40 alloc'd
==79421==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==79421==    by 0x10917E: main (in /home/benny/st/lab6/val_t1)
==79421== 
==79421== 
==79421== HEAP SUMMARY:
==79421==     in use at exit: 0 bytes in 0 blocks
==79421==   total heap usage: 1 allocs, 1 frees, 40 bytes allocated
==79421== 
==79421== All heap blocks were freed -- no leaks are possible
==79421== 
==79421== For lists of detected and suppressed errors, rerun with: -s
==79421== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 0 from 0)
```
ASan 能 , valgrind 能

---

### Stack out-of-bounds
##### source code
```
#include <stdio.h>

int main() {
    int arr[10];

    arr[12] = 7;

    return arr[15];
}
```
##### ASan report
```
$ gcc -fsanitize=address -g -o asan_t2 t2.c
$ ./asan_t2
=================================================================
==79428==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fff666d1160 at pc 0x55f1a36052bb bp 0x7fff666d10f0 sp 0x7fff666d10e0
WRITE of size 4 at 0x7fff666d1160 thread T0
    #0 0x55f1a36052ba in main /home/benny/st/lab6/t2.c:6
    #1 0x7fc3e396fd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7fc3e396fe3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x55f1a3605124 in _start (/home/benny/st/lab6/asan_t2+0x1124)

Address 0x7fff666d1160 is located in stack of thread T0 at offset 96 in frame
    #0 0x55f1a36051f8 in main /home/benny/st/lab6/t2.c:3

  This frame has 1 object(s):
    [48, 88) 'arr' (line 4) <== Memory access at offset 96 overflows this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-buffer-overflow /home/benny/st/lab6/t2.c:6 in main
Shadow bytes around the buggy address:
  0x10006ccd21d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10006ccd21e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10006ccd21f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10006ccd2200: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10006ccd2210: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x10006ccd2220: f1 f1 f1 f1 f1 f1 00 00 00 00 00 f3[f3]f3 f3 f3
  0x10006ccd2230: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10006ccd2240: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10006ccd2250: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10006ccd2260: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x10006ccd2270: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==79428==ABORTING
```
##### valgrind report
```
$ gcc -o val_t2 t2.c
$ valgrind ./val_t2
==79435== Memcheck, a memory error detector
==79435== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==79435== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==79435== Command: ./val_t2
==79435== 
==79435== 
==79435== HEAP SUMMARY:
==79435==     in use at exit: 0 bytes in 0 blocks
==79435==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==79435== 
==79435== All heap blocks were freed -- no leaks are possible
==79435== 
==79435== For lists of detected and suppressed errors, rerun with: -s
==79435== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
ASan 能 , valgrind 不能

---

### Global out-of-bounds
##### source code
```
#include <stdio.h>

int arr[10];

int main() {
    arr[12] = 7;

    return arr[15];
}
```
##### ASan report
```
$ gcc -fsanitize=address -g -o asan_t3 t3.c
$ ./asan_t3
=================================================================
==79443==ERROR: AddressSanitizer: global-buffer-overflow on address 0x55797577a0d0 at pc 0x557975777223 bp 0x7ffe62a1d3f0 sp 0x7ffe62a1d3e0
WRITE of size 4 at 0x55797577a0d0 thread T0
    #0 0x557975777222 in main /home/benny/st/lab6/t3.c:6
    #1 0x7f6c5439dd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f6c5439de3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x557975777124 in _start (/home/benny/st/lab6/asan_t3+0x1124)

0x55797577a0d0 is located 8 bytes to the right of global variable 'arr' defined in 't3.c:3:5' (0x55797577a0a0) of size 40
SUMMARY: AddressSanitizer: global-buffer-overflow /home/benny/st/lab6/t3.c:6 in main
Shadow bytes around the buggy address:
  0x0aafaeae73c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0aafaeae73d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0aafaeae73e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0aafaeae73f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0aafaeae7400: 00 00 00 00 00 00 00 00 f9 f9 f9 f9 f9 f9 f9 f9
=>0x0aafaeae7410: 00 00 00 00 00 00 00 00 00 f9[f9]f9 f9 f9 f9 f9
  0x0aafaeae7420: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0aafaeae7430: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0aafaeae7440: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0aafaeae7450: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0aafaeae7460: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==79443==ABORTING
```
##### valgrind report
```
$ gcc -o val_t3 t3.c
$ valgrind ./val_t3
==79450== Memcheck, a memory error detector
==79450== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==79450== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==79450== Command: ./val_t3
==79450== 
==79450== 
==79450== HEAP SUMMARY:
==79450==     in use at exit: 0 bytes in 0 blocks
==79450==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==79450== 
==79450== All heap blocks were freed -- no leaks are possible
==79450== 
==79450== For lists of detected and suppressed errors, rerun with: -s
==79450== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
ASan 能 , valgrind 不能

---
### Use-after-free
##### source code
```
#include <stdio.h>
#include <stdlib.h>

int main() {
    int *p = (int *)malloc(10 * sizeof(int));
    
    free(p);

    return p[2];
}
```
##### ASan report
```
$ gcc -fsanitize=address -g -o asan_t4 t4.c
$ ./asan_t4
=================================================================
==79457==ERROR: AddressSanitizer: heap-use-after-free on address 0x604000000018 at pc 0x558e75cbd22a bp 0x7ffecf7cec10 sp 0x7ffecf7cec00
READ of size 4 at 0x604000000018 thread T0
    #0 0x558e75cbd229 in main /home/benny/st/lab6/t4.c:9
    #1 0x7fc9b3a9ad8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7fc9b3a9ae3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x558e75cbd104 in _start (/home/benny/st/lab6/asan_t4+0x1104)

0x604000000018 is located 8 bytes inside of 40-byte region [0x604000000010,0x604000000038)
freed by thread T0 here:
    #0 0x7fc9b3d4d517 in __interceptor_free ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:127
    #1 0x558e75cbd1ee in main /home/benny/st/lab6/t4.c:7
    #2 0x7fc9b3a9ad8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

previously allocated by thread T0 here:
    #0 0x7fc9b3d4d867 in __interceptor_malloc ../../../../src/libsanitizer/asan/asan_malloc_linux.cpp:145
    #1 0x558e75cbd1de in main /home/benny/st/lab6/t4.c:5
    #2 0x7fc9b3a9ad8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58

SUMMARY: AddressSanitizer: heap-use-after-free /home/benny/st/lab6/t4.c:9 in main
Shadow bytes around the buggy address:
  0x0c087fff7fb0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7fc0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7fd0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7fe0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0c087fff7ff0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0c087fff8000: fa fa fd[fd]fd fd fd fa fa fa fa fa fa fa fa fa
  0x0c087fff8010: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8020: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8030: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8040: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
  0x0c087fff8050: fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa fa
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==79457==ABORTING
```
##### valgrind report
```
$ gcc -o val_t4 t4.c
$ valgrind ./val_t4
==79464== Memcheck, a memory error detector
==79464== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==79464== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==79464== Command: ./val_t4
==79464== 
==79464== Invalid read of size 4
==79464==    at 0x109193: main (in /home/benny/st/lab6/val_t4)
==79464==  Address 0x4a8e048 is 8 bytes inside a block of size 40 free'd
==79464==    at 0x484B27F: free (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==79464==    by 0x10918E: main (in /home/benny/st/lab6/val_t4)
==79464==  Block was alloc'd at
==79464==    at 0x4848899: malloc (in /usr/libexec/valgrind/vgpreload_memcheck-amd64-linux.so)
==79464==    by 0x10917E: main (in /home/benny/st/lab6/val_t4)
==79464== 
==79464== 
==79464== HEAP SUMMARY:
==79464==     in use at exit: 0 bytes in 0 blocks
==79464==   total heap usage: 1 allocs, 1 frees, 40 bytes allocated
==79464== 
==79464== All heap blocks were freed -- no leaks are possible
==79464== 
==79464== For lists of detected and suppressed errors, rerun with: -s
==79464== ERROR SUMMARY: 1 errors from 1 contexts (suppressed: 0 from 0)
```
ASan 能 , valgrind 能

---
### Use-after-return
##### source code
```
#include <stdio.h>
#include <stdlib.h>

int *p;
__attribute__((noinline))

void func1() {
    int num[20];
    p = &num[3];
}

int main(int argc, char **argv) {
    func1();

    *(p+3) = 13;

    return 0;
}
```
##### ASan report
```
$ gcc -fsanitize=address -g -o asan_t5 t5.c
$ ASAN_OPTIONS=detect_stack_use_after_return=1 ./asan_t5
=================================================================
==79471==ERROR: AddressSanitizer: stack-use-after-return on address 0x7f032bd43048 at pc 0x5559802e8386 bp 0x7ffec3074d90 sp 0x7ffec3074d80
WRITE of size 4 at 0x7f032bd43048 thread T0
    #0 0x5559802e8385 in main /home/benny/st/lab6/t5.c:15
    #1 0x7f032f2dfd8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
    #2 0x7f032f2dfe3f in __libc_start_main_impl ../csu/libc-start.c:392
    #3 0x5559802e8144 in _start (/home/benny/st/lab6/asan_t5+0x1144)

Address 0x7f032bd43048 is located in stack of thread T0 at offset 72 in frame
    #0 0x5559802e8218 in func1 /home/benny/st/lab6/t5.c:7

  This frame has 1 object(s):
    [48, 128) 'num' (line 8) <== Memory access at offset 72 is inside this variable
HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
      (longjmp and C++ exceptions *are* supported)
SUMMARY: AddressSanitizer: stack-use-after-return /home/benny/st/lab6/t5.c:15 in main
Shadow bytes around the buggy address:
  0x0fe0e57a05b0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0e57a05c0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0e57a05d0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0e57a05e0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0e57a05f0: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
=>0x0fe0e57a0600: f5 f5 f5 f5 f5 f5 f5 f5 f5[f5]f5 f5 f5 f5 f5 f5
  0x0fe0e57a0610: f5 f5 f5 f5 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0e57a0620: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0e57a0630: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0e57a0640: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
  0x0fe0e57a0650: 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
Shadow byte legend (one shadow byte represents 8 application bytes):
  Addressable:           00
  Partially addressable: 01 02 03 04 05 06 07 
  Heap left redzone:       fa
  Freed heap region:       fd
  Stack left redzone:      f1
  Stack mid redzone:       f2
  Stack right redzone:     f3
  Stack after return:      f5
  Stack use after scope:   f8
  Global redzone:          f9
  Global init order:       f6
  Poisoned by user:        f7
  Container overflow:      fc
  Array cookie:            ac
  Intra object redzone:    bb
  ASan internal:           fe
  Left alloca redzone:     ca
  Right alloca redzone:    cb
  Shadow gap:              cc
==79471==ABORTING
```
##### valgrind report
```
$ gcc -o val_t5 t5.c
$ valgrind ./val_t5
==79478== Memcheck, a memory error detector
==79478== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
==79478== Using Valgrind-3.18.1 and LibVEX; rerun with -h for copyright info
==79478== Command: ./val_t5
==79478== 
==79478== 
==79478== HEAP SUMMARY:
==79478==     in use at exit: 0 bytes in 0 blocks
==79478==   total heap usage: 0 allocs, 0 frees, 0 bytes allocated
==79478== 
==79478== All heap blocks were freed -- no leaks are possible
==79478== 
==79478== For lists of detected and suppressed errors, rerun with: -s
==79478== ERROR SUMMARY: 0 errors from 0 contexts (suppressed: 0 from 0)
```
ASan 能 , valgrind 不能

---

| Test                 | Valgrind | ASan |
| -------------------- | -------- | ---- |
| Heap out-of-bounds   | 能       | 能   |
| Stack out-of-bounds  | 不能     | 能   |
| Global out-of-bounds | 不能     | 能   |
| Use-after-free       | 能       | 能   |
| Use-after-return     | 不能     | 能   |


## part2
寫一個簡單程式 with ASan，Stack buffer overflow 剛好越過 redzone(並沒有對 redzone 做讀寫)，並說明 ASan 能否找的出來？
##### source code
```
#include <stdio.h>

int main() {
    int a[8], b[8];

    int val;
    // val = a[0];
    // val = a[0 + 8*1];
    // val = a[1 + 8*1];
    // val = a[2 + 8*1];
    // val = a[3 + 8*1];
    // val = a[4 + 8*1];
    // val = a[5 + 8*1];
    // val = a[6 + 8*1];
    // val = a[7 + 8*1];

    // val = a[0 + 8*2];
    // val = a[1 + 8*2];
    // val = a[2 + 8*2];
    // val = a[3 + 8*2];
    // val = a[4 + 8*2];
    // val = a[5 + 8*2];
    // val = a[6 + 8*2];
    // val = a[7 + 8*2];

    // val = a[0 + 8*3];
    // val = a[1 + 8*3];
    // val = a[2 + 8*3];
    // val = a[3 + 8*3];
    // val = a[4 + 8*3];
    // val = a[5 + 8*3];
    // val = a[6 + 8*3];
    // val = a[7 + 8*3];

    // val = a[0 + 8*4];
    // val = a[7 + 8*4];
    // val = a[0 + 8*5];
    // val = a[7 + 8*5];


    // val = b[0];
    // val = b[0 + 8*1];
    // val = b[1 + 8*1];
    // val = b[2 + 8*1];
    // val = b[3 + 8*1];
    // val = b[4 + 8*1];
    // val = b[5 + 8*1];
    // val = b[6 + 8*1];
    // val = b[7 + 8*1];


    // val = b[0 + 8*2];
    // val = b[1 + 8*2];
    // val = b[2 + 8*2];
    // val = b[3 + 8*2];
    // val = b[4 + 8*2];
    // val = b[5 + 8*2];
    // val = b[6 + 8*2];
    // val = b[7 + 8*2];

    // val = b[0 + 8*3];
    // val = b[7 + 8*3];
    // val = b[0 + 8*4];
    // val = b[7 + 8*4];
    

    return 0;
}
```
##### ASan
```
$ gcc -fsanitize=address -g -o asan_t6 t6.c
$ ./asan_t6
```
##### 只有 run a 陣列
| Range       | is_redzone | ASan找的出來 |
| ----------- | ---------- | ------------ |
| a[8]-a[15]  | yes        | yes          |
| a[16]-a[23] | no         | no           |
| a[24]-a[31] | yes        | no           |
| a[32]-a[39] | no         | no           |
| a[40]-      | no         | no           |
##### 只有 run b 陣列
| Range       | is_redzone | ASan找的出來 |
| ----------- |:---------- | ------------ |
| b[8]-b[15]  | yes        | yes          |
| b[16]-b[23] | no         | no           |
| b[24]-b[31] | no         | no           |
| b[32]-      | no         | no           |
##### 同時 run a 和 b 陣列
| Range       | is_redzone | ASan找的出來                  |
| ----------- |:---------- |:----------------------------- |
| a[8]-a[15]  | yes        | yes                           |
| a[16]-a[23] | no         | no                            |
| a[24]-a[31] | yes        | <font color="#f00">yes</font> |
| a[32]-a[39] | no         | no                            |
| a[40]-      | no         | no                            |
| b[8]-b[15]  | yes        | yes                           |
| b[16]-b[23] | no         | no                            |
| b[24]-b[31] | no         | no                            |
| b[32]-      | no         | no                            |
