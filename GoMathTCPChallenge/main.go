package main

import (
	"fmt"
	"net"
	"strconv"
	"strings"
	"time"
)

func oneWordToNum(word string) string {
	word = strings.ToUpper(word)
	switch word {
	case "ONE":
		return "1"
	case "TWO":
		return "2"
	case "THREE":
		return "3"
	case "FOUR":
		return "4"
	case "FIVE":
		return "5"
	case "SIX":
		return "6"
	case "SEVEN":
		return "7"
	case "EIGHT":
		return "8"
	case "NINE":
		return "9"
	case "ZERO":
		return "0"
	}
	return "-1"
}

func wordToNum(word string) int {
	nums := strings.Split(word, "-")
	tempNum := ""
	for i := 0; i < len(nums); i++  {
		tempNum += oneWordToNum(nums[i])
	}
	num, _ := strconv.Atoi(tempNum)
	return num
}

func hexToNum(hex string) int {
	sep := strings.Split(hex, "0x")
	num, _ := strconv.ParseInt(sep[1], 16, 64)
	return int(num)
}

func binToNum(bin string) int {
	sep := strings.Split(bin, "0b")
	num, _ := strconv.ParseInt(sep[1], 2, 64)
	return int(num)
}

func getNum(numString string) int {
	num, err := strconv.Atoi(numString)
	if err == nil {
		return num
	} else if strings.Index(numString, "0x") != -1 {
		return hexToNum(numString)
	} else if strings.Index(numString, "0b") != -1 {
		return binToNum(numString)
	} else  {
		return wordToNum(numString)
	}
}

func solveProblem(problemString string) int {

	sep := strings.Split(problemString, " ")
	first := sep[0]
	second := sep[2]
	firstNum := getNum(first)
	secondNum := getNum(second)
	operator := sep[1]

	if operator == "*" {
		return firstNum * secondNum
	} else if operator == "+" {
		return firstNum + secondNum
	} else if operator == "-" {
		return firstNum - secondNum
	} else {
		return firstNum / secondNum
	}

}

func main() {
	conn, err := net.Dial("tcp", "offsec-chalbroker.osiris.cyber.nyu.edu:1236")
	if err != nil {
	fmt.Println("dial error:", err)
	return
	}
	defer conn.Close()
	//n, err :=fmt.Fprintf(conn, "pk1898\r\n")
	b := []byte("pk1898\n")
	//curMessage := make([]byte, 0)
	curMessageBuff := make([]byte, 4096)
	n, err := conn.Read(curMessageBuff)
	fmt.Println(n)
	fmt.Println(string(curMessageBuff))
	conn.Write(b)
	time.Sleep(1000 * time.Millisecond)
	n, err = conn.Read(curMessageBuff)
	fmt.Println(string(curMessageBuff))
	stringQuestion := strings.SplitAfter(string(curMessageBuff), "\n")
	question := stringQuestion[4]
	answer := solveProblem(question)
	fmt.Println(answer, "\n")
	b = []byte(strconv.Itoa(answer) + "\n")
	conn.Write(b)

	for len(stringQuestion) > 1 {
		curMessageBuff = make([]byte, 4096)
		n, err = conn.Read(curMessageBuff)
		fmt.Println(string(curMessageBuff))
		stringQuestion = strings.SplitAfter(string(curMessageBuff), "\n")
		if len(stringQuestion) > 1 {
			question = stringQuestion[1]
			answer := solveProblem(question)
			fmt.Println(answer, "\n")
			b = []byte(strconv.Itoa(answer) + "\n")
			conn.Write(b)
			fmt.Println(string(curMessageBuff))
		}
	}

}