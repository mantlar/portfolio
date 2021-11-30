TITLE Project 6: String Primitives and Macros     (Proj6_rolphi.asm)

; Author: Ian Rolph
; Last Modified: 12/6/2020
; OSU email address: rolphi@oregonstate.edu
; Course number/section:   CS271 Section 400
; Project Number: 6               Due Date: 12/6/2020
; Description: A program that takes 10 user generated numbers, displays them, then
;              calculates and displays their sum and rounded down average.

INCLUDE Irvine32.inc

; ---------------------------------------------------------------------------------
; Name: mGetString
;
; Uses Irvine's ReadString procedure to get user input from the keyboard.
;
; Preconditions: None
;
; Receives:
; prompt = address of prompt string
; outputAddress = address where the string will be stored
; length = length of string buffer
; bytesRead = address where the number of characters that were entered will be stored
;
; returns: 
; outputAddress = string that was entered
; bytesRead = number of characters that were entered
; ---------------------------------------------------------------------------------
mGetString MACRO prompt, outputAddress, length, bytesRead
    LOCAL _Label1
	PUSH ECX
	PUSH EDX
	PUSH EAX
	mDisplayString prompt
	MOV EDX, outputAddress
	MOV ECX, length
	CALL ReadString
	MOV [bytesRead], EAX
	POP EAX
	POP EDX
	POP ECX
ENDM

; ---------------------------------------------------------------------------------
; Name: mGetString
;
; Uses Irvine's WriteString procedure to output the string at the given address.
;
; Preconditions: None
;
; Postconditions: String is displayed to the output.
;
; Receives:
; address = address of string to be displayed
;
; returns: None
; ---------------------------------------------------------------------------------
mDisplayString MACRO address
	PUSH EDX
	MOV EDX, address
	CALL WriteString
	POP EDX
ENDM


.data

stringValue	SDWORD 0
byteCount	DWORD ?
valueArray	SDWORD 10 DUP(0)
commaSpace	BYTE ", ",0
prompt		BYTE "Please enter a signed number: ",0
intro		BYTE "Project 6: String Primitives and Macros by Ian Rolph",0Ah,0Ah,"Please provide 10 signed decimal integers.",0Ah,"Each number needs to be small enough to fit inside a 32 bit register.",0Ah,"After you have finished inputting the raw numbers I will display a list",0Ah,"of the integers, their sum, and their average value.",0Ah,0Ah,0
listIntro	BYTE "You entered the following numbers: ",0
sumIntro	BYTE "The sum of these numbers is: ",0
avgIntro	BYTE "The rounded average is: ",0
goodbye		BYTE "Goodbye!",0
invalidStr	BYTE "ERROR: You did not enter a signed number or your number was too big.",0Ah,0
displayOut	BYTE 14 DUP(0)
buffer		BYTE 20 DUP(0)

.code

main PROC
	mDisplayString OFFSET intro
	MOV ECX, 10
	MOV EDI, OFFSET valueArray
	MOV ESI, OFFSET valueArray
	_getUserInput:
		PUSH OFFSET invalidStr
		PUSH OFFSET byteCount
		PUSH SIZEOF buffer
		PUSH OFFSET buffer
		PUSH OFFSET prompt
		PUSH OFFSET stringValue
		CALL ReadVal
		MOV EAX, stringValue
		STOSD
		LOOP _getUserInput
	CALL Crlf
	MOV ECX, 9
	mDisplayString OFFSET listIntro
	CALL Crlf
	_displayValues:
		LODSD
		PUSH OFFSET displayOut
		PUSH EAX
		CALL WriteVal
		mDisplayString OFFSET commaSpace
		LOOP _displayValues
		LODSD
		PUSH OFFSET displayOut
		PUSH EAX
		CALL WriteVal
	CALL Crlf
	mDisplayString OFFSET sumIntro
	MOV ECX, 10
	MOV EAX, 0
	MOV EBX, 0
	MOV ESI, OFFSET valueArray
	_sumValues:
		ADD EBX, [ESI]
		LODSD
		LOOP _sumValues
	PUSH OFFSET displayOut
	PUSH EBX
	CALL WriteVal
	CALL Crlf
	mDisplayString OFFSET avgIntro
	MOV EAX, EBX
	MOV EBX, 10
	CDQ
	IDIV EBX
	PUSH OFFSET displayOut
	PUSH EAX
	CALL WriteVal
	CALL Crlf
	CALL Crlf
	mDisplayString OFFSET goodbye
	Invoke ExitProcess,0	; exit to operating system
main ENDP

