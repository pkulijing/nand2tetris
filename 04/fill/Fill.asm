// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input. 
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel. When no key is pressed, the
// program clears the screen, i.e. writes "white" in every pixel.

// Put your code here.
//if(keyboard == 0 && screen != 0)
//       setwhite
//else if(keyboard != 0 && screen == 0)
//        setblack
(LOOP)
    @SCREEN
    D=!M
    @KBD
    D=D|M
    @SETWHITE
    D;JEQ
    @SCREEN
    D=!M
    @KBD
    D=D&M
    @SETBLACK
    D;JNE
    @LOOP
    0;JMP
(SETBLACK)
    @SCREEN
    D=A
    @i
    M=D
(SETBLOOP)
    @i
    A=M
    M=-1
    @i
    M=M+1
    D=M
    @KBD
    D=D-A
    @SETBLOOP
    D;JLT
    @LOOP
    0;JMP
(SETWHITE)
    @SCREEN
    D=A
    @i
    M=D
(SETWLOOP)
    @i
    A=M
    M=0
    @i
    M=M+1
    D=M
    @KBD
    D=D-A
    @SETWLOOP
    D;JLT
    @LOOP
    0;JMP
