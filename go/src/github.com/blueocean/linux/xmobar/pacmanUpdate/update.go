package main

import (
	"fmt"
	"os/exec"
	"strings"
)

func main() {
	cmd := []string{"sudo pacman -Sy", "pacman -Qu | wc -l"}
	// sync database
	sync := exec.Command("bash", "-c", cmd[0])
	sync.Run()

	// query update info
	res, _ := exec.Command("bash", "-c", cmd[1]).Output()
	final := strings.TrimSuffix(string(res), "\n")
	fmt.Printf("%s update", final)
}