; ---------------------------------------------------------------------------------
; Name: ReadVal
;
; Uses mGetString to get user input then converts it to a SDWORD if the given
; input can be expressed in that way. If it can't, reprompts the user.
;
; Preconditions: None
;
; Receives:
; [EBP + 8]		= address where the value will be stored
; [EBP + 12]	= address of prompt string
; [EBP + 16]	= output address for mGetString
; [EBP + 20]	= length of mGetString buffer
; [EBP + 24]	= output address for number of bytes read
; [EBP + 28]	= address of error string (to be printed if the given input can't be parsed)
;
; returns: 
; 
; [EBP + 8]		= value that was read
; ---------------------------------------------------------------------------------
ReadVal PROC	; args: [EBP + 8] = value output address, [EBP + 12] = prompt, [EBP + 16] = outputAddress for macro, [EBP + 20] = length, [EBP + 24] = bytesRead, [EBP + 28] = error string offset
	PUSH EBP
	MOV EBP, ESP
	PUSH ESI
	PUSH EDI
	PUSH ECX
	PUSH EAX
	_start:
		MOV EAX, 0
		TEST EAX, EAX	; clear overflow flag just in case
		mGetString [EBP + 12], [EBP + 16], [EBP + 20], [EBP + 24]
		MOV ECX, [EBP + 24]
		CMP ECX, 0
		JE _invalid
		MOV ESI, [EBP + 16]
		MOV EDI, [EBP + 8]
		MOV SDWORD PTR [EDI], 0
		LODSB	; get first char
		DEC ECX
		CMP AL, "-"
		JE _negativeSign
		CMP AL, "+"
		JE _positiveSign
		CMP AL, 0
		JE _invalid
		JMP _getValuePositive
	_negativeSign:
		CMP ECX, 0
		JE _invalid
		LODSB
		JMP _getValueNegative
	_positiveSign:
		CMP ECX, 0
		JE _invalid
		LODSB
	_getValuePositive:
		CMP AL, 30h
		JB _invalid
		CMP AL, 39h
		JA _invalid
		; valid digit
		SUB AL, 30h
		MOV BL, AL
		PUSH EBX
		MOV EAX, [EDI]
		CDQ
		MOV EBX, 10
		IMUL EBX
		MOV [EDI], EAX
		POP EBX
		JO _invalid
		MOV EAX, 0
		MOV AL, BL
		ADD [EDI], EAX
		JO _invalid
		LODSB
		CMP AL, 0
		JE _finished
		JMP _getValuePositive
	_getValueNegative:
		CMP AL, 30h
		JB _invalid
		CMP AL, 39h
		JA _invalid
		; valid digit
		SUB AL, 30h
		MOV BL, AL
		PUSH EBX
		MOV EAX, [EDI]
		CDQ
		MOV EBX, 10
		IMUL EBX
		MOV [EDI], EAX
		POP EBX
		JO _invalid
		MOV EAX, 0
		MOV AL, BL
		SUB [EDI], EAX
		JO _invalid
		LODSB
		CMP AL, 0
		JE _finished
		JMP _getValueNegative
	_invalid:
		mDisplayString [EBP + 28]
		JMP _start
	_finished:
	POP EAX	
	POP ECX
	POP EDI
	POP ESI
	POP EBP
	RET 24
ReadVal ENDP

; ---------------------------------------------------------------------------------
; Name: WriteVal
;
; Uses mDisplayString to output a SDWORD value to the output.
;
; Preconditions: [EBP + 8] must have an SDWORD value.
;
; Postconditions: Value is written to the output.
;
; Receives:
; [EBP + 8]		= value to be written (SDWORD)
; [EBP + 12]	= address to store the generated string
; [EBP + 16]	= length of [EBP + 12] buffer
;
; returns: 
; [EBP + 12]	= string that was generated by the procedure
; ---------------------------------------------------------------------------------
WriteVal PROC	;args: [EBP + 8] = value to be written (SDWORD), [EBP + 12] = offset of output address, [EBP + 16] = length of offset
	PUSH EBP
	MOV EBP, ESP
	PUSH EAX
	PUSH EDX
	PUSH EBX
	PUSH ECX
	PUSH ESI
	PUSH EDI
	MOV ESI, [EBP + 12]
	MOV EDI, [EBP + 12]
	MOV ECX, 14
	_clearString:
		MOV EAX, 0
		STOSB
		LOOP _clearString
	MOV EDI, [EBP + 12]
	MOV EBX, 10d
	MOV ECX, 0
	MOV EAX, [EBP + 8]
	CMP EAX, 0
	JG _getRemaindersPositive
	_negative:
		PUSH EAX
		MOV AL, "-"
		STOSB
		POP EAX
		JMP _getRemaindersNegative
	_getRemaindersPositive:
		CDQ
		DIV EBX
		ADD EDX, 30h
		INC ECX
		PUSH EDX
		CMP EAX, 0
		JE _reverse
		JMP _getRemaindersPositive
	_getRemaindersNegative:
		CDQ
		IDIV EBX
		NEG EDX
		ADD EDX, 30h
		INC ECX
		PUSH EDX
		CMP EAX, 0
		JE _reverse
		JMP _getRemaindersNegative
	_reverse:
		POP EAX
		STOSB
		LOOP _reverse
	_finished:
	mDisplayString ESI
	POP EDI
	POP ESI
	POP ECX
	POP EBX
	POP EDX
	POP EAX
	POP EBP
	RET 8
WriteVal ENDP
END main
