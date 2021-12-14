package libs

import (
	"crypto/tls"
	"flag"
	"fmt"
	"io"
	"net/http"
	"os"
	"time"
)

// define some variables
var NEW *map[string]Service
var OLD *map[string]Service

// create data struct for login information
type LoginInfo struct {
	Ip       string
	Port     string
	User     string
	Api      string
	Interval int
	Virtual  string
}

// set default information
var DefLogin = &LoginInfo{
	Ip:       "192.168.6.10",
	Port:     "8080",
	User:     "admin",
	Api:      "Wihnyw6AUFVKNv8cLsWnxmM3n4ZUE8UTv6dFoXLEve94uZGbx79bfNSB2kNo2qif",
	Interval: 300,
	Virtual:  "default",
}

// create data struct of service request [{k:v,k:[{k:v},{k:v}...]},k:v]
type Data []struct {
	Uuid             string  `json:"uuid"`
	Service          Service `json:"service"`
	Updatedtimestamp int     `json:"updatedtimestamp"`
}

type Service []struct {
	Protocol string `json:"protocol"`
	Port     string `json:"port"`
	Listen   string `json:"listen"`
	Name     string `json:"name"`
	Exe      string `json:"exe"`
}

// create data struct of workload network [{k:v},[{k:v},{k:v}...],{k:v}]
type Net []struct {
	Uuid             string
	Network          Network
	Updatedtimestamp int
}

type Network []struct {
	Interface string
	Ip        string
	Mask      string
	Mac       string
	ifgateway bool
}

// terminal commind line parse
func (l *LoginInfo) ParseCmd() *LoginInfo {
	ip := flag.String("ip", l.Ip, "QCC ipaddress")
	port := flag.String("port", l.Port, "api port")
	interval := flag.Uint("time", uint(l.Interval), "interval time(seconds)")
	api := flag.String("api", l.Api, "qcc api key")
	user := flag.String("user", l.User, "api user name")
	virtual := flag.String("virtual", l.Virtual, "virtual zoom")
	flag.Parse()
	l.Ip, l.Port, l.Interval, l.Api, l.User, l.Virtual = *ip, *port, int(*interval), *api, *user, *virtual
	return l
}

// function of api url
func ApiUrl(ip, port, virtual, api string) string {
	return "https://" + ip + ":" + port + "/" + virtual + "/" + api
}

// get http request raw data
func RawData(url, user, api string) *[]byte {
	http.DefaultTransport.(*http.Transport).TLSClientConfig = &tls.Config{InsecureSkipVerify: true}

	r, _ := http.NewRequest("GET", url, nil)
	r.SetBasicAuth(user, api)

	c := &http.Client{}
	resp, err := c.Do(r)
	if err != nil {
		fmt.Println(err)
	}
	defer resp.Body.Close()

	// return resp.Body
	content, _ := io.ReadAll(resp.Body)
	return &content
}

// abstract uuid as a key map to Data: uuid -> services
func Map2Json(data *Data) *map[string]Service {
	j_map := make(map[string]Service)

	for _, v := range *data {
		key := v.Uuid
		value := v.Service
		j_map[key] = value
	}
	return &j_map
}

// abstract service name as a key map to Service: service_name -> protocol/port
func Map2Service(service *Service) *map[string]string {
	s_map := make(map[string]string)

	for _, v := range *service {
		key := v.Name
		value := v.Protocol + "/" + v.Port
		s_map[key] = value
	}
	return &s_map
}

// create a map of uuid to ip: uuid -> ips
func MapU2Ip(ipinfo *Net) *map[string]([]string) {
	n_map := make(map[string]([]string))

	for _, v := range *ipinfo {
		var ip_coll = []string{}
		key := v.Uuid
		value := v.Network
		for _, k := range value {
			ip_coll = append(ip_coll, k.Ip)
		}
		n_map[key] = ip_coll
	}
	return &n_map
}

// compare data with x second interval
// pass the same, show the difference
func CompareData(data *Data, ipinfo *Net, tsleep uint, file *os.File) {
	NEW = Map2Json(data)
	var IPS = MapU2Ip(ipinfo)

	// fmt.Println(*NEW)
	// init sign OLD with NEW info
	if OLD == nil {
		OLD = NEW
		time.Sleep(time.Duration(tsleep) * time.Second)
	}

	// loop NEW info compare to OLD
	for uuid := range *OLD {
		new_service, ifkeyexist := (*NEW)[uuid]

		// some services stoped, pass
		if !ifkeyexist {
			continue
		}

		old_service := (*OLD)[uuid]
		ip := (*IPS)[uuid]
		new_mapService := Map2Service(&new_service)
		old_mapService := Map2Service(&old_service)

		for service_name, new_port := range *new_mapService {
			old_port := (*old_mapService)[service_name]

			if len(old_port) == 0 {
				// new started service, record
				message := fmt.Sprintln(time.Now().Local(), "ip:", ip, "\t", "start up new service:", service_name, "\t", "port:", new_port, "\t")
				fmt.Println(message)
				file.WriteString(message)
			} else {
				// not changed information, pass
				if new_port == (*old_mapService)[service_name] {
					// m := fmt.Sprintln(time.Now().Local(), "ip:", ip, "\t", "service:", service_name, "\t", "port:", old_port, "==", new_port)
					// fmt.Print(m)
					continue
				} else {
					// process port changed information, record
					message := fmt.Sprintln(time.Now().Local(), "ip:", ip, "\t", "service:", service_name, "\t", "port:", old_port, "--->", new_port, "\t")
					fmt.Println(message)
					file.WriteString(message)
				}
			}

		}
	}
	// when one loop finished, sign old with new information
	OLD = NEW
	time.Sleep(time.Duration(tsleep) * time.Second)
}
