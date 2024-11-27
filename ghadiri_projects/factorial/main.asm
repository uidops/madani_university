org 100h              
          
_start:
    ; READ THE NUMBER FROM I/O       
    XOR DX, DX            ; clear DX to zero
    _read_num:
        PUSH DX           ; save DX (The actual number)
    
        MOV AH, 01h       ; set AH=1 (get a single char from i/o)
        INT 21h           ; call dos subsystem (it will store the input to AL)
   
        POP DX            ; restore DX
        
        CMP AL, 0Dh       ; if AL == 0Dh
        JE  _factorial    ;   jump to _factorial

        SUB AL, 30h       ; the number is ascii so we subtract 30h ( ascii(0) = 0x30 )
        
        XOR AH, AH        ; set AH=0 (The input is one char which is a byte so it's in AL and we can securly clear AH)
        
        MOV BX, DX        ; set BX=DX (Saving DX to BX) [BX is now the actual number]
        MOV CX, AX        ; set CX=AX (Saving AX (the input) to CX)
                        
        MOV AL, 10        ; set AL=10 (for bl=bl*10)
        MUL BL            ; do AX = AL * BL -> AX = 10 * BL
        
        ADD AX, CX        ; add the input number to CX so -> AX = (10 * BL) + CX -> AX = (10 * prev_number) + current_input
        MOV DX, AX        ; set DX=AX to save the number to DX
        JMP _read_num     ; do these operations again to get all the digits
 
    ; THE FUNCTION WHICH COMPUTE THE FACTORIAL(DX)
    _factorial:      
        MOV AX, 0001h     ; set AX=1 for base of the loop 
        MOV BX, DX        ; set BX=DX  now BX is the number
        do0:       
            MUL BX        ; do AX = AX * BX
            DEC BX        ; BX = BX - 1
            JNZ do0       ; do this loop until the number is zero
         

    ; CONVERT THE OUTPUT OF FACTORIAL(DX) TO A CHAR ARRAY AND PRINT
    _print_number:
        MOV SI, 2         ; set SI=2  for word '$' (it counts the number of bytes in array)
        SUB SP, 16        ; SP = SP - 16byte
        MOV BP, SP        ; BP = SP  save SP to BP

        PUSH 24h          ; push word '$' to stack
                         
        MOV DI, SP        ; DI = SP  save SP to DI
        MOV CX, 0Ah       ; set CX=10  for division

        do1:      
            XOR DX, DX    ; clear DX to zero

            CMP AX, 0h    ; if AX is 0 (The number)
            JZ print      ;    jump to print
  
            DIV CX        ; AX = AX/CX   and   DX = AX%DX
            ADD DX, 30h   ; add 30h to DX to make it ascii
            DEC DI        ; decress the DI for stack pointing
            MOV [DI], DL  ; move DL (only a word which is the ascii character) to the stack at [DI]
            INC SI        ; increase SI for counting byte
            jmp do1       ; do these operation again until the number became zero

        print:        
            MOV AH, 09h   ; move 9 to AH (Write a $-terminated string to output)
            SUB BP, SI    ; BP = BP - SI (The number of bytes to set pointer to beginning of array)
            MOV DX, BP    ; set DX = BP to tell dos subsystem the address of the string
            SUB SP, 10h   ; SP = SP - 16 (The dos subsystem will distroy the stack)
            INT 21h       ; call the dos subsystem

    HLT                   ; HALT THE CPU.....
