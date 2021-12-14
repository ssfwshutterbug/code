package main

import (
	"encoding/json"
	"fmt"
	"monitor_process/libs"
	"os"
)

const LOC string = "./result.txt"

// main function
func main() {

	// set default variables with the ability of parsing terminal input arguments
	var l *libs.LoginInfo = libs.DefLogin.ParseCmd()
	fmt.Printf("program starts! now checking interval is %v seconds.\n", l.Interval)

	// open file for writing
	file, err := os.OpenFile(LOC, os.O_CREATE|os.O_APPEND|os.O_RDWR, 0755)
	if err != nil {
		fmt.Println(err)
	}
	defer file.Close()

	// main loop
	for {
		// get origin workload service data info
		var wslink string = libs.ApiUrl(l.Ip, l.Port, l.Virtual, "workloadservice")
		var content = libs.RawData(wslink, l.User, l.Api)

		// get origin workload network data info
		var netlink string = libs.ApiUrl(l.Ip, l.Port, l.Virtual, "workloadnetwork")
		var ipInfo = libs.RawData(netlink, l.User, l.Api)

		// convert raw data to json
		var data libs.Data
		var ipinfo libs.Net
		json.Unmarshal(*content, &data)
		json.Unmarshal(*ipInfo, &ipinfo)

		// compare data
		libs.CompareData(&data, &ipinfo, uint(l.Interval), file)
	}
}
