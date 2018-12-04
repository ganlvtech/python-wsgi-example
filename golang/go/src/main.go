package main

import (
	"net/http"
)

func hello(w http.ResponseWriter, req *http.Request) {
	w.Write([]byte("Hello, Gopher!"))
}

func main() {
	http.HandleFunc("/hello", hello)
	http.ListenAndServe(":8003", nil)
}
