package main

import (
	"fmt"
	"os/exec"
)

func main() {
	cmd := exec.Command("pamixer", "--get-volume")
	res, _ := cmd.Output()
	fmt.Printf("%s", res)
}
