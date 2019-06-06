package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os/exec"
)

type config struct {
	Name string
	IP   string
}

func main() {

	http.HandleFunc("/new", func(w http.ResponseWriter, r *http.Request) {

		c := config{}

		body, _ := ioutil.ReadAll(r.Body)

		err := json.Unmarshal(body, &c)
		if err != nil {
			panic(err)
		}

		createJail(c)

		fmt.Fprintf(w, "Success!")
	})

	log.Fatal(http.ListenAndServe(":8080", nil))
}

func createJail(c config) {
	ipAddr := "lo1|" + c.IP
	ezjCmd := exec.Command("ezjail-admin", "create", c.Name, ipAddr)

	err := ezjCmd.Run()
	if err != nil {
		fmt.Println(err)
	}
	fmt.Printf("Jail %s has been created!\n", c.Name)

	// resolv.conf
	resolv := []byte("nameserver 1.1.1.1\nnameserver 8.8.8.8\n")
	err = ioutil.WriteFile(fmt.Sprintf("/usr/jails/%s/etc/resolv.conf", c.Name), resolv, 0644)

	ezjCmd = exec.Command("ezjail-admin", "start", c.Name)
	ezjCmd.Run()
	if err != nil {
		fmt.Println(err)
	}
	fmt.Printf("Jail %s has been started!\n", c.Name)
}
