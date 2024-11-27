data SEGMENT
    star:           DB '*', 24h
    space:          DB ' ', 24h
    return:         DB 0Dh, 0Ah, 24h
    invalid_input:  DB 0Dh, 0Ah, 'Invalid input', 0Dh, 0Ah, 24h

ENDS


stack SEGMENT
    DB   32  dup(?)

ENDS


code SEGMENT
    ASSUME CS:code,SS:stack,DS:data

main:

    MOV BX, stack
    MOV SS, BX

    MOV BX, data
    MOV DS, BX

    CALL catch_n
    TEST AX, AX
    JZ _error

    MOV SI, AX

    MOV AX, return
    CALL echo_string

    MOV DX, SI
    SAL DX, 1
    INC DX

    XOR BX, BX

    _loop1:
        CMP BX, SI
        JGE _end

        MOV CX, 1
        _loop2:
            CMP CX, DX
            JG _end_loop1

            MOV DI, SI
            SUB DI, BX

            CMP CX, DI
            JL _space

            MOV DI, SI
            ADD DI, BX

            CMP CX, DI
            JG _end_loop1

            MOV AX, star
            CALL echo_string
            JMP _end_loop2

            _space:
                MOV AX, space
                CALl echo_string

            _end_loop2:
                INC CX
                JMP _loop2

        _end_loop1:
            MOV AX, return
            CALL echo_string

            INC BX
            JMP _loop1
    _error:
        MOV AX, invalid_input
        CALL echo_string
    _end:
        MOV AX, 4C00h
        INT 21h

catch_n:
    XOR BX, BX
    _read_num:
        MOV AH, 01h
        INT 21h

        CMP AL, 0Dh
        JE _on_return


        XOR AH, AH
        SUB AL, 30h

        JS _on_error
        CMP AL, 9
        JG _on_error

        MOV CX, BX

        SHL CX, 03h
        SHL BX, 01h

        ADD BX, CX
        ADD BX, AX


        JMP _read_num

    _on_return:
        MOV AX, BX
        RET

    _on_error:
        XOR AX, AX
        RET


echo_string:
    PUSH AX
    PUSH DX

    MOV DX, AX
    MOV AH, 09h
    INT 21h

    POP DX
    POP AX

    RET


ENDS


END main
