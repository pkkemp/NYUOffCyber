package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"strings"
)




func keepLines(s string, n int) string {
	result := strings.Join(strings.Split(s, "\n")[:n], "\n")
	return strings.Replace(result, "\r", "", -1)
}

func main() {

	//proxyUrl, err := url.Parse("http://127.0.0.1:8080")
	//client := &http.Client{Transport: &http.Transport{Proxy: http.ProxyURL(proxyUrl)}}
	client := &http.Client{}

	req, err := http.NewRequest("GET", "http://offsec-chalbroker.osiris.cyber.nyu.edu:1250", nil)
	if err != nil {
		log.Print(err)
		os.Exit(1)
	}
	req.AddCookie(&http.Cookie{Name: "CHALBROKER_USER_ID", Value: "pk1898"})
	q := req.URL.Query()
	q.Add("debug", "1")
	q.Add("ip", "1.1.1.1")

	req.URL.RawQuery = q.Encode()
	file, err := os.Open("unix")
	if err != nil {
		log.Fatal(err)
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		fmt.Println(scanner.Text())
		q.Set("ip", scanner.Text())
		req.URL.RawQuery = q.Encode()
		fmt.Println()
		resp, _ := client.Do(req)
		fmt.Println(req.URL.String())
		body, _ := ioutil.ReadAll(resp.Body)
		fmt.Println("get:\n", string(body), 5)
	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}




	// Output:
	// http://api.themoviedb.org/3/tv/popular?another_thing=foo+%26+bar&api_key=key_from_environment_or_flag
}