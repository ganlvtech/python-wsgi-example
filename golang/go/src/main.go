package main

import (
	"net/http"
	"os"
)

func main() {
	http.HandleFunc("/go", func(w http.ResponseWriter, req *http.Request) {
		w.Write([]byte("Hello, Gopher!"))
	})
	http.ListenAndServe(":"+os.Args[1], nil)
}
